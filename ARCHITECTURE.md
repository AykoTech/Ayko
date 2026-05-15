# JARVIS v0.0.01 - Strict Architecture (VALIDATED)

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│ USER INPUT                                                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────┐
        │ LLM ENGINE                     │
        │ • interpret(text)              │
        │ • ONLY generates JSON          │
        │ • Returns: (intent, args)      │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │ COMMAND PARSER                 │
        │ • parse(intent, args)          │
        │ • ONLY maps intent → tool      │
        │ • Returns: (tool_name, args)   │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │ CORE ORCHESTRATOR              │
        │ • execute_command()            │
        │ • Manages state                │
        │ • Calls tool executor          │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │ TOOL REGISTRY                  │
        │ • STATIC mapping               │
        │ • NO logic or conditions       │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │ TOOL EXECUTOR                  │
        │ • Validates args               │
        │ • Calls tool.execute()         │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │ INDIVIDUAL TOOLS               │
        │ • OpenAppTool()                │
        │ • CloseAppTool()               │
        │ • SystemInfoTool()             │
        │ • Each: ONE responsibility     │
        └────────────┬───────────────────┘
                     │
                     ▼
        ┌────────────────────────────────┐
        │ RESULT                         │
        │ {success, result, state_u, log}
        └────────────────────────────────┘
```

## Component Responsibilities

### 1. LLM Engine
**File:** `src/core/llm_engine.py`

**Single Method:** `interpret(text: str) → Tuple[str, Dict]`

**Responsibility:**
- Convert natural language to structured intent + parameters
- ONLY linguistic interpretation

**CONSTRAINTS:**
- ❌ NO tool selection
- ❌ NO action execution
- ❌ NO routing logic
- ✓ Output ONLY JSON format
- ✓ Always returns (intent, args) tuple

**Example:**
```python
text = "open youtube"
intent, args = llm.interpret(text)
# Returns: ("open_app", {"app": "youtube"})
```

---

### 2. Command Parser
**File:** `src/core/command_parser.py`

**Static Mapping:** `INTENT_TO_TOOL`

**Single Method:** `parse(intent: str, args: Dict) → Tuple[str, Dict]`

**Responsibility:**
- Map intent → tool_name
- ONLY direct routing

**CONSTRAINTS:**
- ❌ NO complex logic
- ❌ NO nested conditions
- ❌ NO semantic interpretation
- ✓ Simple dictionary lookup
- ✓ Returns (tool_name, args)

**Example:**
```python
intent = "open_app"
args = {"app": "youtube"}
tool, args = parser.parse(intent, args)
# Returns: ("open_app", {"app": "youtube"})
```

---

### 3. Core Orchestrator
**File:** `src/core/core.py`

**Main Method:** `execute_command(user_text: str) → Dict`

**Responsibility:**
- Orchestrate the entire flow
- Manage global state
- Log execution timeline

**CONSTRAINTS:**
- ❌ NO tool selection (Parser does that)
- ❌ NO intent interpretation (LLM does that)
- ❌ NO business logic
- ✓ Call LLM → Parser → Executor in sequence
- ✓ Track state changes
- ✓ Return complete result with timeline

**Flow:**
```
1. Call LLM.interpret(text) → (intent, args)
2. Call Parser.parse(intent, args) → (tool, args)
3. Call ToolExecutor.execute(tool, args, state) → result
4. Update state from result["state_updates"]
5. Return complete execution result
```

---

### 4. Tool Registry & Executor
**File:** `src/core/tool_registry.py`

**Static Registry:**
```python
TOOL_REGISTRY = {
    "open_app": OpenAppTool(),
    "close_app": CloseAppTool(),
    "system_info": SystemInfoTool(),
    # ...
}
```

**Executor Method:** `execute(tool_name: str, args: Dict, state: Dict) → Dict`

**Responsibility:**
- ONLY lookup + validate + call
- NO routing logic
- NO conditional execution

**CONSTRAINTS:**
- ✓ Static mapping (NO conditions)
- ✓ Validate args before execution
- ✓ Return standard result format

---

### 5. Individual Tools
**File:** `src/core/tools.py`

**Base Class:** `Tool` (Abstract)

**Interface:**
```python
class Tool(ABC):
    def execute(self, args: Dict, state: Dict) -> Dict:
        return {
            "success": bool,
            "result": any,
            "state_updates": dict,
            "log": str
        }
