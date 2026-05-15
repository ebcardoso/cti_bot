import time
import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from date_utils import should_send_ticket

# Carregando as variáveis de ambiente
env = open('.env', 'r')
token = env.readline().strip()
username = env.readline().strip()
password = env.readline().strip()

bot = telebot.TeleBot(token)

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

# /ocupacao
@bot.message_handler(['ocupacao'])
def ocupacao(msg:telebot.types.Message):
    message_await = bot.reply_to(msg, "Aguarde enquanto buscamos as informações...")

    # Instância do navegador
    driver = webdriver.Chrome()

    try:
        driver.get("https://suap.ifrn.edu.br/accounts/login/")

        # Preenche os campos do login
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)

        time.sleep(1)

        # Clica no botão de login
        btn = driver.find_element(By.CLASS_NAME, "success")
        btn.click()
        time.sleep(4)

        # Acessa a área de atendentes
        driver.get("https://suap.ifrn.edu.br/centralservicos/relatorio_atendentes/?grupo_atendimento=30&uo=&atendentes_form=Aguarde...")

        # Obtendo o html da página
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Obtendo os cards dos atendentes
        people_scrap = soup.find_all('div', class_='card')

        people_list = []
        for p in people_scrap:
            # Obtendo o nome
            name_content = p.find('h4').get_text().split()
            name = f"{name_content[0]} {name_content[-1]}"

            # Obtendo o número de chamados
            number_current_tickets = "0" # por default
            number_content = p.find('a')
            if (number_content != None):
                number_content = number_content.get_text().split()
                number_current_tickets = number_content[0]

            people_list.append({
                "name": name,
                "number_of_tickets": number_current_tickets
            })

        # Montar a resposta parao chat
        response = "Número de chamados em atendimento:"
        for pl in people_list:
            response = response+f"\n- {pl['name']}: {pl['number_of_tickets']}"
        bot.send_message(msg.chat.id, response)
    except:
        print("Erro ao buscar informações.")
    finally:
        bot.delete_message(msg.chat.id, message_await.message_id)
        driver.quit()

bot.infinity_polling()