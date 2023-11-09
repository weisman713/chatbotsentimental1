import sentir
import publicaciones

def cuentamas(nombre):
#    nombre= input("digite su usuario: ")
    publicaron= publicaciones.getpublicaciones(nombre)
    if len(publicaron) == 0:
        return "el nombre de usuario no existe"
    else:
        sintieron= sentir.getsentimiento(publicaron)
        return sintieron 