# chinese-grammar-helper

A GenAI application to explain Chinese grammatical structures and help point me to relevant pages to understand my Chinese mistakes and uncertainties.

## Example usage

![demo](./assets/demo.gif)

The app also provides the top 3 most relevant web pages allowing you to explore certain grammar points in more detail.

The script `grammar` was created to make running this helper easy. For example:
```
./grammar helper
./grammar updatedb
```

You can also call `main.py` directly if you prefer:
```
python main.py helper
python main.py updatedb
python main.py helper --updatedb
```

You may need to ensure the right Python environment is active. This project uses Poetry to manage the virtual environment. Just run `poetry shell` to enter the virtual environment!

## Tech stack

* OpenAI `gpt-3.5-turbo-1106` for the LLM
* OpenAI `text-embedding-ada-002` for the text embeddings
* [QDrant](https://qdrant.tech/) for the vector store

## Setup

1. Clone the repo, and make sure `poetry` is installed and Python 3.12 available.
2. Use the right version of Python and install the package dependencies into a virtual environment:
```
poetry env use python3.12
poetry install
```
3. Activate the virtual environment in a shell `poetry shell`. Now you can run all of the scripts in this repo with the correct virtual environment.

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
python ./src/data/scrape_data.py
```

#### 2. Chinese grammar PDF download
This dataset is currently not used in the project but I plan to extend the vector store to include it in the future.
```
curl https://www.kinezika.com/pdf/ModernMandarinChineseGrammar_Textbook.pdf -o data/chinese_grammar_textbook/ModernMandarinChineseGrammar_Textbook.pdf
```

## Future improvements

* Improve web scraping functionality when fetching data. More data sources to add to the vector store?
* Extend the application so that when I type in a subtly incorrect sentence, the model is able to notice
  my mistake, correct it to something more natural, and link to the relevant grammar URL to help me
  improve
* Package it up and release it to the wild
