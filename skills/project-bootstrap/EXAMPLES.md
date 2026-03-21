# Project Bootstrap - Usage Examples

## Quick Start

### 启动一个编码项目

```
使用 project-bootstrap skill 启动项目：
- project_name: gpr-gui-optimization
- project_type: coding
- channel_id: 1478098802937303100
- goal: Optimize GPR GUI rendering performance
- priority: high
```

### 启动一个研究项目

```
使用 project-bootstrap skill 启动项目：
- project_name: gpr-svd-research
- project_type: research
- channel_id: 1476983838994600109
- goal: Research SVD-based background suppression
- priority: normal
```

### 启动一个审查项目

```
使用 project-bootstrap skill 启动项目：
- project_name: code-review-gpr-core
- project_type: review
- channel_id: 1476983838994600109
- goal: Review GPR core module for edge cases
- priority: high
```

## Expected Output

Each invocation produces an EDL-formatted bootstrap report:

```markdown
EDL-ID: 20260309-<project_name>-bootstrap
Goal: <goal>
Inputs: project=<name>, type=<type>, channel=<channel>
Context: <3-line summary from qmd search>
Subagents: <agent1> → <agent2> → <agent3>
Plan: 1) <agent1>: <task> 2) <agent2>: <task> 3) <agent3>: <task>
Result: Project initialized with N subagents
Risks: <blockers>
Next: Confirm to dispatch
```

## Integration with Subagent Manager

After bootstrap confirmation, automatically dispatch:

```bash
# If user confirms
openclaw agent dispatch <primary_agent> --project <project_name> --channel <channel_id>
```

## Notes

- Always produces ≤8 line output (excluding evidence)
- Always includes evidence commands
- Respects user's EDL rules
- Waits for confirmation before dispatching
