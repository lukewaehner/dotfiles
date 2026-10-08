import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Plan, Step, StepStatus } from '../types'
import {
  createPlan,
  etaMs,
  finishAgent,
  formatDuration,
  isPlanFinished,
  progressBar,
  backgroundAgent,
  readinessOf,
  backgroundAgentIds,
  setStatus,
  startAgent,
  stepIdOf,
} from './plan'
import type { StepInput } from './plan'

const plan = atom({ plugin: 'plan-band', key: 'plan' } as const, null)
const now = atom({ plugin: 'plan-band', key: 'now' } as const, 0)
const isHidden = atom({ plugin: 'plan-band', key: 'isHidden' } as const, false)

const PLAN_TOOL = 'mcp__plan-band__plan'
const STEP_TOOL = 'mcp__plan-band__step'
const TICK_MS = 5000
const PANE = 'plan'

const GUIDANCE = [
  '# Progress sidebar',
  'When work has 3 or more distinct steps (an issue, a multi-file change, a plan you are executing), call the `plan` tool once before starting, with every step and its `after` dependencies, then call `step` to mark each one in_progress and completed as you go. Re-call `plan` if the plan changes.',
  'When a step is handed to a subagent, start the Agent call\'s description with that step\'s id, e.g. `#3 write API tests`: the sidebar marks the step running and checks it off when the agent finishes, so do not call `step` for it. Steps that depend on several parallel subagent steps list all of them in `after`.',
  'Skip both tools for single-step or conversational requests.',
].join('\n\n')

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await update($, now, () => 0)
    await $.tool.register({
      name: 'plan',
      description:
        'Lay out a multi-step plan in the progress sidebar. Replaces any current plan. Each step has a short id ("1", "2", ...), a title, and optional `after`: ids of steps that must finish first.',
      isDeferred: false,
      inputSchema: {
        type: 'object',
        properties: {
          title: { type: 'string', description: 'What the plan accomplishes, a few words' },
          steps: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                id: { type: 'string' },
                title: { type: 'string', description: 'A few words' },
                after: { type: 'array', items: { type: 'string' } },
              },
              required: ['id', 'title'],
            },
          },
        },
        required: ['title', 'steps'],
      },
    })
    await $.tool.register({
      name: 'step',
      description: 'Move a step of the current plan to in_progress, completed or skipped.',
      isDeferred: false,
      inputSchema: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          status: { type: 'string', enum: ['in_progress', 'completed', 'skipped', 'pending'] },
        },
        required: ['id', 'status'],
      },
    })

    await $.command.register({ name: 'plan', description: 'Show the current plan in the sidebar' })
    $.clock.every(TICK_MS, () => void tick($))

    // A reload closes the pane; bring it back for a plan still under way.
    const current = await read($, plan)
    if (current !== null && !isPlanFinished(current) && !(await read($, isHidden))) {
      void $.ui.open({ id: PANE, title: current.title })
    }

    return next(e)
  })

  on('command.run', { command: 'plan' }, async $ => {
    const current = await read($, plan)
    if (current === null) return { text: 'No plan yet: Claude lays one out for multi-step work.' }

    await update($, isHidden, () => false)
    await $.ui.open({ id: PANE, title: current.title })

    return { text: 'Plan sidebar opened.' }
  })

  // Closing the sidebar keeps it closed until the next plan or /plan.
  on('ui.close', { id: PANE }, async ($, e, next) => {
    if (e.origin.kind === 'person') await update($, isHidden, () => true)

    return next(e)
  }).catch(($, e, next) => next(e))

  on('prompt.compose', async ($, e, next) => {
    const composed = await next(e)
    if (!e.tools.includes(PLAN_TOOL)) return composed

    return { sections: [...composed.sections, { id: 'plan-band:guidance', text: GUIDANCE, scope: 'session' as const }] }
  })

  on('tool.call', { tool: PLAN_TOOL }, async ($, e) => {
    const inputs = (e.steps ?? []) as StepInput[]
    if (inputs.length === 0) return { result: 'A plan needs at least one step.' }

    const at = await $.clock.now()
    await update($, plan, () => createPlan(String(e.title ?? 'Plan'), inputs, at))
    await update($, now, () => at)
    await update($, isHidden, () => false)
    await openSidebar($, String(e.title ?? 'Plan'))

    return { result: `Plan laid out in the sidebar: ${inputs.length} steps.` }
  })

  on('tool.call', { tool: STEP_TOOL }, async ($, e) => {
    const current = await read($, plan)
    const id = String(e.id)
    if (current === null || !current.steps.some(step => step.id === id)) {
      return { result: `No step ${id} in the current plan; call plan first.` }
    }

    const at = await $.clock.now()
    await update($, plan, p => (p === null ? p : setStatus(p, id, e.status as StepStatus, at)))
    await update($, now, () => at)

    return { result: `Step ${id} is ${e.status}.` }
  })

  // The step lights up as soon as its agent is dispatched, under the call's
  // id; once the call returns it either finished (foreground) or carries the
  // background agent's id, which the tick then watches.
  on('tool.call', { tool: 'Agent' }, async ($, e, next) => {
    const stepId = stepIdOf(e.description)
    const current = await read($, plan)
    if (stepId === undefined || current === null || !current.steps.some(step => step.id === stepId)) return next(e)

    const callId = e.tool_use_id
    const dispatchedAt = await $.clock.now()
    await update($, plan, p => (p === null ? p : startAgent(p, stepId, callId, dispatchedAt)))
    const ran = await next(e)
    const at = await $.clock.now()
    const launchedId = backgroundIdOf(ran.result)

    await update($, plan, p => {
      if (p === null) return p
      if (launchedId !== undefined) return backgroundAgent(p, callId, launchedId)
      return finishAgent(p, callId, ran.isError !== true && ran.deny === undefined, at)
    })

    return ran
  }).catch(($, e, next) => next(e)) // a tracking failure never blocks the subagent

  // A finished plan stays up until the next prompt, then clears.
  on('prompt.submit', async ($, e, next) => {
    const current = await read($, plan)
    if (current !== null && isPlanFinished(current)) {
      await update($, plan, () => null)
      await $.ui.close({ id: PANE })
    }

    return next(e)
  }).catch(($, e, next) => next(e))

  // The sidebar already shows what these calls did, so their transcript rows are
  // noise. An errored call still draws, so a failure is never hidden.
  on('ui.render', { component: ['ToolUse', 'ToolResult'] }, ($, e, next) => {
    const isOwnTool = e.props.tool === PLAN_TOOL || e.props.tool === STEP_TOOL
    if (!isOwnTool || e.props.isErrored) return next(e)

    const { Box } = $.ui.resolve(e)
    return <Box display="none" />
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const current = await read($, plan)
    const at = await read($, now)
    if (current === null) return <Text dimColor>No plan.</Text>

    const done = current.steps.filter(step => step.status === 'completed' || step.status === 'skipped').length
    const total = current.steps.length
    const elapsed = formatDuration(at - current.createdAt)
    const eta = etaMs(current, at)
    const isDone = done === total
    const timing = isDone
      ? `done in ${elapsed}`
      : `${eta === undefined ? 'ETA after first step' : `~${formatDuration(eta)} left`} · ${elapsed}`

    return (
      <Box flexDirection="column" rowGap={1}>
        <Box flexDirection="column">
          <Box flexDirection="row" columnGap={1}>
            <Text color={isDone ? 'success' : 'claude'}>
              {progressBar(done, total, Math.max(6, e.props.bodyColumns - 6))}
            </Text>
            <Text>{done}/{total}</Text>
          </Box>
          <Text dimColor>{timing}</Text>
        </Box>
        <Box flexDirection="column">
          {current.steps.map(step => {
            const readiness = readinessOf(current, step)
            const running = step.agents.filter(run => run.status === 'running').length
            const hasFailed = step.agents.some(run => run.status === 'failed')
            const took = step.startedAt === undefined ? '' : formatDuration((step.doneAt ?? at) - step.startedAt)
            const notes = [
              running > 0 ? `⚙ ${running > 1 ? `${running} agents` : 'agent'}` : '',
              readiness.kind === 'waiting' ? `waits on ${readiness.on.map(id => `#${id}`).join(' ')}` : '',
              took,
            ].filter(note => note !== '')

            return (
              <Box key={`step-${step.id}`} flexDirection="column">
                <Box flexDirection="row" columnGap={1}>
                  <Text color={colorOf(readiness.kind, hasFailed)}>{glyphOf(current, step)}</Text>
                  <Text
                    dimColor={readiness.kind === 'waiting' || step.status === 'skipped'}
                    strikethrough={step.status === 'skipped'}
                    wrap="truncate"
                  >
                    #{step.id} {step.title}
                  </Text>
                </Box>
                {hasFailed && <Text color="error">  agent failed</Text>}
                {notes.length > 0 && (
                  <Text dimColor wrap="truncate">
                    {'  '}
                    {notes.join(' · ')}
                  </Text>
                )}
              </Box>
            )
          })}
        </Box>
      </Box>
    )
  })
}

