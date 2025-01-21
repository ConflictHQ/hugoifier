"""
This script translates web content using OpenAI, maintaining the original context and meaning.
It processes the content and returns the translated version.
"""

from config import setup_openai_api, TRANSLATION_MODEL, MAX_TOKENS, TEMPERATURE
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to translate content using OpenAI
def translate(path):
    logging.info(f"Starting translation for content in {path}...")
    try:
        # Set up OpenAI API key
        setup_openai_api()

        # Load the content of the file
        with open(path, 'r') as file:
            content = file.read()

        # Define the prompt for the AI model
        prompt = f"""
        You are an AI designed to translate web content. Translate the following content into the desired language while maintaining the original context and meaning.

        Content:
        {content}
        """

        # Call the OpenAI API
        response = openai.Completion.create(
            engine=TRANSLATION_MODEL,
            prompt=prompt,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )

        # Log and return the translated content
        translated_content = response.choices[0].text.strip()
        logging.info("Translation complete.")
        return translated_content
    except Exception as e:
        logging.error(f"Error during translation: {e}")
        return "Translation failed" 