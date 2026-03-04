from strands import tool

@tool
def add_numbers(a: float, b: float) -> float:
    '''
    Add two numbers together and return the result.
    
    Args:
        a: The first number to add
        b: The second number to add
    
    Returns:
        The sum of a and b
    '''
    return a + b
