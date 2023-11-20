import nltk
from nltk.chat.util import Chat, reflections
from spellchecker import SpellChecker
import unidecode  # Para quitar las tildes
import datetime

# Define pares de preguntas y respuestas usando variantes
generocam = {"Acción": "Action","Aventura": "Adventure","Comedia": "Comedy","Drama": "Drama","Ecchi": "Ecchi","Fantasía": "Fantasy","Mecha": "Mecha","Música": "Music","Misterio": "Mystery","Romance": "Romance","Slice of life": "Slice of Life","Terror": "Horror","Sobrenatural":"supernatural","Deporte":"sports","psicológico":"psychological","chica magica":"mahou shoujo","hentai":"hentai","thriller":"thriller","sci-fi":"sci-fi",}
generosos=""
for clave in generocam:
    generosos=generosos+clave+","
generoscambia="estos son los generos disponibles:"+ generosos
hora_actual = "son las: "+str(datetime.datetime.now().time())
fecha_actual = "estamos a: "+str(datetime.date.today())
pares = [
    (r"(hola|ola|saludos)", ["¡Hola!", "Hola, ¿en qué puedo ayudarte?"]),
    (r"(como estas|cómo te va|como te encuentras)", ["Estoy bien, gracias.", "¡Estoy aquí para ayudarte!"]),
    (r"(adios|hasta luego|bye)", ["¡Hasta luego!", "Adiós, ¡ten un buen día!"]),
    (r"(quien eres|cuál es tu nombre)", ["Soy un chatbot simple.", "Me llaman Weisman."]),
    (r"(que hora es|hora actual)", [hora_actual]),
    (r"(que dia es|fecha)", [fecha_actual]),
    (r"(recomendar.*anime|recomiendame|recomiendame un anime|anime|recomendar|muestrame un anime)",  ["te recomiendo:"]),
    (r"(ingress cents|ingresa.*cuenta|cuenta|meter cuenta|guarda.*cuenta)", ["Por favor ingresa una cuenta:"]),
    (r"(quiero ver descripcion|ver description|ver descripcion|descripcion.*anime)", ["deseas la descripcion del ultimo anime?"]),
    (r"(que es el anime|define anime)", ["se utiliza para referirse a la animación japonesa"]),
    (r"(cual es tu nombre|como te llamas|tu nombre)", ["me llamo Darkill"]),
    (r"(reiniciar cents|reiniciar.*cuenta)", ["estas seguro de reiniciar tu cuenta? esto eliminaria la cuenta anterior"]),
    (r"(reiniciar generous|reiniciar.*generos)", ["estas seguro de reiniciar tus generos? esto eliminaria los anteriores"]),
    (r"(reiniciar recomendaciones|reiniciar.*recomendaciones)", ["estas seguro de reiniciar tus recomendaciones? esto eliminaria los anteriores"]),
    (r"(guarda.*generos|guardar generos|ingresar generos|meter generos|ingresar.*generos|ingress generous)", [generoscambia]),
    
    # Agrega más variantes de preguntas y respuestas aquí
]

# Configura el chatbot
chatbot = Chat(pares, reflections)

# Configura el corrector ortográfico
spell = SpellChecker()

def chatbot1(usuario_input):

    # Aplica corrección ortográfica y quita las tildes
    usuario_input = " ".join(spell.correction(palabra) if spell.correction(palabra) is not None else palabra for palabra in unidecode.unidecode(usuario_input).lower().split())
    print(usuario_input)
    respuesta = chatbot.respond(usuario_input)

    if respuesta is  None:
       
        respuesta = "recuerda digitar lo necesario para obtener la recomendacion como:ingresar cuenta,ingresar generos o recomendar anime."

    
    return respuesta
