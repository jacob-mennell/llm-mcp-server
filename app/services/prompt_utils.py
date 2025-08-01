def clean_prompt(prompt: str) -> str:
    """
    Cleans the prompt by stripping leading and trailing whitespace.
    Args:
        prompt (str): The prompt to clean.
    Returns:
        str: The cleaned prompt.
    """
    return prompt.strip()


def add_context(prompt: str, context: str) -> str:
    """
    Prepends context or instructions to the prompt.
    Args:
        prompt (str): The user prompt.
        context (str): The context or system instructions to add.
    Returns:
        str: The combined context and prompt.
    """
    return f"{context.strip()}\n\n{prompt.strip()}"


def truncate_prompt(prompt: str, max_length: int = 2048) -> str:
    """
    Truncates the prompt to a maximum number of characters.
    Args:
        prompt (str): The prompt to truncate.
        max_length (int): The maximum allowed length.
    Returns:
        str: The truncated prompt.
    """
    return prompt[:max_length]
