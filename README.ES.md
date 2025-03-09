# DeltoBotChallenge
Prueba técnica de Delto

### Configuration
Vas a necesitar:
- Una APIKEY de OpenAI, puedes obtener una aquí: [`OpenAI`](https://platform.openai.com/api-keys)
- Una APIKEY de OpenWeatherMap, puedes obtener una aquí: [`OpenWeatherMapAPI`](https://openweathermap.org/api)
- Un Token de TelegramBot, puedes obtener uno siguiendo las instrucciones: [`TelegramBot`](https://core.telegram.org/bots#how-do-i-create-a-bot)
- Si quieres que las notificaciones de error te lleguen a tu chat con el bot vas a necesitar obtener el CHAT_ID

Después de tener todo esto, crea un archivo settings_local.py con esas variables

```python
TELEGRAM_BOT_TOKEN=''
OPENWEATHER_API_KEY=''
MAGICLOOP_WEATHER_FUNCTION_KEY=''
OPENAI_API_KEY=''
DEVELOPER_CHAT_ID=''
```


### Intalacaión

Este proyecto requiere Python 3.10 o superior.

Crea un entorno virtual:
```bash
python -m venv venv
```

Activa el entorno virtual:
```bash
source venv/bin/activate
```

Para instalar las dependencias:
```bash
pip install -r requirements.txt
```

Además para usar la libería de `whisper` necesitas instalar la herramienta [`ffmpeg`](https://ffmpeg.org/) 

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

Es posible que necesites instalar [`rust`](http://rust-lang.org), en caso de que [tiktoken](https://github.com/openai/tiktoken) no provea una pre-built wheel para tu SO. Si ves errores de instalación durante la ejecución del comando `pip install` de abajo, por favor dirígete a [Getting started page](https://www.rust-lang.org/learn/get-started) para instalar el Entorno de desarrollo de Rust. Adicionalmente, necesitarás configurar la variable de entorno `PATH` -> `export PATH="$HOME/.cargo/bin:$PATH"`. Si la instalación falla con `No module named 'setuptools_rust'`, necesitas instalar `setuptools_rust`, ejecutando:

```bash
pip install setuptools-rust
```

### Uso

Para correr el proyecto:
```bash
python main.py
```

### Testing

Para correr los tests:
```bash
pytest
```

### Estructura principal del proyecto

El proyecto está organizado de la siguiente forma:

```
DeltoBotChallenge/
├── bot/                    # Source code files
│   ├── commands/           # Main commands of the bot
│   ├── flows/              # Main command flows of the bot
│   └── handlers/           # Bot conversation handlers
│   └── services/           # Modules that interact with external services
├── db/                     # DB modules
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

Esta estructura ayuda a mantener el código limpio y organizado, haciendolo más fácil de navegar y administrar.

### Explicación de la funcionalidad libre

Se le agregó al bot el comando `/resume` el cual le da como opciones al usuario resumir un audio o un documento PDF, esta idea surgio en base a que (al menos a mi) a veces me suelen mandar audios muy largos (superando el minuto), lo cual en ocasiones me genera mucha pereza escuchar, con este comando podría mandarle el audio al bot y este me generaría un resumen del contenido del audio y no tendría que escuchar el audio completo! Además me da la libertad de elegir obtener el resumen como texto o como audio.

En el caso de mandar un PDF la funcionalidad es la misma, esta podría servir para resumir contenidos como un contrato pequeño, un documento universitario o incluso, el challenge técnico de una empresa...

Como funcionalidad extra se agregó que en el momento de obtener el análisis del clima de la ciudad solicitada, se obtengan imagenes de la ropa recomendada a usar. A mi me encanta tener opciones de que ropa usar, creo que esta funcionalidad podría servirle a personas que les interesa 'la moda'. Como aclaración, este servicio está limitado a dos usos por día, porque sino me consume todos los créditos de OpenAI.

### Posibles mejoras

Mejoras que creo que se le podrían hacer al bot
- Cuando el usuario solicita el clima de una ciudad, se use OpenAI para intentar convertir el input en una ciudad válida, ya que po ejemplo si ingresas **Iguazú** no te lo toma como una ciudad válida ya que el nombre correcto sería **Puerto Iguazú**, de esta forma se evitaría la mala experiencia del usuario. Esto se podría agregar con un prompt a OpenAI o el uso de un endpoint de MagicLoops
- Generación de imagenes de la ropa más clara, esto de todas formas depende mucho del modelo que se está usando, dado el caso se podría mejorar usando algún modelo específicamente entrenado para la generación de imágenes de ropa. De todas formas la implementación actual está hecha a modo de probar el uso de un generador de imágenes.
- Estética, se podría mejorar la estética de las respuestas del bot agregando más emojis o usando un formato de markdown o html.