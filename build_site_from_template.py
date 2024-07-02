import re

def read_html_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_html_content(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def sanitize_id(text):
    return re.sub(r'\s+', '-', text.lower().strip())

def extract_and_assign_headings(content):
    pattern = r'(<h1>(.*?)</h1>|<h2>(.*?)</h2>)'
    matches = re.findall(pattern, content)
    structured_data = []
    current_h1 = None
    for match in matches:
        if match[1]:
            current_h1 = {'id': sanitize_id(match[1]), 'text': match[1], 'subheadings': []}
            structured_data.append(current_h1)
        elif match[2] and current_h1:
            current_h1['subheadings'].append({'id': sanitize_id(match[2]), 'text': match[2]})
    return structured_data

def generate_navbar_html(structured_data):
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
    return template_content.replace('__navbar_body', navbar_html)

def adjust_pre_blocks(content):
    # Split the content into lines to check <pre> and </pre> placements
    lines = content.split('\n')
    adjusted_lines = []
    inside_pre = False
    code_lines = []

    for line in lines:
        # Check for <pre> on its own line
        if '<pre>' in line:
            if line.strip() != '<pre>':
                raise ValueError('Error: <pre> must be on its own line.')
            adjusted_lines.append('<pre><code>')
            inside_pre = True
            continue

        # Check for </pre> on its own line
        if '</pre>' in line:
            if line.strip() != '</pre>':
                raise ValueError('Error: </pre> must be on its own line.')

            # Process the collected code lines: calculate minimum indent and adjust lines
            if code_lines:
                min_indent = min(len(line) - len(line.lstrip()) for line in code_lines if line.strip())
                for code_line in code_lines:
                    if not code_line.strip():  # handle lines that are only whitespace
                        adjusted_lines.append(' &#10;')
                    else:
                        adjusted_lines.append(code_line[min_indent:])  # strip the minimum indent
            adjusted_lines.append('</code></pre>')
            code_lines = []  # reset for any potential next <pre> block
            inside_pre = False
            continue

        if inside_pre:
            # Collect lines inside <pre></pre> for later processing
            code_lines.append(line)
        else:
            adjusted_lines.append(line)

    # Reconstruct the content
    return '\n'.join(adjusted_lines)

def main():
    template_path = 'template.html'
    output_path = 'index.html'
    template_content = read_html_content(template_path)
    structured_data = extract_and_assign_headings(template_content)
    navbar_html = generate_navbar_html(structured_data)
    final_content = replace_navbar_placeholder(template_content, navbar_html)
    final_content = adjust_pre_blocks(final_content)
    write_html_content(output_path, final_content)
    print("index.html built.")

if __name__ == "__main__":
    main()
