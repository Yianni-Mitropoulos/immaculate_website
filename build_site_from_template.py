import re

def read_html_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_html_content(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def sanitize_id(text):
    """ Sanitize text to create a valid HTML ID """
    return re.sub(r'\s+', '-', text.lower().strip())

def extract_and_assign_headings(content):
    """ Parses the HTML content to assign h1 and h2 tags into structured data """
    pattern = r'(<h1>(.*?)</h1>|<h2>(.*?)</h2>)'
    matches = re.findall(pattern, content)

    structured_data = []
    current_h1 = None

    for match in matches:
        if match[1]:  # This is an h1
            current_h1 = {'id': sanitize_id(match[1]), 'text': match[1], 'subheadings': []}
            structured_data.append(current_h1)
        elif match[2] and current_h1:  # This is an h2
            current_h1['subheadings'].append({'id': sanitize_id(match[2]), 'text': match[2]})

    return structured_data

def generate_navbar_html(structured_data):
    """ Generates nested HTML for the navbar from structured data """
    navbar_html = '<ul>'
    for item in structured_data:
        navbar_html += f'<li><a href="#{item["id"]}">{item["text"]}</a>'
        if item['subheadings']:
            navbar_html += '<ul class="sub-menu">'
            for sub in item['subheadings']:
                navbar_html += f'<li><a href="#{sub["id"]}">{sub["text"]}</a></li>'
            navbar_html += '</ul>'
        navbar_html += '</li>'
    navbar_html += '</ul>'
    return navbar_html

def replace_navbar_placeholder(template_content, navbar_html):
    """ Replaces the navbar placeholder in the template with generated navbar HTML """
    return template_content.replace('__navbar_body', navbar_html)

def main():
    # Paths to your files
    template_path = 'template.html'
    output_path = 'index.html'

    # Read the HTML template
    template_content = read_html_content(template_path)
    # Extract headings, assign them, and generate navbar HTML
    structured_data = extract_and_assign_headings(template_content)
    navbar_html = generate_navbar_html(structured_data)
    # Replace the placeholder with actual navbar HTML
    final_content = replace_navbar_placeholder(template_content, navbar_html)
    # Write the final HTML content to file
    write_html_content(output_path, final_content)
    print("index.html built.")

if __name__ == "__main__":
    main()
