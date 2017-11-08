
import requests
import sys
from bs4 import BeautifulSoup

#Peticion get
def peticionget(url,host):
	try:
		#Peticion get a url+query
		response = requests.get(url)

		return response

	except:
		return "Error-request-get:"+host

#Obtener lista de urls donde extraer la letra
def get_url_lyric(url,host):
	url_lyric = {
		#Test
		"error":"Error:default",
		"url":url,
		"host":host,
		#Enlaces
		"playmusic":"",
		"otra":"",
	}
	try:
		#Peticion get a url+query
		response = requests.get(url)

		#Evaluar peticion de url_lyric
		if response.status_code == 200:
			contenido = response.content
			soup = BeautifulSoup(contenido,"lxml")

			#Obteniendo url-cancion-google-music
			datos = soup.find_all("a", {"class": "fl"})
			try:
				#for tag in datos:

				#Obteniendo url-playmusic
				tag = datos[0]
				enlace = str(tag['href'])
				if enlace[0:4]=="http":
					url_lyric["playmusic"] = enlace
				else:
					url_lyric["playmusic"] = "No encontrado"
					url_lyric["error"] = "Playmusic:No encontrado"

			except:
				print "Error-enlace:",host
				url_lyric["error"] = "Error:enlace"

		else:
			print "Error(1)-",response.status_code
			url_lyric["error"] = "Error:request-"+response.status_code
			pass
		return url_lyric

	except:
		url_lyric["error"] = "Error:except-request"
		url_lyric["host"] = host
		print url_lyric["error"],":",url_lyric["host"]
		return url_lyric

#Obtener letra de playmusic
def getlyric_from_playmusic(url_lyric):
	response = peticionget(url_lyric,"play-music")
	if response.status_code == 200:
		contenido = response.content

		#Obteniendo div-content-letra
		contenido = contenido.encode('utf-8')
		soup = BeautifulSoup(contenido,"lxml")
		datos = soup.find_all("div", {"class": "content-container lyrics"})

		#Encode utf-8
		cadena = ""
		for dato in datos:
			cadena+= dato.encode('utf-8')

		#Obteniendo titulo
		titulo = soup.find_all("div", {"class": "title fade-out"})
		#Obteniendo nombre-artista
		artista = soup.find_all("div", {"class": "album-artist fade-out"})

		#Obteniendo contenido de las letras
		soup = BeautifulSoup(cadena,"html.parser")
		datos = soup.find_all("p")

		try:
			#Imprimir titulo-artista
			print titulo[0].text," - ",artista[0].text,"\n"

			#Imprimir letra
			for tag in datos:
				linea = str(tag).replace("<br/>","\n")
				linea = linea.replace("<p>","")
				linea = linea.replace("</p>","")
				print linea

		except:
			print("Error(2)-contenido")


	else:
		print "Error(2)-",response.status_code
		pass

def obtener_query(texto):
	texto = texto.replace(" ","+")
	return str("q=lyrics+"+texto)


def main():
	var_titulo = sys.argv[1]

	var_titulo = obtener_query(var_titulo)
	url_lyric = get_url_lyric("https://www.google.com.pe/search?"+var_titulo,"google")
	
	#Obtener de play music

	#url_lyric["error"]!="request-get" and 
	if url_lyric["playmusic"]!="":
		if url_lyric["playmusic"]!="No encontrado":
			getlyric_from_playmusic(url_lyric["playmusic"])
		else:
			print "No encontrado"
	else:
		print url_lyric["error"]


if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding("utf-8")
	main()
