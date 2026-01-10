"""
Tutorial System - Main Entry Point

This module provides the public API for the tutorial system.
It was previously missing, causing all tutorial_event() calls to fail.

Public Functions:
- start_tutorial(): Start the tutorial from beginning or resume
- tutorial_event(event_name): Handle tutorial events for progression
- skip_tutorial(): Skip the tutorial entirely
"""

from .tutorial_manager import get_tutorial_manager


def start_tutorial():
    """
    Start the interactive tutorial.

    If the tutorial is already completed, this does nothing.
    Otherwise, it starts from the beginning or resumes from saved progress.
    """
    manager = get_tutorial_manager()
    manager.start_tutorial()


def tutorial_event(event_name: str):
    """
    Handle a tutorial event.

    This function is called throughout the codebase when specific actions occur.
    It routes events to the TutorialManager to check for step progression.

    Events:
    - "panel_opened": Panel becomes visible
    - "panel_closed": Panel becomes hidden
    - "text_highlighted": User highlights text with Cmd held
    - "add_to_chat": User uses "Add to Chat" action
    - "shortcut_used": User uses a template shortcut (e.g., Cmd+Shift+S)
    - "settings_opened": User clicks the settings gear icon

    Args:
        event_name: Name of the event that occurred
    """
    try:
        manager = get_tutorial_manager()
        manager.handle_event(event_name)
    except Exception as e:
        # Fail silently to avoid breaking addon functionality
        print(f"Tutorial event error: {e}")


def skip_tutorial():
    """
    Skip the tutorial entirely.

    Marks the tutorial as completed and hides all tutorial UI.
    """
    manager = get_tutorial_manager()
    manager.skip_tutorial()


def is_tutorial_active():
    """
    Check if the tutorial is currently active.

    Returns:
        bool: True if tutorial is running, False otherwise
    """
    manager = get_tutorial_manager()
    return manager.tutorial_active


def get_current_step_index():
    """
    Get the current tutorial step index.

    Returns:
        int: 0-based step index
    """
    manager = get_tutorial_manager()
    return manager.current_step_index
