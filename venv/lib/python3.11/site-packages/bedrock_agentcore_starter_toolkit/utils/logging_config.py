"""Centralized logging configuration for bedrock-agentcore-starter-toolkit."""

import logging

_LOGGING_CONFIGURED = False


def setup_toolkit_logging(mode: str = "sdk") -> None:
    """Setup logging for bedrock-agentcore-starter-toolkit.

    Args:
        mode: "cli" or "sdk" (defaults to "sdk")
    """
    global _LOGGING_CONFIGURED
    if _LOGGING_CONFIGURED:
        return  # Already configured, prevent duplicates

    if mode == "cli":
        _setup_cli_logging()
    elif mode == "sdk":
        _setup_sdk_logging()
    else:
        raise ValueError(f"Invalid logging mode: {mode}. Must be 'cli' or 'sdk'")

    _LOGGING_CONFIGURED = True


def _setup_cli_logging() -> None:
    """Setup logging for CLI usage with RichHandler."""
    try:
        from rich.logging import RichHandler

        from ..cli.common import console

        FORMAT = "%(message)s"
        logging.basicConfig(
            level="INFO",
            format=FORMAT,
            handlers=[RichHandler(show_time=False, show_path=False, show_level=False, console=console)],
            force=True,  # Override any existing configuration
        )
    except ImportError:
        # Fallback if rich is not available
        _setup_basic_logging()


def _setup_sdk_logging() -> None:
    """Setup logging for SDK usage (notebooks, scripts, imports) with StreamHandler."""
    # Configure logger for ALL toolkit modules (ensures all operation logs appear)
    toolkit_logger = logging.getLogger("bedrock_agentcore_starter_toolkit")

    if not toolkit_logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        toolkit_logger.addHandler(handler)
        toolkit_logger.setLevel(logging.INFO)


def _setup_basic_logging() -> None:
    """Setup basic logging as fallback."""
    logging.basicConfig(level=logging.INFO, format="%(message)s", force=True)


def is_logging_configured() -> bool:
    """Check if toolkit logging has been configured."""
    return _LOGGING_CONFIGURED


def reset_logging_config() -> None:
    """Reset logging configuration state (for testing)."""
    global _LOGGING_CONFIGURED
    _LOGGING_CONFIGURED = False
