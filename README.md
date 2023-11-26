# **Introduction**
此示範程式皆為Python
## download.py以及web_parse.py
1. 程式的相關資訊以及`download.py`中有需要更新`comcrawl`中的程式請參考:https://github.com/neil-zt/common-crawl-client/tree/main

2. 請將取得的程式更改
* download.py
```js
searching_uri = "www.cna.com.tw/news/afe/*"
```
```js
searching_uri_dir = searching_uri.replace("/", "-").replace("*", "-all")
```
更改為
```js
searching_uri = "https://zh.wikipedia.org/zh-tw/*"
```
```js
searching_uri_dir = searching_uri.replace("/", "-").replace(":", "-").replace("*", "-all")
```
刪除下列程式
```js
from web_parse import extract_main_paragraphs
for result in client.results:
    extracted_text = extract_main_paragraphs(result["html"])
    if len(extracted_text) < 100:
        continue
    with open(f"output/{time_code}/{searching_uri_dir}/{result['urlkey'].replace('/', '-')}.txt", "w") as f:
        f.write(extracted_text)
```
* web_parse.py
```js
from bs4 import BeautifulSoup

def extract_main_paragraphs(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    paragraphs = soup.find_all('p')
    
    main_paragraphs = []
    for paragraph in paragraphs:
        # Skip short UI phrases based on character count
        if len(paragraph.get_text(strip=True)) > 10:
            main_paragraphs.append(paragraph.get_text(strip=True))
    
    return "\n\n".join(main_paragraphs)
```
更改為
```js
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
```
## 使用方法
1. 請先使用`download.py`，並設定`time_code`。`time_code`可從Common Crawl的[官網列表](https://commoncrawl.org/get-started)獲得。最後會得到一個資料夾`output`，資料夾內會有數個CSV檔。
