# UI API Reference

## Modern UI

### `launch_modern_ui()`

Launch AYKO modern interface.

**Example:**
```python
from ui.modern_ui import launch_modern_ui
launch_modern_ui()
```

---

## Hotkey Manager

### `set_active_monitor(monitor_id: int) -> bool`

Set active monitor for hotkey capture.

**Parameters:**
- `monitor_id` (int): Monitor ID

**Returns:**
- bool: Success status

---

## Sphere Animator

### `set_state_animation(ayko_state: str) -> Dict`

Set animation based on AYKO state.

**Parameters:**
- `ayko_state` (str): State (idle, listening, processing, speaking, error)

**Returns:**
- Dict: Animation configuration

---

## Suggestions Panel

### `search_suggestions(query: str) -> List[Dict]`

Search command suggestions.

**Parameters:**
- `query` (str): Search query

**Returns:**
- List[Dict]: Matching suggestions

