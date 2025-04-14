# Anthropic API Configuration
import os

# Get API key from environment variable
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')  # Set this using environment variable

# Raise an error if the API key is not set
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set. Please set it before running the script.") 