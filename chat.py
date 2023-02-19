from math import ceil

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

        self.completion_length = self.max_tokens

        self.db = dbm()

    def generate_future(self, past: str, present: str):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self.generate_prompt_multiple(past=past, present=present),
            temperature=self.temperature,
            max_tokens=self.completion_length,
        )
        return response.choices[0].text.strip()

    def generate_prompt_single(self, present: str):
        return f"""
        Summarize the following text into a clear idea. Try to be as specific and detailed as possible.
        
        Text: {present}.
        Answer:
        """

    def generate_prompt_multiple(self, past, present):
        if past is None:
            prompt = self.generate_prompt_single(present)
        else:
            prompt = f"""
            Combine the following two parts of a text into one clear idea.
            Try to be as specific and detailed as possible.
            Point out logical inconsistencies if such exist.

            Part A: {past}.
            Part B: {present}.
            Answer:
            """

        # Calculate the number of tokens we pass into the gpt.
        # The number is always bigger than the actual tokenization, but it doesn't return an error this way.
        tokens_by_chars: int = ceil(len(prompt)/4)

        self.completion_length = self.max_tokens - tokens_by_chars

        return prompt

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

        # Run GPT-3
        summarization = chat.generate_future(past=past, present=text)
        print(f"gpt3 returned: {summarization}")
        chat.db.insert_db(name="gpt3", text=tp.preprocess(summarization))

        print("\nHistory: ")
        history = chat.db.query_db()
        for (id, name, text, timestamp) in history:
            print(f"Id:{id}, time:{timestamp}, {name}: {text}")

        past = summarization
        name = input("\nName: ")