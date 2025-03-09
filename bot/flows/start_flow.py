from telegram.ext import (ContextTypes, ConversationHandler)
from telegram import Update, ReplyKeyboardMarkup
from settings import MENU, WEATHER, ANALIZE_CONVERSATION, CLOTH_RECOMENDATIONS
from db.connection import add_count_to_user, reached_cloth_generation_limit, add_count_cloth_generation
from bot.utils.openweather import get_weather
from bot.utils.magicloop import get_weather_analisis
from bot.utils.openai import analize_conversation, get_weather_analisis_openai, generate_outfit_images, WeatherResponse
from settings import MAX_CLOTH_GENERATION_USES

import logging

logger = logging.getLogger(__name__) 

async def menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Intermediate state that will handle the user's choice and return the next state."""
    logger.info("menu_choice")

    choice = update.message.text

    if choice == '¡Quiero saber el clima!':
        await update.message.reply_text("Has elegido conocer el clima. Por favor, ingresa el nombre de la ciudad:")
        return WEATHER
    
    elif choice == '¡Quiero contar!':
        
        await count_option(update, context)

        return ConversationHandler.END
    
    elif choice == '¡Quiero analizar nuestra conversación!':
        await update.message.reply_text("Has elegido analizar una conversación. Por favor, envíame la conversación que deseas analizar.")
        return ANALIZE_CONVERSATION

    else:
        reply_keyboard = [['¡Quiero saber el clima!', '¡Quiero contar!', '¡Quiero analizar nuestra conversación!']]
        await update.message.reply_text(f"Opción no válida, por favor selecciona entre las siguientes opciones **{reply_keyboard[0][0]}**\n**{reply_keyboard[0][1]}**\n**{reply_keyboard[0][2]}**",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
        
        return MENU
    
async def weather_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Weather flow where user asks for a city and the bot will move to the next state with the user input."""
    logger.info("weather_flow")

    city = update.message.text
    weather_response = get_weather(city)
    if weather_response.get('cod', 400) != 200:
        await update.message.reply_text(f"Ha ocurrido un error al obtener el clima de la ciudad {city}, ¿Podrías asegurarte de haber solicitado una ciudad válida? Capaz el nombre está mal.")
    else:

        await update.message.reply_text("Aguarda un momento mientras analizamos el clima...")

        analisis:WeatherResponse = get_weather_analisis_openai(weather_response)
        analisis_text = f'''🌤️ **Análisis del clima en {city}**:\n{analisis.weather_general_analisis}
👖 **Recomendación de ropa**:\n{analisis.clothes_recomendation}\n🏃 **Actividades recomendadas:**\n{analisis.recommended_activities}'''

        await update.message.reply_text(analisis_text, parse_mode="Markdown")

        reply_keyboard = [['¡Si!', 'No gracias']]
        
        context.user_data['clothes_recomendation'] = analisis.clothes_recomendation

        await update.message.reply_text("¿Te gustaría que te demos unas imagenes de ideas para la ropa recomendada?", 
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))

    return CLOTH_RECOMENDATIONS

async def cloth_recommendation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cloth recommendation flow where user will receive outfit images if wanted."""
    logger.info("cloth_recommendation")
    user_id = update.effective_user.id
    choice = update.message.text
    if choice == '¡Si!':

        reached = reached_cloth_generation_limit(user_id=user_id)
        if reached == -1:
            await update.message.reply_text("Ha ocurrido un error al verificar si has alcanzado el límite de generación de ropa.")
            return ConversationHandler.END
        
        elif reached == 1:
            await update.message.reply_text("❌ Has alcanzado el límite máximo de generaciones de imágenes por hoy. Vuelve mañana para más recomendaciones")
            return ConversationHandler.END
        
        await update.message.reply_text("Aquí tienes algunas ideas de ropa que podrías usar:")
        clothes_recommendation = context.user_data.get('clothes_recomendation', "Sin recomendación de ropa")[:1000]
        image_urls = generate_outfit_images(clothes_recommendation, num_options=2)

        for url in image_urls:
            await update.message.reply_photo(photo=url)

        actual_user_count = add_count_cloth_generation(user_id)
        
        if actual_user_count != -1:
            await update.message.reply_text(f"Tienes {MAX_CLOTH_GENERATION_USES-actual_user_count} generaciones de ropa restantes para hoy.")

        return ConversationHandler.END
    
    elif choice == 'No gracias':
        await update.message.reply_text("¡Gracias por usar DeltoBot! Esperamos haberte ayudado.")
        return ConversationHandler.END
    
    else:
        reply_keyboard = [['¡Si!', 'No gracias']]
        await update.message.reply_text("Opción no válida, por favor selecciona entre '¡Si!' o 'No gracias'.",
                                        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
        return CLOTH_RECOMENDATIONS

async def count_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Count option to be used in the menu."""
    logger.info("count_option")
    
    user_id = update.effective_user.id    
    actual_user_count = add_count_to_user(user_id)
    if actual_user_count == -1:
        await update.message.reply_text("Ha ocurrido un error al incrementar el contador.")
    else:
        await update.message.reply_text(f"Contador incrementado. Tu contador actual es: {actual_user_count}")
    return ConversationHandler.END

async def analize_conversation_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Analize conversation flow where user sends a conversation and the bot will use OpenAI to analize it."""
    logger.info("analize_conversation")

    conversation = update.message.text

    await update.message.reply_text("Aguarda un momento mientras analizamos la conversación...")

    response = analize_conversation(conversation)
    
    await update.message.reply_text(response)

    return ConversationHandler.END