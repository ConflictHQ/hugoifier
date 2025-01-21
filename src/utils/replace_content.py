import os
from bs4 import BeautifulSoup

# Function to replace hardcoded content with Hugo template tags

def replace_hardcoded_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Replace static links with Hugo template tags
    for a in soup.find_all('a', href=True):
        a['href'] = '{{ .Permalink }}'

    # Replace inline text content with placeholders
    for p in soup.find_all('p'):
        p.string = '{{ .Params.variable }}'

    # Replace hardcoded image URLs
    for img in soup.find_all('img', src=True):
        img['src'] = '{{ .Site.BaseURL }}' + img['src']

    return str(soup)

# Example usage
if __name__ == "__main__":
    # Load an example HTML file
    with open('themes/example/index.html', 'r') as file:
        html_content = file.read()

    # Replace hardcoded content
    updated_content = replace_hardcoded_content(html_content)
    print(updated_content) 