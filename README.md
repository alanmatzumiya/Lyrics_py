# Lyrics_py
Programa en python para buscar la letra de una canción.

## Dependencias
- BeautifulSoup 
- Request
- lxml

## Info

Aplicación hecha en python, permite buscar las letras de las canciones en base a los resultados de busqueda realizados en **Google**. Tiene soporte para resultados donde te redireccionan a:
  * Google playmusic
  * Metrolyrics.com

## Instalacion
 ```
    pip install -r requirements.txt
 ```

## Uso
 ```
    python lyrics.py "Nombre de la cancion"
 ``` 
 
## Author
Paolo Ramirez - phaoliop@gmail.com

## Bug
- Redireccionamiento de enlaces no soportado.
- Errores de busqueda no esperados.

## Versiones
  * ### Lyrics_0.2.py
    - Soporte agregado resultados basados en **Metrolyrics.com**
    - Mejoras en obtencion de urls de busqueda para futuras versiones.
    
  * ### Lyrics_0.1.py
    - Resultados de busqueda basada en **Google**
    - Solo soporte para resultados basados en **Google play music**

## Vista de la aplicacion en consola
![Imagen no disponible](https://github.com/phaoliop/Lyrics_py/blob/master/imagenes/prueba_0-2.png)
