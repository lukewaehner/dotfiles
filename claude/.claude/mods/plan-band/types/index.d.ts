export type StepStatus = 'pending' | 'in_progress' | 'completed' | 'skipped'

export type AgentRun = { id: string; status: 'running' | 'done' | 'failed'; isBackground?: boolean }

export type Step = {
  id: string
  title: string
  status: StepStatus
  after: string[]
  startedAt?: number
  doneAt?: number
  agents: AgentRun[]
}

export type Plan = { title: string; createdAt: number; steps: Step[] }

declare module 'claude-code' {
  interface PluginState {
    'plan-band': { plan: Plan | null; now: number; isHidden: boolean }
  }
}
