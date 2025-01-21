"""
This script completes the workflow for converting HTML templates, websites, or Hugo themes into fully integrated Hugo themes with Decap CMS.
It detects the input state and executes the necessary conversion steps.
"""

import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to complete the workflow based on input state
def complete(path):
    logging.info(f"Starting workflow completion for {path}...")
    try:
        # Detect input state by checking file extensions and directory structure
        if os.path.isdir(path):
            if 'config.toml' in os.listdir(path):
                input_type = "Hugo theme"
            else:
                input_type = "HTML website"
        elif path.endswith('.html'):
            input_type = "HTML template"
        else:
            logging.warning("Unknown input type")
            return "Unknown input type"

        # Execute necessary steps based on input type
        if input_type == "HTML template":
            logging.info("Converting HTML template to Hugo theme...")
            hugoify(path)
        elif input_type == "Hugo theme":
            logging.info("Integrating Decap CMS...")
            decapify(path)
        elif input_type == "HTML website":
            logging.info("Converting HTML website to Hugo theme...")
            # Additional logic for HTML website conversion
            hugoify(path)
            decapify(path)

        logging.info("Workflow completion complete.")
        return "Completion complete"
    except Exception as e:
        logging.error(f"Error during workflow completion: {e}")
        return "Completion failed" 