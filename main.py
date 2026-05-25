import time
import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from date_utils import should_send_ticket
from op_importar import op_importar
from op_ocupacao import op_ocupacao

# Carregando as variáveis de ambiente
env = open('.env', 'r')
token = env.readline().strip()
username = env.readline().strip()
password = env.readline().strip()
credentials = {
    "username": username,
    "password": password
}

# Criando a instâcia do Bot
bot = telebot.TeleBot(token)
print("Bot Iniciado!")

# /start
@bot.message_handler(['start'])
def start(msg:telebot.types.Message):
    bot.reply_to(msg, "Bem Vindo. Você receberá os novos chamados abertos para a CTI/JC.")

    while(True):
        print("-----Iniciando Verificacao")
        driver = webdriver.Chrome()
        try:
            # Instância do navegador
            driver.get("https://suap.ifrn.edu.br/accounts/login/")

            # Preenche os campos do login
            driver.find_element(By.NAME, "username").send_keys(username)
            driver.find_element(By.NAME, "password").send_keys(password)

            time.sleep(1)

            # Clica no botão de login
            btn = driver.find_element(By.CLASS_NAME, "success")
            btn.click()
            time.sleep(10)

            # Acessa a área de chamados
            driver.get("https://suap.ifrn.edu.br/centralservicos/listar_chamados_suporte/")

            # Obtendo o html da página
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Obtendo os cards dos chamados
            tickets_scrap = soup.find_all('div', class_='general-box')

            # Imprimindo Log
            try:
                print("Chamados Analisados: "+str(len(tickets_scrap)))
            except:
                print("Chamados Analisados: ")

            # Separando os dados dos cards dos chamados
            tickets_list = []
            for ts in tickets_scrap:
                ticket = []
                ticket.append("https://suap.ifrn.edu.br"+ts.find('a').get('href'))
                ticket.append(ts.find('strong').get_text())
                ticket.append(ts.find('p').get_text())
                
                for ticket_data in ts.find_all('div', class_='list-item'):
                    ticket.append(ticket_data.find('dd').get_text())

                # Checagem da Data
                if (should_send_ticket(ticket[4])):
                    tickets_list.append({
                        "link": ticket[0],
                        "type": ticket[1],
                        "description": ticket[2],
                        "opener": ticket[3],
                        "opening_date": ticket[4],
                        "sla": ticket[5]
                    })

            for ticket in tickets_list:
                bot.send_message(msg.chat.id, "⚠️NOVO CHAMADO⚠️"+"\n\n- Tipo: "+ticket["type"]+".\n- Descrição: "+ticket["description"]+"\n\n- Interessado: "+ticket["opener"]+"\n- Data de Abertura: "+ticket["opening_date"]+"\n\n"+ticket["link"])

            # Imprimindo Log
            try:
                print("Chamados Enviados: "+str(len(tickets_list)))
            except:
                print("Chamados Enviados: ")

            print("-----Verificação Concluída")
        except:
            print("-----Falha ao Realizar Verificacao")
        finally:
            driver.quit()

        time.sleep(600) # Nova verificação em 10 minutos

# /importar <numero-do-ticket>
@bot.message_handler(['importar'])
def importar(msg:telebot.types.Message):
    op_importar(bot, msg, credentials)

# /ocupacao
@bot.message_handler(['ocupacao'])
def ocupacao(msg:telebot.types.Message):
    op_ocupacao(bot, msg, credentials)

bot.infinity_polling()