"""
Tests for MVCP CLI.
"""

import unittest
from unittest import mock
from click.testing import CliRunner

from mvcp.cli import cli


class TestCLI(unittest.TestCase):
    """Test CLI commands."""
    
    def setUp(self):
        """Set up test environment."""
        self.runner = CliRunner()
    
    @mock.patch("mvcp.cli.save")
    def test_save_cmd(self, mock_save):
        """Test save command."""
        mock_save.return_value = "mvcp/test/step1@20240522T0942"
        
        # Run command
        result = self.runner.invoke(cli, ["save", "--agent", "test", "--step", "1", "--desc", "Test description"])
        
        # Check result
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Checkpoint created: mvcp/test/step1@20240522T0942", result.output)
        
        # Check that save was called with correct arguments
        mock_save.assert_called_once_with(
            agent="test",
            step=1,
            description="Test description",
            tools_used=[]
        )
    
    @mock.patch("mvcp.cli.list_checkpoints")
    def test_list_cmd(self, mock_list):
        """Test list command."""
        mock_list.return_value = ["mvcp/test/step1@20240522T0942", "mvcp/test/step2@20240522T0943"]
        
        # Run command
        result = self.runner.invoke(cli, ["list"])
        
        # Check result
        self.assertEqual(result.exit_code, 0)
        self.assertIn("mvcp/test/step1@20240522T0942", result.output)
        self.assertIn("mvcp/test/step2@20240522T0943", result.output)
        
        # Test with filters
        result = self.runner.invoke(cli, ["list", "--agent", "test", "--step", "1"])
        
        # Check that list_checkpoints was called with correct arguments
        mock_list.assert_called_with(agent="test", step=1)
    
    @mock.patch("mvcp.cli.restore")
    def test_restore_cmd(self, mock_restore):
        """Test restore command."""
        # Run command
        result = self.runner.invoke(cli, ["restore", "mvcp/test/step1@20240522T0942"])
        
        # Check result
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Restored to checkpoint: mvcp/test/step1@20240522T0942", result.output)
        
        # Check that restore was called with correct arguments
        mock_restore.assert_called_once_with(checkpoint="mvcp/test/step1@20240522T0942")
    
    @mock.patch("mvcp.cli.diff")
    def test_diff_cmd(self, mock_diff):
        """Test diff command."""
        mock_diff.return_value = "diff output"
        
        # Run command
        result = self.runner.invoke(cli, [
            "diff",
            "mvcp/test/step1@20240522T0942",
            "mvcp/test/step2@20240522T0943"
        ])
        
        # Check result
        self.assertEqual(result.exit_code, 0)
        self.assertIn("diff output", result.output)
        
        # Check that diff was called with correct arguments
        mock_diff.assert_called_once_with(
            checkpoint1="mvcp/test/step1@20240522T0942",
            checkpoint2="mvcp/test/step2@20240522T0943"
        )


if __name__ == "__main__":
    unittest.main() 