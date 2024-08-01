import smtplib
import email.message
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Função para configurar o driver do Selenium
def setup_selenium_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")  # Adicione este argumento para o modo headless
    options.add_argument("--disable-gpu")  # Adicione este argumento para desabilitar GPU
    options.add_argument("--remote-debugging-port=9222")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(options=options)


# Função para realizar login no Instagram
def login_to_instagram(driver, username, password):
    # Acessar a página inicial do Instagram
    driver.get("https://www.instagram.com/")
    time.sleep(10)  # Esperar 10 segundos para carregar tudo

    # Inserir o nome de usuário
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input"))
    )
    username_input.send_keys(username)

    # Inserir a senha
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input"))
    )
    password_input.send_keys(password)

    # Clicar no botão de login
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]"))
    )
    login_button.click()

    # Aguardar 15 segundos para o processo de login ser concluído
    time.sleep(15)

# Função para obter informações da página do perfil
def get_profile_info(driver):
    try:
        info_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul"))
        )
        return info_element.text
    except:
        return None

# Função para enviar o e-mail
def send_email(email_input, profile_info):
    corpo_email = f""" 
    <p>Dear User,</p>
    <p>Instagram Profile Information: {profile_info}</p>
    <p>If you need another kind of value you can ask on:</p>
    <p>https://www.linkedin.com/in/leandro-frco/</p>
    <p>Best Regards,</p>
    <p>Leandro Ramos</p>
    """

    msg = email.message.Message()
    msg['Subject'] = 'Instagram Profile Information Update'  # Assunto do E-mail
    msg['From'] = 'xxxxxxxxxx@gmail.com'  # E-mail que vai enviar
    msg['To'] = email_input
    password = 'xxxx xxxx xxxx xxxx'  # Senha para o "App passwords of Google"
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com:587')  # Configuração do SMTP
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    s.quit()

# Função principal
def main():
    # Nome de usuário e senha do Instagram
    instagram_username = "xxxxx"
    instagram_password = "xxxxx"  # Substitua pela senha correta
    email_input = "xxxxx@gmail.com"  # Substitua pelo e-mail correto

    driver = setup_selenium_driver()

    try:
        # Realizar login no Instagram
        login_to_instagram(driver, instagram_username, instagram_password)

        # Redirecionar para a página específica
        driver.get("https://www.instagram.com/xxxxxx") # Perfil a ser monitorado
        time.sleep(5)  # Aguardar 5 segundos para a página carregar completamente

        while True:
            # Obter informações da página do perfil
            profile_info = get_profile_info(driver)

            # Enviar e-mail se as informações do perfil forem encontradas
            if profile_info:
                send_email(email_input, profile_info)
                print(f"Sent email with Instagram profile information: {profile_info}")
            else:
                print("Profile info not found, continuing monitoring...")

            # Esperar 1 hora antes de executar novamente
            time.sleep(3600)

            # Atualizar a página
            driver.refresh()
            time.sleep(10)  # Esperar 10 segundos para carregar tudo novamente
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
