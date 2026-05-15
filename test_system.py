#!/usr/bin/env python3
"""Complete JARVIS system test."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all imports work."""
    print("\n[TEST 1] Imports")
    print("─" * 50)
    
    try:
        from src.core.llm_engine import LLMEngine
        print("✓ LLMEngine")
        
        from src.core.command_parser import CommandParser
        print("✓ CommandParser")
        
        from src.core.audio_input import AudioInputManager
        print("✓ AudioInputManager")
        
        from src.core.tts_engine import TTSEngine
        print("✓ TTSEngine")
        
        from src.core.core import JARVISCore
        print("✓ JARVISCore")
        
        from src.core.tool_registry import ToolExecutor, TOOL_REGISTRY
        print("✓ ToolRegistry")
        
        from src.core.tools import (
            OpenAppTool, CloseAppTool, SystemInfoTool,
            VolumeControlTool, WebSearchTool, OpenUrlTool
        )
        print("✓ Tools")
        
        from src.utils.config import Config
        print("✓ Config")
        
        print("\n✓ All imports successful")
        return True
    except ImportError as e:
        print(f"\n✗ Import failed: {e}")
        return False

def test_config():
    """Test configuration loading."""
    print("\n[TEST 2] Configuration")
    print("─" * 50)
    
    try:
        from src.utils.config import Config
        
        config = Config()
        config.load()
        
        wake_word = config.get("wake_word")
        print(f"✓ Wake-word: {wake_word}")
        
        model = config.get("llm_model")
        print(f"✓ LLM Model: {model}")
        
        print("\n✓ Configuration loaded")
        return True
    except Exception as e:
        print(f"\n✗ Config test failed: {e}")
        return False

def test_tools():
    """Test tool interface and registry."""
    print("\n[TEST 3] Tool Registry & Interface")
    print("─" * 50)
    
    try:
        from src.core.tool_registry import TOOL_REGISTRY, ToolExecutor
        
        print(f"✓ Tools registered: {len(TOOL_REGISTRY)}")
        for name in TOOL_REGISTRY.keys():
            print(f"  • {name}")
        
        # Test tool interface
        tool = TOOL_REGISTRY.get("system_info")
        if tool:
            result = tool.execute({"type": "time"}, {})
            if "success" in result and "log" in result:
                print(f"\n✓ Tool interface valid")
                print(f"  Result: {result['log']}")
            else:
                print(f"\n✗ Tool result missing required fields")
                return False
        
        print("\n✓ Tools working")
        return True
    except Exception as e:
        print(f"\n✗ Tool test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_core():
    """Test Core orchestrator (without full LLM)."""
    print("\n[TEST 4] Core Orchestrator")
    print("─" * 50)
    
    try:
        from src.core.llm_engine import LLMEngine
        from src.core.core import JARVISCore
        
        llm = LLMEngine()
        core = JARVISCore(llm)
        
        print("✓ JARVISCore initialized")
        
        state = core.get_state()
        if isinstance(state, dict):
            print(f"✓ State management working")
            print(f"  Keys: {list(state.keys())}")
        else:
            print("✗ State not valid")
            return False
        
        print("\n✓ Core orchestrator ready")
        return True
    except Exception as e:
        print(f"\n✗ Core test failed: {e}")
        return False

def test_architecture():
    """Test strict architecture constraints."""
    print("\n[TEST 5] Architecture Validation")
    print("─" * 50)
    
    checks_passed = 0
    checks_total = 5
    
    # Check 1: LLM only has interpret
    try:
        from src.core.llm_engine import LLMEngine
        llm = LLMEngine()
        
        has_interpret = hasattr(llm, 'interpret')
        has_no_parse_intent = not hasattr(llm, 'parse_intent')
        
        if has_interpret and has_no_parse_intent:
            print("✓ LLM: Only interpret() - no parsing")
            checks_passed += 1
        else:
            print("✗ LLM: Has unexpected methods")
    except:
        pass
    
    # Check 2: Parser is simple
    try:
        from src.core.command_parser import CommandParser
        parser = CommandParser()
        
        if hasattr(parser, 'INTENT_TO_TOOL'):
            print("✓ Parser: Static mapping")
            checks_passed += 1
        else:
            print("✗ Parser: Missing static mapping")
    except:
        pass
    
    # Check 3: Registry is static
    try:
        from src.core.tool_registry import TOOL_REGISTRY
        
        if isinstance(TOOL_REGISTRY, dict):
            print("✓ Registry: Static dict")
            checks_passed += 1
        else:
            print("✗ Registry: Not static")
    except:
        pass
    
    # Check 4: Core orchestrates
    try:
        from src.core.core import JARVISCore
        core = JARVISCore(None)
        
        has_execute = hasattr(core, 'execute_command')
        has_state = hasattr(core, 'state')
        
        if has_execute and has_state:
            print("✓ Core: Orchestrator with state management")
            checks_passed += 1
        else:
            print("✗ Core: Missing orchestration")
    except:
        pass
    
    # Check 5: Tools are atomic
    try:
        from src.core.tools import OpenAppTool
        tool = OpenAppTool()
        
        has_execute = hasattr(tool, 'execute')
        has_validate = hasattr(tool, 'validate_args')
        
        if has_execute and has_validate:
            print("✓ Tools: Atomic with interface")
            checks_passed += 1
        else:
            print("✗ Tools: Invalid interface")
    except:
        pass
    
    print(f"\n✓ Architecture: {checks_passed}/{checks_total} checks passed")
    return checks_passed >= 4

def main():
    print("╔" + "═" * 48 + "╗")
    print("║" + " " * 12 + "JARVIS COMPLETE SYSTEM TEST" + " " * 10 + "║")
    print("╚" + "═" * 48 + "╝")
    
    results = {
        "Imports": test_imports(),
        "Configuration": test_config(),
        "Tool Registry": test_tools(),
        "Core Orchestrator": test_core(),
        "Architecture": test_architecture(),
    }
    
    print("\n" + "═" * 50)
    print("TEST RESULTS")
    print("═" * 50)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "═" * 50)
    if all_passed:
        print("✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("\nJARVIS is ready to run!")
        print("Next: python run.py")
        return 0
    else:
        print("✗ Some tests failed")
        print("\nCheck errors above and run:")
        print("  python check_environment.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())
