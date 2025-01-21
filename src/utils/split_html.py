"""
This script splits an HTML file into Hugo partials, such as header, footer, and navigation.
It helps modularize the theme by creating reusable components.
"""

import os
from bs4 import BeautifulSoup

# Function to split HTML into partials

def split_html_into_partials(html_content, output_dir):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract and save header
    header = soup.find('header')
    if header:
        with open(os.path.join(output_dir, 'header.html'), 'w') as file:
            file.write(str(header))

    # Extract and save footer
    footer = soup.find('footer')
    if footer:
        with open(os.path.join(output_dir, 'footer.html'), 'w') as file:
            file.write(str(footer))

    # Extract and save navigation
    nav = soup.find('nav')
    if nav:
        with open(os.path.join(output_dir, 'nav.html'), 'w') as file:
            file.write(str(nav))

    # Extract and save sidebar
    sidebar = soup.find('aside')
    if sidebar:
        with open(os.path.join(output_dir, 'sidebar.html'), 'w') as file:
            file.write(str(sidebar))

# Example usage
if __name__ == "__main__":
    # Load an example HTML file
    with open('themes/example/index.html', 'r') as file:
        html_content = file.read()

    # Split the HTML into partials
    split_html_into_partials(html_content, 'themes/example/partials') 