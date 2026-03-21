# Project Bootstrap

Initialize a new project with proper context retrieval and subagent assignment.

## When to Use

Use this skill when starting a new project or task that requires:
- Context-aware initialization
- Subagent coordination
- Structured planning

## Input Parameters

```yaml
project_name: string        # Project identifier (e.g., "GPR-GUI-Optimization")
project_type: enum          # One of: [coding, research, review, mixed]
channel_id: string          # Discord/Telegram channel ID for delivery
goal: string               # One-line project goal (≤50 chars)
priority: enum             # One of: [high, normal, low] (default: normal)
```

## Workflow

### Step 1: Context Retrieval

Search for relevant patterns based on `project_type`:

**For coding projects:**
```bash
qmd search "subagent_manager" -c openclaw_workspace --limit 3
qmd search "Evidence Delivery" -c openclaw_workspace --limit 3
qmd search "code review" -c openclaw_workspace --limit 3
```

**For research projects:**
```bash
qmd search "researcher agent" -c openclaw_workspace --limit 3
qmd search "literature review" -c openclaw_workspace --limit 3
qmd search "evidence command" -c openclaw_workspace --limit 3
```

**For review projects:**
```bash
qmd search "reviewer agent" -c openclaw_workspace --limit 3
qmd search "checklist" -c openclaw_workspace --limit 3
qmd search "quality metrics" -c openclaw_workspace --limit 3
```

**For mixed projects:**
Run all three search sets above, deduplicate results.

### Step 2: Subagent Assignment

Based on `project_type`, determine subagent pipeline:

| Project Type | Primary Agent | Secondary | Tertiary |
|-------------|---------------|-----------|----------|
| coding | coder | reviewer | - |
| research | researcher | coder | reviewer |
| review | reviewer | researcher | - |
| mixed | researcher | coder | reviewer |

### Step 3: Generate Bootstrap Report

Format the output following EDL rules:

```markdown
EDL-ID: <timestamp>-<project_name>-bootstrap
Goal: <goal>
Inputs: project=<project_name>, type=<project_type>, channel=<channel_id>
Context: <key findings from qmd search, ≤3 lines>
Subagents: <agent1> → <agent2> → <agent3> (as applicable)
Plan:
1. <agent1>: <specific task>
2. <agent2>: <review/validation task>
3. <agent3>: <final check if applicable>
Evidence:
- qmd search "<primary_keyword>" -c openclaw_workspace --limit 3
- tail -n 20 /mnt/e/Openclaw/.openclaw/workspace/memory/$(date +%Y-%m-%d).md
Result/Conclusion: Project <project_name> initialized with <N> subagents
Risks: <any blockers or dependencies>
Next: Await user confirmation to dispatch subagents
```

## Output Format

Total output MUST be ≤8 lines (excluding EDL-ID and Evidence).

## Examples

### Example 1: Coding Project

**Input:**
```yaml
project_name: gpr-gui-qt-migration
project_type: coding
channel_id: "1478098802937303100"
goal: Migrate GPR GUI from Tkinter to PyQt6
priority: high
```

**Output:**
```markdown
EDL-ID: 20260309-gpr-gui-qt-migration-bootstrap
Goal: Migrate GPR GUI from Tkinter to PyQt6
Inputs: project=gpr-gui-qt-migration, type=coding, channel=1478098802937303100
Context: Qt packaging skill available; PyQt6 best practices documented
Subagents: coder → reviewer
Plan: 1) coder: Create PyQt6 migration branch with UI parity 2) reviewer: Validate UI/UX consistency and code quality
Result: Project initialized with 2 subagents, estimated 4h work
Risks: Qt dependencies may require Windows build testing
Next: Confirm to dispatch coder agent
```

### Example 2: Mixed Project

**Input:**
```yaml
project_name: gpr-algorithm-research
project_type: mixed
channel_id: "1476983838994600109"
goal: Research SVD background suppression algorithms for GPR
priority: normal
```

**Output:**
```markdown
EDL-ID: 20260309-gpr-algorithm-research-bootstrap
Goal: Research SVD background suppression algorithms for GPR
Inputs: project=gpr-algorithm-research, type=mixed, channel=1476983838994600109
Context: Existing GPR processing pipeline documented; SVD methods referenced in memory
Subagents: researcher → coder → reviewer
Plan: 1) researcher: Literature review of SVD/RPCA methods 2) coder: Prototype implementation 3) reviewer: Validate against requirements
Result: 3-phase project initialized, literature search first
Risks: External paper access may require VPN
Next: Confirm pipeline or adjust agent order
```

## Evidence Commands

Default evidence (always include):
```bash
# Project memory location
tail -n 20 /mnt/e/Openclaw/.openclaw/workspace/memory/$(date +%Y-%m-%d).md

# Relevant skill reference
qmd get qmd://openclaw_workspace/skills/project-bootstrap/SKILL.md --from 1 -l 30
```

## Notes

- Always wait for user confirmation before dispatching subagents
- If search returns no results, fall back to: `qmd get qmd://openclaw_workspace/skills/user-preferences/SKILL.md --from 1 -l 30`
- Respect user's "subagent_manager mandatory" rule - always use subagent_manager for applicable tasks
- Token-efficient: Use qmd search first, only use qmd get when necessary
