import configparser

# Create a config parser object
config_file = configparser.ConfigParser()


# Add Database Settings section to the config file
config_file.add_section('Database Settings')
# Add settings to the section
config_file.set('Database Settings', 'database_name', 'chat.db')
config_file.set('Database Settings', 'table_name', 'chat')
config_file.set('Database Settings', 'clear_db','True')

# Add Gpt3 Settings section to the config file
config_file.add_section('Gpt3 Settings')
# Add settings to the section
config_file.set('Gpt3 Settings', 'api_key_path', 'api_key.txt')
config_file.set('Gpt3 Settings', 'temperature', '0.3')

# Commit and push
with open(r"settings/config.ini", "w") as file:
    config_file.write(file)
    file.flush()
    file.close()

print("Config file created successfully")