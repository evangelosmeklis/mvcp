# MVCP (Model Version Control Protocol)

A lightweight, Git-compatible version control protocol designed specifically for AI agents to save, restore, and diff checkpoints during code or data transformations.

## 🧩 Overview

**MVCP** introduces a unified and human-readable system for agent iteration tracking, enabling rollback, auditing, and collaboration. It serves as a thin layer on top of Git, making it perfect for AI agent workflows.

# TODO:
MVCP should also server as a tool which multiple agents will use when they work towards a common goal like building a repo autonomously

## 📦 Installation

```bash
pip install mvcp (not yet on pip, will be soon)
```

MVCP requires Git to be installed on your system. The library automatically handles:
- Git repository initialization (if needed)
- Git user configuration (if not already set up)
- Creating necessary directory structures for metadata

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

### Start the API server for AI agents

```bash
mvcp serve --host 0.0.0.0 --port 8000
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

### CLI Integration

Agents can invoke MVCP as a CLI subprocess:

```python
subprocess.run(["mvcp", "save", "--agent", "planner", "--step", "5"])
```

### Python Library Integration

Or import it as a module:

```python
from mvcp import save
save(agent="planner", step=5, description="generated plan scorer")
```

### HTTP API Integration (MCP-Compatible)

MVCP provides an HTTP API server for AI agents to call as a tool:

```bash
# Start the server
mvcp serve --host 0.0.0.0 --port 8000
```

The API server exposes endpoints for all MVCP operations:

- `GET /schema` - Get the tool schema in MCP-compatible format
- `POST /tool/mvcp` - Call the MVCP tool with the provided parameters
- `POST /save` - Save a checkpoint
- `POST /list` - List checkpoints
- `POST /restore` - Restore to a checkpoint
- `POST /diff` - Show diff between checkpoints

### MCP-Compatible Tool Schema

The MVCP tool provides a Model Context Protocol (MCP) compatible schema:

```json
{
  "type": "function",
  "function": {
    "name": "mvcp",
    "description": "Model Version Control Protocol for saving, restoring, and comparing checkpoints during code transformations",
    "parameters": {
      "type": "object",
      "properties": {
        "action": {
          "type": "string",
          "enum": ["save", "list", "restore", "diff"],
          "description": "The action to perform"
        },
        "agent": {
          "type": "string",
          "description": "Name of the agent"
        },
        "step": {
          "type": "integer",
          "description": "Step number in the agent's workflow"
        },
        "description": {
          "type": "string",
          "description": "Description of the changes"
        },
        "tools_used": {
          "type": "array",
          "items": {"type": "string"},
          "description": "List of tools used by the agent"
        },
        "checkpoint": {
          "type": "string",
          "description": "Checkpoint tag to restore to"
        },
        "checkpoint1": {
          "type": "string",
          "description": "First checkpoint for comparison"
        },
        "checkpoint2": {
          "type": "string",
          "description": "Second checkpoint for comparison"
        }
      },
      "required": ["action"]
    }
  }
}
```

### Example API Usage

```python
import requests

# Get the tool schema
response = requests.get("http://localhost:8000/schema")
schema = response.json()

# Call the tool to save a checkpoint
tool_call = {
    "name": "mvcp",
    "arguments": {
        "action": "save",
        "agent": "coding_assistant",
        "step": 1,
        "description": "Initial code generation",
        "tools_used": ["code_generator", "linter"]
    }
}
response = requests.post("http://localhost:8000/tool/mvcp", json=tool_call)
result = response.json()
print(f"Checkpoint created: {result['tag']}")
```

## 🔧 Contributing

We welcome contributions from the community! Please check out our [Contributing Guidelines](CONTRIBUTING.md) to get started.

Here's how you can contribute:
- Report bugs and request features by creating [issues](https://github.com/evangelosmeklis/mvcp/issues)
- Submit pull requests for bug fixes or new features
- Improve documentation
- Share ideas and feedback

All contributors are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md).


## 📜 License

Distributed under the MIT license. See the [LICENSE](LICENSE) file for more details.