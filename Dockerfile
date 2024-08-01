# Use uma imagem base do Selenium com Chrome
# OBS: Certifique-se que a versão do selenium e chrome webdriver estão com versões compativeis.
FROM selenium/standalone-chrome:114.0

# Instale o Python e ferramentas necessárias
USER root
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv wget unzip

# Crie e ative um ambiente virtual
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Instale o ChromeDriver compatível com a versão do Chrome instalada
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip -d /usr/local/bin/

# Configurações do diretório de trabalho
WORKDIR /app

# Copie o código da aplicação para o contêiner
COPY . .

# Instale as dependências Python no ambiente virtual
RUN pip install --no-cache-dir -r requirements.txt

# Comando para executar a aplicação
CMD ["python", "app.py"]
