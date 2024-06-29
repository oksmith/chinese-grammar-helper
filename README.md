# chinese-grammar-helper

A GenAI application to explain Chinese grammatical structures and help point me to relevant pages to understand my Chinese mistakes and uncertainties.

* TODO: add a demonstration gif or something
* TODO: turn main.py into a proper command line tool
* TODO: proper logging

## Tech stack

* OpenAI `gpt-3.5-turbo-1106` for the LLM
* OpenAI `text-embedding-ada-002` for the text embeddings
* DataStax [Astra](https://astra.datastax.com/) database for vector store

## Setup

### Setting up API keys

Create an account and an API key here: https://platform.openai.com/api-keys

Then populate it in your `.env` file. An example of what the `.env` file should look like is in `t.env.dist`.

### Setting up vector database

Create new vector database with Astra, and put the relevant endpoint and token in `.env` as above.

### Fetching data
There are two ways to get data.

#### 1. Scraping website data from allsetlearning
This is a Chinese grammar wiki I have frequently found to be incredibly useful in my language learning journey.
```
python ./src/data/fetch_data.py
```

#### 2. Chinese grammar PDF download
This dataset is currently not used in the project but it could be extended to include it in the future.
```
curl https://www.kinezika.com/pdf/ModernMandarinChineseGrammar_Textbook.pdf -o data/chinese_grammar_textbook/ModernMandarinChineseGrammar_Textbook.pdf
```

## Future improvements

* Improve web scraping functionality when fetching data. More data sources to add to the vector store?
* Extend the application so that when I type in a subtly incorrect sentence, the model is able to notice
  my mistake, correct it to something more natural, and link to the relevant grammar URL to help me
  improve