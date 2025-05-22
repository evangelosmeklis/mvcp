"""
MVCP Tool Interface for AI Agents

This module provides a tool interface for AI agents to interact with MVCP
following the Model Context Protocol (MCP) standards.
"""

import json
from typing import Dict, List, Optional, Any, Union

from mvcp.core import save, restore, diff, list_checkpoints


def format_tool_schema() -> Dict[str, Any]:
    """
    Return the tool schema in MCP-compatible JSON Schema format.
    
    This function returns a schema that can be used by AI systems
    to understand how to call the MVCP functions.
    """
    return {
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
                        "description": "The action to perform (save a checkpoint, list checkpoints, restore to a checkpoint, or show diff between checkpoints)"
                    },
                    "agent": {
                        "type": "string",
                        "description": "Name of the agent (required for 'save', optional filter for 'list')"
                    },
                    "step": {
                        "type": "integer",
                        "description": "Step number in the agent's workflow (required for 'save', optional filter for 'list')"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the changes (for 'save' action)"
                    },
                    "tools_used": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "List of tools used by the agent (for 'save' action)"
                    },
                    "checkpoint": {
                        "type": "string",
                        "description": "Checkpoint tag to restore to (for 'restore' action)"
                    },
                    "checkpoint1": {
                        "type": "string",
                        "description": "First checkpoint for comparison (for 'diff' action)"
                    },
                    "checkpoint2": {
                        "type": "string",
                        "description": "Second checkpoint for comparison (for 'diff' action)"
                    }
                },
                "required": ["action"]
            }
        }
    }


def handle_tool_call(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle a tool call with the given parameters.
    
    Args:
        params: Dictionary of parameters for the tool call
        
    Returns:
        Dictionary with the results of the operation
    """
    action = params.get("action")
    
    try:
        if action == "save":
            # Validate required parameters
            if "agent" not in params:
                return {"error": "Missing required parameter: agent"}
            if "step" not in params:
                return {"error": "Missing required parameter: step"}
            
            # Get optional parameters
            description = params.get("description", "")
            tools_used = params.get("tools_used", [])
            
            # Call save function
            tag = save(
                agent=params["agent"],
                step=params["step"],
                description=description,
                tools_used=tools_used
            )
            
            return {
                "success": True,
                "tag": tag,
                "message": f"Checkpoint created: {tag}"
            }
            
        elif action == "list":
            # Get optional filter parameters
            agent = params.get("agent")
            step = params.get("step")
            
            # Call list_checkpoints function
            tags = list_checkpoints(agent=agent, step=step)
            
            return {
                "success": True,
                "checkpoints": tags
            }
            
        elif action == "restore":
            # Validate required parameters
            if "checkpoint" not in params:
                return {"error": "Missing required parameter: checkpoint"}
            
            # Call restore function
            restore(checkpoint=params["checkpoint"])
            
            return {
                "success": True,
                "message": f"Restored to checkpoint: {params['checkpoint']}"
            }
            
        elif action == "diff":
            # Validate required parameters
            if "checkpoint1" not in params:
                return {"error": "Missing required parameter: checkpoint1"}
            if "checkpoint2" not in params:
                return {"error": "Missing required parameter: checkpoint2"}
            
            # Call diff function
            diff_output = diff(
                checkpoint1=params["checkpoint1"],
                checkpoint2=params["checkpoint2"]
            )
            
            return {
                "success": True,
                "diff": diff_output
            }
            
        else:
            return {
                "error": f"Unknown action: {action}",
                "valid_actions": ["save", "list", "restore", "diff"]
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def process_tool_request(request_json: Union[str, Dict]) -> Dict[str, Any]:
    """
    Process a tool request in MCP format.
    
    Args:
        request_json: JSON string or dictionary containing the tool request
        
    Returns:
        Dictionary with the results to be returned to the caller
    """
    # Parse request if it's a string
    if isinstance(request_json, str):
        try:
            request = json.loads(request_json)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON in request"}
    else:
        request = request_json
    
    # Extract parameters and handle the tool call
    params = request.get("arguments", {})
    result = handle_tool_call(params)
    
    return result 