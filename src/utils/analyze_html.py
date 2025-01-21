"""
This script analyzes an HTML file to identify reusable components and suggest Hugo template tags.
It provides insights into how the HTML can be converted into a Hugo-compatible theme.
"""

import os
from openai import OpenAI

client = OpenAI()
from config import setup_openai_api, DEFAULT_COMPLETION_MODEL, MAX_TOKENS, TEMPERATURE

# Function to analyze HTML and suggest Hugo template tags
def analyze_html(html_content):
    # Set up OpenAI API key
    setup_openai_api()

    # Define the prompt for the AI model
    prompt = f"""
    You are an AI designed to convert an HTML theme into a Hugo-compatible theme. Analyze the following HTML file and provide the following:
    1. Identify reusable components like headers, footers, navbars, and sidebars.
    2. Suggest Hugo template tags (e.g., {{ .Title }}, {{ .Content }}, {{ .Params.hero }}) for dynamic content replacement.
    3. Recommend splitting the file into Hugo partials where applicable.
    4. Score the content blocks for whether they need specialized Hugo `data` configurations.

    HTML Input:
    {html_content}
    """

    # Call the OpenAI API
    response = client.chat.completions.create(model=DEFAULT_COMPLETION_MODEL,
    messages=[{"role": "system", "content": "You are an AI designed to convert an HTML theme into a Hugo-compatible theme."},
              {"role": "user", "content": prompt}],
    max_tokens=MAX_TOKENS,
    temperature=TEMPERATURE)

    # Return the AI's suggestions
    return response.choices[0].message.content.strip()

# Example usage
if __name__ == "__main__":
    # Load an example HTML file
    with open('themes/example/index.html', 'r') as file:
        html_content = file.read()

    # Analyze the HTML
    suggestions = analyze_html(html_content)
    print(suggestions) 