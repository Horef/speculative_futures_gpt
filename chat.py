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
        self.temperature = float(config.get("Gpt3 Settings", "temperature"))
        self.api_key_path = config.get("Gpt3 Settings", "api_key_path")

        self.db = dbm()

    def generate_future(self, past: str, present: str):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self.generate_prompt_multiple(past=past, present=present),
            temperature=self.temperature,
        )
        return response.choices[0].text.strip()

    def generate_prompt_single(self, present: str):
        return f"""
        Summarize the following text into a coherent story, but add as little information as possible.
        
        Text A: We have certain problems with our social norms and as a solution I would propose gradually lowering the confines imposed upon the moral values of the population.
        Summarization: A possible solution to problems with social norms would be to gradually lower the confines imposed upon the moral values of the population.
        Text A: {present}
        Summarization:
        """

    def generate_prompt_multiple(self, past, present):
        if past is None:
            return self.generate_prompt_single(present)
        return f"""
        Summarize the following two texts into a coherent story, but add as little information as possible.
        
        Text A: We have certain problems with our social norms and as a solution I would propose gradually lowering the confines imposed upon the moral values of the population.
        Text B: I would suggest we start by slowly changing the way we teach our children about the world, and only then to lowering the confines.
        Summarization: A possible solution to problems with social norms would be to start by changing the educational system, and then gradually lower the confines imposed upon the moral values of the population.
        Text A: {past}
        Text B: {present}
        Summarization:
        """

if __name__ == "__main__":
    chat = Chat()

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