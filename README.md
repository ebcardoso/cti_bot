
# CTI BOT

Bot para acompanhar os chamados da CTI no Telegram.

# Requisitos

```
# python local environment
python3 -m venv local_env
source local_env/bin/activate

# required libraries
pip3 install selenium beautifulsoup4 telebot
```

# Comandos
- **/start** - Cadastrar-se no bot.
- **/desinscrever** - Desinscrever-se do bot.
- **/chamados** - Receber novos chamados via telegram.
- **/importar <id-chamado>** - Importar um chamado a partir do seu ID.
