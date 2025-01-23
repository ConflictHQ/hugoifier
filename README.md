# Hugoifier (AI-Powered Theme Converter)

A utility that takes your HTML template/website or Hugo them and generates a production-ready Hugo theme with Decap CMS integration. 

## What is it?

Hugoifier is a Python-based utility that:

- Converts any HTML/JS/CSS theme into a Hugo-compatible theme using AI.
- Extracts layout data into structured files (`data/*.yaml` or `data/*.json`) to make the theme editable via Decap CMS.
- Generates and wires Decap CMS into the Hugo setup, making it fully ready for content management.
- Uses OpenAI's efficient AI models to analyze theme files and determine the best Hugo template tag placements.

## Core Features & Workflow

### Step 1: AI-Powered HTML Conversion

- Uses GPT-4-Turbo to analyze an HTML theme and suggest where Hugo template tags (`{{ .Title }}`, `{{ .Content }}`, etc.) should be placed.
- Identifies partials (e.g., `header.html`, `footer.html`) and reusable elements.
- Converts all hardcoded links, images, and text into Hugo-friendly components.

### Step2 2: Decap CMS Integration

- Extracts the site structure elements (navigation, hero sections, footers) into YAML/JSON files in Hugo's `data/` directory.
- Generates a Decap CMS `config.yml` file with proper collections for pages, posts, and layout elements.
- Ensures the generated theme is fully editable via Decap CMS.

### Step3 3: Automation & Deployment

- Provides a Python CLI tool to automate the entire conversion process.
- Offer interactive mode for customization and auto mode for full automation.
- Ensure themes are deployable on Cloudflare Pages CMS setups.
- Deploy the CMS on Cloudflare Pages.

## Getting Started

### Prerequisites

- Python 3.11.4
- Hugo extended version
- OpenAI API key
- Cloudflare account (for deployment)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/hugo-ifier.git
   ```

2. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the CLI tool to start the conversion process:

```bash
python cli.py convert --input theme.html --output hugo-theme
```
