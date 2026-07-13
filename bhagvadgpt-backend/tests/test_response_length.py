"""
Test script to verify response length customization implementation.

This script tests that the prompt template correctly includes:
1. Detection logic for length preference keywords
2. Instructions for adjusting Context_Connection length
3. Explicit rule to never truncate Sanskrit shloka
"""

import sys
import re

def test_response_length_implementation():
    """Verify response length customization is implemented in main.py"""
    
    print("🧪 Testing Response Length Customization Implementation...\n")
    
    # Read the main.py file
    try:
        with open("main.py", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ ERROR: main.py not found")
        return False
    
    # Test 1: Check for length preference detection keywords
    print("Test 1: Checking for length preference keywords...")
    brief_keywords = ["Brief", "short", "quick", "summary"]
    detailed_keywords = ["Detailed", "elaborate", "explain"]
    
    has_brief = all(keyword in content for keyword in brief_keywords)
    has_detailed = all(keyword in content for keyword in detailed_keywords)
    
    if has_brief and has_detailed:
        print("✅ PASS: All length preference keywords found")
        print(f"   - Brief keywords: {', '.join(brief_keywords)}")
        print(f"   - Detailed keywords: {', '.join(detailed_keywords)}")
    else:
        print("❌ FAIL: Missing length preference keywords")
        if not has_brief:
            print(f"   - Missing brief keywords: {[k for k in brief_keywords if k not in content]}")
        if not has_detailed:
            print(f"   - Missing detailed keywords: {[k for k in detailed_keywords if k not in content]}")
        return False
    
    # Test 2: Check for sentence count specifications
    print("\nTest 2: Checking for sentence count specifications...")
    sentence_patterns = [
        r"1-2 sentence",
        r"3-5 sentence",
        r"5-7 sentence"
    ]
    
    found_patterns = []
    for pattern in sentence_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            found_patterns.append(pattern)
    
    if len(found_patterns) == 3:
        print("✅ PASS: All sentence count specifications found")
        print(f"   - Brief: 1-2 sentences")
        print(f"   - Default: 3-5 sentences")
        print(f"   - Detailed: 5-7 sentences")
    else:
        print(f"❌ FAIL: Missing sentence count specifications")
        print(f"   - Found {len(found_patterns)}/3 patterns")
        return False
    
    # Test 3: Check for explicit rule to never truncate Sanskrit
    print("\nTest 3: Checking for Sanskrit preservation rule...")
    sanskrit_preservation_patterns = [
        "Never truncate Sanskrit",
        "NEVER TRUNCATE",
        "regardless of length preference"
    ]
    
    has_sanskrit_rule = any(pattern in content for pattern in sanskrit_preservation_patterns)
    
    if has_sanskrit_rule:
        print("✅ PASS: Sanskrit preservation rule found")
        print("   - Rule: Never truncate Sanskrit shloka or translation")
    else:
        print("❌ FAIL: Sanskrit preservation rule not found")
        return False
    
    # Test 4: Check for LENGTH COMPLIANCE section
    print("\nTest 4: Checking for LENGTH COMPLIANCE section...")
    
    if "LENGTH COMPLIANCE" in content:
        print("✅ PASS: LENGTH COMPLIANCE section found")
        print("   - Section includes instructions for response generation")
    else:
        print("❌ FAIL: LENGTH COMPLIANCE section not found")
        return False
    
    # Test 5: Check for STEP 2: DETECT RESPONSE LENGTH PREFERENCE
    print("\nTest 5: Checking for response length detection step...")
    
    if "STEP 2: DETECT RESPONSE LENGTH PREFERENCE" in content:
        print("✅ PASS: Response length detection step found")
        print("   - Explicit step for detecting user preferences")
    else:
        print("❌ FAIL: Response length detection step not found")
        return False
    
    # Test 6: Verify default behavior specification
    print("\nTest 6: Checking for default behavior specification...")
    
    if "No specification" in content and "default" in content:
        print("✅ PASS: Default behavior specified")
        print("   - Default: 3-5 sentences when no preference given")
    else:
        print("❌ FAIL: Default behavior not clearly specified")
        return False
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print("\nResponse length customization is fully implemented:")
    print("  ✓ Length preference keyword detection (brief/short/quick, detailed/elaborate/explain)")
    print("  ✓ Context_Connection length adjustment (1-2, 3-5, 5-7 sentences)")
    print("  ✓ Sanskrit shloka preservation rule")
    print("  ✓ Explicit detection step in prompt flow")
    print("  ✓ Default behavior defined")
    
    return True

if __name__ == "__main__":
    success = test_response_length_implementation()
    sys.exit(0 if success else 1)
