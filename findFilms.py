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
lessInfoMovies = []
z = 0    
with pw() as p:
    #pesquisar e coletar os filmes
    search = input(str('Digite o nome completo do filme: ')).lower()
    browser = p.chromium.launch(executable_path='/usr/bin/brave-browser-stable', headless=True)
    page = browser.new_page()
    url = page.goto(f"https://torrentdosfilmes.site")
    page.fill('xpath=/html/body/header/div[1]/div[1]/form/input', search)
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
        
        if(len(ManyFilms) == 0):
            print("Nenhum resultado encontrado.")
            exit()

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
            lessInfoMovie = titlesFormated[0:title]
            s = ' '
            t = s.join(listJoin)
            lessInfoMovieJoin = s.join(lessInfoMovie)
            print(f'{z} - {t}')
            moviesAvaible.append(t)
            lessInfoMovies.append(lessInfoMovieJoin.lower())
    
    import unidecode

    film = input('Digite o numero do filme desejado: ')
    nameMovie = lessInfoMovies[int(film) - 1]
    AccNameMovie = unidecode.unidecode(nameMovie)
    nameMovieUrl = AccNameMovie.replace(' ', '-')
    page2 = browser.new_page()
    url = page2.goto(f"https://torrentdosfilmes.site/{nameMovieUrl}-torrent")
    urlStatus = url.status
    print(url)
    if(urlStatus != 404):
        # Coletando e filtrando os links de download
        sleep(2)
        downloadLink = page2.evaluate('() => window.arrDBLinks')
        for mg in range(len(downloadLink)):
            mGSplit = downloadLink[mg].split(':')[0]
            if(mGSplit == 'magnet'):
                downloadLinkMg = downloadLink[mg]

    else:
        print('Desculpe não encontramos essa página')
        browser.close()


# Realizando download do filme
import time
import datetime
import libtorrent as lt

ses = lt.session()
ses.listen_on(6881, 6891)
params = {
    'save_path': '/home/wesley/Área de Trabalho/Filmes_torrent',}

handle = lt.add_magnet_uri(ses, downloadLinkMg, params)
ses.start_dht()

begin = time.time()
print(datetime.datetime.now())

print ('Baixando os metadados...')
while (not handle.has_metadata()):
    time.sleep(1)
print ('Tem metadados, iniciando o download do torrent...')

print("Starting", handle.name())

while (handle.status().state != lt.torrent_status.seeding):
    s = handle.status()
    state_str = ['enfileirado', 'verificando', 'baixando metadados', \
            'baixando', 'concluído', 'semear', 'alocando']
    print ('%.2f%% Completo (down: %.1f kb/s up: %.1f kB/s Pares: %d) %s ' % \
            (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
            s.num_peers, state_str[s.state]))
    time.sleep(5)

end = time.time()
print(handle.name(), "COMPLETO")

print("Tempo decorrido: ",int((end-begin)//60),"min :", int((end-begin)%60), "sec")
print(datetime.datetime.now())

