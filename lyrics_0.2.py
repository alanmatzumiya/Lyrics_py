
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
		"error":"",
		"url":url,
		"host":host,
		#Enlaces
		"playmusic":"",
		"musica.com":"",
		"azlyrics":"",
		"letras.com":"",
		"genius":"",
		"metrolyrics":"",
	}
	try:
		#Peticion get a url+query
		response = requests.get(url)
		#Evaluar peticion de url_lyric
		if response.status_code == 200:
			contenido = response.content
			soup = BeautifulSoup(contenido,"lxml")

			try:
				#Obteniendo url-cancion-google-music
				google = soup.find_all("a", {"class": "fl"})
				resultados = soup.find_all("div",{"class":"g"})
				#Obteniendo url-playmusic
				tag = google[0]
				enlace = str(tag['href'])
				if enlace[0:4]=="http":
					url_lyric["playmusic"] = enlace
				#Obteniendo url-resultados-10
				for tag in resultados:
					#Evaluar tag
					soup = BeautifulSoup(str(tag),"html.parser")
					url = soup.find_all("a")
					referencia = soup.find_all("cite")
					if referencia:
						var = url[0]
						#Editar url
						enlace = str(var['href']).replace("/url?q=","")
						enlace = enlace.replace("%3F","?")
						enlace = enlace.replace("%3D","=")
						enlace = enlace.split('&')[0]

						if "azlyrics" in referencia[0].text:
							url_lyric["azlyrics"] = enlace
						elif "genius" in referencia[0].text:
							url_lyric["genius"] = enlace
						elif "metrolyrics" in referencia[0].text:
							url_lyric["metrolyrics"] = enlace
						elif "musixmatch" in referencia[0].text:
							url_lyric["musixmatch"] = enlace
						elif "musica.com" in referencia[0].text:
							url_lyric["musica.com"] = enlace
						elif "letras.com" in referencia[0].text:
							url_lyric["letras.com"] = enlace
						else:
							url_lyric["error"]="Busqueda-no-soportada"
					pass

			except:
				print "Error-enlace:",host
				url_lyric["error"] = "Error:enlace"

		else:
			url_lyric["error"] = "Error:request-"+response.status_code
			pass
		return url_lyric

	except:
		url_lyric["error"] = "Error:except-request"
		url_lyric["host"] = host
		return url_lyric

#Obtener letra de playmusic
def getlyric_from_playmusic(url_lyric,host):
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
			print titulo[0].text,"-",artista[0].text,"\n"

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

#Obtener letra de playmusic
def getlyric_from_metrolyrics(url_lyric,host):
	response = peticionget(url_lyric,host)
	if response.status_code == 200:
		contenido = response.content
		
		#Obteniendo div-content-letra
		contenido = contenido.encode('utf-8')
		soup = BeautifulSoup(contenido,"lxml")
		datos = soup.find_all("div", {"class": "js-lyric-text"})

		#Encode utf-8
		cadena = ""
		for dato in datos:
			cadena+= dato.encode('utf-8')
		
		content_description = soup.find_all("div", {"class": "banner-heading"})
		#Obteniendo titulo
		soup = BeautifulSoup(str(content_description),"html.parser")
		titulo = soup.find_all("h1")
		#Obteniendo nombre-artista
		artista = soup.find_all("h2")


		#Obteniendo contenido de las letras
		soup = BeautifulSoup(cadena,"html.parser")
		datos = soup.find_all("p",{"class":"verse"})
		
		try:
			#Imprimir titulo-artista
			print titulo[0].text.replace("Lyrics",""),"-",artista[0].text,"\n"

			#Imprimir letra
			for tag in datos:
				print tag.text,"\n"


		except:
			print("Error(2)-contenido")

	else:
		print "Error(2)-",response.status_code
		pass

'''
	Seleccionar host a buscar
'''
def switch_lyrics(url_lyrics,host):
	#Obtener de play music

	if host=="playmusic":
		getlyric_from_playmusic(url_lyrics[host],host)
	else:
		if host=="metrolyrics":
			getlyric_from_metrolyrics(url_lyrics[host],host)
		else:
			print url_lyrics["error"]

'''
	Funcion Principal+gen_query
'''
def get_query(texto):
	texto = texto.replace(" ","+")
	return str("q=lyrics+"+texto)

def main():
	var_titulo = sys.argv[1]

	var_titulo = get_query(var_titulo)
	url_lyrics = get_url_lyric("https://www.google.com.pe/search?"+var_titulo,"google")
	
	eval_rpt = [
		#Test
		"error",
		"url",
		"host",
		#Enlaces
		"playmusic",
		#"azlyrics",	
		#"musica.com",
		#"letras.com",
		#"genius",
		"metrolyrics",
	]
	for linea in eval_rpt[3:]:
		if url_lyrics[linea]:
			switch_lyrics(url_lyrics,linea)
			break
			pass


if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding("utf-8")
	main()
