import time
import telebot
from lib_sql_connection import LibSqlConnection
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

# Inicia o banco de dados
sql_connection = LibSqlConnection()

# Criando a instâcia do Bot
bot = telebot.TeleBot(token)
print("Bot Iniciado!")

# /start
@bot.message_handler(['start'])
def start(msg:telebot.types.Message):
    bot.reply_to(msg, "Bem Vindo ao bot da CTI/JC.")

    # Armazena o ID do novo usuário
    try:
        sql_connection.store_chat_id(msg.chat.id)
    except Exception as e:
        print(f"Error: {e}")

# /desinscrever
@bot.message_handler(['desinscrever'])
def desinscrever(msg:telebot.types.Message):
    # Deletar o id de quem se desinscreve do bot
    try:
        sql_connection.delete_chat_id(msg.chat.id)
    except Exception as e:
        print(f"Error: {e}")

# /chamados
@bot.message_handler(['chamados'])
def chamados(msg:telebot.types.Message):
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