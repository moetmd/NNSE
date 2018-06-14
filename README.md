# NNSE - NXU News Search Engine
A Tiny Search Engine for NXU News
include Spider & Web


# Require
* Python = 3.6 
* Flask  = 0.12
* Flask-WTF = 0.14
* Scrapy = 1.3
* Jieba = 0.39

# How to Lunch
1.
> spider under folder nnse

>cd to /nnse and run scrapy crawl nnspider

>the news will be saved in /origin_text as .txt files
2.
>then run 

> word_cut() & word_to_vec()

>functions will be found in jieba_process.py
3.
>run nnse_webapp.py to lunch web server

>and the search engine in your web browser could work!
