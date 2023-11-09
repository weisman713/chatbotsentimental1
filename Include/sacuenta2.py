import transformers
import pysentimiento
from mastodon import Mastodon
from bs4 import BeautifulSoup
def getsentimiento(publicacion):
    # Carga el modelo de aprendizaje automático
    model = transformers.BertModel.from_pretrained("bert-base-uncased")

    # Obtiene el texto de la publicación
    text = publicacion['content']

    # Analiza el texto utilizando el modelo de aprendizaje automático
    inputs = transformers.Input(text=text)
    outputs = model(**inputs)

    # Obtiene las probabilidades de las emociones
    probabilidades = outputs['logits']

    # Determina el sentimiento general de la publicación
    sentimiento = pysentimiento.get_sentimiento(probabilidades)

    return sentimiento

def cuentamas(nombre):
    # Crea una instancia de Mastodon
    mastodon = Mastodon(
    client_id="b-gIqSAmV--QCoWVMdFNU7H2dhw-9fWVfMA2OMsdELY",
        client_secret="dGs1iyZFpjD3Ti_XaN45qYYXOPqT_rieGcTOk61u89o",
        api_base_url="https://mastodon.social",
        access_token="xjseene3D_LIAPWd-J5OHT3-hSKTrh1_rieGcTOk61u89o"
    )

    # Obtiene las publicaciones del usuario especificado
    timeline = mastodon.account_search(nombre)
    timeline2 = timeline[0]
    timeline3=timeline2['id']

    # Busca publicaciones del usuario con nombre de usuario "usuario_especifico"
    results = mastodon.account_statuses(timeline3)

    # Obtiene el sentimiento de cada publicación
    sentimientos = []
    for status in results:
        sentimiento = getsentimiento(status)
        sentimientos.append(sentimiento)

    # Devuelve el sentimiento general del usuario
    sentimiento_general = sum(sentimientos) / len(sentimientos)
    return sentimiento_general
