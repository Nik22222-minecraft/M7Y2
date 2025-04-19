import telebot
import requests  
from PIL import Image
import io
import os  
from logic import detect_pet  

TOKEN = "Твой токен"

bot = telebot.TeleBot(TOKEN)

# База знаний об уходе за животными (пример, нужно будет расширить и улучшить)
CARE_TIPS = {
    "Кошка": "Кошкам нужен сбалансированный рацион, регулярная чистка лотка и игры. Не забывайте про когтеточку!",
    "Собака": "Собакам нужны регулярные прогулки, дрессировка и внимание. Выбирайте корм, подходящий для возраста и породы вашей собаки.",
    "Попугай": "Попугаям нужна просторная клетка, свежие фрукты и овощи, а также общение. Обеспечьте попугаю возможность грызть предметы.",
    "Черепаха": "Черепахам нужен террариум с ультрафиолетовой лампой и зоной для купания. Кормите черепаху сбалансированным кормом и регулярно чистите террариум."
}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне фотографию питомца, и я расскажу, как за ним ухаживать.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Получаем информацию о фотографии
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        image_path = "temp_image.jpg"  
        with open(image_path, "wb") as f:
            f.write(downloaded_file)

        
        prediction = detect_pet(image_path)

        
        os.remove(image_path)

        if prediction is not None:
            
            animal_name = prediction

            
            care_tips = CARE_TIPS.get(animal_name, "К сожалению, у меня пока нет информации об уходе за этим животным.")

            
            bot.reply_to(message, f"На фотографии {animal_name}.\n\nСоветы по уходу:\n{care_tips}")
        else:
            bot.reply_to(message, "К сожалению, не удалось распознать животное. Попробуйте другую фотографию.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        bot.reply_to(message, "Произошла ошибка при обработке фотографии. Попробуйте еще раз.")

bot.infinity_polling()
