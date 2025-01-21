"""
This script generates a Decap CMS configuration file (config.yml) for a Hugo theme.
It analyzes the theme structure, optimizes it for Decap CMS, and creates the necessary configuration.
"""

import os
import yaml
import logging
from config import setup_openai_api

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to generate Decap CMS config.yml

def generate_decap_config(theme_path):
    logging.info(f"Generating Decap CMS config for theme at {theme_path}...")
    try:
        # Set up OpenAI API key
        setup_openai_api()

        # Analyze theme structure
        analyze_theme(theme_path)

        # Optimize theme for Decap CMS
        optimize_for_decap(theme_path)

        # Generate config.yml
        config = create_config_yaml(theme_path)

        # Save config.yml
        config_path = os.path.join(theme_path, 'config.yml')
        with open(config_path, 'w') as file:
            yaml.dump(config, file)

        logging.info("Decap CMS config generation complete.")
        return "Decap CMS config generation complete"
    except Exception as e:
        logging.error(f"Error during Decap CMS config generation: {e}")
        return "Decap CMS config generation failed"

# Analyze theme structure

def analyze_theme(theme_path):
    logging.info("Analyzing theme structure...")
    # Example logic to parse the theme's directory structure
    theme_elements = {
        "navigation": [],
        "hero": [],
        "footer": []
    }
    for root, dirs, files in os.walk(theme_path):
        for file in files:
            if file.endswith('.html'):
                # Analyze HTML files for key components
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    if "nav" in content:
                        theme_elements["navigation"].append(file)
                    if "hero" in content:
                        theme_elements["hero"].append(file)
                    if "footer" in content:
                        theme_elements["footer"].append(file)
    logging.info(f"Theme elements identified: {theme_elements}")
    return theme_elements

# Optimize theme for Decap CMS

def optimize_for_decap(theme_path):
    logging.info("Optimizing theme for Decap CMS...")
    # Example logic to ensure data files are used
    data_dir = os.path.join(theme_path, 'data')
    os.makedirs(data_dir, exist_ok=True)
    # Create example data files
    with open(os.path.join(data_dir, 'navigation.yaml'), 'w') as f:
        yaml.dump({"menu": ["Home", "About", "Contact"]}, f)
    logging.info("Data files created for Decap CMS.")

# Create config.yml

def create_config_yaml(theme_path):
    logging.info("Creating config.yml...")
    # Example logic to create config.yml
    config = {
        "backend": {
            "name": "git-gateway",
            "branch": "main"
        },
        "media_folder": "static/images/uploads",
        "collections": [
            {
                "name": "pages",
                "label": "Pages",
                "folder": "content/page",
                "create": True,
                "fields": [
                    {"label": "Title", "name": "title", "widget": "string"},
                    {"label": "Body", "name": "body", "widget": "markdown"}
                ]
            },
            {
                "name": "blog",
                "label": "Blog",
                "folder": "content/blog",
                "create": True,
                "fields": [
                    {"label": "Title", "name": "title", "widget": "string"},
                    {"label": "Body", "name": "body", "widget": "markdown"}
                ]
            }
        ]
    }
    logging.info("config.yml created.")
    return config 