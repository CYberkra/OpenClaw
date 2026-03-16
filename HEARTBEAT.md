# HEARTBEAT

## Periodic Tasks

- Every 2 hours: report system status to Discord channel: 1479758987728650445
- Include: gateway status (running/port), disk usage summary, active subagents count, task queue summary, queued tasks if any, last commit hash if any.

## Post-Build Checks (After GPR_GUI build)

- [ ] **Release Version Tag** - Verify EXE filename or metadata contains version number per user rule (03-09)

## Checklist (Rotate Through These)

### Daily Checks (2-4 times per day)
- [ ] **Gateway Health** - Check main gateway (port 18890) status
- [ ] **Disk Usage** - Monitor workspace disk usage, warn if >80%
- [ ] **Active Subagents** - Count and report active subagents
- [ ] **Task Queue** - Check for queued tasks, report if any pending
- [ ] **Token Efficiency** - Monitor daily token consumption trend, alert if >50% spike
- [ ] **GPR Isolation Zone** - Check `isolated/GPR_GUI_evolve/` for pending optimizations ready to merge

### Weekly Checks (every few days)
- [ ] **Memory Maintenance** - Review recent `memory/YYYY-MM-DD.md` files, update `MEMORY.md`
- [ ] **Project Sync** - Check `repos/` for uncommitted changes, remind if stale
- [ ] **Log Cleanup** - Review and archive old logs if needed
- [ ] **Skill Sync** - Check subagent-manager skill version consistency between `repos/openclaw-skill-subagent-manager/` and `skills/`
- [ ] **GPR Performance Baseline** - Check isolated optimization results haven't regressed (compare to 236s→57s, 223ms→7ms benchmarks)
- [ ] **Rule Backup & Drift Audit (7-14 days)** - Follow `rules/self-backup-audit-v1.md` for lightweight rule consistency check + optional backup snapshot + commit/push decision

## When to Report (Not Just HEARTBEAT_OK)

Report actively when:
- Gateway is down or unstable
- Disk usage >80%
- Tasks are queued for >30 minutes
- Uncommitted changes in repos for >3 days
- Important events logged in recent memory files
- Token consumption spikes >50% vs baseline
- GPR isolation zone has completed optimization ready for merge
- EXE release uploaded without version tag
- Skill version mismatch detected

## State Tracking

Track last check times and baselines in `memory/heartbeat-state.json`:

```json
{
  "lastChecks": {
    "gateway": null,
    "disk": null,
    "subagents": null,
    "queue": null,
    "memory": null,
    "token": null,
    "isolation": null,
    "skillSync": null,
    "perfBaseline": null
  },
  "baselines": {
    "tokenDailyAvg": null,
    "gprOptRuntime": 57.42,
    "gprDepthConvert": 7.00
  }
}
```
