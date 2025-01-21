# Hugo-ifier (AI-Powered Theme Converter)
This project aims to create a fully production-ready, AI-assisted Hugo theme converter with Decap CMS support as efficiently as possible. 

Objective
To build a Hugo-ifier, a Python-based utility that:
- Converts any HTML/JS/CSS theme into a Hugo-compatible theme using AI.
- Extracts layout data into structured files (data/*.yaml or data/*.json) to make the theme editable via Decap CMS.
- Generates and wires Decap CMS into the Hugo setup, making it fully ready for content management.
- Uses OpenAI's cheapest and most efficient model to analyze theme files and determine the best Hugo template tag placements.

Core Features & Workflow
- Phase 1: AI-Powered HTML Conversion
- - Use GPT-4-Turbo to analyze an HTML theme and suggest where Hugo template tags ({{ .Title }}, {{ .Content }}, etc.) should be placed.
- - Identify partials (header.html, footer.html, etc.) and reusable elements.
- -Convert hardcoded links, images, and text into Hugo-friendly components.
- Phase 2: Decap CMS Integration
- - Extract site structure elements (navigation, hero sections, footers) into YAML/JSON files in Hugo’s data/ directory.
- - Generate a Decap CMS config.yml file with proper collections for pages, posts, and layout elements.
- - Ensure the generated theme is fully editable via Decap CMS.
- Phase 3: Automation & Deployment
- - Provide a Python CLI tool to automate the entire conversion process.
- - Offer interactive mode for customization and auto mode for full automation.
- - Ensure themes are deployable on Cloudflare Pages CMS setups.
- - CMS will be deployed on Cloudflare Pages too.

TODOs
- Setup the project with the necessary files and folders.
- Prototype AI-powered template conversion (parse an HTML file, apply Hugo modifications).
- Implement Decap CMS integration (extract layout elements, generate CMS config).
- Refine automation to ensure a seamless pipeline from theme to Hugo + Decap-ready setup.
- Test with existing template library (local library with an initial bunch of themes) to validate output and improve efficiency.
- Develop an initial AI-powered script to process basic HTML templates.
- Expand functionality to support complex, multi-page themes.
- Fully automate Decap CMS setup and data file generation.
- Use python-based code harnesses to generate the Decap CMS config.yml file, analyze the HTML file and generate the Hugo-ready templates, etc.
- If the template is partially implemented, the AI should be able to identify the missing parts and generate the necessary code to complete the theme.
- The project should be able to be deployed on Cloudflare Pages.
- The project should manage the workflow of the conversion process, from the initial HTML file to the fully converted Hugo theme with Decap CMS integration and any ai connected api calls, it should also have a checker to ensure the theme is fully compatible with the Decap CMS.
- The project requires a linter to ensure the code is clean and follows the best practices.
- the project should use AI to fix any errors or issues that may arise during the conversion process, deployment or linting.
- The project should use different AI models for different tasks, for example:
    - GPT-4-Turbo for the initial analysis of the HTML file and the generation of the Hugo-ready templates.
    - GPT-4o for the generation of the Decap CMS config.yml file.
    - GPT-4o for the generation of the Python code harnesses.

- Use the below prompts for the corresponding AI integrations part of the code.

## Phase 1: AI-Powered HTML Conversion

### **Step 1: Analyze HTML Theme with GPT-4-Turbo**
**Prompt**:
```plaintext
You are an AI designed to convert an HTML theme into a Hugo-compatible theme. Analyze the following HTML file and provide the following:
1. Identify reusable components like headers, footers, navbars, and sidebars.
2. Suggest Hugo template tags (e.g., {{ .Title }}, {{ .Content }}, {{ .Params.hero }}) for dynamic content replacement.
3. Recommend splitting the file into Hugo partials where applicable.
4. Score the content blocks for whether they need specialized Hugo `data` configurations.

Example HTML:
{html_code}

Provide a clear explanation, the transformed Hugo-ready template, and code harness for parsing similar HTML files.
```

---

### **Step 2: Split HTML into Hugo Partials**
**Prompt**:
```plaintext
You are converting an HTML theme into a Hugo-compatible theme. Based on the analysis of the provided HTML file, split the following reusable components into partials:

1. Header (header.html)
2. Footer (footer.html)
3. Navigation (nav.html)
4. Sidebar (sidebar.html, if applicable)
5. Boxes, lists, and special containers

Here’s the HTML file:
{html_code}

Output:
1. Extracted partial files.
2. Placeholder template to include these partials in Hugo’s base layout.
3. Python code to automate this splitting process.
```

---

### **Step 3: Replace Hardcoded Content**
**Prompt**:
```plaintext
Analyze the provided HTML and replace all hardcoded links, images, and text with Hugo-compatible template tags. Examples include:

1. Replace static links with {{ .Permalink }} or {{ .RelPermalink }}.
2. Replace inline text content with placeholders like {{ .Params.variable }}.
3. Replace hardcoded image URLs with {{ .Site.BaseURL }} or similar.
4. Ensure support for all Hugo data types (string, list, map, etc.) where appropriate.

HTML Input:
{html_code}

Provide the updated Hugo template-ready file with the changes applied and a Python parser to automate this process.
```

---

## Phase 2: Decap CMS Integration

### **Step 1: Extract Layout Data**
**Prompt**:
```plaintext
You are building a Hugo-compatible theme with Decap CMS integration. Extract the following elements from the provided HTML/CSS structure into structured YAML or JSON files:

1. Navigation menu items.
2. Hero section text and images.
3. Footer links and copyright text.
4. Boxes, lists, or other specialized containers.

Output the data as YAML files in the following format:

Example YAML:
```yaml
navigation:
  - label: "Home"
    url: "/"
  - label: "About"
    url: "/about/"

hero:
  title: "Welcome to My Website"
  subtitle: "Your tagline here"
  image: "static/images/hero.jpg"

footer:
  copyright: "© 2025 My Website"
```

HTML Input:
{html_code}

Provide the extracted YAML files and a Python harness for automating this extraction.
```

---

### **Step 2: Generate Decap CMS `config.yml`**
**Prompt**:
```plaintext
You are setting up Decap CMS for a Hugo site. Generate a `config.yml` file based on the following requirements:

1. Create collections for Pages (`content/page/`), Blog Posts (`content/blog/`), and Layout Elements (navigation, hero sections, footer, etc.).
2. Define widgets for editing text, images, lists, and links.
3. Configure media uploads to use `static/images/uploads` as the folder.
4. Include support for editing CSS, theme images, and specialized content blocks.

Use the extracted YAML data structure as part of the CMS configuration.

Example Data:
{yaml_data}

Output a `config.yml` file for Decap CMS and Python code for generating it programmatically.
```

---

## Phase 3: Automation & Deployment

### **Step 1: Python CLI Tool**
**Prompt**:
```plaintext
You are designing a Python CLI tool for automating the conversion of HTML themes to Hugo-compatible themes with Decap CMS integration. Define the CLI commands and their functionality:

1. `convert`: Parse an HTML theme and generate Hugo-compatible templates.
2. `cms-setup`: Set up Decap CMS configuration and integrate it with the Hugo project.
3. `deploy`: Generate Cloudflare Pages configuration for deployment and trigger CI.

Provide a Python script template for implementing this CLI tool. Ensure it includes argument parsing, modular functions for each command, and support for Cloudflare Pages deployment.
```

---

### **Step 2: Deployment Hooks for Cloudflare Pages**
**Prompt**:
```plaintext
You are configuring deployment for a Hugo site with Decap CMS. Generate a configuration file for Cloudflare Pages that:

1. Defines the build command as `hugo`.
2. Sets the publish directory to `public/`.
3. Supports environment variables for Hugo version and other necessary configurations.
4. Automatically integrates Cloudflare's autogenerated project name for callbacks.

Output the complete configuration file and Python code to programmatically generate it.
```

---

### **Step 3: Testing with Real-World Templates**
**Prompt**:
```plaintext
Analyze the following HTML theme and test its conversion into a Hugo theme using the provided Hugo-ifier pipeline. Identify any issues with:

1. Template tag placement.
2. Partial splitting logic.
3. Decap CMS data extraction and integration.
4. Compatibility with Cloudflare Pages deployment.

Theme:
{html_code}

Output:
1. A summary of identified issues.
2. Recommendations for improving the pipeline.
3. Python code for debugging or resolving the issues.
```

---

### Next Steps

Use these prompts in an AI-assisted tool like Cursor.com to segment tasks and iteratively build and refine the Hugo-ifier Python-based utility. By combining these detailed prompts with GPT-4-Turbo, you can streamline the development process and ensure accurate results.


