# zhongwen-llm


## Setting up API key

Create an account and an API key here: https://platform.openai.com/api-keys

Then populate it in your `.env` file. An example of what the `.env` file should look like is in `t.env.dist`.


## Fetching data
Scraping website data from allsetlearning.
```
zhongwen-llm % python ./src/data/fetch_data.py
```

Chinese grammar PDF download:
```
curl https://www.kinezika.com/pdf/ModernMandarinChineseGrammar_Textbook.pdf  -o data/chinese_grammar_textbook/ModernMandarinChineseGrammar_Textbook.pdf
```
