from translate import Translator

def espanolyingles(cambio):
    # Crea un objeto Translator
    translator = Translator(from_lang="en", to_lang="es")


    # Realiza la traducción
    translation = translator.translate(cambio)

    # Imprime la traducción
    return(translation)
