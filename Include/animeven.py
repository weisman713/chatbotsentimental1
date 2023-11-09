from AnilistPython import Anilist

#diccionario del anime
#['name_romaji', 'name_english', 'starting_time', 'ending_time', 'cover_image', 'banner_image', 'airing_format', 'airing_status', 'airing_episodes', 'season', 'desc', 'average_score', 'genres', 'next_airing_ep'])
#generos
#Acción, Aventura,Comedia, Drama, Ecchi, Fantasía, Harem, Histórico, Josei, Mecha, Música, Misterio, Parodia, Romance, Seinen, Shoujo, Shounen, Slice of life,Terror, Yaoi, Yuri
def getlistanime(lista):
    anilist = Anilist()
    m = anilist.search_anime(genre=lista, score=range(80, 95),)
    i=0
    listo=[]
    while i<13:
        mm = m[i]
        listo.append(mm['name_romaji'])
        i+=1
    return listo
def getinfor(name):
    anilist = Anilist()
    anime2=anilist.get_anime(name)
    return anime2['desc']

def getanime(name):

    anilist = Anilist()
    anime2= anilist.get_anime(name)        # returns a dictionary containing info about owari no seraph
    return anime2

def getimagen(name):
    anilist = Anilist()
    anime2=anilist.get_anime(name)
    return anime2['cover_image']
