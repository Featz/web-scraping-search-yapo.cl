from requests import get
from bs4 import BeautifulSoup
from smtplib import SMTP
from time import sleep
from datetime import date

def get_soup(url):
	headers = {"User-Agent":"Chrome/39.0.2171.95"}
	response = get(url, headers=headers)
	soup = BeautifulSoup(response.text, 'lxml')
	return soup

def format_price(price):
	return int(price[1:8].replace('.',''))

def send_mail(body):
	server = SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('from_mail@gmail.com', 'dosmtdvgiblpbslf')
	
	subjet = f'Nuevos Tucson en venta'
	msg = f'Subject: {subjet} ({date.today()})\n\n{body}'\

	server.sendmail('from_mail@gmail.com', 'to_mail@gmail.com', msg)
	print('Correo Enviado')
	server.quit()

# Yapo.cl search
def get_list():
	url = 'https://www.yapo.cl/chile/autos?ca=15_s&l=0&q=tucson&cmn=&st=s&br=40&rs=2016&fu=4&gb=1'
	soup = get_soup(url)
	body = ""
	for tr in soup.find_all('tr', class_="ad listing_thumbs"):
		if tr.find('td', class_='listing_thumbs_date').span.text.strip() == 'Hoy':
			tr_id = tr.get('id')
			link = tr.find('td', class_='listing_thumbs_date').a.get('href')
			titulo = tr.find('td', class_='thumbs_subject').a.text.strip()
			precio = tr.find('td', class_='thumbs_subject').span.text.strip()
			print(f"ID: {tr_id}")
			print(f"Link: {link}")
			print(f"Titulo: {titulo}")
			print(f"Precio: {precio}")
			body = body + f"Titulo: {titulo}\t Precio: {precio}\nLink: {link}\n\n"
	if body == "":
		send_mail("No hay nuevas ofertas")
	else:
		send_mail(body)
	
while(True):
	get_list()
	sleep(60 * 60 * 24)








