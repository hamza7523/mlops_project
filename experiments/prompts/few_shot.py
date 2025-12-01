def get_prompt(question, context_class=None):
    """
    Few-Shot Prompting Strategy.
    Provides examples (k=3) to guide the model's response style.
    """
    examples = """
Example 1:
Context: Apple___Apple_scab
Question: My apple tree leaves have olive-green spots. What should I do?
Answer: This is Apple Scab. Remove fallen leaves to reduce spores and apply fungicides like captan early in the season.

Example 2:
Context: Tomato___Early_blight
Question: I see dark rings on my tomato leaves. How do I fix it?
Answer: This is Tomato Early Blight. Improve air circulation, avoid overhead watering, and apply copper-based fungicides.

Example 3:
Context: Corn_(maize)___healthy
Question: My corn looks green and tall. Is it okay?
Answer: Yes, your corn plant appears healthy. No treatment is needed.
"""

    if context_class:
        prompt = f"""You are a plant disease expert. Answer the question based on the context.
{examples}

Context: {context_class}
Question: {question}
Answer:"""
    else:
        prompt = f"""You are a plant disease expert. Answer the question.
{examples}

Question: {question}
Answer:"""
    return prompt
