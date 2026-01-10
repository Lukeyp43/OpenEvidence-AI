"""
Tutorial Steps - Definition of tutorial sequence

This module defines the complete tutorial flow as a sequence of steps,
each with a target, content, and progression trigger.
"""

from dataclasses import dataclass
from typing import Optional, Callable, Any
from PyQt6.QtCore import QRect, QPoint

from .tutorial_helpers import (
    get_toolbar_icon_rect_async,
    get_reviewer_card_rect,
    get_gear_button_rect,
    get_chat_input_rect_async,
)


@dataclass
class TutorialStep:
    """
    Definition of a single tutorial step.

    Attributes:
        step_id: Unique identifier for this step
        target_type: Type of target ("widget", "coordinates", "html", "none")
        target_ref: Reference to get target location (callable or tuple)
        title: Main message to display
        subtext: Optional secondary message
        advance_on_event: Event name that advances to next step (None = manual button)
        action_button: Text for manual advance button (e.g., "Next", "Finish")
    """
    step_id: str
    target_type: str  # "widget", "coordinates", "html", "none"
    target_ref: Optional[Any]  # Callable returning QRect/QPoint, or tuple for HTML
    title: str
    subtext: Optional[str] = None
    advance_on_event: Optional[str] = None
    action_button: Optional[str] = None


# Define the complete tutorial sequence
TUTORIAL_STEPS = [
    # ===== SECTION 1: SETUP =====
    
    # Step 1: Click toolbar book icon to toggle panel
    TutorialStep(
        step_id="toggle_panel",
        target_type="html",
        target_ref=("toolbar", "openevidence_button"),
        title="Click the book icon to toggle the sidebar.",
        subtext="Clicking it opens or closes the sidebar.",
        advance_on_event="panel_toggled",
        action_button=None
    ),

    # Step 2: Auto-create demo deck and start reviewing
    TutorialStep(
        step_id="create_demo_deck",
        target_type="none",
        target_ref=None,
        title="Let's create a practice deck to test OpenEvidence features.",
        subtext="This will add sample medical flashcards for you to try.",
        advance_on_event=None,
        action_button="Create Practice Deck"
    ),

    # ===== SECTION 2: QUICK ACTIONS - ASK QUESTION =====
    
    # Step 3: Intro to first feature
    TutorialStep(
        step_id="feature_intro",
        target_type="none",
        target_ref=None,
        title="Let's show you the main feature called Quick Actions and how to use it.",
        subtext=None,
        advance_on_event=None,
        action_button="Next"
    ),

    # Step 4: Highlight text with Cmd held
    TutorialStep(
        step_id="highlight_text",
        target_type="coordinates",
        target_ref=get_reviewer_card_rect,
        title="Hold down ⌘ Cmd while highlighting the word \"hypertension\".",
        subtext=None,
        advance_on_event="text_highlighted",
        action_button=None
    ),

    # Step 5: Quick Action bar intro
    TutorialStep(
        step_id="quick_action_intro",
        target_type="none",
        target_ref=None,
        title="This is the Quick Action bar!",
        subtext="It appears whenever you ⌘ Cmd + highlight text.",
        advance_on_event=None,
        action_button="Next"
    ),

    # Step 6: Click Ask Question
    TutorialStep(
        step_id="ask_question",
        target_type="none",
        target_ref=None,
        title="Now click \"Ask Question\" on the Quick Action bar.",
        subtext="Type something like \"What does this mean?\" then press Enter or click the arrow.",
        advance_on_event="ask_question_submitted",
        action_button=None
    ),

    # Step 7: Ask Question success
    TutorialStep(
        step_id="ask_question_success",
        target_type="none",
        target_ref=None,
        title="Great! OpenEvidence is generating a response.",
        subtext="This is the fastest way to get answers — just highlight and ask!",
        advance_on_event=None,
        action_button="Next"
    ),

    # ===== SECTION 3: QUICK ACTIONS - ADD TO CHAT =====
    
    # Step 8: Add to Chat intro
    TutorialStep(
        step_id="add_to_chat_intro",
        target_type="none",
        target_ref=None,
        title="Now let's try \"Add to Chat\".",
        subtext="This adds your highlighted text directly to the chat input.",
        advance_on_event=None,
        action_button="Next"
    ),

    # Step 9: Highlight again for Add to Chat
    TutorialStep(
        step_id="highlight_for_add_to_chat",
        target_type="coordinates",
        target_ref=get_reviewer_card_rect,
        title="⌘ Cmd + highlight some text again.",
        subtext=None,
        advance_on_event="text_highlighted",
        action_button=None
    ),

    # Step 10: Click Add to Chat
    TutorialStep(
        step_id="add_to_chat",
        target_type="none",
        target_ref=None,
        title="Now click \"Add to Chat\" on the Quick Action bar.",
        subtext="Your highlighted text will be added to the chat input.",
        advance_on_event="add_to_chat",
        action_button=None
    ),

    # ===== SECTION 4: KEYBOARD SHORTCUTS =====
    
    # Step 11: Shortcuts intro
    TutorialStep(
        step_id="shortcuts_intro",
        target_type="none",
        target_ref=None,
        title="There's an even faster way — keyboard shortcuts!",
        subtext="You can skip the Quick Action bar entirely and use shortcuts.",
        advance_on_event=None,
        action_button="Show Me"
    ),

    # Step 12: Use shortcut
    TutorialStep(
        step_id="use_shortcut",
        target_type="coordinates",
        target_ref=get_reviewer_card_rect,
        title="Highlight any text (no ⌘ Cmd needed), then press ⌘ Cmd+Shift+S.",
        subtext="This instantly sends your card content to the chat using a template.",
        advance_on_event="shortcut_used",
        action_button=None
    ),

    # ===== SECTION 5: TEMPLATES & SETTINGS =====
    
    # Step 13: Templates intro
    TutorialStep(
        step_id="templates_intro",
        target_type="none",
        target_ref=None,
        title="That shortcut used a Template!",
        subtext="Templates let you customize exactly what gets sent to OpenEvidence. Each template has its own keyboard shortcut.",
        advance_on_event=None,
        action_button="Next"
    ),

    # Step 14: Open settings
    TutorialStep(
        step_id="open_settings",
        target_type="widget",
        target_ref=get_gear_button_rect,
        title="Click the gear icon to open Settings.",
        subtext=None,
        advance_on_event="settings_opened",
        action_button=None
    ),

    # Step 15: Settings overview
    TutorialStep(
        step_id="settings_overview",
        target_type="none",
        target_ref=None,
        title="Welcome to Settings!",
        subtext="Here you can customize your Quick Actions and Templates. You can change keyboard shortcuts, edit templates, or create new ones.",
        advance_on_event=None,
        action_button="Next"
    ),

    # Step 16: Finish
    TutorialStep(
        step_id="finish",
        target_type="none",
        target_ref=None,
        title="You're all set! 🎉",
        subtext="You now know how to use Quick Actions, shortcuts, and templates. Create an account on openevidence.com to save your chat history.",
        advance_on_event=None,
        action_button="Finish"
    ),
]


