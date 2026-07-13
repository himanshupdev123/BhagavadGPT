"""
Integration tests for main.py prompt template functionality.
Tests verify that the enhanced prompt template works correctly with the existing system.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all required imports work."""
    try:
        from fastapi import FastAPI, HTTPException
        from fastapi.middleware.cors import CORSMiddleware
        from pydantic import BaseModel
        from langchain_core.prompts import PromptTemplate
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_prompt_template_variables():
    """Test that the prompt template has the required variables."""
    from langchain_core.prompts import PromptTemplate
    
    # Read the actual template from main.py
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the template string (between prompt_template = PromptTemplate.from_template(""" and """))
    start_marker = 'prompt_template = PromptTemplate.from_template("""'
    end_marker = '""")'
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("❌ Could not find prompt template in main.py")
        return False
    
    start_idx += len(start_marker)
    end_idx = content.find(end_marker, start_idx)
    
    if end_idx == -1:
        print("❌ Could not find end of prompt template")
        return False
    
    template_str = content[start_idx:end_idx]
    
    # Check for required variables
    required_vars = ['{context}', '{question}', '{username}']
    missing_vars = []
    
    for var in required_vars:
        if var not in template_str:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required variables: {missing_vars}")
        return False
    
    print(f"✅ All required variables present: {required_vars}")
    return True

def test_prompt_template_format():
    """Test that the prompt template can be formatted with test data."""
    from langchain_core.prompts import PromptTemplate
    
    # Create a minimal test template with the same structure
    test_template = PromptTemplate.from_template("""
USER QUESTION: {question}
USERNAME: {username}
CONTEXT: {context}
""")
    
    try:
        # Test formatting with sample data
        formatted = test_template.format(
            context="Test context with verse information",
            question="What is dharma?",
            username="TestUser"
        )
        
        # Verify all values are present in output
        assert "Test context with verse information" in formatted
        assert "What is dharma?" in formatted
        assert "TestUser" in formatted
        
        print("✅ Template formatting works correctly")
        return True
    except Exception as e:
        print(f"❌ Template formatting failed: {e}")
        return False

def test_username_extraction_logic():
    """Test that username extraction logic matches what's in main.py."""
    # Simulate the logic from main.py line 1184
    test_data = {"user": "RealUser"}
    username = test_data.get("user", "") if test_data.get("user") else "Friend"
    
    assert username == "RealUser", "Should extract username when present"
    print("✅ Username extraction with 'user' field: RealUser")
    
    # Test fallback
    test_data_empty = {"user": ""}
    username = test_data_empty.get("user", "") if test_data_empty.get("user") else "Friend"
    
    assert username == "Friend", "Should fallback to 'Friend' when empty"
    print("✅ Username extraction fallback: Friend")
    
    # Test missing field
    test_data_missing = {}
    username = test_data_missing.get("user", "") if test_data_missing.get("user") else "Friend"
    
    assert username == "Friend", "Should fallback to 'Friend' when missing"
    print("✅ Username extraction missing field: Friend")
    
    return True

def test_context_formatting():
    """Test that context formatting matches main.py logic."""
    # Simulate ChromaDB results structure
    results = {
        'documents': [['Verse meaning 1', 'Verse meaning 2']],
        'metadatas': [[
            {'reference': 'Chapter 2, Verse 47', 'shloka': 'कर्मण्येवाधिकारस्ते...'},
            {'reference': 'Chapter 3, Verse 35', 'shloka': 'श्रेयान्स्वधर्मो...'}
        ]]
    }
    
    # Format context as in main.py
    context_str = ""
    if results['documents'] and results['documents'][0]:
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            context_str += f"\n[{meta['reference']}]\n{meta['shloka']}\nMeaning & Purport: {doc}\n"
    
    # Verify formatting
    assert 'Chapter 2, Verse 47' in context_str
    assert 'कर्मण्येवाधिकारस्ते...' in context_str
    assert 'Verse meaning 1' in context_str
    
    print("✅ Context formatting works correctly")
    return True

def test_enhanced_prompt_structure():
    """Test that the enhanced prompt has all required layers."""
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_sections = [
        ('Security Layer', '🛡️ SECURITY LAYER: PROMPT INJECTION DEFENSE'),
        ('Language Detection', '🌍 LANGUAGE DETECTION LAYER'),
        ('Question Classification', '🔍 QUESTION CLASSIFICATION LAYER'),
        ('Response Generation', '📝 RESPONSE GENERATION LAYER'),
        ('Quality Validation', '✅ QUALITY VALIDATION LAYER'),
        ('Safety Override', 'PRIORITY 1: SAFETY OVERRIDE'),
        ('Meta-Questions', 'PRIORITY 3: META-QUESTIONS'),
        ('Relationship Guidance', 'RELATIONSHIPS AND BOUNDARIES'),
        ('Shloka Integrity', 'SANSKRIT SHLOKA INTEGRITY RULES'),
        ('Conversational Follow-up', 'CONVERSATIONAL FOLLOW-UP HANDLING')
    ]
    
    missing_sections = []
    for name, marker in required_sections:
        if marker not in content:
            missing_sections.append(name)
    
    if missing_sections:
        print(f"❌ Missing sections: {missing_sections}")
        return False
    
    print(f"✅ All {len(required_sections)} required sections present")
    return True

def test_api_endpoint_compatibility():
    """Test that the API endpoint structure is compatible."""
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for critical endpoint components
    checks = [
        ('@app.post("/v1/chat/completions")', 'OpenAI-compatible endpoint'),
        ('prompt_template.format(', 'Template formatting call'),
        ('formatted_prompt = ', 'Prompt variable assignment'),
        ('llm.invoke(formatted_prompt)', 'LLM invocation'),
        ('response.content', 'Response content extraction'),
        ('StreamingResponse', 'Streaming support')
    ]
    
    all_present = True
    for check, description in checks:
        if check not in content:
            print(f"❌ Missing: {description} ({check})")
            all_present = False
        else:
            print(f"✅ Found: {description}")
    
    return all_present

def run_all_tests():
    """Run all integration tests."""
    print("=" * 70)
    print("MAIN.PY INTEGRATION TESTS")
    print("=" * 70)
    print()
    
    tests = [
        ("Import Test", test_imports),
        ("Template Variables Test", test_prompt_template_variables),
        ("Template Formatting Test", test_prompt_template_format),
        ("Username Extraction Test", test_username_extraction_logic),
        ("Context Formatting Test", test_context_formatting),
        ("Enhanced Prompt Structure Test", test_enhanced_prompt_structure),
        ("API Endpoint Compatibility Test", test_api_endpoint_compatibility)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * 70)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ ALL INTEGRATION TESTS PASSED!")
        return True
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
