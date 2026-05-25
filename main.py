import time
import telebot
from op_chamados import op_chamados
from op_importar import op_importar
from op_ocupacao import op_ocupacao

# Carregando as variáveis de ambiente
env = open('.env', 'r')
token = env.readline().strip()
credentials = {
    "username": env.readline().strip(),
    "password": env.readline().strip()
}

# Criando a instâcia do Bot
bot = telebot.TeleBot(token)
print("Bot Iniciado!")

# /start
@bot.message_handler(['start'])
def start(msg:telebot.types.Message):
    bot.reply_to(msg, "Bem Vindo. Você receberá os novos chamados abertos para a CTI/JC.")

    op_chamados(bot, msg, credentials)

    while(True):
        time.sleep(600) # Nova verificação em 10 minutos
        op_chamados(bot, msg, credentials)

# /importar <numero-do-ticket>
@bot.message_handler(['importar'])
def importar(msg:telebot.types.Message):
    op_importar(bot, msg, credentials)

# /ocupacao
@bot.message_handler(['ocupacao'])
def ocupacao(msg:telebot.types.Message):
    op_ocupacao(bot, msg, credentials)

bot.infinity_polling()