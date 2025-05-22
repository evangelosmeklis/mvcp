# MVCP (Model Version Control Protocol)

A lightweight, Git-compatible version control protocol designed specifically for AI agents to save, restore, and diff checkpoints during code or data transformations.

## 🧩 Overview

**MVCP** introduces a unified and human-readable system for agent iteration tracking, enabling rollback, auditing, and collaboration. It serves as a thin layer on top of Git, making it perfect for AI agent workflows.

## 📦 Installation

```bash
pip install mvcp
```

## 🚀 Quick Start

### Save a checkpoint

```bash
mvcp save --agent refactorer --step 3 --desc "Refactored utils"
```

### List all checkpoints

```bash
mvcp list
```

### Filter checkpoints by agent

```bash
mvcp list --agent refactorer
```

### Restore to a checkpoint

```bash
mvcp restore mvcp/refactorer/step3@20240522T0932
```

### Show diff between checkpoints

```bash
mvcp diff mvcp/agentA/step2 mvcp/agentA/step3
```

## 🧠 Protocol Conventions

### Tag Format

```
mvcp/<agent>/<step>@<timestamp>
```

Example: `mvcp/planner/step3@20240522T0942`

### Metadata JSON

MVCP stores additional metadata in `.agent-meta/<tag>.json`:

```json
{
  "agent": "planner",
  "step": 3,
  "timestamp": "2025-05-22T09:42:00Z",
  "description": "Improved scoring logic",
  "parent_checkpoint": "mvcp/planner/step2@20240522T0930",
  "tools_used": ["optimizer", "unit_tester"]
}
```

### Commit Message Format

```
checkpoint(mvcp): <agent> step <step> - <desc>
```

## 🧩 Agent Integration

Agents can invoke MVCP as a CLI subprocess:

```python
subprocess.run(["mvcp", "save", "--agent", "planner", "--step", "5"])
```

Or import it as a module:

```python
from mvcp import save
save(agent="planner", step=5, description="generated plan scorer")
```

## 🔧 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📌 License

MIT 