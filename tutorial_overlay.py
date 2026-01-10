"""
Tutorial Overlay - Semi-transparent backdrop with highlight cutout

This module provides a full-screen overlay that dims the background and highlights
a specific target element by creating a cutout in the overlay.
"""

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QRect, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QRegion, QPainterPath


class TutorialOverlay(QWidget):
    """
    Full-screen semi-transparent overlay with cutout highlight.

    Creates a dark backdrop that covers the entire screen except for a
    highlighted rectangular area. The highlighted area has a glowing border
    and allows click-through, while clicks outside are blocked.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Window setup - full screen, always on top, no frame
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Highlight rectangle (empty by default)
        self.highlight_rect = QRect()

        # Make full screen
        self._resize_to_screen()

    def _resize_to_screen(self):
        """Resize the overlay to cover the entire screen."""
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)

    def set_highlight_rect(self, rect: QRect):
        """
        Set the rectangular area to highlight (cutout).

        Args:
            rect: QRect in global screen coordinates to highlight
        """
        # Ensure overlay is full screen
        self._resize_to_screen()
        self.highlight_rect = rect
        self.update()  # Trigger repaint

    def clear_highlight(self):
        """Remove the highlight cutout."""
        self.highlight_rect = QRect()
        self.update()

    def paintEvent(self, event):
        """
        Render the overlay with cutout highlight.

        Uses QPainterPath to create a rounded rectangle cutout in the
        semi-transparent backdrop. Draws a glowing blue border around
        the highlighted area.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create full-screen region
        full_region = QRegion(self.rect())

        # Create cutout for highlight if rect exists
        if not self.highlight_rect.isEmpty():
            # Add padding around highlight
            padded_rect = self.highlight_rect.adjusted(-8, -8, 8, 8)

            # Create rounded rectangle path for highlight
            highlight_path = QPainterPath()
            highlight_path.addRoundedRect(QRectF(padded_rect), 4, 4)

            # Convert path to region and subtract from full region
            highlight_region = QRegion(highlight_path.toFillPolygon().toPolygon())
            full_region = full_region.subtracted(highlight_region)

        # Draw semi-transparent backdrop (everywhere except highlight)
        painter.setClipRegion(full_region)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 180))

        # Draw glowing blue border around highlight
        if not self.highlight_rect.isEmpty():
            painter.setClipping(False)
            padded_rect = self.highlight_rect.adjusted(-8, -8, 8, 8)

            # Blue border with slight glow effect
            pen = QPen(QColor("#3b82f6"), 2)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(padded_rect, 4, 4)

    def mousePressEvent(self, event):
        """
        Block clicks outside the highlight area.

        Clicks inside the highlight are passed through to the underlying
        widget, while clicks outside are consumed by the overlay.
        """
        if not self.highlight_rect.isEmpty():
            # Check if click is inside highlight (with padding)
            padded_rect = self.highlight_rect.adjusted(-8, -8, 8, 8)
            if padded_rect.contains(event.pos()):
                # Pass through to highlighted element
                event.ignore()
                return

        # Block the click
        event.accept()

    def mouseReleaseEvent(self, event):
        """Block mouse releases outside highlight."""
        if not self.highlight_rect.isEmpty():
            padded_rect = self.highlight_rect.adjusted(-8, -8, 8, 8)
            if padded_rect.contains(event.pos()):
                event.ignore()
                return
        event.accept()

    def mouseMoveEvent(self, event):
        """Allow mouse movement (for hover effects in highlighted area)."""
        event.ignore()  # Pass through all mouse moves
