from openai import OpenAI, AuthenticationError, RateLimitError, OpenAIError
from settings import OPENAI_API_KEY
import logging

logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_openai_with_role(prompt: str, role: str) -> str:
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
                temperature=0.5,
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
    
    return ask_openai_with_role(prompt, role)

def get_weather_analisis_openai(weather_info: dict) -> str:
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

    return ask_openai_with_role(prompt, role)