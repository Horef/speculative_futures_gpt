import sqlite3
from database import DatabaseManager as dbm
import text_processing as tp

import configparser

import openai

class Chat:
    def __init__(self):
        # Setting up the configurations.
        config = configparser.ConfigParser()
        config.read("settings/config.ini")

        # Loading the settings.
        self.temperature = config.getfloat("Gpt3 Settings", "temperature")
        self.api_key_path = config.get("Gpt3 Settings", "api_key_path")
        self.max_tokens = config.getint("Gpt3 Settings", "max_tokens")

        self.db = dbm()

    def generate_future(self, past: str, present: str):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self.generate_prompt_multiple(past=past, present=present),
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].text.strip()

    def generate_prompt_single(self, present: str):
        return f"""
        Summarize the following text into a concise idea, but try to keep as many specific names or details as possible.
        
        Text: {present}.
        Answer:
        """

    def generate_prompt_multiple(self, past, present):
        if past is None:
            return self.generate_prompt_single(present)
        return f"""
        Combine and summarize the following two parts of a text into one concise idea.
        But try to keep as many specific names or details as possible.
        Point out logical inconsistencies if such exist.

        Part A: {past}.
        Part B: {present}.
        Answer:
        """

if __name__ == "__main__":
    chat = Chat()

    if chat.db.clear:
        chat.db.clear_table()

    # Setting up the API key.
    openai.api_key_path = chat.api_key_path

    past = None

    name = input("Name: ")
    while name != "exit":
        text = input("Your opinion: ")
        chat.db.insert_db(name=name, text=tp.preprocess(text))
        print(f"Inserted into db: name:{name}, text:{text}")

        summarization = chat.generate_future(past=past, present=text)
        print(f"gpt3 returned: {summarization}")
        chat.db.insert_db(name="gpt3", text=tp.preprocess(summarization))

        print("\nHistory: ")
        history = chat.db.query_db()
        for (id, name, text, timestamp) in history:
            print(f"Id:{id}, time:{timestamp}, {name}: {text}")

        previous = summarization
        name = input("Name: ")