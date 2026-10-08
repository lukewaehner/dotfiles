import type { Plan, Step, StepStatus } from '../types'

export type StepInput = { id: string; title: string; after?: string[] }

export type Readiness = { kind: 'done' | 'running' | 'ready' } | { kind: 'waiting'; on: string[] }

export function createPlan(title: string, inputs: StepInput[], now: number): Plan {
  const ids = new Set(inputs.map(input => input.id))
  const steps = inputs.map(input => ({
    id: input.id,
    title: input.title,
    status: 'pending' as const,
    // Dependencies on ids the plan doesn't define would block a step forever.
    after: (input.after ?? []).filter(id => ids.has(id) && id !== input.id),
    agents: [],
  }))

  return { title, createdAt: now, steps }
}

const isFinished = (step: Step) => step.status === 'completed' || step.status === 'skipped'

export const isPlanFinished = (plan: Plan) => plan.steps.every(isFinished)

export function setStatus(plan: Plan, id: string, status: StepStatus, now: number): Plan {
  return mapStep(plan, id, step => {
    if (step.status === status) return step
    if (status === 'in_progress') return { ...step, status, startedAt: step.startedAt ?? now }
    if (status === 'pending') return { ...step, status, startedAt: undefined, doneAt: undefined }

    return { ...step, status, startedAt: step.startedAt ?? startOf(plan, step), doneAt: now }
  })
}

export function startAgent(plan: Plan, stepId: string, agentId: string, now: number): Plan {
  const started = setStatus(plan, stepId, 'in_progress', now)

  return mapStep(started, stepId, step => ({
    ...step,
    agents: [...step.agents.filter(run => run.id !== agentId), { id: agentId, status: 'running' }],
  }))
}

/** Settles one subagent; its step completes once every agent on it has succeeded. */
export function finishAgent(plan: Plan, agentId: string, hasSucceeded: boolean, now: number): Plan {
  const owner = plan.steps.find(step => step.agents.some(run => run.id === agentId))
  if (owner === undefined) return plan

  const settled = mapStep(plan, owner.id, step => ({
    ...step,
    agents: step.agents.map(run =>
      run.id === agentId ? { ...run, status: hasSucceeded ? 'done' : 'failed' } : run,
    ),
  }))
  const step = settled.steps.find(one => one.id === owner.id)!
  const isAllDone = step.agents.every(run => run.status === 'done')

  return isAllDone ? setStatus(settled, owner.id, 'completed', now) : settled
}

/** Re-keys a dispatched agent by its background id, so the tick can watch it. */
export function backgroundAgent(plan: Plan, callId: string, agentId: string): Plan {
  return {
    ...plan,
    steps: plan.steps.map(step => ({
      ...step,
      agents: step.agents.map(run => (run.id === callId ? { ...run, id: agentId, isBackground: true } : run)),
    })),
  }
}

export const backgroundAgentIds = (plan: Plan) =>
  plan.steps.flatMap(step =>
    step.agents.filter(run => run.status === 'running' && run.isBackground === true).map(run => run.id),
  )

/** The step an Agent call is for, from a leading `#<id>` in its description. */
export function stepIdOf(description: string): string | undefined {
  return /^\s*\[?#([\w-]+)\]?/.exec(description)?.[1]
}

export function readinessOf(plan: Plan, step: Step): Readiness {
  if (isFinished(step)) return { kind: 'done' }
  if (step.status === 'in_progress') return { kind: 'running' }

  const open = step.after.filter(id => {
    const blocker = plan.steps.find(one => one.id === id)
    return blocker !== undefined && !isFinished(blocker)
  })

  return open.length === 0 ? { kind: 'ready' } : { kind: 'waiting', on: open }
}

/**
 * Time left along the plan's critical path, using the mean duration of the
 * steps finished so far as every open step's cost. Steps that can run side by
 * side (no path between them) overlap rather than add, so four parallel
 * subagents cost one step, not four. Undefined until a step has finished.
 */
export function etaMs(plan: Plan, now: number): number | undefined {
  const durations = plan.steps
    .filter(step => step.status === 'completed' && step.startedAt !== undefined && step.doneAt !== undefined)
    .map(step => step.doneAt! - step.startedAt!)
  if (durations.length === 0) return undefined

  const mean = durations.reduce((sum, ms) => sum + ms, 0) / durations.length
  const costOf = (step: Step) => {
    if (isFinished(step)) return 0
    if (step.status === 'in_progress') return Math.max(mean - (now - (step.startedAt ?? now)), mean * 0.1)
    return mean
  }

  const byId = new Map(plan.steps.map(step => [step.id, step]))
  const memo = new Map<string, number>()
  const pathTo = (step: Step, visiting: Set<string>): number => {
    const known = memo.get(step.id)
    if (known !== undefined) return known
    if (visiting.has(step.id)) return 0

    visiting.add(step.id)
    const before = step.after
      .map(id => byId.get(id))
      .filter((one): one is Step => one !== undefined)
      .map(one => pathTo(one, visiting))
    visiting.delete(step.id)

    const total = costOf(step) + Math.max(0, ...before)
    memo.set(step.id, total)
    return total
  }

  return Math.max(0, ...plan.steps.map(step => pathTo(step, new Set())))
}

export function formatDuration(ms: number): string {
  const seconds = Math.max(0, Math.round(ms / 1000))
  if (seconds < 60) return `${seconds}s`
  const minutes = Math.round(seconds / 60)
  if (minutes < 60) return `${minutes}m`

  return `${Math.floor(minutes / 60)}h${String(minutes % 60).padStart(2, '0')}m`
}

export function progressBar(done: number, total: number, width: number): string {
  const filled = total === 0 ? 0 : Math.round((done / total) * width)

  return '█'.repeat(filled) + '░'.repeat(width - filled)
}

function mapStep(plan: Plan, id: string, fn: (step: Step) => Step): Plan {
  return { ...plan, steps: plan.steps.map(step => (step.id === id ? fn(step) : step)) }
}

// A step marked done without ever being started began when its last
// dependency finished (or, with none, when the previous step finished), or
// when the plan was laid out.
function startOf(plan: Plan, step: Step): number {
  const before = step.after.length > 0 ? plan.steps.filter(one => step.after.includes(one.id)) : plan.steps
  const ends = before
    .map(one => one.doneAt)
    .filter((end): end is number => end !== undefined)

  return Math.max(plan.createdAt, ...ends)
}
