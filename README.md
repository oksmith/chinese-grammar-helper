# zhongwen-llm

An application to help me understand mistakes in my Chinese sentences.

## Setting up API key

Create an account and an API key here: https://platform.openai.com/api-keys

Then populate it in your `.env` file. An example of what the `.env` file should look like is in `t.env.dist`.


## Fetching data
There are two ways to get data. TODO: decide which one I want to keep.

### 1. Scraping website data from allsetlearning.
```
zhongwen-llm % python ./src/data/fetch_data.py
```

### 2. Chinese grammar PDF download:
```
curl https://www.kinezika.com/pdf/ModernMandarinChineseGrammar_Textbook.pdf -o data/chinese_grammar_textbook/ModernMandarinChineseGrammar_Textbook.pdf
```
