def get_prompt(question, context_class=None):
    """
    Zero-Shot Prompting Strategy.
    Directly asks the model to answer the question based on the context class if provided.
    """
    if context_class:
        prompt = f"""You are an AI assistant for plant disease detection.
The user has a plant with the following condition: {context_class}.

Question: {question}

Answer:"""
    else:
        prompt = f"""Question: {question}

Answer:"""
    return prompt
