"""
MVCP HTTP Server

This module provides an HTTP API server that exposes MVCP functionality
to AI agents using the Model Context Protocol (MCP) standards.
"""

import os
import json
from typing import Dict, Any, Optional, List, Union, Literal

from fastapi import FastAPI, HTTPException, Body
import uvicorn
from pydantic import BaseModel, Field

from mvcp.tool import format_tool_schema, handle_tool_call


# Create FastAPI app
app = FastAPI(
    title="MVCP Tool API",
    description="Model Version Control Protocol API for AI agents",
    version="0.1.0"
)


class ToolCallRequest(BaseModel):
    """Model for tool call requests."""
    name: str = Field(description="The name of the tool to call (should be 'mvcp')")
    arguments: Dict[str, Any] = Field(description="The arguments for the tool call")


class SaveParams(BaseModel):
    """Parameters for the save action."""
    action: Literal["save"] = "save"
    agent: str = Field(description="Name of the agent")
    step: int = Field(description="Step number in the agent's workflow")
    description: Optional[str] = Field(None, description="Description of the changes")
    tools_used: Optional[List[str]] = Field(None, description="List of tools used by the agent")


class ListParams(BaseModel):
    """Parameters for the list action."""
    action: Literal["list"] = "list"
    agent: Optional[str] = Field(None, description="Filter by agent name")
    step: Optional[int] = Field(None, description="Filter by step number")


class RestoreParams(BaseModel):
    """Parameters for the restore action."""
    action: Literal["restore"] = "restore"
    checkpoint: str = Field(description="Checkpoint tag to restore to")


class DiffParams(BaseModel):
    """Parameters for the diff action."""
    action: Literal["diff"] = "diff"
    checkpoint1: str = Field(description="First checkpoint for comparison")
    checkpoint2: str = Field(description="Second checkpoint for comparison")


@app.get("/")
async def root():
    """Root endpoint that provides basic information about the API."""
    return {
        "name": "MVCP Tool API",
        "version": "0.1.0",
        "description": "Model Version Control Protocol API for AI agents"
    }


@app.get("/schema")
async def get_schema():
    """Get the tool schema in MCP-compatible format."""
    return format_tool_schema()


@app.post("/tool/mvcp")
async def call_tool(request: ToolCallRequest):
    """
    Call the MVCP tool with the provided parameters.
    
    This is the main endpoint that AI agents should use to interact with MVCP.
    """
    if request.name != "mvcp":
        raise HTTPException(status_code=400, detail=f"Unknown tool: {request.name}")
    
    result = handle_tool_call(request.arguments)
    
    if "error" in result and not result.get("success", False):
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@app.post("/save")
async def save_checkpoint(params: SaveParams):
    """Save a checkpoint with the current state."""
    result = handle_tool_call(params.dict(exclude_none=True))
    
    if "error" in result and not result.get("success", False):
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@app.post("/list")
async def list_checkpoints_endpoint(params: ListParams):
    """List all checkpoints, optionally filtered by agent and step."""
    result = handle_tool_call(params.dict(exclude_none=True))
    
    if "error" in result and not result.get("success", False):
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@app.post("/restore")
async def restore_checkpoint(params: RestoreParams):
    """Restore to a specific checkpoint."""
    result = handle_tool_call(params.dict(exclude_none=True))
    
    if "error" in result and not result.get("success", False):
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@app.post("/diff")
async def diff_checkpoints(params: DiffParams):
    """Show diff between two checkpoints."""
    result = handle_tool_call(params.dict(exclude_none=True))
    
    if "error" in result and not result.get("success", False):
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """Run the MVCP API server."""
    uvicorn.run("mvcp.server:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    # Get host and port from environment variables or use defaults
    host = os.environ.get("MVCP_HOST", "0.0.0.0")
    port = int(os.environ.get("MVCP_PORT", 8000))
    
    run_server(host=host, port=port) 