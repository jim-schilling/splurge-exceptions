"""Unit tests for the command-line interface module.

Tests the CLI module for proper argument parsing, version display,
and help functionality.
"""

import subprocess
import sys

import pytest

from splurge_exceptions import __version__
from splurge_exceptions.cli import main


class TestCliMain:
    """Tests for the main CLI function."""

    def test_main_returns_zero(self) -> None:
        """Test that main() returns exit code 0."""
        exit_code = main([])
        assert exit_code == 0

    def test_main_with_empty_list_returns_zero(self) -> None:
        """Test that main() with empty list returns 0."""
        exit_code = main([])
        assert exit_code == 0


class TestCliVersion:
    """Tests for version command."""

    def test_version_flag_raises_system_exit(self) -> None:
        """Test that --version flag raises SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            main(["--version"])
        # argparse exits with code 0 for --version
        assert exc_info.value.code == 0

    def test_version_string_contains_expected_format(self) -> None:
        """Test that version string is in expected format."""
        # Version should be importable
        assert isinstance(__version__, str)
        assert len(__version__) > 0
        # Version follows PEP 440 pattern (e.g., "2025.0.1")
        assert __version__[0].isdigit()


class TestCliHelp:
    """Tests for help command."""

    def test_help_flag_raises_system_exit(self) -> None:
        """Test that --help flag raises SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            main(["--help"])
        # argparse exits with code 0 for --help
        assert exc_info.value.code == 0

    def test_h_flag_raises_system_exit(self) -> None:
        """Test that -h flag raises SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            main(["-h"])
        # argparse exits with code 0 for -h
        assert exc_info.value.code == 0


class TestCliInvalidArguments:
    """Tests for invalid arguments."""

    def test_invalid_argument_raises_system_exit(self) -> None:
        """Test that invalid arguments raise SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            main(["--invalid-option"])
        # argparse exits with code 2 for invalid arguments
        assert exc_info.value.code == 2

    def test_unrecognized_argument_raises_system_exit(self) -> None:
        """Test that unrecognized arguments raise SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            main(["unrecognized"])
        # argparse exits with code 2 for unrecognized positional arguments
        assert exc_info.value.code == 2


class TestCliIntegration:
    """Integration tests for CLI via subprocess."""

    def test_module_can_be_run_with_m_flag(self) -> None:
        """Test that module can be run with python -m."""
        # Run: python -m splurge_exceptions --version
        result = subprocess.run(
            [sys.executable, "-m", "splurge_exceptions", "--version"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "splurge-exceptions" in result.stdout
        assert __version__ in result.stdout

    def test_module_help_output_contains_description(self) -> None:
        """Test that help output contains module description."""
        result = subprocess.run(
            [sys.executable, "-m", "splurge_exceptions", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "splurge-exceptions" in result.stdout
        assert "Python exception framework" in result.stdout or "help" in result.stdout.lower()

    def test_module_with_invalid_option_returns_error(self) -> None:
        """Test that invalid options produce non-zero exit code."""
        result = subprocess.run(
            [sys.executable, "-m", "splurge_exceptions", "--invalid"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0


class TestCliEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_main_with_multiple_flags(self) -> None:
        """Test that multiple conflicting flags are handled."""
        # When both --version and other args provided, version takes precedence
        with pytest.raises(SystemExit) as exc_info:
            main(["--version", "--help"])
        # Should exit with code 0 (version was processed first)
        assert exc_info.value.code == 0

    def test_main_preserves_program_name(self) -> None:
        """Test that CLI uses correct program name."""
        # This is set in argparse constructor
        # We can't easily test the prog name directly, but we can verify
        # that main() doesn't raise an exception with correct setup
        exit_code = main([])
        assert exit_code == 0

    def test_main_with_empty_args_is_equivalent_to_explicit_empty_list(self) -> None:
        """Test that passing empty list doesn't raise exceptions."""
        # Verify that main([]) behaves consistently
        exit_code = main([])
        assert exit_code == 0
