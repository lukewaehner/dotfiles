import { expect, mock, test } from 'claude-code/testing'

const PLAN = {
  title: 'Ship it',
  steps: [
    { id: '1', title: 'Scaffold' },
    { id: '2', title: 'API', after: ['1'] },
    { id: '3', title: 'UI', after: ['1'] },
    { id: '6', title: 'Integrate', after: ['2', '3'] },
  ],
}

test('band_shows_the_join_step_waiting_on_its_open_parallel_steps', async ($, on) => {
  const clock = mock.clock(on, { now: 1_000_000 })
  for (const surface of ['terminal', 'desktop'] as const) {
    // arrange
    await $.tool.call({ tool: 'mcp__plan-band__plan', ...PLAN })
    await clock.advance(60_000)
    await $.tool.call({ tool: 'mcp__plan-band__step', id: '1', status: 'completed' })
    await $.tool.call({ tool: 'mcp__plan-band__step', id: '3', status: 'completed' })

    // act
    const ui = await $.ui.mount({
      plugin: 'plan-band',
      surface,
      component: 'AbovePrompt',
      props: { hasSurvey: false, isWorking: true, maxRows: 12, bodyColumns: 80, scroll: { offset: 0, bodyRows: 12 }, view: {} },
    })

    // assert
    expect(await ui.find({ type: 'Text', text: /waits on #2$/ })).toBeDefined()
    expect(await ui.find({ type: 'Text', text: '2/4' })).toBeDefined()
    await ui.unmount()
  }
})

// Regression: a registered tool's result must be text (or content blocks);
// the engine refused the object results the tools first returned.
test('plan_and_step_tools_answer_with_text', async ($, on) => {
  // arrange
  mock.clock(on, { now: 1_000_000 })

  // act
  const planned = await $.tool.call({ tool: 'mcp__plan-band__plan', ...PLAN })
  const stepped = await $.tool.call({ tool: 'mcp__plan-band__step', id: '1', status: 'in_progress' })

  // assert
  expect([typeof planned.result, typeof stepped.result]).toEqual(['string', 'string'])
})
