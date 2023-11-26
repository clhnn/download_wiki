# **Introduction**
此示範程式皆為Python
## download.py
程式內有需要更新comcrawl中的程式以及程式的相關資訊請參考:https://github.com/neil-zt/common-crawl-client/tree/main

請將從https://github.com/neil-zt/common-crawl-client/tree/main
取得的程式更改
\.```js
searching_uri = "www.cna.com.tw/news/afe/*"
```
```js
searching_uri_dir = searching_uri.replace("/", "-").replace("*", "-all")
```
改為
```js
searching_uri = "https://zh.wikipedia.org/zh-tw/*"
```
```js
searching_uri_dir = searching_uri.replace("/", "-").replace(":", "-").replace("*", "-all")
```
