"""
Integration test for enhanced prompt template in main.py

Tests that:
1. Prompt template can be formatted with all required parameters
2. Username extraction works correctly
3. Context formatting is compatible
4. Template contains enhanced features (security, language detection, classification)
"""

import sys
import os

# Add parent directory to path to import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_prompt_template_formatting():
    """Test that prompt template can be formatted with required parameters"""
    from main import prompt_template
    
    # Test data
    test_context = """
[Chapter 2, Verse 47]
Sanskrit: कर्मण्येवाधिकारस्ते मा फलेषु कदाचन।
Translation: You have a right to perform your prescribed duty, but you are not entitled to the fruits of action.
Meaning & Purport: This verse teaches about performing duty without attachment to results.
"""
    test_question = "I am feeling anxious about my exam results"
    test_username = "TestUser"
    
    try:
        # Try to format the prompt
        formatted = prompt_template.format(
            context=test_context,
            question=test_question,
            username=test_username
        )
        
        # Verify the formatted prompt contains all key elements
        assert "{context}" not in formatted, "Context placeholder not replaced"
        assert "{question}" not in formatted, "Question placeholder not replaced"
        assert "{username}" not in formatted, "Username placeholder not replaced"
        
        assert test_context in formatted, "Context not in formatted prompt"
        assert test_question in formatted, "Question not in formatted prompt"
        assert test_username in formatted, "Username not in formatted prompt"
        
        print("✅ Test 1 PASSED: Prompt template formatting works correctly")
        return True
    except Exception as e:
        print(f"❌ Test 1 FAILED: Error formatting prompt template: {e}")
        return False


def test_enhanced_features_present():
    """Test that enhanced features are present in the template"""
    from main import prompt_template
    
    template_str = prompt_template.template
    
    # Check for key enhanced features
    checks = {
        "Security Layer": "🛡️ SECURITY LAYER: PROMPT INJECTION DEFENSE" in template_str,
        "Language Detection": "🌍 LANGUAGE DETECTION LAYER" in template_str,
        "Classification System": "🔍 QUESTION CLASSIFICATION LAYER" in template_str,
        "Priority Ordering": "PRIORITY 1: SAFETY OVERRIDE" in template_str,
        "Meta-Questions": "META-QUESTIONS ABOUT THE GITA" in template_str,
        "Quality Validation": "✅ QUALITY VALIDATION LAYER" in template_str,
        "Shloka Integrity": "SANSKRIT SHLOKA INTEGRITY RULES" in template_str,
        "Relationship Guidance": "RELATIONSHIPS AND BOUNDARIES" in template_str,
        "Follow-up Handling": "CONVERSATIONAL FOLLOW-UP HANDLING" in template_str,
    }
    
    all_passed = True
    for feature, present in checks.items():
        if present:
            print(f"✅ {feature}: Present")
        else:
            print(f"❌ {feature}: Missing")
            all_passed = False
    
    if all_passed:
        print("\n✅ Test 2 PASSED: All enhanced features are present")
    else:
        print("\n❌ Test 2 FAILED: Some enhanced features are missing")
    
    return all_passed


def test_template_variables():
    """Test that template uses correct variable names"""
    from main import prompt_template
    
    # Check that template expects the right input variables
    expected_vars = {"context", "question", "username"}
    actual_vars = set(prompt_template.input_variables)
    
    if actual_vars == expected_vars:
        print(f"✅ Test 3 PASSED: Template variables are correct: {actual_vars}")
        return True
    else:
        print(f"❌ Test 3 FAILED: Template variables mismatch")
        print(f"   Expected: {expected_vars}")
        print(f"   Actual: {actual_vars}")
        return False


def test_username_extraction_logic():
    """Test the username extraction logic from the endpoint"""
    # Simulate the logic from the endpoint
    
    # Test case 1: username provided
    data1 = {"user": "Arjuna"}
    username1 = data1.get("user", "") if data1.get("user") else "Friend"
    assert username1 == "Arjuna", "Username extraction failed for provided username"
    
    # Test case 2: username empty string
    data2 = {"user": ""}
    username2 = data2.get("user", "") if data2.get("user") else "Friend"
    assert username2 == "Friend", "Username extraction failed for empty username"
    
    # Test case 3: username not provided
    data3 = {}
    username3 = data3.get("user", "") if data3.get("user") else "Friend"
    assert username3 == "Friend", "Username extraction failed for missing username"
    
    print("✅ Test 4 PASSED: Username extraction logic works correctly")
    return True


def run_all_tests():
    """Run all integration tests"""
    print("=" * 70)
    print("Enhanced Prompt Template Integration Tests")
    print("=" * 70)
    print()
    
    results = []
    
    # Run tests
    results.append(("Prompt Template Formatting", test_prompt_template_formatting()))
    print()
    results.append(("Enhanced Features Present", test_enhanced_features_present()))
    print()
    results.append(("Template Variables", test_template_variables()))
    print()
    results.append(("Username Extraction Logic", test_username_extraction_logic()))
    print()
    
    # Summary
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 70)
    
    return all(result for _, result in results)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
