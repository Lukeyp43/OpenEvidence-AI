"""
Tutorial Coach Mark - Floating tooltip bubble with arrow

This module provides a dark tooltip bubble that points to specific UI elements
with a dynamic triangle arrow. The bubble auto-positions itself based on available
screen space.
"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QApplication, QSizePolicy
from PyQt6.QtCore import Qt, QRect, QPoint, QTimer
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath


class CoachMark(QWidget):
    """
    Floating tooltip bubble with directional arrow.

    Features:
    - Dark bubble (#1e1e1e) with white text
    - Dynamic triangle arrow that points to target
    - Auto-positions based on available screen space
    - Supports optional action button
    - Includes "Skip Tutorial" link
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Window setup - always on top, no frame, does NOT steal focus
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        # Arrow properties
        self.arrow_direction = None  # "top", "bottom", "left", "right", or None
        self.arrow_x = 0  # X offset for arrow position
        self.arrow_y = 0  # Y offset for arrow position
        self.arrow_size = 10  # Half-width/height of arrow triangle

        # Fixed content width for consistent layout
        self.content_width = 320
        
        # UI components - create content widget with proper layout
        self.content_widget = QWidget(self)
        self.content_widget.setStyleSheet("background: transparent;")
        
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 16)
        self.content_layout.setSpacing(10)

        # Title label
        self.title_label = QLabel()
        self.title_label.setWordWrap(True)
        self.title_label.setMinimumWidth(self.content_width)
        self.title_label.setMaximumWidth(self.content_width)
        self.title_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 15px;
                font-weight: 500;
                background: transparent;
            }
        """)
        self.content_layout.addWidget(self.title_label)

        # Subtext label (optional)
        self.subtext_label = QLabel()
        self.subtext_label.setWordWrap(True)
        self.subtext_label.setMinimumWidth(self.content_width)
        self.subtext_label.setMaximumWidth(self.content_width)
        self.subtext_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.subtext_label.setStyleSheet("""
            QLabel {
                color: #9ca3af;
                font-size: 13px;
                background: transparent;
            }
        """)
        self.subtext_label.hide()
        self.content_layout.addWidget(self.subtext_label)

        # Action button (optional)
        self.action_button = QPushButton()
        self.action_button.setFixedHeight(44)
        self.action_button.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        self.action_button.hide()
        self.content_layout.addWidget(self.action_button)

        # Skip link - in its own container for proper alignment
        self.skip_link = QLabel('<a href="#" style="color: #6b7280; font-size: 12px; text-decoration: none;">Skip Tutorial</a>')
        self.skip_link.setOpenExternalLinks(False)
        self.skip_link.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.skip_link.setStyleSheet("QLabel { background: transparent; margin-top: 8px; }")
        self.content_layout.addWidget(self.skip_link)

    def set_content(self, title: str, subtext: str = None, action_button_text: str = None):
        """
        Set the content of the coach mark.

        Args:
            title: Main message text
            subtext: Optional secondary text
            action_button_text: Optional button text (e.g., "Next", "Finish")
        """
        self.title_label.setText(title)
        # Force label to recalculate its size for wrapped text
        self.title_label.adjustSize()

        if subtext:
            self.subtext_label.setText(subtext)
            self.subtext_label.adjustSize()
            self.subtext_label.show()
        else:
            self.subtext_label.hide()

        if action_button_text:
            self.action_button.setText(action_button_text)
            self.action_button.show()
        else:
            self.action_button.hide()
        
        # Force layout update and size recalculation
        self.content_layout.activate()
        self.content_widget.adjustSize()
        self._update_size()

    def _update_size(self):
        """Calculate and set the widget size based on content."""
        # Force all labels to recalculate their sizes
        self.title_label.adjustSize()
        if self.subtext_label.isVisible():
            self.subtext_label.adjustSize()
        
        # Get actual heights from labels
        title_height = self.title_label.sizeHint().height()
        subtext_height = self.subtext_label.sizeHint().height() if self.subtext_label.isVisible() else 0
        button_height = 44 if self.action_button.isVisible() else 0
        skip_height = 30
        
        # Calculate spacing between visible elements
        num_spacings = 1  # Always have at least 1 spacing (before skip link)
        if self.subtext_label.isVisible():
            num_spacings += 1
        if self.action_button.isVisible():
            num_spacings += 1
        spacing_total = num_spacings * 10  # 10px spacing
        
        # Content area height
        content_height = title_height + subtext_height + button_height + skip_height + spacing_total
        
        # Add margins (20 top + 16 bottom)
        total_content_height = content_height + 36
        
        # Add space for arrow if needed
        arrow_space = 15 if self.arrow_direction in ["top", "bottom"] else 0
        
        # Widget size (add padding for bubble drawing)
        total_width = self.content_width + 40 + 20  # content + margins (20*2) + bubble padding (10*2)
        total_height = total_content_height + arrow_space + 20  # +20 for bubble padding

        self.setFixedSize(total_width, total_height)

    def position_at_target(self, target_rect: QRect):
        """
        Position the coach mark next to a target rectangle.

        Automatically chooses the best position based on available screen space
        and adjusts the arrow direction accordingly.

        Args:
            target_rect: QRect in global coordinates of the target element
        """
        screen = QApplication.primaryScreen().geometry()

        # Calculate available space in each direction
        space_above = target_rect.top() - screen.top()
        space_below = screen.bottom() - target_rect.bottom()
        space_left = target_rect.left() - screen.left()
        space_right = screen.right() - target_rect.right()

        # First, estimate size with current arrow direction
        self._update_size()
        bubble_width = self.width()
        bubble_height = self.height()

        # Choose position based on priority: below > above > right > left
        if space_below >= bubble_height + 20:
            self._position_below(target_rect, screen, bubble_width, bubble_height)
        elif space_above >= bubble_height + 20:
            self._position_above(target_rect, screen, bubble_width, bubble_height)
        elif space_right >= bubble_width + 20:
            self._position_right(target_rect, screen, bubble_width, bubble_height)
        elif space_left >= bubble_width + 20:
            self._position_left(target_rect, screen, bubble_width, bubble_height)
        else:
            # Fallback: center of screen, no arrow
            self._position_center(screen, bubble_width, bubble_height)

        # Recalculate size now that arrow direction is set
        self._update_size()

    def _position_below(self, target_rect, screen, bubble_width, bubble_height):
        """Position bubble below target with arrow pointing up."""
        self.arrow_direction = "top"

        # Center bubble horizontally on target
        bubble_x = target_rect.center().x() - (bubble_width // 2)
        bubble_y = target_rect.bottom() + 20

        # Arrow at top center
        self.arrow_x = bubble_width // 2
        self.arrow_y = 10

        # Apply screen boundaries
        original_x = bubble_x
        bubble_x = max(20, min(bubble_x, screen.width() - bubble_width - 20))

        # Adjust arrow if bubble was moved
        self.arrow_x += (original_x - bubble_x)
        self.arrow_x = max(20, min(self.arrow_x, bubble_width - 20))

        self.move(bubble_x, bubble_y)
        self._update_content_position()
        self.update()

    def _position_above(self, target_rect, screen, bubble_width, bubble_height):
        """Position bubble above target with arrow pointing down."""
        self.arrow_direction = "bottom"

        bubble_x = target_rect.center().x() - (bubble_width // 2)
        bubble_y = target_rect.top() - bubble_height - 20

        # Arrow at bottom center
        self.arrow_x = bubble_width // 2
        self.arrow_y = bubble_height - 10

        # Apply screen boundaries
        original_x = bubble_x
        bubble_x = max(20, min(bubble_x, screen.width() - bubble_width - 20))
        bubble_y = max(20, bubble_y)

        # Adjust arrow
        self.arrow_x += (original_x - bubble_x)
        self.arrow_x = max(20, min(self.arrow_x, bubble_width - 20))

        self.move(bubble_x, bubble_y)
        self._update_content_position()
        self.update()

    def _position_right(self, target_rect, screen, bubble_width, bubble_height):
        """Position bubble to the right with arrow pointing left."""
        self.arrow_direction = "left"

        bubble_x = target_rect.right() + 20
        bubble_y = target_rect.center().y() - (bubble_height // 2)

        # Arrow at left center
        self.arrow_x = 10
        self.arrow_y = bubble_height // 2

        # Apply screen boundaries
        bubble_x = min(bubble_x, screen.width() - bubble_width - 20)
        original_y = bubble_y
        bubble_y = max(20, min(bubble_y, screen.height() - bubble_height - 20))

        # Adjust arrow
        self.arrow_y += (original_y - bubble_y)
        self.arrow_y = max(20, min(self.arrow_y, bubble_height - 20))

        self.move(bubble_x, bubble_y)
        self._update_content_position()
        self.update()

    def _position_left(self, target_rect, screen, bubble_width, bubble_height):
        """Position bubble to the left with arrow pointing right."""
        self.arrow_direction = "right"

        bubble_x = target_rect.left() - bubble_width - 20
        bubble_y = target_rect.center().y() - (bubble_height // 2)

        # Arrow at right center
        self.arrow_x = bubble_width - 10
        self.arrow_y = bubble_height // 2

        # Apply screen boundaries
        bubble_x = max(20, bubble_x)
        original_y = bubble_y
        bubble_y = max(20, min(bubble_y, screen.height() - bubble_height - 20))

        # Adjust arrow
        self.arrow_y += (original_y - bubble_y)
        self.arrow_y = max(20, min(self.arrow_y, bubble_height - 20))

        self.move(bubble_x, bubble_y)
        self._update_content_position()
        self.update()

    def _position_center(self, screen, bubble_width, bubble_height):
        """Position bubble at center of screen with no arrow."""
        self.arrow_direction = None

        bubble_x = (screen.width() - bubble_width) // 2
        bubble_y = (screen.height() - bubble_height) // 2

        self.move(bubble_x, bubble_y)
        self._update_content_position()
        self.update()

    def _update_content_position(self):
        """Update the position of the content widget based on arrow direction."""
        # Content widget fills the bubble area (inside the 10px padding for bubble border)
        content_x = 10
        content_y = 10
        content_w = self.width() - 20
        content_h = self.height() - 20
        
        if self.arrow_direction == "top":
            # Leave extra space at top for arrow
            content_y = 15
            content_h = self.height() - 25
        elif self.arrow_direction == "bottom":
            # Leave extra space at bottom for arrow
            content_h = self.height() - 25
        
        self.content_widget.setGeometry(content_x, content_y, content_w, content_h)

    def paintEvent(self, event):
        """
        Render the coach mark bubble and arrow.

        Uses QPainter to draw a rounded rectangle for the main bubble
        and a triangle for the directional arrow.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Determine bubble rect position based on arrow
        bubble_x = 10
        bubble_y = 10
        bubble_w = self.width() - 20
        bubble_h = self.height() - 20
        
        if self.arrow_direction == "top":
            bubble_y = 10
        elif self.arrow_direction == "bottom":
            bubble_h = self.height() - 20

        # Draw main bubble (rounded rectangle)
        bubble_rect = QRect(bubble_x, bubble_y, bubble_w, bubble_h)
        painter.setBrush(QBrush(QColor("#1e1e1e")))
        painter.setPen(QPen(QColor("#4b5563"), 1))
        painter.drawRoundedRect(bubble_rect, 8, 8)

        # Draw arrow triangle
        if self.arrow_direction:
            arrow_path = QPainterPath()

            if self.arrow_direction == "top":
                # Arrow pointing up (bubble below target)
                arrow_path.moveTo(self.arrow_x - self.arrow_size, 10)
                arrow_path.lineTo(self.arrow_x, 0)  # Point
                arrow_path.lineTo(self.arrow_x + self.arrow_size, 10)
                arrow_path.closeSubpath()

            elif self.arrow_direction == "bottom":
                # Arrow pointing down (bubble above target)
                arrow_path.moveTo(self.arrow_x - self.arrow_size, self.height() - 10)
                arrow_path.lineTo(self.arrow_x, self.height())  # Point
                arrow_path.lineTo(self.arrow_x + self.arrow_size, self.height() - 10)
                arrow_path.closeSubpath()

            elif self.arrow_direction == "left":
                # Arrow pointing left (bubble to the right)
                arrow_path.moveTo(10, self.arrow_y - self.arrow_size)
                arrow_path.lineTo(0, self.arrow_y)  # Point
                arrow_path.lineTo(10, self.arrow_y + self.arrow_size)
                arrow_path.closeSubpath()

            elif self.arrow_direction == "right":
                # Arrow pointing right (bubble to the left)
                arrow_path.moveTo(self.width() - 10, self.arrow_y - self.arrow_size)
                arrow_path.lineTo(self.width(), self.arrow_y)  # Point
                arrow_path.lineTo(self.width() - 10, self.arrow_y + self.arrow_size)
                arrow_path.closeSubpath()

            # Fill arrow with same color as bubble
            painter.fillPath(arrow_path, QBrush(QColor("#1e1e1e")))

            # Draw border on arrow
            painter.setPen(QPen(QColor("#4b5563"), 1))
            painter.drawPath(arrow_path)
