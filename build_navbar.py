import re

def read_html_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_html_content(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def generate_navbar_html(content):
    headings = re.findall(r'<h1>(.*?)</h1>', content)
    navbar_html = '<ul>'
    for heading in headings:
        id_link = heading.lower().replace(' ', '-')
        navbar_html += f'<li><a href="#{id_link}">{heading}</a></li>'
    navbar_html += '</ul>'
    return navbar_html

def replace_navbar_placeholder(template_content, navbar_html):
    return template_content.replace('__navbar_body', navbar_html)

def main():
    # Path to your HTML template
    template_path = 'template.html'
    # Path where the final HTML will be saved
    output_path = 'index.html'

    # Read the HTML template
    template_content = read_html_content(template_path)
    # Generate navbar HTML based on template content
    navbar_html = generate_navbar_html(template_content)
    # Replace the placeholder with actual navbar HTML
    final_content = replace_navbar_placeholder(template_content, navbar_html)
    # Write the final HTML content to file
    write_html_content(output_path, final_content)
    print("Navbar has been built and HTML file is updated.")

if __name__ == "__main__":
    main()
