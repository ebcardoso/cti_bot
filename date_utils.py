from datetime import datetime

# Converte a data no formato do SUAP em um datetime
def date_parser(date_str):
    months = {
        "Janeiro": "01",
        "Fevereiro": "02",
        "Março": "03",
        "Abril": "04",
        "Maio": "05",
        "Junho": "06",
        "Julho": "07",
        "Agosto": "08",
        "Setembro": "09",
        "Outubro": "10",
        "Novembro": "11",
        "Dezembro": "12"
    }

    day, _, month, _, year, _, timestamp = date_str.split()

    formatted_date = f"{day}/{months[month]}/{year} {timestamp}"
    formatted_datetime = datetime.strptime(formatted_date, "%d/%m/%Y %H:%M")
    return(formatted_datetime)

# Checa se a data do ticket é menos de 10 minutos que a hora atual
def should_send_ticket(ticket_date):
    difference = datetime.now() - date_parser(ticket_date)
    minutes = difference.total_seconds() / 60
    if (minutes <= 10):
        return(True)
    else:
        return(False)
