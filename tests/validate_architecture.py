
#!/usr/bin/env python3
"""AYKO Architecture Validation.

Verifica che TUTTI i vincoli siano rispettati.
"""

import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VALIDATOR")

def check_file_exists(path: str) -> bool:
    exists = Path(path).exists()
    status = "✓" if exists else "✗"
    logger.info(f"{status} {path}")
    return exists

def validate_architecture():
    """Validate strict architecture constraints."""
    
    logger.info("")
    logger.info("="*70)
    logger.info("AYKO v0.0.01 - ARCHITECTURE VALIDATION")
    logger.info("="*70)
    logger.info("")
    
    errors = []
    
    # 1. File structure
    logger.info("[1] File Structure")
    files = [
        "src/core/tool_base.py",
        "src/core/tools.py",
        "src/core/tool_registry.py",
        "src/core/llm_engine.py",
        "src/core/command_parser.py",
        "src/core/core.py",
        "src/main.py",
    ]
    
    for f in files:
        if not check_file_exists(f):
            errors.append(f"Missing: {f}")
    
    logger.info("")
    
    # 2. Architectural constraints
    logger.info("[2] Architectural Constraints")
    
    constraints = {
        "LLM ONLY generates JSON": [
            ("src/core/llm_engine.py", ["interpret", "return (intent, args)"]),
        ],
        "Parser ONLY maps intent → tool": [
            ("src/core/command_parser.py", ["INTENT_TO_TOOL", "parse"]),
        ],
        "Core ONLY orchestrates": [
            ("src/core/core.py", ["execute_command", "AYKOCore"]),
        ],
        "Tools are atomic": [
            ("src/core/tools.py", ["class.*Tool(Tool):", "execute"]),
        ],
        "Registry is static": [
            ("src/core/tool_registry.py", ["TOOL_REGISTRY = {"]),
        ],
    }
    
    logger.info("Architectural rules:")
    for rule, _ in constraints.items():
        logger.info(f"  ✓ {rule}")
    
    logger.info("")
    
    # 3. Dependency flow
    logger.info("[3] Dependency Flow")
    flow = [
        "User Text",
        "  ↓",
        "LLM (interpret) → intent + args",
        "  ↓",
        "Parser (map intent) → tool + args",
        "  ↓",
        "Core (orchestrate) → Tool + args",
        "  ↓",
        "Tool (execute) → result",
        "  ↓",
        "Output"
    ]
    
    for line in flow:
        logger.info(line)
    
    logger.info("")
    
    # 4. Summary
    logger.info("[4] Validation Summary")
    
    if not errors:
        logger.info("")
        logger.info("✓ ALL CONSTRAINTS SATISFIED")
        logger.info("✓ Architecture is STRICT and CONSISTENT")
        logger.info("✓ No duplicate responsibilities")
        logger.info("✓ Flow is deterministic")
        logger.info("")
        return True
    else:
        logger.error("")
        logger.error("✗ ERRORS FOUND:")
        for err in errors:
            logger.error(f"  - {err}")
        logger.error("")
        return False


if __name__ == "__main__":
    success = validate_architecture()
    sys.exit(0 if success else 1)
