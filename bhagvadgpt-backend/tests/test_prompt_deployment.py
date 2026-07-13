"""
Test script to verify the enhanced prompt template can be instantiated correctly
"""
from langchain_core.prompts import PromptTemplate

def test_prompt_template():
    """Test that the prompt template from main.py can be loaded and formatted"""
    try:
        # Read main.py to extract the prompt template
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the prompt template section
        start_marker = 'prompt_template = PromptTemplate.from_template("""'
        end_marker = '""")'
        
        start_idx = content.find(start_marker)
        if start_idx == -1:
            print("❌ ERROR: Could not find prompt_template in main.py")
            return False
        
        # Find the end of the template
        start_idx += len(start_marker)
        end_idx = content.find(end_marker, start_idx)
        
        if end_idx == -1:
            print("❌ ERROR: Could not find end of prompt_template")
            return False
        
        template_str = content[start_idx:end_idx]
        
        # Try to create the PromptTemplate
        prompt = PromptTemplate.from_template(template_str)
        
        # Verify it has the expected input variables
        expected_vars = ['context', 'question', 'username']
        if not all(var in prompt.input_variables for var in expected_vars):
            print(f"❌ ERROR: Missing expected input variables. Found: {prompt.input_variables}")
            return False
        
        # Try to format it with sample data
        test_context = "[Test Context]"
        test_question = "What is dharma?"
        test_username = "TestUser"
        
        formatted = prompt.format(
            context=test_context,
            question=test_question,
            username=test_username
        )
        
        # Verify the formatting worked
        if test_context not in formatted or test_question not in formatted or test_username not in formatted:
            print("❌ ERROR: Template formatting failed to include all variables")
            return False
        
        # Verify key sections are present
        required_sections = [
            "SYSTEM CORE IDENTITY",
            "SECURITY LAYER",
            "LANGUAGE DETECTION LAYER",
            "QUESTION CLASSIFICATION LAYER",
            "RESPONSE GENERATION LAYER",
            "QUALITY VALIDATION LAYER"
        ]
        
        for section in required_sections:
            if section not in template_str:
                print(f"❌ ERROR: Missing required section: {section}")
                return False
        
        print("✅ SUCCESS: Prompt template loaded and validated successfully!")
        print(f"   - Input variables: {prompt.input_variables}")
        print(f"   - Template length: {len(template_str)} characters")
        print(f"   - All 6 required layers present")
        print(f"   - Template formatting works correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_prompt_template()
    exit(0 if success else 1)
