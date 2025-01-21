import os
import openai

# Configuration module for AI models and other settings

# OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Function to set up OpenAI API key
def setup_openai_api():
    openai.api_key = OPENAI_API_KEY

# Default AI models for different tasks
DEFAULT_COMPLETION_MODEL = "gpt-4-turbo"
TRANSLATION_MODEL = "gpt-4-turbo"
ANALYSIS_MODEL = "gpt-4-turbo"

# Other AI parameters
MAX_TOKENS = 1500
TEMPERATURE = 0.7

# Add any other global settings or constants here 