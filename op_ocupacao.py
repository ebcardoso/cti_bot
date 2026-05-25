import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def op_ocupacao(bot, msg, credentials):
    message_await = bot.reply_to(msg, "Aguarde enquanto buscamos as informações...")
    print("-----Buscando ocupação do setor")

    # Instância do navegador
    driver = webdriver.Chrome()

    try:
        driver.get("https://suap.ifrn.edu.br/accounts/login/")
        
        driver.find_element(By.NAME, "username").send_keys(credentials["username"])
        driver.find_element(By.NAME, "password").send_keys(credentials["password"])

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
        
        print("-----Verificação finalizada")
    except:
        print("Erro ao buscar informações.")
    finally:
        bot.delete_message(msg.chat.id, message_await.message_id)
        driver.quit()