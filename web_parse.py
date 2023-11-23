from bs4 import BeautifulSoup

def extract_main_paragraphs(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    paragraphs = soup.find_all(['p', 'table', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    main_paragraphs = []
    for element in paragraphs:
        if element.name == 'table':
            # Process table elements
            table_text = process_table(element)
            if table_text:
                main_paragraphs.append(table_text)
        else:
            # Process other elements as paragraphs
            text = element.get_text(strip=True)
            if text:
                main_paragraphs.append(text)
    
    return "\n\n".join(main_paragraphs)


def process_table(table_element):
    # Process table elements and convert them to text
    table_text = ""
    rows = table_element.find_all('tr')
    for row in rows:
        cells = row.find_all(['td', 'th'])
        row_text = ""
        for cell in cells:
            cell_text = cell.get_text(strip=True)
            row_text += cell_text + "\t"
        # Remove trailing tab and add a newline
        row_text = row_text.rstrip('\t') + "\n"
        table_text += row_text
    
    return table_text