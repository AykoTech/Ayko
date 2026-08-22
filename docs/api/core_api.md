# Core API Reference

## AYKOCore

### `execute_command(text: str) -> Dict`

Execute a AYKO command.

**Parameters:**
- `text` (str): Command to execute

**Returns:**
- `success` (bool): Execution status
- `result` (str): Execution result
- `timestamp` (str): Execution time
- `error` (str, optional): Error message

**Example:**
```python
result = core.execute_command("open chrome")
print(result["success"])  # True
```

---

## CommandMemory

### `add_command(text: str, intent: str, success: bool) -> bool`

Add command to history.

**Parameters:**
- `text` (str): Command text
- `intent` (str): Command intent
- `success` (bool): Execution success

**Returns:**
- bool: Success status

---

## Personality Engine

### `get_response(user_input: str) -> Optional[str]`

Get personality-driven response.

**Parameters:**
- `user_input` (str): User input

**Returns:**
- str: Response or None

---

## Learning Schedule

### `predict_next_command() -> Optional[str]`

Predict next command based on patterns.

**Returns:**
- str: Predicted command or None

---

## Voice Emotion

### `synthesize_emotional_speech(text: str, emotion: str) -> Dict`

Synthesize speech with emotion.

**Parameters:**
- `text` (str): Text to speak
- `emotion` (str): Emotion (happy, sad, angry, etc.)

**Returns:**
- Dict: Synthesis parameters

