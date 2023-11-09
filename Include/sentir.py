from pysentimiento import create_analyzer

def getsentimiento (cadena):
    emotion_analyzer = create_analyzer(task="emotion", lang="es")
    sentimiento2 = emotion_analyzer.predict(" ") 
    sentimiento3 = emotion_analyzer.predict(" ") 
    e=0
    suma = {}
    for clave, valor in sentimiento2.probas.items():
            if clave in sentimiento3.probas:
                suma[clave] = valor - sentimiento3.probas[clave]


    for i in cadena:

        sentimiento1 = emotion_analyzer.predict(cadena[0])
            
        for clave, valor in suma.items():
            if clave in sentimiento1.probas:
                suma[clave] = valor + sentimiento1.probas[clave]
        #  print(suma)

    del suma['others']
    sentimientofnal = max(suma.items(), key=lambda x: x[1])[0]

    listo = []
    listo.append(sentimientofnal)
    #    print(sentimientofnal)

    del suma[sentimientofnal]
    sentimientofnal = max(suma.items(), key=lambda x: x[1])[0]

    listo.append(sentimientofnal)
    return listo