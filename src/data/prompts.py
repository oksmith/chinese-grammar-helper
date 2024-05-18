from llama_index import PromptTemplate

new_prompt = PromptTemplate(
    """
    You're working with a textbook which teaches students who are learning
    Chinese how the grammar works.
    If you see that a piece of Chinese text is written incorrectly, look for the
    right section in the textbook when correcting it.

    Question: {question}
    """
)