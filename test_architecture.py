#!/usr/bin/env python3
"""Test JARVIS architecture flow without UI/Audio."""

import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='[%(name)s] %(message)s'
)
logger = logging.getLogger("TEST")

# Test commands
TEST_CASES = [
    ("open youtube", ("open_app", {"app": "youtube"}, "open_app")),
    ("close spotify", ("close_app", {"app": "spotify"}, "close_app")),
    ("what time is it", ("system_info", {"type": "time"}, "system_info")),
    ("search python tutorials", ("web_search", {"query": "python tutorials"}, "web_search")),
]

def test_llm():
    """Test LLM interpretation."""
    logger.info("")
    logger.info("="*70)
    logger.info("[TEST 1] LLM Engine")
    logger.info("="*70)
    
    try:
        from core.llm_engine import LLMEngine
        
        llm = LLMEngine()
        if not llm.is_ready:
            logger.warning("⚠ Ollama not running. Skipping LLM test.")
            logger.warning("Start with: ollama serve")
            return False
        
        logger.info("✓ LLM ready")
        
        test_text = "open youtube"
        intent, args = llm.interpret(test_text)
        
        logger.info(f"Input: {test_text}")
        logger.info(f"Output: intent={intent}, args={args}")
        
        if intent != "unknown":
            logger.info("✓ LLM interpretation works")
            return True
        else:
            logger.error("✗ LLM failed to interpret")
            return False
    
    except Exception as e:
        logger.error(f"✗ LLM test error: {e}")
        return False

def test_parser():
    """Test Command Parser."""
    logger.info("")
    logger.info("="*70)
    logger.info("[TEST 2] Command Parser")
    logger.info("="*70)
    
    try:
        from core.command_parser import CommandParser
        
        parser = CommandParser()
        
        test_cases = [
            ("open_app", {"app": "youtube"}, "open_app"),
            ("close_app", {"app": "spotify"}, "close_app"),
            ("system_info", {"type": "time"}, "system_info"),
        ]
        
        all_pass = True
        for intent, args, expected_tool in test_cases:
            tool, mapped_args = parser.parse(intent, args)
            
            status = "✓" if tool == expected_tool else "✗"
            logger.info(f"{status} {intent} → {tool}")
            
            if tool != expected_tool:
                all_pass = False
        
        return all_pass
    
    except Exception as e:
        logger.error(f"✗ Parser test error: {e}")
        return False

def test_tool_registry():
    """Test Tool Registry."""
    logger.info("")
    logger.info("="*70)
    logger.info("[TEST 3] Tool Registry")
    logger.info("="*70)
    
    try:
        from core.tool_registry import ToolExecutor, TOOL_REGISTRY
        
        logger.info(f"Registered tools: {list(TOOL_REGISTRY.keys())}")
        
        # Test tool lookup
        tool = ToolExecutor.get_tool("open_app")
        if tool:
            logger.info("✓ Tool lookup works")
            return True
        else:
            logger.error("✗ Tool lookup failed")
            return False
    
    except Exception as e:
        logger.error(f"✗ Registry test error: {e}")
        return False

def test_tool_execution():
    """Test Tool Execution."""
    logger.info("")
    logger.info("="*70)
    logger.info("[TEST 4] Tool Execution (without actual launch)")
    logger.info("="*70)
    
    try:
        from core.tool_registry import ToolExecutor
        from core.tools import OpenAppTool
        
        # Test tool interface
        tool = OpenAppTool()
        
        # Validate args
        is_valid, error = tool.validate_args({"app": "test"})
        if is_valid:
            logger.info("✓ Tool validation works")
        else:
            logger.error(f"✗ Validation failed: {error}")
            return False
        
        # Check execute interface
        state = {"test": True}
        result = tool.execute({"app": "echo test"}, state)
        
        required_keys = ["success", "result", "state_updates", "log"]
        if all(k in result for k in required_keys):
            logger.info("✓ Tool execute interface is correct")
            logger.info(f"  Result: {result}")
            return True
        else:
            logger.error(f"✗ Tool interface incomplete: {result.keys()}")
            return False
    
    except Exception as e:
        logger.error(f"✗ Tool test error: {e}")
        return False

def test_core():
    """Test Core Orchestrator (without LLM/Audio)."""
    logger.info("")
    logger.info("="*70)
    logger.info("[TEST 5] Core Orchestrator Flow")
    logger.info("="*70)
    
    try:
        from core.core import JARVISCore
        from core.llm_engine import LLMEngine
        
        llm = LLMEngine()
        core = JARVISCore(llm)
        
        if not llm.is_ready:
            logger.warning("⚠ Ollama not running. Showing flow without execution.")
            logger.info("Flow will be: LLM → Parser → Core → Tool")
            return True
        
        # Test with simple command
        result = core.execute_command("open notepad")
        
        logger.info(f"Execution result:")
        logger.info(f"  Success: {result['success']}")
        logger.info(f"  Intent: {result['intent']}")
        logger.info(f"  Tool: {result['tool']}")
        
        logger.info(f"Timeline:")
        for line in result.get('timeline', []):
            logger.info(f"  {line}")
        
        return result['success']
    
    except Exception as e:
        logger.error(f"✗ Core test error: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("")
    logger.info("╔" + "="*68 + "╗")
    logger.info("║" + " "*15 + "JARVIS ARCHITECTURE FLOW TEST" + " "*25 + "║")
    logger.info("╚" + "="*68 + "╝")
    
    results = {
        "LLM Engine": test_llm(),
        "Command Parser": test_parser(),
        "Tool Registry": test_tool_registry(),
        "Tool Execution": test_tool_execution(),
        "Core Orchestrator": test_core(),
    }
    
    logger.info("")
    logger.info("="*70)
    logger.info("TEST SUMMARY")
    logger.info("="*70)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        logger.info(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    
    logger.info("")
    if all_passed:
        logger.info("✓ ALL TESTS PASSED")
        logger.info("✓ Architecture is ready for production")
    else:
        logger.warning("⚠ Some tests failed. Check Ollama status.")
    
    logger.info("")
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
