"""
Command-line interface for MVCP.
"""

import sys
import click
from typing import List, Optional

from mvcp.core import save, restore, diff, list_checkpoints
from mvcp.server import run_server


@click.group()
@click.version_option()
def cli():
    """MVCP - Model Version Control Protocol for AI agent workflows."""
    pass


@cli.command(name="save")
@click.option("--agent", "-a", required=True, help="Name of the agent")
@click.option("--step", "-s", required=True, type=int, help="Step number")
@click.option("--desc", "-d", default="", help="Description of the changes")
@click.option("--tools", "-t", multiple=True, help="Tools used by the agent")
def save_cmd(agent: str, step: int, desc: str, tools: List[str]):
    """Save a checkpoint with the current state."""
    try:
        tag = save(agent=agent, step=step, description=desc, tools_used=list(tools))
        click.echo(f"Checkpoint created: {tag}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command(name="list")
@click.option("--agent", "-a", help="Filter by agent name")
@click.option("--step", "-s", type=int, help="Filter by step number")
def list_cmd(agent: Optional[str], step: Optional[int]):
    """List all checkpoints, optionally filtered by agent and step."""
    try:
        tags = list_checkpoints(agent=agent, step=step)
        if not tags:
            click.echo("No checkpoints found")
            return
        
        for tag in tags:
            click.echo(tag)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command(name="restore")
@click.argument("checkpoint")
def restore_cmd(checkpoint: str):
    """Restore to a specific checkpoint."""
    try:
        restore(checkpoint=checkpoint)
        click.echo(f"Restored to checkpoint: {checkpoint}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command(name="diff")
@click.argument("checkpoint1")
@click.argument("checkpoint2")
def diff_cmd(checkpoint1: str, checkpoint2: str):
    """Show diff between two checkpoints."""
    try:
        diff_output = diff(checkpoint1=checkpoint1, checkpoint2=checkpoint2)
        click.echo(diff_output)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command(name="serve")
@click.option("--host", default="0.0.0.0", help="Host to bind the server to")
@click.option("--port", default=8000, type=int, help="Port to bind the server to")
def serve_cmd(host: str, port: int):
    """Start the MVCP API server for AI agent access."""
    click.echo(f"Starting MVCP API server at http://{host}:{port}")
    try:
        run_server(host=host, port=port)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli() 