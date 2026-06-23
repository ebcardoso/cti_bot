import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def op_importar(bot, msg, env_vars):
    print("-----Iniciando busca do chamado")

    # Instância do navegador
    driver = webdriver.Chrome()

    try:
        # Extraindo o número do ticket
        _, ticket_id = msg.text.split()

        driver.get("https://suap.ifrn.edu.br/accounts/login/")

        # Preenche os campos do login
        driver.find_element(By.NAME, "username").send_keys(env_vars["username"])
        driver.find_element(By.NAME, "password").send_keys(env_vars["password"])

        time.sleep(1)

        # Clica no botão de login
        btn = driver.find_element(By.CLASS_NAME, "success")
        btn.click()
        time.sleep(4)

        # Acessa a página do chamado
        driver.get("https://suap.ifrn.edu.br/centralservicos/chamado/"+ticket_id)

        # Obtendo o html da página
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        ticket = {
            "link": "https://suap.ifrn.edu.br/centralservicos/chamado/"+ticket_id,
        }
        
        #Obtendo o tipo
        ticket_type = soup.find("button", class_="accordion-button").get_text()
        ticket["type"] = ticket_type.lstrip().rstrip()

        #Obtendo a descrição
        div_description = soup.find("div", class_="flex-basis-100")
        description = div_description.find("dd").get_text()
        ticket["description"] = description
        
        #Obtendo o interessado
        opener = soup.find("a", class_="popup-user-trigger").get_text()
        ticket["opener"] = opener

        bot.send_message(msg.chat.id, "⚠️CHAMADO⚠️"+"\n\n- Tipo: "+ticket["type"]+".\n- Descrição: "+ticket["description"]+"\n\n- Interessado: "+ticket["opener"]+"\n\n"+ticket["link"])
        print("-----Verificação Concluída")
    except:
        print("-----Falha ao buscar o chamado")
    finally:
        driver.quit()
