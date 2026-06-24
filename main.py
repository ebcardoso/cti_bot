import time
import telebot
from lib_sql_connection import LibSqlConnection
from selenium.webdriver.chrome.options import Options
from op_chamados import op_chamados
from op_importar import op_importar
from op_ocupacao import op_ocupacao

# Carregando as variáveis de ambiente
env = open('.env', 'r')
env_vars = {
    "token": env.readline().strip(),
    "username": env.readline().strip(),
    "password": env.readline().strip()
}

# Inicia o banco de dados
sql_connection = LibSqlConnection()

# Instanciando o options do chrome
chrome_options = Options()
chrome_options.add_argument("headless")
chrome_options.add_argument("no-sandbox")
chrome_options.add_argument("disable-dev-shm-usage")
chrome_options.add_argument("disable-gpu")  

# Criando a instâcia do Bot
bot = telebot.TeleBot(env_vars["token"])
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
    op_chamados(bot, msg, env_vars, chrome_options)

    while(True):
        time.sleep(600) # Nova verificação em 10 minutos
        op_chamados(bot, msg, env_vars, chrome_options)

# /importar <numero-do-ticket>
@bot.message_handler(['importar'])
def importar(msg:telebot.types.Message):
    op_importar(bot, msg, env_vars, chrome_options)

# /ocupacao
@bot.message_handler(['ocupacao'])
def ocupacao(msg:telebot.types.Message):
    op_ocupacao(bot, msg, env_vars, chrome_options)

bot.infinity_polling()
