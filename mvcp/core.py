"""
Core MVCP functionality for creating, listing, restoring, and diffing checkpoints.
"""

import os
import json
import subprocess
from datetime import datetime
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mvcp")

# Constants
META_DIR = ".agent-meta"
TAG_PREFIX = "mvcp"


def _run_git_command(cmd: List[str]) -> Tuple[int, str, str]:
    """Run a git command and return exit code, stdout, and stderr."""
    process = subprocess.Popen(
        ["git"] + cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr


def _format_tag(agent: str, step: int, timestamp: Optional[str] = None) -> str:
    """Format a tag according to MVCP conventions."""
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%dT%H%M")
    return f"{TAG_PREFIX}/{agent}/step{step}@{timestamp}"


def _parse_tag(tag: str) -> Dict[str, Any]:
    """Parse a tag into its components."""
    if not tag.startswith(f"{TAG_PREFIX}/"):
        raise ValueError(f"Invalid tag format: {tag}")
    
    parts = tag.split("/")
    if len(parts) != 3:
        raise ValueError(f"Invalid tag format: {tag}")
    
    step_and_timestamp = parts[2].split("@")
    if len(step_and_timestamp) != 2:
        raise ValueError(f"Invalid tag format: {tag}")
    
    step = step_and_timestamp[0]
    if not step.startswith("step"):
        raise ValueError(f"Invalid step format: {step}")
    
    try:
        step_num = int(step[4:])
    except ValueError:
        raise ValueError(f"Invalid step number: {step}")
    
    return {
        "agent": parts[1],
        "step": step_num,
        "timestamp": step_and_timestamp[1]
    }


def _get_parent_checkpoint(agent: str, step: int) -> Optional[str]:
    """Get the parent checkpoint for a given agent and step."""
    if step <= 1:
        return None
    
    tags = list_checkpoints(agent=agent, step=step-1)
    if not tags:
        return None
    
    # Return the most recent one
    return tags[-1]


def save(agent: str, step: int, description: str = "", tools_used: Optional[List[str]] = None) -> str:
    """
    Save a checkpoint with the current state.
    
    Args:
        agent: The name of the agent creating the checkpoint
        step: The step number in the agent's workflow
        description: A short description of the changes
        tools_used: A list of tools used by the agent
        
    Returns:
        The created tag name
    """
    # Ensure meta directory exists
    os.makedirs(META_DIR, exist_ok=True)
    
    # Stage all changes
    returncode, stdout, stderr = _run_git_command(["add", "--all"])
    if returncode != 0:
        raise RuntimeError(f"Failed to stage changes: {stderr}")
    
    # Create timestamp
    timestamp = datetime.now().strftime("%Y%m%dT%H%M")
    
    # Format tag
    tag = _format_tag(agent, step, timestamp)
    
    # Get parent checkpoint
    parent_checkpoint = _get_parent_checkpoint(agent, step)
    
    # Create commit message
    commit_message = f"checkpoint(mvcp): {agent} step {step} - {description}"
    
    # Create commit
    returncode, stdout, stderr = _run_git_command(["commit", "-m", commit_message])
    if returncode != 0:
        raise RuntimeError(f"Failed to create commit: {stderr}")
    
    # Create tag
    returncode, stdout, stderr = _run_git_command(["tag", tag])
    if returncode != 0:
        raise RuntimeError(f"Failed to create tag: {stderr}")
    
    # Create metadata
    metadata = {
        "agent": agent,
        "step": step,
        "timestamp": datetime.now().isoformat(),
        "description": description,
        "parent_checkpoint": parent_checkpoint,
        "tools_used": tools_used or []
    }
    
    # Write metadata to file
    meta_path = os.path.join(META_DIR, f"{tag}.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"Created checkpoint: {tag}")
    return tag


def list_checkpoints(agent: Optional[str] = None, step: Optional[int] = None) -> List[str]:
    """
    List all checkpoints, optionally filtered by agent and step.
    
    Args:
        agent: Filter by agent name
        step: Filter by step number
        
    Returns:
        List of matching tags
    """
    # Get all tags
    returncode, stdout, stderr = _run_git_command(["tag", "-l", f"{TAG_PREFIX}/*"])
    if returncode != 0:
        raise RuntimeError(f"Failed to list tags: {stderr}")
    
    tags = stdout.strip().split("\n")
    tags = [tag for tag in tags if tag]  # Remove empty strings
    
    # Filter by agent and step if provided
    if agent or step is not None:
        filtered_tags = []
        for tag in tags:
            try:
                tag_info = _parse_tag(tag)
                if agent and tag_info["agent"] != agent:
                    continue
                if step is not None and tag_info["step"] != step:
                    continue
                filtered_tags.append(tag)
            except ValueError:
                continue
        tags = filtered_tags
    
    return tags


def restore(checkpoint: str) -> None:
    """
    Restore to a specific checkpoint.
    
    Args:
        checkpoint: The tag to restore to
    """
    # Validate tag format
    try:
        _parse_tag(checkpoint)
    except ValueError as e:
        raise ValueError(f"Invalid checkpoint format: {e}")
    
    # Check if tag exists
    returncode, stdout, stderr = _run_git_command(["tag", "-l", checkpoint])
    if returncode != 0 or not stdout.strip():
        raise ValueError(f"Checkpoint not found: {checkpoint}")
    
    # Perform reset
    returncode, stdout, stderr = _run_git_command(["reset", "--hard", checkpoint])
    if returncode != 0:
        raise RuntimeError(f"Failed to restore checkpoint: {stderr}")
    
    logger.info(f"Restored to checkpoint: {checkpoint}")


def diff(checkpoint1: str, checkpoint2: str) -> str:
    """
    Show diff between two checkpoints.
    
    Args:
        checkpoint1: The first checkpoint
        checkpoint2: The second checkpoint
        
    Returns:
        Git diff output
    """
    # Validate tag formats
    try:
        _parse_tag(checkpoint1)
        _parse_tag(checkpoint2)
    except ValueError as e:
        raise ValueError(f"Invalid checkpoint format: {e}")
    
    # Run diff
    returncode, stdout, stderr = _run_git_command(["diff", checkpoint1, checkpoint2])
    if returncode not in [0, 1]:  # Git diff returns 1 if there are differences
        raise RuntimeError(f"Failed to diff checkpoints: {stderr}")
    
    return stdout 