import anthropic
from config import ANTHROPIC_API_KEY

def get_claude_response(prompt: str) -> str:
    """
    Send a prompt to Claude and get the response
    
    Args:
        prompt (str): The input prompt to send to Claude
        
    Returns:
        str: Claude's response
    """
    try:
        # Initialize the Anthropic client
        client = anthropic.Anthropic(
            api_key=ANTHROPIC_API_KEY
        )

        # Send message to Claude
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return message.content[0].text
        
    except Exception as e:
        return f"Error occurred: {str(e)}"

def main():
    # Example usage
    test_prompt = "What is the capital of France?"
    response = get_claude_response(test_prompt)
    print(f"Prompt: {test_prompt}")
    print(f"Response: {response}")

if __name__ == "__main__":
    main() 