from openai import OpenAI, AuthenticationError, RateLimitError, OpenAIError
from telegram import File
import whisper
import tempfile
from io import BytesIO
import PyPDF2
from pydantic import BaseModel, Field
from settings import OPENAI_API_KEY
import logging

logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)
whisper_model = whisper.load_model("tiny")

class WeatherResponse(BaseModel):
    """Model format for the weather response."""
    weather_general_analisis: str = Field(..., description="Análisis general del clima.")
    clothes_recomendation: str = Field(..., description="Sugerencias sobre qué ropa usar.")
    recommended_activities: str = Field(..., description="Actividades recomendadas considerando el clima actual.")

def ask_openai_with_format(prompt: str, role:str, temp:float=0.5, output_format=None):
    """Ask OpenAI with a specific prompt, role and output format.
    Returns the response from OpenAI."""
    try:
        response = client.beta.chat.completions.parse(
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text":role
                        }
                    ],                    
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                },
            ],
            model="gpt-4o-mini",
            max_completion_tokens=300,
            temperature=temp,
            response_format=output_format
        )

        return response.choices[0].message.parsed
    
    except AuthenticationError:
        logger.error("Error de autenticación: Verifica tu API Key de OpenAI.")
        return "Hubo un problema con la autenticación del servicio de análisis. Inténtalo más tarde."

    except RateLimitError:
        logger.warning("Se ha superado el límite de uso de OpenAI.")
        return "El servicio de análisis está temporalmente sobrecargado. Intenta más tarde."

    except OpenAIError as e:
        logger.error(f"Error con OpenAI: {str(e)}")
        return "Ocurrió un error al procesar la solicitud de analisis. Intenta más tarde."

    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return "Ocurrió un error inesperado. Intenta más tarde."

def ask_openai(prompt: str, role: str, temp:float=0.5) -> str:
    """Ask OpenAI with a specific role and prompt.
    Returns the response from OpenAI."""

    try:
        response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text":role
                            }
                        ],                    
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    },
                ],
                model="gpt-4o-mini",
                max_completion_tokens=300,
                temperature=temp
            )
            
        return response.choices[0].message.content
    
    except AuthenticationError:
        logger.error("Error de autenticación: Verifica tu API Key de OpenAI.")
        return "Hubo un problema con la autenticación del servicio de análisis. Inténtalo más tarde."

    except RateLimitError:
        logger.warning("Se ha superado el límite de uso de OpenAI.")
        return "El servicio de análisis está temporalmente sobrecargado. Intenta más tarde."

    except OpenAIError as e:
        logger.error(f"Error con OpenAI: {str(e)}")
        return "Ocurrió un error al procesar la solicitud de analisis. Intenta más tarde."

    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return "Ocurrió un error inesperado. Intenta más tarde."

def analize_conversation(conversation: str) -> str:
    """Analize a conversation using OpenAI.
    returns a string with the analisis from OpenAI."""
    if not conversation:
        return "¡No puedo analizar una conversación vacía!"
    
    prompt = f'''Analiza la siguiente conversación y responde en **máximo 5 oraciones**.
            Clasifica el sentimiento como positivo, negativo o neutral y explica **brevemente** tu elección:
            \n{conversation}\n'''
    
    role = '''Eres un psicólogo especializado en análisis de sentimientos, te destacas por tu gran capacidad de análisis. 
    Tu objetivo es analizar conversaciones entre usuarios y dar un diagnóstico de la situación.'''
    
    return ask_openai(prompt, role)

def generate_outfit_images(base_recomendation: str, num_options: int = 1) -> list:
    """Generate outfit images based on the weather information.
    Returns a list with the URLs of the generated images
    """
    
    prompt = f'''
    [ITS PROHIBITED SHOWING HUMANS] Create a professional empty garment product photography, no humans or mannequins, 
    strict clothing-only display based on this recommendations: {base_recomendation}

    Technical Specifications:
    - Clothing display: Floating levitation effect against light grey background OR flat lay arrangement on neutral table surface
    - Detail requirements: High-resolution textile texture visibility, accessory close-ups
    - Lighting: Studio-quality softbox illumination with subtle shadow definition
    - Style: Hyper-realistic e-commerce product photography
    - Prohibited elements: Human figures, facial features, body parts, silhouettes, or any anthropomorphic shapes

    DO NOT SHOW: People, models, mannequins, or any human-like forms. ONLY DISPLAY CLOTHING ITEMS.'''
    
    response = client.images.generate(
        prompt=prompt,
        n=num_options,
        size="512x512"    
    )
    
    image_urls = [item.url for item in response.data]
    return image_urls

