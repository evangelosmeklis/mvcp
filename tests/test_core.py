"""
Tests for core MVCP functionality.
"""

import os
import unittest
from unittest import mock
import tempfile
import shutil
from pathlib import Path

from mvcp.core import (
    _format_tag,
    _parse_tag,
    save,
    list_checkpoints,
    restore,
    diff,
)


class TestTagFormatting(unittest.TestCase):
    """Test tag formatting and parsing functions."""
    
    def test_format_tag(self):
        """Test _format_tag function."""
        tag = _format_tag("test", 1, "20240522T0942")
        self.assertEqual(tag, "mvcp/test/step1@20240522T0942")
    
    def test_parse_tag(self):
        """Test _parse_tag function."""
        tag_info = _parse_tag("mvcp/test/step1@20240522T0942")
        self.assertEqual(tag_info["agent"], "test")
        self.assertEqual(tag_info["step"], 1)
        self.assertEqual(tag_info["timestamp"], "20240522T0942")
    
    def test_parse_invalid_tag(self):
        """Test _parse_tag with invalid tag formats."""
        with self.assertRaises(ValueError):
            _parse_tag("invalid")
        
        with self.assertRaises(ValueError):
            _parse_tag("mvcp/test")
        
        with self.assertRaises(ValueError):
            _parse_tag("mvcp/test/step1")
        
        with self.assertRaises(ValueError):
            _parse_tag("mvcp/test/invalid@20240522T0942")


class TestGitOperations(unittest.TestCase):
    """Test Git operations using mocks."""
    
    @mock.patch("mvcp.core._run_git_command")
    @mock.patch("mvcp.core.os.makedirs")
    @mock.patch("mvcp.core.open", new_callable=mock.mock_open)
    def test_save(self, mock_open, mock_makedirs, mock_run_git):
        """Test save function."""
        # Mock Git command responses
        mock_run_git.side_effect = [
            (0, "", ""),  # git add
            (0, "", ""),  # git commit
            (0, "", ""),  # git tag
        ]
        
        # Call save
        tag = save("test", 1, "Test description")
        
        # Check that Git commands were called
        self.assertEqual(mock_run_git.call_count, 3)
        
        # Check that metadata file was written
        mock_makedirs.assert_called_once()
        mock_open.assert_called_once()
    
    @mock.patch("mvcp.core._run_git_command")
    def test_list_checkpoints(self, mock_run_git):
        """Test list_checkpoints function."""
        mock_run_git.return_value = (0, "mvcp/test/step1@20240522T0942\nmvcp/test/step2@20240522T0943\n", "")
        
        # Call list_checkpoints
        tags = list_checkpoints()
        
        # Check results
        self.assertEqual(len(tags), 2)
        self.assertEqual(tags[0], "mvcp/test/step1@20240522T0942")
        self.assertEqual(tags[1], "mvcp/test/step2@20240522T0943")
        
        # Test filtering
        mock_run_git.return_value = (0, "mvcp/test/step1@20240522T0942\nmvcp/other/step1@20240522T0943\n", "")
        
        # Call list_checkpoints with filter
        tags = list_checkpoints(agent="test")
        
        # Check results
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0], "mvcp/test/step1@20240522T0942")
    
    @mock.patch("mvcp.core._run_git_command")
    def test_restore(self, mock_run_git):
        """Test restore function."""
        mock_run_git.side_effect = [
            (0, "mvcp/test/step1@20240522T0942\n", ""),  # git tag -l
            (0, "", ""),  # git reset
        ]
        
        # Call restore
        restore("mvcp/test/step1@20240522T0942")
        
        # Check that Git commands were called
        self.assertEqual(mock_run_git.call_count, 2)
    
    @mock.patch("mvcp.core._run_git_command")
    def test_diff(self, mock_run_git):
        """Test diff function."""
        mock_run_git.return_value = (0, "diff output", "")
        
        # Call diff
        output = diff("mvcp/test/step1@20240522T0942", "mvcp/test/step2@20240522T0943")
        
        # Check results
        self.assertEqual(output, "diff output")
        mock_run_git.assert_called_once_with(["diff", "mvcp/test/step1@20240522T0942", "mvcp/test/step2@20240522T0943"])


if __name__ == "__main__":
    unittest.main() 