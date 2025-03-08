from openai import OpenAI, AuthenticationError, RateLimitError, OpenAIError
from settings import OPENAI_API_KEY
import logging

logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)

def analize_conversation(conversation: str) -> str:
    """Analize a conversation using OpenAI.
    returns a string with the analisis from OpenAI."""

    prompt = f'''Analiza la siguiente conversación y responde en **máximo 3 oraciones**.
            Clasifica el sentimiento como positivo, negativo o neutral y explica **brevemente** tu elección:
            \n{conversation}\n'''

    try:
        response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text":'''Eres un psicólogo especializado en análisis de sentimientos, te destacas por tu gran capacidad de análisis. 
                                        Tu objetivo es analizar conversaciones entre usuarios y dar un diagnóstico de la situación.'''
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