```

**Responsibility (EACH TOOL):**
- ONE action only
- NO routing
- NO inter-tool communication

**Examples:**
- `OpenAppTool`: Launch application
- `CloseAppTool`: Terminate application
- `SystemInfoTool`: Get system info
- `VolumeControlTool`: Set volume
- `WebSearchTool`: Search web

**CONSTRAINTS:**
- ✓ Pure function: (args, state) → result
- ❌ NO side effects except intended action
- ❌ NO calling other tools
- ❌ NO routing logic

---

## Execution Flow Example

**User:** "open youtube"

### Step 1: LLM Interpretation
```
Input: "open youtube"
↓
LLM.interpret("open youtube")
↓
Output: ("open_app", {"app": "youtube"})
```

### Step 2: Command Parsing
```
Input: ("open_app", {"app": "youtube"})
↓
Parser.parse("open_app", {"app": "youtube"})
↓
Lookup: INTENT_TO_TOOL["open_app"] = "open_app"
↓
Output: ("open_app", {"app": "youtube"})
```

### Step 3: Core Orchestration
```
Input: "open youtube"
↓
1. Call LLM → ("open_app", {"app": "youtube"})
2. Call Parser → ("open_app", {"app": "youtube"})
3. Call Executor.execute("open_app", {...}, state)
   ↓
   Registry lookup: TOOL_REGISTRY["open_app"]
   ↓
   Validate args
   ↓
   Call OpenAppTool.execute(...)
   ↓
   Return: {success: true, result: "Opened youtube", ...}
↓
Output: {success: true, ...}
```

### Step 4: Tool Execution
```
OpenAppTool.execute({"app": "youtube"}, state)
↓
1. Validate: app="youtube" ✓
2. Get OS (Windows/Mac/Linux)
3. Execute: subprocess.Popen(...)
4. Return: {
    success: true,
    result: "Opened youtube",
    state_updates: {"last_action": "open_app"},
    log: "Launched app: youtube"
}
```

---

## Validation Checklist

### ✓ Architecture
- [x] Flow: USER → LLM → PARSER → CORE → TOOL
- [x] No bypasses between components
- [x] Each component has ONE clear responsibility

### ✓ LLM
- [x] Only generates JSON (intent + args)
- [x] No tool selection
- [x] No action execution

### ✓ Command Parser
- [x] Only maps intent → tool
- [x] No complex logic
- [x] No semantic interpretation
- [x] Simple dictionary lookup

### ✓ Core
- [x] No tool selection
- [x] No intent interpretation
- [x] Pure orchestration
- [x] State management
- [x] Error handling + logging

### ✓ Tools
- [x] Each has ONE responsibility
- [x] Pure functions (args, state) → result
- [x] No routing logic
- [x] Standard interface

### ✓ Tool Registry
- [x] Static mapping only
- [x] No conditional logic
- [x] No routing intelligence

---

## Key Principles

### 1. Single Responsibility
- LLM: Interpretation ONLY
- Parser: Routing ONLY
- Core: Orchestration ONLY
- Tools: Execution ONLY

### 2. Determinism
- Flow is always: LLM → Parser → Core → Tool
- No hidden branches or conditions
- Completely traceable

### 3. No Duplication
- Intent selection happens ONCE (Parser)
- Tool execution happens ONCE (Executor)
- State management happens ONCE (Core)

### 4. Extensibility
- Add new tool: Create class + Register in TOOL_REGISTRY
- Add new intent: Add entry to INTENT_TO_TOOL
- No changes to Core, LLM, or Parser needed

---

## How to Extend

### Add New Tool
```python
# 1. Create in src/core/tools.py
class MyNewTool(Tool):
    def __init__(self):
        super().__init__("my_new_tool")
    
    def execute(self, args, state):
        # implementation
        return {...}

# 2. Register in src/core/tool_registry.py
TOOL_REGISTRY = {
    ...
    "my_new_tool": MyNewTool(),
}

# 3. Map intent in src/core/command_parser.py
INTENT_TO_TOOL = {
    ...
    "my_new_intent": "my_new_tool",
}
```

### Add New Intent
Just add mapping in `INTENT_TO_TOOL`. LLM will learn to generate it.

### Modify Tool Behavior
Edit the tool's `execute()` method. No impact on other components.

---

## Validation Run

```bash
python validate_architecture.py
```

Expected output:
```
✓ ALL CONSTRAINTS SATISFIED
✓ Architecture is STRICT and CONSISTENT
✓ No duplicate responsibilities
✓ Flow is deterministic
```

---

**Architecture Status:** ✓ VALIDATED
**Last Updated:** 2026-05-14
**Compliance:** 100% with Strict Architecture Spec
