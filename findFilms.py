from playwright.sync_api import sync_playwright as pw
from time import sleep
import requests
from bs4 import BeautifulSoup

def createUrl(currentUrl):
    urlFormated1 = currentUrl.replace('/', ' ')
    urlFormated2 = urlFormated1.split()
    urlFormated2.append('newValue')
    urlFormated2[3] = urlFormated2[2]
    urlFormated2[2] = (f'/page/{x+1}')
    urlManipulated = urlFormated2[0] + '//' + urlFormated2[1] + urlFormated2[2] + urlFormated2[3]
    return urlManipulated

moviesAvaible = []
z = 0    
with pw() as p:
    #pesquisar e coletar os filmes
    browser = p.chromium.launch(executable_path='C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe', headless=True)
    page = browser.new_page()
    url = page.goto(f"https://torrentdosfilmes.site")
    pesquisa = 'batman'
    page.fill('xpath=/html/body/header/div[1]/div[1]/form/input', pesquisa)
    page.locator('xpath=/html/body/header/div[1]/div[1]/form/button').click()
    currentUrl = page.url

    #Identificar a quantidade de paginas
    res = requests.get(currentUrl)
    soup_data = BeautifulSoup(res.text, 'html.parser')
    numberOfPages = soup_data.find_all(class_='wp-pagenavi')

    for pages in numberOfPages:
        pagesWithoutFormatted = pages.get_text()
        
    pagesFormated = pagesWithoutFormatted.split()
    identify = page.locator('xpath=/html/body/div/main/div[14]/a[1]')
    identify2 = identify.is_visible()

    if(len(pagesFormated) == 6):
        pagesFormated.pop(3)
        pagesFormated.pop(4)
        lastPageString = pagesFormated[-1]
        lastPage = int(lastPageString)
    elif (len(pagesFormated) >= 1 and len(pagesFormated) < 6):
        lastPageString = pagesFormated[-2]
        lastPage = int(lastPageString)
    elif(identify2 == False):
        lastPage = 1

    for x in range(lastPage):    
        #print(f'Pagina: {x+1}')

        currentUrl = page.url

        urlManipulated = createUrl(currentUrl)

        res = requests.get(urlManipulated)
        soup_data = BeautifulSoup(res.text, 'html.parser')
        content = soup_data.find_all(class_='post green')
            
        texto = []
        for textos in content:
            texto.append(textos.get_text())
            
        ManyFilms = []
        contador = 0
        for x in texto:
            ManyFilms.append(x.replace('\n', ''))

        for films in ManyFilms:
            z+=1
            idenQualityMovie = films.replace('/', ' ')
            titlesFormated = idenQualityMovie.split()
            title = titlesFormated.index('Torrent')
               
            for ql in titlesFormated:
    
               if(ql == '720p'):
                    quality = titlesFormated.index('720p')
               elif(ql == '1080p'):
                    quality = titlesFormated.index('1080p')
            listJoin = titlesFormated[0:title] + titlesFormated[quality:-1]
            s = ' '
            t = s.join(listJoin)
            print(f'{z} - {t}')
            moviesAvaible.append(t)
 
    film = input('Digite o numero do filme desejado: ')
    print(moviesAvaible[int(film) - 1])
            
