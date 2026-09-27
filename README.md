# agentseism-example

A worked example of **[AgentSeism](https://github.com/lyr-ai/agentseism)**, CI for
stochastic AI agents, running as a GitHub check on real pull requests.

**The agent here is simulated.** [`agent/support_agent.py`](agent/support_agent.py)
is a customer-support "agent" with real handler code and fixed per-task success
rates. Which runs fail is pseudo-random, derived from the code, the task and the
run number. It costs nothing to run and needs no API key. The CI around it is the
real thing: the `seism` CLI, the committed baseline, the GitHub Action and the PR
report.

## The two example PRs

| PR | What changed | AgentSeism |
|---|---|---|
| harmless | a comment and a log message | the success rates are unchanged, so the runs only jitter |
| broken checkout | a bug in the `checkout` handler | `checkout` fails every run |

Open the pull requests in this repository to see the check and the report
AgentSeism posts on each.

## How it's wired

- [`.agentseism/contract.yaml`](.agentseism/contract.yaml): the runner, the
  evaluator, and both regression gates.
- [`.agentseism/baselines/main.json`](.agentseism/baselines/main.json): the
  baseline, recorded on `main` with `seism baseline --trials 8` and committed.
- [`.github/workflows/agentseism.yml`](.github/workflows/agentseism.yml): runs
  `seism check --trials 8` on every PR and posts the report.

For real-agent evidence and limitations, see the
[AgentSeism README](https://github.com/lyr-ai/agentseism#evidence).
