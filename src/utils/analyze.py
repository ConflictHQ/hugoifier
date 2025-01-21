"""
This script analyzes HTML themes using OpenAI to provide recommendations for converting them into Hugo-compatible themes.
It identifies reusable components, suggests Hugo template tags, and recommends splitting the file into partials.
"""

from config import setup_openai_api, ANALYSIS_MODEL, MAX_TOKENS, TEMPERATURE
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to analyze inputs and provide recommendations
def analyze(path):
    logging.info(f"Starting analysis for {path}...")
    try:
        # Set up OpenAI API key
        setup_openai_api()

        # Load the content of the file
        with open(path, 'r') as file:
            content = file.read()

        # Define the prompt for the AI model
        prompt = f"""
        You are an AI designed to convert an HTML theme into a Hugo-compatible theme. Analyze the following HTML file and provide the following:
        1. Identify reusable components like headers, footers, navbars, and sidebars.
        2. Suggest Hugo template tags (e.g., {{ .Title }}, {{ .Content }}, {{ .Params.hero }}) for dynamic content replacement.
        3. Recommend splitting the file into Hugo partials where applicable.
        4. Score the content blocks for whether they need specialized Hugo `data` configurations.

        HTML Input:
        {content}
        """

        # Call the OpenAI API
        response = openai.Completion.create(
            engine=ANALYSIS_MODEL,
            prompt=prompt,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )

        # Log and return the AI's suggestions
        suggestions = response.choices[0].text.strip()
        logging.info("Analysis complete.")
        return suggestions
    except Exception as e:
        logging.error(f"Error during analysis: {e}")
        return "Analysis failed" 