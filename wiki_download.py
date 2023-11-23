import os
import csv
import requests
from urllib.parse import urlparse, unquote

def read_csv_files(folder_path, target_column):
    error_count = 0  

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    is_first_row = True
                    for row in csv_reader:
                        if is_first_row:
                            is_first_row = False
                            continue
                        if len(row) > target_column:
                            url = row[target_column]

                            parsed_url = urlparse(url)
                            path = parsed_url.path
                            decoded_path = unquote(path)

                            output = decoded_path.replace("/zh-tw/", "").replace("/", "_")
                            # print(output)
                            if not os.path.exists("html"):
                                os.makedirs("html")
                            if not os.path.exists("txt"):
                                os.makedirs("txt")
                            try:
                                response = requests.get(url)
                                response.raise_for_status()
                                with open(os.path.join("html", f"{output}.html"), "wb") as htmlFile:
                                    htmlFile.write(response.content)

                                from web_parse import extract_main_paragraphs

                                with open(os.path.join("html", f"{output}.html"), "r", encoding="utf-8") as htmlFile:
                                    extracted_text = extract_main_paragraphs(htmlFile.read())
                                    # if len(extracted_text) >= 1:
                                    with open(os.path.join("txt", f"{output}.txt"), "w", encoding="utf-8") as f:
                                        f.write(extracted_text)
                                        
                            except requests.exceptions.RequestException as e:
                                error_count += 1  
                                print(f'Error downloading {url}: {e}')
    
    print(f'All downloads completed. Error count: {error_count}')  

folder_path = 'output'
target_column = 2
read_csv_files(folder_path, target_column)