import json
import requests
import random
import telebot
from telebot import types
from config import *

main_bot_token = main_token

monitoring_bot_token = monitor_token

main_bot = telebot.TeleBot(main_bot_token)
monitoring_bot = telebot.TeleBot(monitoring_bot_token)

# Simple logging function
def log(message):
    log_text = f"[{message.date}] {message.from_user.username}: {message.text}"
    print(log_text)
    monitoring_bot.send_message(chat_id , log_text)

@main_bot.message_handler(commands=['start'])
def start(message):
    log(message)
    username = message.from_user.username if message.from_user.username else "User"
    start_message = (
        f"👋 Hello {username}!\n\n"
        "This bot can generate realistic images from a text query or a photo using AI. Use the command /gen followed by your prompt. For example, /gen YourPromptHere 🙂\n\n"
        "If you're unsure what to generate, visit our channel for examples and enjoy ❤️\n\n"
        "Links to the channel are available via the buttons below 👇"
    )
    inline_keyboard = types.InlineKeyboardMarkup()
    channel_button = types.InlineKeyboardButton(text="Visit Channel", url="https://t.me/midjourneyArtwork89")
    inline_keyboard.add(channel_button)
    main_bot.send_message(message.chat.id, start_message, reply_markup=inline_keyboard)

@main_bot.message_handler(commands=['gen'])
def generate_image(message):
    log(message)
    try:
        if len(message.text.split()) > 1:
            main_bot.send_chat_action(message.chat.id, 'upload_photo')
            random_seed = random.randint(1, 10000000000000000)
            user_prompt = ' '.join(message.text.split()[1:])
            payload = {
                "prompt": user_prompt,
                "negative_prompt": "((close up)),(octane render, render, drawing, bad photo, bad photography:1.3), (worst quality, low quality, blurry:1.2), (bad teeth, deformed teeth, deformed lips), (bad anatomy, bad proportions:1.1), (deformed iris, deformed pupils), (deformed eyes, bad eyes), (deformed face, ugly face, bad face), (deformed hands, bad hands, fused fingers), morbid, mutilated, mutation, disfigured",
                "scheduler": "DPM++ SDE",
                "num_inference_steps": 10,
                "guidance_scale": 1,
                "samples": 1,
                "seed": random_seed,
                "img_width": 512,
                "img_height": 768,
                "base64": False
            }
            api_url = "https://api.segmind.com/v1/sdxl1.0-dreamshaper-lightning"
            headers = {
                "x-api-key": segmind_api_key,
                "Content-Type": "application/json"
            }
            response = requests.post(api_url, headers=headers, data=json.dumps(payload))
            model_info = response.headers.get('X-Model')
            caption = (
                f"Model: {model_info}\n"
                f"LoRa's: {response.headers.get('X-LoRas')}\n"
                f"Size: {payload['img_width']}x{payload['img_height']}\n"
                f"Steps: {payload['num_inference_steps']}\n"
                f"Sampler: {payload['scheduler']}\n"
                f"CFG: {payload['guidance_scale']}\n"
                f"Seed: {payload['seed']}"
            )
            main_bot.send_photo(message.chat.id, response.content, caption=caption, reply_to_message_id=message.message_id)
        else:
            main_bot.reply_to(message, "Please provide a prompt after the /gen command. For example, /gen YourPromptHere")
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        main_bot.reply_to(message, error_message)

@main_bot.message_handler(commands=['settings'])
def settings(message):
    log(message)
    # Implement settings functionality or provide information about available settings

@main_bot.message_handler(commands=['help'])
def help_command(message):
    log(message)
    # Provide information about available commands and how to use the bot

@main_bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    log(message)
    main_bot.reply_to(message, "➡️ Please provide a prompt after the /gen command. \n\n ➡️ For example, \n/gen YourPromptHere")

# Example function to send logs to the monitoring bot

@main_bot.message_handler(commands=['send_logs'])
def send_logs(message):
    log(message)
    # Fetch logs or any relevant information you want to send
    logs = "Some logs or monitoring data here..."
    monitoring_bot.send_message(chat_id, logs)

# Polling to keep both bots running
main_bot.polling()
monitoring_bot.polling()