def get_weather_analisis_openai(weather_info: dict) -> dict:
    """Obtiene un análisis del clima y recomendaciones basadas en la ciudad y el clima."""
    
    city = weather_info.get("name", "")
    country = weather_info.get("sys", {}).get("country", "")

    prompt = f'''Analiza la siguiente información del clima en {city} - {country} y responde en **máximo 5 oraciones**:
    
    Clima actual:
    - **Temperatura**: {weather_info.get("main", {}).get("temp", "")}°C se siente como {weather_info.get("main", {}).get("feels_like", "")}°C
    - **Humedad**: {weather_info.get("main", {}).get("humidity", "")}%
    - **Viento**: {weather_info.get("wind", {}).get("speed", "")} km/h
    - **Nubosidad**: {weather_info.get("clouds", {}).get("all", "")}%
    - **Descripción**: {weather_info.get("weather", [{}])[0].get("description", "")}
    - **Visibilidad**: {weather_info.get("visibility", "")} m

    Basado en esta información, proporciona:
    1. Un análisis general del clima.
    2. Recomendaciones sobre qué ropa usar.
    3. **Actividades recomendadas específicas para {city} - {country}**, considerando la información proporcionada del clima actual.
    
    Si el clima no es adecuado para actividades al aire libre, sugiere alternativas en interiores.'''
    
    role = '''Eres un meteorólogo experto y guía turístico. Tu tarea es analizar el clima de una ciudad específica 
    y proporcionar recomendaciones personalizadas. Considera actividades comunes en la ciudad y cómo el clima afecta 
    esas actividades para sugerir las mejores opciones.'''

    return ask_openai_with_format(prompt, role, output_format=WeatherResponse)

async def summarize_audio(audio:File, extension:str)->str:
    """Summarize an audio file using OpenAI.
    Returns a string with the summary."""

    transcription = ''
    try:
        with tempfile.NamedTemporaryFile(delete=True, suffix=extension) as temp_audio:
            await audio.download_to_drive(temp_audio.name)

            result = whisper_model.transcribe(temp_audio.name)
            transcription = result.get("text","")

        if not transcription:
            return "No se pudo procesar el audio. Inténtalo de nuevo."
        
        prompt = f'Resumir el siguiente audio en **no más de 5 oraciones**:\n\n{transcription}'
        role = f'Eres un asistente que resume contenido de manera concisa.'

        return ask_openai(prompt, role, temp=0.3)
    
    except Exception as e:
        logger.error(f"Error al procesar el audio: {str(e)}")
        return "Ocurrió un error al procesar el audio. Inténtalo de nuevo."
    
async def summarize_pdf(pdf:File)->str:
    """Summarize a PDF file (MAX 4 PAGES)
    Returns a string with the summary"""

    text = ""
    with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as tmp:
        await pdf.download_to_drive(tmp.name)
        
        with open(tmp.name, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            if len(reader.pages) > 4:
                return "El pdf es muy grande, por favor intenta con un PDF más chico (El actual PDF tiene más de 4 páginas)"
            
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    
    if not text:
        return "No se pudo extraer texto del PDF. Asegúrate de que el PDF contenga texto seleccionable."

    chunks = [text[i:i+3500] for i in range(0, len(text), 3500)]

    prompt = '''Resume el siguiente texto en máximo 5 oraciones, devuelve el texto como si estuvieras contando el resumen del PDF a una persona y
    usa formato Markdown con títulos y listas si es necesario:\n\n{}'''
    role = "Eres un asistente que resume documentos PDF de forma clara y concisa."

    summaries = [ask_openai(prompt.format(chunk), role, temp=0.5) for chunk in chunks]
    
    final_summary = " ".join(summaries)
    return final_summary

def convert_text_to_audio(text:str) -> BytesIO:
    """Convert text to audio using a text-to-speech service.
    Returns the audio file."""
    
    response = client.audio.speech.create(
        model="tts-1",
        input=text,
        voice="nova",
        response_format='mp3',
        speed=1.25
    )
    audio_bytes = BytesIO(response.content)
    audio_bytes.name = "summary.mp3"
    return audio_bytes
