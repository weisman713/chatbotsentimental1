import sacuenta
import animeven
import nltk
from nltk.chat.util import Chat, reflections
from spellchecker import SpellChecker
import re

# Define pares de preguntas y respuestas usando variantes
generocam = {"Acción": "Action","Aventura": "Adventure","Comedia": "Comedy","Drama": "Drama","Ecchi": "Ecchi","Fantasía": "Fantasy","Harem": "Harem","Histórico": "Historical","Josei": "Josei","Mecha": "Mecha","Música": "Music","Misterio": "Mystery","Parodia": "Parody","Romance": "Romance","Shounen": "Shounen","Slice of life": "Slice of Life","Terror": "Horror",}
respuestadeg = "Chatbot: estos son los generos disponibles",generocam.keys()
pares = [
    (r"(hola|ola|saludos)", ["¡Hola!", "Hola, ¿en qué puedo ayudarte?"]),
    (r"(como estas|cómo te va|como te encuentras)", ["Estoy bien, gracias.", "¡Estoy aquí para ayudarte!"]),
    (r"(adios|hasta luego|bye)", ["¡Hasta luego!", "Adiós, ¡ten un buen día!"]),
    (r"(quien eres|cuál es tu nombre)", ["Soy un chatbot simple.", "Me llaman weisman."]),
    (r"(que hora es|hora actual)", ["Lo siento, no tengo la capacidad de decirte la hora."]),
    (r"(recomendar.*anime|recomiendame)",  ["te recomiendo:"]),
    (r"(ingresar.*cuenta|guarda.*cuenta|cuenta)", ["Por favor ingresa una cuenta:"]),
     (r"(ingresar.*generos|guarda.*generos|generos)", [respuestadeg]),

    
    # Agrega más variantes de preguntas y respuestas aquí
]

# Configura el chatbot
chatbot = Chat(pares, reflections)

# Configura el corrector ortográfico
spell = SpellChecker()

# Variable para almacenar la cuenta
cuenta = None

# Define las emociones de Paul Ekman
emociones = ["alegria", "ira", "miedo", "asco", "sorpresa", "tristeza"]
emociones2 ={"joy":"alegria","anger":"ira", "fear":"miedo", "disgust":"asco", "surprise":"sorpresa", "sadness":"tristeza"}
resultado2 = []

# Define el diccionario para almacenar las emociones
emociones_usuario = {}

# Inicia la conversación
print("¡Hola! Soy un chatbot simple. Puedes comenzar a preguntarme lo que quieras o escribir 'salir' para terminar la conversación.")

while True:
    usuario_input = input("Usuario: ").lower()  # Convierte la entrada del usuario a minúsculas
    
    if usuario_input == 'salir':
        print("Chatbot: ¡Hasta luego!")
        break
    
    # Corrección ortográfica
    usuario_input_corregido = " ".join(spell.correction(palabra) if spell.correction(palabra) is not None else palabra for palabra in usuario_input.split())
    
    # Si el chatbot espera una cuenta
    if cuenta is not None:
        cuenta = usuario_input_corregido
        resultado1=sacuenta.cuentamas(cuenta)
        print(resultado1)
        print("Chatbot: ¡Cuenta guardada con éxito!")
        cuenta = None  # Reinicia la variable para que el chatbot vuelva a solicitarla cuando sea necesario
    else:
        # Busca la respuesta en las variantes de preguntas utilizando expresiones regulares insensibles a la capitalización
        respuesta = None
        for patron, respuestas in pares:
            if re.search(patron, usuario_input_corregido, re.IGNORECASE):
                respuesta = respuestas
                break
        
        if respuesta is not None:
            # Si se encuentra una respuesta, selecciona una de las respuestas al azar
            import random
            respuesta = random.choice(respuesta)
        else:
            respuesta = "Lo siento, no entendí tu pregunta."
        
        # Si el chatbot solicita una cuenta, configura la variable para almacenarla
        if "Por favor ingresa una cuenta:" in respuesta:
            cuenta = "Esperando cuenta"  # Puedes usar un valor temporal aquí
        
        #espacio para ingresar los generos que quieres ver cuando pases por esas emociones
        if re.search(r"ingresar emociones", usuario_input, re.IGNORECASE):
        # Inicia el ciclo para pedir el valor de cada emoción
            
            print("Chatbot: estos son los generos disponibles",generocam.keys())
            for emocion in emociones:
                # Pide el valor de la emoción
                valor = generocam[input(f"Ingresa el valor de la emoción {emocion}: ")]

                # Guarda el valor en el diccionario
                emociones_usuario[emocion] = valor

                # Imprime la confirmación
                print(f"Chatbot: El valor de la emoción {emocion} es {valor}.")
            for clave in resultado1:
                resultado2.append(emociones2[clave])
            print(resultado2)
        #llama la funcion que trae los animes cuando se le manda la lista de generos que nesecita el usuario   
        if "te recomiendo:" in respuesta:
             listareco=[emociones_usuario[resultado2[0]],emociones_usuario[resultado2[1]]]
             print(listareco)
             resultado3=animeven.getlistanime(listareco)
             print(resultado3)
            

        print("Chatbot:", respuesta)
        