def get_step_target_rect(step: TutorialStep, callback: Callable[[Optional[QRect]], None]):
    """
    Get the target rectangle for a tutorial step.

    Handles different target types:
    - "widget": Directly calls target_ref() to get QRect
    - "coordinates": Calls target_ref() to get QRect
    - "html": Asynchronously queries HTML element via JavaScript
    - "none": Returns None (center screen, no target)

    Args:
        step: The tutorial step to get target for
        callback: Function to call with QRect result (or None)
    """
    if step.target_type == "none":
        callback(None)
        return

    elif step.target_type in ["widget", "coordinates"]:
        # Directly call the target_ref function
        try:
            rect = step.target_ref()
            callback(rect)
        except Exception as e:
            print(f"Error getting target rect for step {step.step_id}: {e}")
            callback(None)

    elif step.target_type == "html":
        # Asynchronous HTML element query
        try:
            # target_ref is a tuple: (web_view_attr, selector)
            web_view_attr, selector = step.target_ref

            # Special handling for toolbar
            if web_view_attr == "toolbar":
                get_toolbar_icon_rect_async(callback)
            else:
                # Panel input box
                get_chat_input_rect_async(callback)
        except Exception as e:
            print(f"Error getting HTML target for step {step.step_id}: {e}")
            callback(None)

    else:
        # Unknown target type
        print(f"Unknown target type: {step.target_type}")
        callback(None)


def get_total_steps():
    """Get the total number of tutorial steps."""
    return len(TUTORIAL_STEPS)


def get_step_by_index(index: int) -> Optional[TutorialStep]:
    """
    Get a tutorial step by its index.

    Args:
        index: 0-based step index

    Returns:
        TutorialStep or None if index out of range
    """
    if 0 <= index < len(TUTORIAL_STEPS):
        return TUTORIAL_STEPS[index]
    return None


def get_step_by_id(step_id: str) -> Optional[TutorialStep]:
    """
    Get a tutorial step by its ID.

    Args:
        step_id: The step's unique identifier

    Returns:
        TutorialStep or None if not found
    """
    for step in TUTORIAL_STEPS:
        if step.step_id == step_id:
            return step
    return None


def find_step_index_for_event(event_name: str) -> Optional[int]:
    """
    Find the step index that advances on a specific event.

    Args:
        event_name: Event name to search for

    Returns:
        0-based step index, or None if no step uses this event
    """
    for i, step in enumerate(TUTORIAL_STEPS):
        if step.advance_on_event == event_name:
            return i
    return None
