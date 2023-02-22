import configparser

def generate_settings():
    """
    Generates setting for all of the chat properties.
    """

    # Create a config parser object
    config_file = configparser.ConfigParser()

    # Database Settings section
    config_file['Database Settings']={
        'database_name': 'chat.db',
        'table_name': 'chat',
        'clear_db': 'True',
        'first_run': 'True'
    }

    # Gpt3 Settings section
    config_file['Gpt3 Settings'] = {
        'api_key_path': 'api_key.txt',
        'temperature': '0.3',
        'max_tokens': '4090'
    }

    # PDF Generator Settings section
    config_file['PDF Generator Settings'] = {
        'pdf_name': 'output/chat_results.pdf',
        'document_title': 'Chat Results',
        'title': 'Chat Results',
        'encryption': 'False',
        'password': 'password',
    }

    # Commit and push
    with open(r"settings/config.ini", "w") as file:
        config_file.write(file)
        file.flush()
        file.close()

    print("Config file created successfully")