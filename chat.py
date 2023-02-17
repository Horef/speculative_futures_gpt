import sqlite3
import database as db

import os
import openai

conn = sqlite3.connect("chat.db")
db.table_name = "chat"

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_future(text_a, text_b):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt_multiple(text_a=text_a, text_b=text_b),
        temperature=0.6,
    )
    return response.choices[0].text

def generate_prompt_single(text_a):
    return f"""
    Summarize the following text into a coherent story, but add as little information as possible.
    
    Text A: We have certain problems with our social norms and as a solution I would propose gradually lowering the confines imposed upon the moral values of the population.
    Summarization: A possible solution to problems with social norms would be to gradually lower the confines imposed upon the moral values of the population.
    Text A: {text_a}
    Summarization:
    """

def generate_prompt_multiple(text_a, text_b):
    return f"""
    Summarize the following two texts into a coherent story, but add as little information as possible.
    
    Text A: We have certain problems with our social norms and as a solution I would propose gradually lowering the confines imposed upon the moral values of the population.
    Text B: I would suggest we start by slowly changing the way we teach our children about the world, and only then to lowering the confines.
    Summarization: A possible solution to problems with social norms would be to start by changing the educational system, and then gradually lower the confines imposed upon the moral values of the population.
    Text A: {text_a}
    Text B: {text_b}
    Summarization:
    """