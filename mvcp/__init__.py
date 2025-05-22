"""
MVCP - Model Version Control Protocol

A lightweight, Git-compatible version control protocol for AI agents
to save, restore, and diff checkpoints during code transformations.
"""

from mvcp.core import save, restore, diff, list_checkpoints

__version__ = "0.1.0"
__all__ = ["save", "restore", "diff", "list_checkpoints"] 