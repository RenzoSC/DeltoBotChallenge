# DeltoBotChallenge
Technical challenge Delto

### Configuration
You will need:
- An OpenAI APIKEY, you can get one from here: [`OpenAI`](https://platform.openai.com/api-keys)
- An OpenWeatherMap APIKEY, you can get one from here: [`OpenWeatherMapAPI`](https://openweathermap.org/api)
- A TelegramBot Token, you can get one following the next instructions: [`TelegramBot`](https://core.telegram.org/bots#how-do-i-create-a-bot)
- If you want to get notifications of the error in your chat with the bot you may need your CHAT_ID with the bot

After having all these, create a settings_local.py file with these variables 

```python
TELEGRAM_BOT_TOKEN=''
OPENWEATHER_API_KEY=''
MAGICLOOP_WEATHER_FUNCTION_KEY=''
OPENAI_API_KEY=''
DEVELOPER_CHAT_ID=''
```

### Installation

This project requires Python 3.10 or higher.

Create a virtual enviornment:
```bash
python -m venv venv
```

Activate the virtual environment:
```bash
source venv/bin/activate
```

To install the dependencies, run:
```bash
pip install -r requirements.txt
```

Also to use whisper library you need to install the command-line tool [`ffmpeg`](https://ffmpeg.org/) 

```bash
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

You may need [`rust`](http://rust-lang.org) installed as well, in case [tiktoken](https://github.com/openai/tiktoken) does not provide a pre-built wheel for your platform. If you see installation errors during the `pip install` command above, please follow the [Getting started page](https://www.rust-lang.org/learn/get-started) to install Rust development environment. Additionally, you may need to configure the `PATH` environment variable, e.g. `export PATH="$HOME/.cargo/bin:$PATH"`. If the installation fails with `No module named 'setuptools_rust'`, you need to install `setuptools_rust`, e.g. by running:

```bash
pip install setuptools-rust
```

### Usage

To start the project, run:
```bash
python main.py
```

### Testing

To run tests, use:
```bash
pytest
```

### Project Main Structure

The project is organized as follows:

```
DeltoBotChallenge/
├── bot/                    # Source code files
│   ├── commands/           # Main commands of the bot
│   ├── flows/              # Main command flows of the bot
│   └── handlers/           # Bot conversation handlers
│   └── services/           # Modules that interact with external services
├── db/                     # DB files
│   ├── connection.py       # Functions to interact with DB tables
│   ├── main.py             # Initialization of DB 
│   └── tables.py           # Definition of DB tables
├── tests/                  # Unit tests
│   ├── commands/           # Tests for command modules
│   ├── database/           # Tests for database modules 
│   ├── flows/              # Tests for flow modules
│   └── helpers.py          # Helper module for testing
├── .gitignore              # Git ignore file
├── README.md               # Project README file
├── requirements.txt        # Python dependencies
├── settings_local.py       # Store private variables (acts like a .env file)
└── settings.py             # Global variables


```

This structure helps in maintaining a clean and organized codebase, making it easier to navigate and manage.

### Free funcionality explanation (EN)

The bot now includes the `/resume` command, which allows users to summarize either an audio file or a PDF document. This idea arose from personal experience: when receiving very long audio messages (exceeding a minute), it can feel tedious to listen to them entirely. With this command, users can send the audio to the bot and receive a summarized version of its content, eliminating the need to listen to the full recording. Additionally, users can choose to receive the summary as text or as an audio file.

For PDF files, the functionality works similarly. This could be useful for summarizing short contracts, academic documents or even technical challenges from an enterprise...

As extra functionality, it was added that when obtaining the climate analysis of the requested city, the bot sends images of the clothes recommended to use. I love having options of what clothes to wear, I think this feature could be useful for people who are interested in 'fashion'. As a clarification, this service is limited to two uses per day, otherwise it consumes all my OpenAI credits :(

### Possible improvements

Improvements that I think that it could be made to the bot
- When the users request the weather for a city, should be used OpenAI to try to convert the input in a valid city, since for example if you request **Iguazú** it returns that the city is invalid due to the correct name is **Puerto Iguazú**, in this way we will avoid the bad experience from the user. This could be done by adding a prompt to OpenAI ot the use of a MagicLoops's endpoint.
- Clearer generation of clothing images, this in any case depends a lot on the model being used, in this case it could be improved by using a model specifically trained for the generation of clothing images. In any case, the current implementation is made to test the use of an image generator.
- Aesthetics enhancement, the aesthetics of the bot's responses could be improved by adding more emojis or using a markdown or html format.