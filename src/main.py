"""
This script serves as the main entry point for the Hugo-ifier tool.
It initializes the application and can be used to run the tool directly.
"""

import os
from utils.analyze_html import analyze_html
from utils.split_html import split_html_into_partials
from utils.replace_content import replace_hardcoded_content

# Directory containing themes
THEMES_DIR = 'themes'

# Process each theme in the themes directory recursively
def process_themes():
    for root, dirs, files in os.walk(THEMES_DIR):
        for file in files:
            if file.endswith('.html'):
                theme_path = os.path.join(root, file)
                print(f"Processing file: {theme_path}")

                # Load the HTML file
                with open(theme_path, 'r') as file:
                    html_content = file.read()

                # Analyze HTML
                suggestions = analyze_html(html_content)
                print("Analysis Suggestions:", suggestions)

                # Split HTML into partials
                partials_dir = os.path.join(root, 'partials')
                os.makedirs(partials_dir, exist_ok=True)
                split_html_into_partials(html_content, partials_dir)

                # Replace hardcoded content
                updated_content = replace_hardcoded_content(html_content)
                with open(theme_path, 'w') as file:
                    file.write(updated_content)

                print(f"Finished processing file: {theme_path}")

                # Checkpoint: Log progress
                with open('processing_log.txt', 'a') as log_file:
                    log_file.write(f"Processed: {theme_path}\n")

# Main function to run the application
def main():
    print("Welcome to the Hugo-ifier tool!")
    # Additional initialization or setup code can be added here
    process_themes()

if __name__ == "__main__":
    main() 