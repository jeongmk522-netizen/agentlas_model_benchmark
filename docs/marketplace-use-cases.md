# Agent Team Marketplace Use Cases

Date: 2026-06-02

These 10 team use cases are public-safe marketplace specs. Nine come from the long-timeout Agentlas model benchmark. One non-public case is intentionally replaced by an unscored public procurement workflow.

| Prompt | Marketplace team | Selected model | Score | Avg wall-time evidence |
|--------|------------------|----------------|------:|------------------------|
| P01 | [Small Fund Research OS](../marketplace/agent-teams/benchmark-small-fund-research-os.en.json) | gpt-5.5 | 96.0 | 68.048s |
| P02 | [AML & Fraud Investigation Team](../marketplace/agent-teams/benchmark-aml-fraud-investigation-team.en.json) | gemini-3.1-pro-preview | 96.0 | 38.574s |
| P03 | [Disaster Drone Swarm Command](../marketplace/agent-teams/benchmark-disaster-drone-swarm-command.en.json) | solar-pro2 | 98.0 | 10.381s |
| P04 | [Film Studio Production OS](../marketplace/agent-teams/benchmark-film-studio-production-os.en.json) | solar-pro2 | 96.0 | 8.204s |
| P05 | [AI Marketing Agency HQ](../marketplace/agent-teams/benchmark-ai-marketing-agency-hq.en.json) | solar-pro2 | 96.0 | 9.467s |
| P06 | [Enterprise Software Delivery HQ](../marketplace/agent-teams/benchmark-enterprise-software-delivery-hq.en.json) | solar-pro2 | 96.0 | 8.403s |
| P07 | [Hospital Operations Command Center](../marketplace/agent-teams/benchmark-hospital-operations-command-center.en.json) | solar-pro2 | 96.0 | 9.877s |
| P08 | [Supply Chain Control Tower](../marketplace/agent-teams/benchmark-supply-chain-control-tower.en.json) | solar-pro2 | 96.0 | 9.774s |
| P09 | [SOC Threat Response HQ](../marketplace/agent-teams/benchmark-soc-threat-response-hq.en.json) | solar-pro2 | 95.0 | 9.999s |
| S10 | [Vendor Risk & Procurement Review Desk](../marketplace/agent-teams/benchmark-vendor-risk-procurement-desk.en.json) | public-safe-template | unscored | n/a |

## Web Marketplace Path

The same JSON specs are exported into the Agentlas web app at `src/lib/teams/samples/` and wired into `src/lib/teams/catalog.ts`, so they appear on `/marketplace` under ready-made agent teams and at `/marketplace/team/<slug>`.

## Public Files

- `marketplace/agent-teams/manifest.json`: index for all 10 use cases.
- `marketplace/agent-teams/*.json`: Korean marketplace specs.
- `marketplace/agent-teams/*.en.json`: English marketplace specs.
