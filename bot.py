from config import bot, BOT_TOKEN
from modules.url_shortener import UrlShortener
from telebot.types import Message


shorten_active = False

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, '¡Hola! Soy Tiny Ameba Bot.')

@bot.message_handler(commands=['info'])
def info(message):
    bot.reply_to(message, """Tiny Ameba Bot fue creado por Ana, alias DreamDrop. 
    \nPuedes seguirla en Github:
    \nhttps://github.com/AnaSuarez180""")

#Modules
#URL shortener
@bot.message_handler(commands=['shorten'])
def activate_shorten(message: Message):
    """
    Activa el acortamiento de URL
    """
    global shorten_active
    shorten_active = True
    bot.reply_to(message, 'La función de acortamiento de URL ha sido activada. Envía una URL para acortarla.')

@bot.message_handler(commands=['stop'])
def deactivate_shorten(message: Message):
    """
    Desactiva el acortamiento de URLs
    """
    global shorten_active
    shorten_active = False
    bot.reply_to(message, 'Acortamiento de URLs desactivado.')

#Para que la función no esté activa todo el tiempo, se tiene que especificar dentro del handler que dependa del shorten_active
@bot.message_handler(func=lambda msg: msg.entities is not None and any(e.type == 'url' for e in msg.entities) and shorten_active)
def shorten_service(message: Message) -> None:
    
    global shorten_active
    url = message.text
    chat_id = message.chat.id

    if shorten_active:
        url_shortener = UrlShortener()
        services = ['tinyurl', 'clckru', 'chilpit', 'cuttly']
    
        for service in services:
            try:
                short_url = url_shortener.shorten_url(url, service)
                bot.reply_to(message, f'URL acortada con {service}:\n{short_url}')
                break
            except ValueError as e:
                print(e)
        else:
            bot.reply_to(message, 'No se pudo acortar la URL con ninguno de los servicios disponibles.')
    else:
        bot.reply_to(message, 'Lo siento, la función de acortar URLs está desactivada.')


@bot.message_handler(func=lambda msg: not shorten_active and msg.entities is not None and any(e.type == 'url' for e in msg.entities))
def inactive_shorten(message: Message):
    """
    Envía un error si la función de acortamiento de URL está desactivada.
    """
    bot.reply_to(message, 'La función de acortamiento de URL está desactivada. Para activarla, usa el comando /shorten.')


# Con esto se inicia el bot
if __name__ == '__main__':
    bot.polling(none_stop=True)