// Opened by the model rather than the person, the pane only seats on a wide
// terminal (144 columns, 110 once /plan has opened it); below that, say how
// to open it.
async function openSidebar($: EngineInterface, title: string) {
  const opened = await $.ui.open({ id: PANE, title })
  if (!opened.isPlaced) $.ui.toast('Plan ready: /plan opens the sidebar')
}

// The background agent's id when the Agent call returned before it finished.
function backgroundIdOf(result: unknown): string | undefined {
  if (typeof result !== 'object' || result === null) return undefined
  const record = result as { status?: unknown; agentId?: unknown }

  return record.status === 'async_launched' && typeof record.agentId === 'string' ? record.agentId : undefined
}

function glyphOf(p: Plan, step: Step): string {
  if (step.status === 'skipped') return '–'
  const kind = readinessOf(p, step).kind
  if (kind === 'done') return '✓'
  if (kind === 'running') return '●'
  if (kind === 'ready') return '○'

  return '◌'
}

function colorOf(kind: string, hasFailed: boolean): string {
  if (hasFailed) return 'error'
  if (kind === 'done') return 'success'
  if (kind === 'running') return 'claude'
  if (kind === 'ready') return 'text'

  return 'inactive'
}

// Keeps elapsed/ETA moving while a plan is open, and settles background
// subagents, whose Agent call returned before they finished.
async function tick($: EngineInterface) {
  const current = await read($, plan)
  if (current === null || isPlanFinished(current)) return

  const at = await $.clock.now()
  await update($, now, () => at)

  const waiting = backgroundAgentIds(current)
  if (waiting.length === 0) return

  const agents = await $.agent.list()
  for (const id of waiting) {
    const agent = agents.find(one => one.id === id)
    // An agent the list no longer holds has ended; its result was delivered.
    const status = agent?.status ?? 'completed'
    if (status === 'completed' || status === 'failed' || status === 'killed') {
      await update($, plan, p => (p === null ? p : finishAgent(p, id, status === 'completed', at)))
    }
  }
}
