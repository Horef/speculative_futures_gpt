import sqlite3
import database as db
import text_processing as tp

import os
import openai

conn = sqlite3.connect("chat.db")
db.table_name = "chat"

openai.api_key_path = "api_key.txt"

def generate_future(text_a, text_b):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt_multiple(text_a=text_a, text_b=text_b),
        temperature=0.6,
    )
    return response.choices[0].text.strip()

def generate_prompt_single(text_a):
    return f"""
    Summarize the following text into a coherent story, but add as little information as possible.
    
    Text A: We have certain problems with our social norms and as a solution I would propose gradually lowering the confines imposed upon the moral values of the population.
    Summarization: A possible solution to problems with social norms would be to gradually lower the confines imposed upon the moral values of the population.
    Text A: {text_a}
    Summarization:
    """

def generate_prompt_multiple(text_a, text_b):
    if text_a is None:
        return generate_prompt_single(text_b)
    return f"""
    Summarize the following two texts into a coherent story, but add as little information as possible.
    
    Text A: We have certain problems with our social norms and as a solution I would propose gradually lowering the confines imposed upon the moral values of the population.
    Text B: I would suggest we start by slowly changing the way we teach our children about the world, and only then to lowering the confines.
    Summarization: A possible solution to problems with social norms would be to start by changing the educational system, and then gradually lower the confines imposed upon the moral values of the population.
    Text A: {text_a}
    Text B: {text_b}
    Summarization:
    """

if __name__ == "__main__":
    db.create_table(conn=conn)
    db.clear_table(conn=conn)

    name = input("Name: ")
    previous = None

    while name != "exit":
        text = input("Your opinion: ")
        print(f"Inserted into db: name:{name}, text:{text}")
        db.insert_db(conn=conn, name=name, text=tp.preprocess(text))

        summarization = generate_future(text_a=previous, text_b=text)
        print(f"gpt3 returned: {summarization}")
        db.insert_db(conn=conn, name="gpt3", text=tp.preprocess(summarization))

        print("History: ")
        history = db.query_db(conn=conn)
        for (id, name, text, timestamp) in history:
            print(f"Id:{id}, time:{timestamp}, {name}: {text}")

        previous = summarization
        name = input("Name: ")