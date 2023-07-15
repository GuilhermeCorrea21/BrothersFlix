from playwright.sync_api import sync_playwright as pw
from time import sleep


with pw() as p:
    nameMovie = input(str('Digite o nome completo do filme: ')).lower()
    nameMovieUrl = nameMovie.replace(' ', '-')
    MovieUrl = ''

    browser = p.chromium.launch(executable_path='/usr/bin/brave-browser-stable', headless=True)
    #page = browser.new_page()
    #page.goto(f"https://limontorrents.com//{nameMovieUrl}")
    #downloadButton = page.locator('xpath=//*[@id="main"]/div/div[1]/div[2]/div[3]/a[1]') 
    #hrefValue = downloadButton.get_attribute('href')

    page2 = browser.new_page()
    url = page2.goto(f"https://torrentdosfilmes.site/{nameMovieUrl}")
    urlStatus = url.status

    if(urlStatus != 404):
        downloadButton2 = page2.locator('xpath=/html/body/div[1]/main/section/div/article/div[2]/center[3]/a')
        XpIsViseble = downloadButton2.is_visible()

        if(XpIsViseble == False):
            page2.reload()
            downloadButton2 = page2.locator('xpath=/html/body/div[1]/main/section/div/article/div[2]/center[2]/center[1]/div/a')
            MovieUrl = downloadButton2.get_attribute('href')
        else:
            MovieUrl = downloadButton2.get_attribute('href')
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
    'save_path': '/home/wesley/Área de Trabalho/Filmes_torrent/',}

handle = lt.add_magnet_uri(ses, MovieUrl, params)
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
            'baixar', 'concluído', 'semear', 'alocando']
    print ('%.2f%% Completo (down: %.1f kb/s up: %.1f kB/s Pares: %d) %s ' % \
            (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
            s.num_peers, state_str[s.state]))
    time.sleep(5)

end = time.time()
print(handle.name(), "COMPLETO")

print("Tempo decorrido: ",int((end-begin)//60),"min :", int((end-begin)%60), "sec")
print(datetime.datetime.now())