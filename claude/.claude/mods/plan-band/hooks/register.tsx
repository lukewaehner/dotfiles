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

const GUIDANCE = [
  '# Progress band',
  'When work has 3 or more distinct steps (an issue, a multi-file change, a plan you are executing), call the `plan` tool once before starting, with every step and its `after` dependencies, then call `step` to mark each one in_progress and completed as you go. Re-call `plan` if the plan changes.',
  'When a step is handed to a subagent, start the Agent call\'s description with that step\'s id, e.g. `#3 write API tests`: the band marks the step running and checks it off when the agent finishes, so do not call `step` for it. Steps that depend on several parallel subagent steps list all of them in `after`.',
  'Skip both tools for single-step or conversational requests.',
].join('\n\n')

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await update($, now, () => 0)
    await $.tool.register({
      name: 'plan',
      description:
        'Lay out a multi-step plan in the progress band above the prompt. Replaces any current plan. Each step has a short id ("1", "2", ...), a title, and optional `after`: ids of steps that must finish first.',
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

    $.clock.every(TICK_MS, () => void tick($))

    return next(e)
  })

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

    return { result: `Plan laid out in the band: ${inputs.length} steps.` }
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
    if (current !== null && isPlanFinished(current)) await update($, plan, () => null)

    return next(e)
  }).catch(($, e, next) => next(e))

  // The band already shows what these calls did, so their transcript rows are
  // noise. An errored call still draws, so a failure is never hidden.
  on('ui.render', { component: ['ToolUse', 'ToolResult'] }, ($, e, next) => {
    const isOwnTool = e.props.tool === PLAN_TOOL || e.props.tool === STEP_TOOL
    if (!isOwnTool || e.props.isErrored) return next(e)

    const { Box } = $.ui.resolve(e)
    return <Box display="none" />
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const current = await read($, plan)
    const at = await read($, now)
    if (e.props.hasSurvey || current === null || (await read($, isHidden))) return next(e)

    const { Box, Button, Text } = $.ui.resolve(e)
    const done = current.steps.filter(step => step.status === 'completed' || step.status === 'skipped').length
    const total = current.steps.length
    const elapsed = formatDuration(at - current.createdAt)
    const eta = etaMs(current, at)
    const barWidth = Math.max(8, Math.min(24, Math.floor(e.props.bodyColumns / 5)))
    const isDone = done === total
    const isCompact = total + 2 > e.props.maxRows

    return (
      <Box flexDirection="column">
        <Box flexDirection="row" columnGap={1}>
          <Text bold wrap="truncate">{current.title}</Text>
          <Text color={isDone ? 'success' : 'claude'}>{progressBar(done, total, barWidth)}</Text>
          <Text>{done}/{total}</Text>
          <Text dimColor>
            · {isDone ? `done in ${elapsed}` : `${eta === undefined ? 'ETA after first step' : `~${formatDuration(eta)} left`} · ${elapsed}`}
          </Text>
          <Button key="hide" label="hide" plain onPress={() => update($, isHidden, () => true)} />
        </Box>
        {isCompact ? (
          <Text wrap="truncate">{current.steps.map(step => `${glyphOf(current, step)}${step.id}`).join(' ')}</Text>
        ) : (
          current.steps.map(step => {
            const readiness = readinessOf(current, step)
            const running = step.agents.filter(run => run.status === 'running').length
            const hasFailed = step.agents.some(run => run.status === 'failed')
            const took = step.startedAt === undefined ? '' : formatDuration((step.doneAt ?? at) - step.startedAt)

            return (
              <Box key={`step-${step.id}`} flexDirection="row" columnGap={1}>
                <Text color={colorOf(readiness.kind, hasFailed)}>{glyphOf(current, step)}</Text>
                <Text
                  dimColor={readiness.kind === 'waiting' || step.status === 'skipped'}
                  strikethrough={step.status === 'skipped'}
                  wrap="truncate"
                >
                  #{step.id} {step.title}
                </Text>
                {running > 0 && <Text color="claude">⚙ {running > 1 ? `${running} agents` : 'agent'}</Text>}
                {hasFailed && <Text color="error">agent failed</Text>}
                {readiness.kind === 'waiting' && (
                  <Text dimColor>waits on {readiness.on.map(id => `#${id}`).join(' ')}</Text>
                )}
                {took !== '' && <Text dimColor>{took}</Text>}
              </Box>
            )
          })
        )}
      </Box>
    )
  })
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
