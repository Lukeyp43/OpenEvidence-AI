"""
Reviewer highlight feature - Cursor-style floating action bar
Shows a floating action bar when text is highlighted on flashcards
"""

from aqt import mw, gui_hooks


# JavaScript code to inject into the reviewer
HIGHLIGHT_BUBBLE_JS = """
(function() {
    // Only inject once
    if (window.ankiHighlightBubbleInjected) {
        return;
    }
    window.ankiHighlightBubbleInjected = true;
    console.log('Anki: Injecting highlight bubble for OpenEvidence');

    let bubble = null;
    let currentState = 'default'; // 'default' or 'input'
    let selectedText = '';

    // Create the bubble element
    function createBubble() {
        const div = document.createElement('div');
        div.id = 'anki-highlight-bubble';
        div.style.cssText = `
            position: absolute;
            background: #1f2937;
            border-radius: 6px;
            padding: 8px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
            z-index: 9999;
            display: none;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 12px;
            color: white;
            gap: 4px;
        `;
        document.body.appendChild(div);
        return div;
    }

    // Render default state with two buttons
    function renderDefaultState() {
        currentState = 'default';
        bubble.innerHTML = `
            <div style="display: flex; gap: 4px;">
                <button id="add-to-chat-btn" style="
                    background: transparent;
                    border: none;
                    color: white;
                    padding: 6px 12px;
                    cursor: pointer;
                    border-radius: 4px;
                    font-size: 12px;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    transition: background 0.2s;
                ">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                    </svg>
                    <span>Add to Chat</span>
                </button>
                <button id="ask-question-btn" style="
                    background: transparent;
                    border: none;
                    color: white;
                    padding: 6px 12px;
                    cursor: pointer;
                    border-radius: 4px;
                    font-size: 12px;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    transition: background 0.2s;
                ">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                        <line x1="12" y1="17" x2="12.01" y2="17"></line>
                    </svg>
                    <span>Ask Question</span>
                </button>
            </div>
        `;

        // Add hover effects
        const addToChatBtn = bubble.querySelector('#add-to-chat-btn');
        const askQuestionBtn = bubble.querySelector('#ask-question-btn');

        addToChatBtn.addEventListener('mouseenter', () => {
            addToChatBtn.style.background = 'rgba(255, 255, 255, 0.1)';
        });
        addToChatBtn.addEventListener('mouseleave', () => {
            addToChatBtn.style.background = 'transparent';
        });

        askQuestionBtn.addEventListener('mouseenter', () => {
            askQuestionBtn.style.background = 'rgba(255, 255, 255, 0.1)';
        });
        askQuestionBtn.addEventListener('mouseleave', () => {
            askQuestionBtn.style.background = 'transparent';
        });

        // Add click handlers
        addToChatBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            handleAddToChat();
        });

        askQuestionBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            renderInputState();
        });
    }

    // Render input state with text field and submit button
    function renderInputState() {
        currentState = 'input';
        bubble.innerHTML = `
            <div style="display: flex; gap: 4px; align-items: center;">
                <input
                    type="text"
                    id="question-input"
                    placeholder="Ask a question..."
                    style="
                        background: rgba(255, 255, 255, 0.1);
                        border: 1px solid rgba(255, 255, 255, 0.2);
                        border-radius: 4px;
                        color: white;
                        padding: 6px 10px;
                        font-size: 12px;
                        outline: none;
                        min-width: 200px;
                    "
                />
                <button id="submit-btn" style="
                    background: rgba(59, 130, 246, 0.8);
                    border: none;
                    color: white;
                    padding: 6px 10px;
                    cursor: pointer;
                    border-radius: 4px;
                    font-size: 12px;
                    display: flex;
                    align-items: center;
                    transition: background 0.2s;
                ">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="5" y1="12" x2="19" y2="12"></line>
                        <polyline points="12 5 19 12 12 19"></polyline>
                    </svg>
                </button>
            </div>
        `;

        const input = bubble.querySelector('#question-input');
        const submitBtn = bubble.querySelector('#submit-btn');

        // Focus the input
        setTimeout(() => input.focus(), 0);

        // Submit on Enter key
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                handleSubmitQuestion();
            }
        });

        // Hover effect for submit button
        submitBtn.addEventListener('mouseenter', () => {
            submitBtn.style.background = 'rgba(59, 130, 246, 1)';
        });
        submitBtn.addEventListener('mouseleave', () => {
            submitBtn.style.background = 'rgba(59, 130, 246, 0.8)';
        });

        // Click handler for submit button
        submitBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            handleSubmitQuestion();
        });
    }

    // Handle "Add to Chat" action
    function handleAddToChat() {
        console.log('Anki: Add to Chat clicked, text:', selectedText);
        // Send message to Python
        pycmd('openevidence:add_context:' + encodeURIComponent(selectedText));
        hideBubble();
    }

    // Handle question submission
    function handleSubmitQuestion() {
        const input = bubble.querySelector('#question-input');
        const query = input.value.trim();

        if (query) {
            console.log('Anki: Question submitted:', query, 'Context:', selectedText);
            // Send message to Python with format: query|context
            pycmd('openevidence:ask_query:' + encodeURIComponent(query) + '|' + encodeURIComponent(selectedText));
            hideBubble();
        }
    }

    // Position the bubble above the selection
    function positionBubble(rect) {
        const bubbleHeight = bubble.offsetHeight;
        const bubbleWidth = bubble.offsetWidth;

        // Calculate center of selection
        const centerX = rect.left + (rect.width / 2);

        // Position bubble centered above selection with 8px gap
        let left = centerX - (bubbleWidth / 2);
        let top = rect.top - bubbleHeight - 8;

        // Keep bubble within viewport bounds
        const padding = 10;
        if (left < padding) left = padding;
        if (left + bubbleWidth > window.innerWidth - padding) {
            left = window.innerWidth - bubbleWidth - padding;
        }

        // If bubble would be above viewport, show it below instead
        if (top < padding) {
            top = rect.bottom + 8;
        }

        bubble.style.left = left + window.scrollX + 'px';
        bubble.style.top = top + window.scrollY + 'px';
    }

    // Show the bubble
    function showBubble(rect, text) {
        selectedText = text;
        renderDefaultState();
        bubble.style.display = 'block';

        // Position after render so we have accurate dimensions
        setTimeout(() => positionBubble(rect), 0);
    }

    // Hide the bubble
    function hideBubble() {
        bubble.style.display = 'none';
        currentState = 'default';
    }

    // Handle mouseup event
    document.addEventListener('mouseup', (e) => {
        // Small delay to allow selection to complete
        setTimeout(() => {
            const selection = window.getSelection();
            const text = selection.toString().trim();

            if (text && text.length > 0) {
                // Get selection range and position
                const range = selection.getRangeAt(0);
                const rect = range.getBoundingClientRect();

                showBubble(rect, text);
            } else {
                // No selection, hide bubble if clicking outside
                if (!bubble.contains(e.target)) {
                    hideBubble();
                }
            }
        }, 10);
    });

    // Hide bubble when clicking outside
    document.addEventListener('mousedown', (e) => {
        if (bubble && !bubble.contains(e.target)) {
            const selection = window.getSelection();
            if (!selection.toString().trim()) {
                hideBubble();
            }
        }
    });

    // Create the bubble on load
    bubble = createBubble();
    console.log('Anki: Highlight bubble ready');
})();
"""


def inject_highlight_bubble(html, card, context):
    """Inject the highlight bubble JavaScript into reviewer cards

    Args:
        html: The HTML of the question or answer
        card: The current card object
        context: One of "reviewQuestion", "reviewAnswer", "clayoutQuestion",
                "clayoutAnswer", "previewQuestion", "previewAnswer"

    Returns:
        Modified HTML with injected JavaScript
    """
    # Only inject in review context (not in card layout or preview)
    if context in ("reviewQuestion", "reviewAnswer"):
        # Add the JavaScript to the card HTML
        html += f"<script>{HIGHLIGHT_BUBBLE_JS}</script>"

    return html


def setup_highlight_hooks():
    """Register the highlight bubble injection hook"""
    gui_hooks.card_will_show.append(inject_highlight_bubble)
