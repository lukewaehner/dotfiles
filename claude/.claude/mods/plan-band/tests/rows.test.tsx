import { expect, test } from 'claude-code/testing'

const stepRow = (isErrored: boolean) => ({
  component: 'ToolUse' as const,
  props: {
    tool_use_id: 'toolu_1',
    tool: 'mcp__plan-band__step',
    input: { id: '3', status: 'in_progress' },
    isRunning: false,
    isErrored,
    isInterrupted: false,
    output: 'Step 3 is in_progress.',
  },
})

test('band_tool_calls_draw_nothing_in_the_transcript', async $ => {
  for (const surface of ['terminal', 'desktop'] as const) {
    // act
    const ui = await $.ui.mount({ plugin: 'plan-band', surface, ...stepRow(false) })

    // assert
    expect(await ui.find({ type: 'Text' })).toBe(undefined)
    await ui.unmount()
  }
})
