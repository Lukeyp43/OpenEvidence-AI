# Bug Fix: Anki Crash When Deleting Shortcut

## Problem
When deleting a shortcut and pressing "Confirm", Anki would crash with a `SIGBUS` error (pointer authentication failure) in Qt's property access code.

## Root Cause
The crash occurred because:
1. When clicking "Confirm?" to delete, the code accessed Qt properties (`button.property()`) on the delete button
2. The deletion was scheduled with `QTimer.singleShot(0, ...)` which happened too quickly
3. The `delete_keybinding()` method would refresh the list and delete all widgets, including the button that was just clicked
4. Qt would try to complete the button click event handling on a button that was already scheduled for deletion
5. Accessing Qt properties on a deleted/invalid object caused a segmentation fault

## Solution
The fix involves several key changes to `settings.py`:

### 1. Use Instance Variables Instead of Qt Properties
- Added `self.revert_timers = {}` dictionary to track timer objects
- Store timer references by button ID: `self.revert_timers[id(button)] = timer`
- This avoids Qt's property system which can fail on deleted objects

### 2. Increase Deletion Delay
- Changed from `QTimer.singleShot(0, ...)` to `QTimer.singleShot(50, ...)`
- 50ms delay ensures the button click event fully completes before deletion starts

### 3. Disconnect Button Signal
- Added `button.clicked.disconnect()` before scheduling deletion
- Prevents any additional click events from being processed

### 4. Proper Timer Cleanup
- Stop timer before deletion: `timer.stop()`
- Remove from tracking dictionary: `del self.revert_timers[button_id]`
- Added cleanup in `refresh_list()` to stop all active timers before deleting widgets

### 5. Safety Checks
- Added existence check in `revert_delete_button()`: `if not button or not hasattr(button, 'property')`
- Wrapped in try-except to catch `RuntimeError` if button is deleted

## Testing
To verify the fix:
1. Open Anki and go to the OpenEvidence panel
2. Click the settings gear icon
3. Click the delete (trash) icon on any shortcut
4. Click "Confirm?" when it appears
5. The shortcut should be deleted without crashing Anki

## Files Modified
- `settings.py`: Updated `SettingsListView` class with proper timer management
