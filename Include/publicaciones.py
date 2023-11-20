from mastodon import Mastodon
from bs4 import BeautifulSoup

def getpublicaciones(nombre):
# Crea una instancia de Mastodon
    mastodon = Mastodon(
    client_id="b-gIqSAmV--QCoWVMdFNU7H2dhw-9fWVfMA2OMsdELY",
        client_secret="dGs1iyZFpjD3Ti_XaN45qYYXOPqT_rieGcTOk61u89o",
        api_base_url="https://mastodon.social",
        access_token="xjseene3D_LIAPWd-J5OHT3-hSKTrh1-0ZcfkGa2UZ0"
    )
    
    timeline = mastodon.account_search(nombre)
    if len(timeline) == 0:
        return timeline
    timeline2 = timeline[0]
    timeline3=timeline2['id']

    # Busca publicaciones del usuario con nombre de usuario "usuario_especifico"
    results = mastodon.account_statuses(timeline3)

    # Imprime los resultados
    cadena = []
    i=0
    for status in results:
        i=i+1;
        soup =BeautifulSoup(status['content'],'html.parser')
        paragraph = soup.find('p')
        
        if paragraph:
            cadena.append(paragraph.get_text())
        if i== 5:
            break

    return cadena