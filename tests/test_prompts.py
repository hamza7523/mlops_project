import sys
import os

# Add the project root to sys.path so we can import experiments
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.prompts import zero_shot, few_shot, meta_prompt


def test_zero_shot_prompt_structure():
    """Test that zero-shot prompt generates a string with the question."""
    question = "What is apple scab?"
    prompt = zero_shot.get_prompt(question)
    assert isinstance(prompt, str)
    assert question in prompt
    assert "Answer:" in prompt


def test_few_shot_prompt_structure():
    """Test that few-shot prompt includes examples and the question."""
    question = "How to treat rust?"
    context = "Corn_Rust"
    prompt = few_shot.get_prompt(question, context)
    assert isinstance(prompt, str)
    assert question in prompt
    assert context in prompt
    assert "Example 1:" in prompt
    assert "Example 2:" in prompt


def test_meta_prompt_structure():
    """Test that meta-prompt includes the persona and rules."""
    question = "Is my plant sick?"
    prompt = meta_prompt.get_prompt(question)
    assert isinstance(prompt, str)
    assert "Dr. Flora" in prompt
    assert "RULES:" in prompt
    assert question in prompt
