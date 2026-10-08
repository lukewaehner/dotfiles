import { describe, expect, test } from 'claude-code/testing'

import {
  backgroundAgent,
  backgroundAgentIds,
  createPlan,
  etaMs,
  finishAgent,
  readinessOf,
  setStatus,
  startAgent,
  stepIdOf,
} from '../hooks/plan'

const MIN = 60_000

// 1 → (2,3,4,5 in parallel) → 6
const fanOut = () =>
  createPlan(
    'Ship it',
    [
      { id: '1', title: 'Scaffold' },
      { id: '2', title: 'API', after: ['1'] },
      { id: '3', title: 'UI', after: ['1'] },
      { id: '4', title: 'Tests', after: ['1'] },
      { id: '5', title: 'Docs', after: ['1'] },
      { id: '6', title: 'Integrate', after: ['2', '3', '4', '5'] },
    ],
    0,
  )

const stepOf = (plan: ReturnType<typeof fanOut>, id: string) => plan.steps.find(step => step.id === id)!

describe('readiness', () => {
  test('join_step_waits_on_every_unfinished_parallel_step', async () => {
    // arrange
    let plan = setStatus(fanOut(), '1', 'completed', 1 * MIN)
    plan = setStatus(plan, '3', 'completed', 2 * MIN)
    plan = setStatus(plan, '5', 'completed', 3 * MIN)

    // act
    const readiness = readinessOf(plan, stepOf(plan, '6'))

    // assert
    expect(readiness).toEqual({ kind: 'waiting', on: ['2', '4'] })
  })

  test('join_step_is_ready_once_parallel_steps_finish_in_any_order', async () => {
    // arrange
    let plan = setStatus(fanOut(), '1', 'completed', 1 * MIN)
    plan = setStatus(plan, '5', 'completed', 2 * MIN)
    plan = setStatus(plan, '2', 'completed', 3 * MIN)
    plan = setStatus(plan, '4', 'skipped', 4 * MIN)
    plan = setStatus(plan, '3', 'completed', 5 * MIN)

    // act
    const readiness = readinessOf(plan, stepOf(plan, '6'))

    // assert
    expect(readiness).toEqual({ kind: 'ready' })
  })

  test('dependency_on_an_unknown_step_is_dropped', async () => {
    // arrange
    const plan = createPlan('p', [{ id: '1', title: 'a', after: ['9', '1'] }], 0)

    // act
    const readiness = readinessOf(plan, stepOf(plan, '1'))

    // assert
    expect(readiness).toEqual({ kind: 'ready' })
  })
})

describe('subagents', () => {
  test('step_completes_only_when_all_its_agents_finish', async () => {
    // arrange
    let plan = startAgent(fanOut(), '2', 'a1', 1 * MIN)
    plan = startAgent(plan, '2', 'a2', 1 * MIN)

    // act
    plan = finishAgent(plan, 'a1', true, 2 * MIN)

    // assert
    expect(stepOf(plan, '2').status).toBe('in_progress')
    expect(stepOf(finishAgent(plan, 'a2', true, 3 * MIN), '2').status).toBe('completed')
  })

  test('failed_agent_leaves_its_step_open', async () => {
    // arrange
    const plan = startAgent(fanOut(), '3', 'a1', 1 * MIN)

    // act
    const settled = finishAgent(plan, 'a1', false, 2 * MIN)

    // assert
    expect(stepOf(settled, '3').status).toBe('in_progress')
  })

  test('step_id_is_read_from_a_leading_hash_in_the_description', async () => {
    expect([stepIdOf('#3 write API tests'), stepIdOf('[#12] docs'), stepIdOf('write #3')]).toEqual([
      '3',
      '12',
      undefined,
    ])
  })
})

describe('eta', () => {
  test('is_unknown_before_any_step_finishes', async () => {
    expect(etaMs(fanOut(), 5 * MIN)).toBe(undefined)
  })

  test('counts_parallel_steps_once_along_the_critical_path', async () => {
    // arrange: step 1 took 2 minutes, so each open step is costed at 2
    const plan = setStatus(setStatus(fanOut(), '1', 'in_progress', 0), '1', 'completed', 2 * MIN)

    // act
    const eta = etaMs(plan, 2 * MIN)

    // assert: one parallel layer (2..5) plus step 6, not five steps
    expect(eta).toBe(4 * MIN)
  })
})

describe('background agents', () => {
  test('only_background_agents_are_watched_for_completion', async () => {
    // arrange: two agents dispatched under their call ids
    let plan = startAgent(fanOut(), '2', 'toolu_a', 1 * MIN)
    plan = startAgent(plan, '3', 'toolu_b', 1 * MIN)

    // act: only the first went to the background
    plan = backgroundAgent(plan, 'toolu_a', 'agent-7')

    // assert
    expect(backgroundAgentIds(plan)).toEqual(['agent-7'])
  })
})
