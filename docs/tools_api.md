# Tools API Reference

## Base Tool

### `execute(args: str, **kwargs) -> Dict`

Execute tool with arguments.

**Parameters:**
- `args` (str): Tool arguments

**Returns:**
- Dict: Execution result with success, data, and error

---

## Open App Tool

Open applications by name.

```python
tool = OpenAppTool()
result = tool.execute("chrome")
```

---

## System Info Tool

Get system information.

```python
tool = SystemInfoTool()
result = tool.execute("")
# Returns: OS, CPU, memory, disk info
```

---

## Volume Control Tool

Control system volume.

```python
tool = VolumeControlTool()
result = tool.execute("up")  # Increase volume
result = tool.execute("50")  # Set to 50%
```

---

## Web Search Tool

Search the web.

```python
tool = WebSearchTool()
result = tool.execute("python tutorial")
```

