import animeven
import sacuenta
import traductor
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

import bot2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'your-secret-key'  # Cambia esto a una clave segura en un entorno de producción
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

#variables globales para que se guarden despues de cada interaccion
respuesta2=0 #me maneja los cambios del chat
conteando=0 #servira como un contador
cuenta1="" #aqui se guardara la cuenta del usuario
emocion1="" #aqui se guardara la emocion del usuario seran las dos mas altas
emociones1={} #es el dict de los generos del usuario
listatotal=[] #es la lista total de animes a recomendar 
#recomendaciones_pasadas=[]
anime1="" #es el anime que se recomienda actualmente
descripcion1=""
imagen1=''

# Definición de las tablas
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # Relación con las recomendaciones
    recomendaciones = db.relationship('Recomendacion', backref='usuario', lazy=True)
    # Relación con los géneros asociados a las emociones
    generos_emociones = db.relationship('GeneroEmocion', backref='usuario', lazy=True)



class Recomendacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    imagen = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    
class GeneroEmocion(db.Model):
    #{"joy":"alegria","anger":"ira", "fear":"miedo", "disgust":"asco", "surprise":"sorpresa", "sadness":"tristeza"}
    id = db.Column(db.Integer, primary_key=True)
    joy = db.Column(db.String(50), nullable=False)
    anger = db.Column(db.String(50), nullable=False)
    fear = db.Column(db.String(50), nullable=False)
    disgust = db.Column(db.String(50), nullable=False)
    surprise = db.Column(db.String(50), nullable=False)
    sadness = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        return render_template('dashboard.html', user=user)
    return render_template('login.html')





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Procesar la solicitud de inicio de sesión
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect('/chat')
        else:
            # Puedes agregar un mensaje de error si el inicio de sesión falla
            error_message = "Credenciales incorrectas. Inténtalo de nuevo."
            return render_template('login.html', error=error_message)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Verificar si el correo electrónico ya existe en la base de datos
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            error_message = "Este correo electrónico ya está registrado. Por favor, use otro."
            return render_template('register.html', error=error_message)

        # Si el correo electrónico no existe, proceder con el registro
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('register.html')



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/ver_usuarios', methods=['GET'])
def ver_usuarios():
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, Nombre de usuario: {user.username}, Correo electrónico: {user.email}")
    return "Verifica la consola para ver la lista de usuarios registrados."

@app.route('/get_username', methods=['POST'])
def get_username():
    if request.method == 'POST':
        email = request.form['email']  # Obtén el correo electrónico del formulario

        # Busca el usuario en la base de datos por su correo electrónico
        user = User.query.filter_by(email=email).first()

        if user:
            # Se encontró el usuario, y ahora puedes acceder a su nombre de usuario
            username = user.username
            return f"El nombre de usuario asociado con el correo {email} es {username}"
        else:
            # No se encontró un usuario con ese correo
            return "No se encontró un usuario con el correo proporcionado"

    return "Solicitud no válida"


# Ruta de la página de chat
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session:
        # Si el usuario no ha iniciado sesión, redirige a la página de inicio de sesión
        return redirect('/login')

    user = User.query.filter_by(id=session['user_id']).first()

    if request.method == 'POST':
       
        user_input = request.form['user_input']  # Obtén la entrada del usuario desde el formulario
        
        global respuesta2
            
        respuesta = bot2.chatbot1(user_input)

        # En este punto, user_input es la entrada del usuario del formulario
        

        return render_template('chat.html', respuesta=respuesta, user=user)

    return render_template('chat.html', respuesta='', user=user)

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('user_message')
    #variable que me ayuda en la conversion de español a ingles en los generos
    generocam = {"Acción": "Action","Aventura": "Adventure","Comedia": "Comedy","Drama": "Drama","Ecchi": "Ecchi","Fantasía": "Fantasy","Harem": "Harem","Histórico": "Historical","Josei": "Josei","Mecha": "Mecha","Música": "Music","Misterio": "Mystery","Parodia": "Parody","Romance": "Romance","Shounen": "Shounen","Slice of life": "Slice of Life","Terror": "Horror",}
    #variable donde se muestran las emociones sirve para iterar
    emociones = ["alegria", "ira", "miedo", "asco", "sorpresa", "tristeza"]
    #variable dict que me sirve de conversion de ingles a español con las emociones
    emociones2 ={"joy":"alegria","anger":"ira", "fear":"miedo", "disgust":"asco", "surprise":"sorpresa", "sadness":"tristeza"}
    user = User.query.filter_by(id=session.get('user_id')).first()
    global respuesta2
    global cuenta1
    global conteando
    global emocion1
    global emociones1
    global listatotal
    global anime1
    #global recomendaciones_pasadas
    global descripcion1
    global imagen1
    # Llama a tu chatbot para obtener una respuesta
    # Reemplaza 'server_response' con la respuesta real del chatbot
    match respuesta2:
            case 1:
                respuesta2=0
                if len(cuenta1)==0:
                    emocion1=sacuenta.cuentamas(user_message)
                    
                    
                    if emocion1=="el nombre de usuario no existe":
                        server_response=emocion1
                        
                    else:
                        server_response="cuenta guardada con exito"
                        cuenta1=user_message
                        print("la emocion es: "+emocion1[0]+" segunda emocion: "+ emocion1[1])
                    
                    
                else:
                    server_response="ya hay una cuenta ingresada la cual es: "+ cuenta1
                    emocion1=sacuenta.cuentamas(user_message)
                    

            case 2:
                if user_message=="si":
                    if conteando>=12:
                      server_response="son todas las recomendaciones"
                      respuesta2=0
                    else:
                        conteando=conteando+1
                        server_response="te recomiendo tambien: "
                        anime1=listatotal[conteando]
                        existing_recommendation = Recomendacion.query.filter_by(nombre=anime1, user_id=user.id).first()

                        while existing_recommendation:
                            conteando +=1
                            anime1=listatotal[conteando]
                            existing_recommendation = Recomendacion.query.filter_by(nombre=anime1, user_id=user.id).first()


                        descripcion1=traductor.espanolyingles(animeven.getinfor(anime1)[:500])
                        imagen1=animeven.getimagen(anime1)
                        anime2={
                            'id': 2,
                            'nombre': anime1,
                            'imagen': imagen1,
                            'descripcion': descripcion1
                        }
                        if 'user_id' in session:
                            recomendacion_actual = Recomendacion(nombre=anime1, imagen=imagen1, descripcion=descripcion1, user_id=user.id)
                            db.session.add(recomendacion_actual)
                            user.recomendaciones.append(recomendacion_actual)
                            db.session.commit()
                        
                        server_response=server_response+anime1+" deseas otra recomendacion?"
                else:
                    server_response="desea ver de que trata la recomendacion?"

                    respuesta2=4
                

            case 3:
                if conteando>=5:
                    respuesta2=0
                    valor = generocam[user_message]
                    emociones1[emociones[conteando]]=valor
                    genero_emocion = GeneroEmocion(
                        joy=emociones1.get("alegria"),
                        anger=emociones1.get("ira"),
                        fear=emociones1.get("miedo"),
                        disgust=emociones1.get("asco"),
                        surprise=emociones1.get("sorpresa"),
                        sadness=emociones1.get("tristeza"),
                        user_id=user.id
                    )
                    db.session.add(genero_emocion)
                    db.session.commit()
                    server_response= "emociones editadas con exito"
                    print(str(emociones1.keys()))
                    conteando=0
                else:
                    if user_message in generocam:
                        valor = generocam[user_message]
                        emociones1[emociones[conteando]]=valor# variable global
                        conteando=conteando+1
                        server_response="genero para la emocion de "+emociones[conteando]+": "
                    else:
                        server_response="error. digite bien el genero para la emocion de "+emociones[conteando]+": "
            
            case 4:
                if user_message=="si":
                    if not user.recomendaciones:
                        server_response="aun no se a hecho la recomendacion"
                        respuesta2=0
                    else:
                        latest_recommendation = user.recomendaciones[-1]
                        server_response=latest_recommendation.descripcion
                        respuesta2=0
                else:
                    server_response="aun puedes ver la descripcion cuando gustes"
                    respuesta2=0
            
            case 5:
                if user_message=="si":
                    generos_a_eliminar = GeneroEmocion.query.filter_by(user_id=user.id).all()
                    for genero in generos_a_eliminar:
                        db.session.delete(genero)

                    # Guarda los cambios en la base de datos
                    db.session.commit()
                    server_response="eliminado con exito"
                else:
                    server_response="se conservan los generos actuales"
                respuesta2=0

            case _:
                server_response = bot2.chatbot1(user_message)
                respuesta2=respuesta2
    print(server_response)
    #aqui comienza a comparar las respuestas del chatbot para su siguiente iteracion
    if server_response=="te recomiendo:":
        if len(cuenta1)==0:
            server_response="no a ingresado la cuenta"
        elif not(user.generos_emociones):
            server_response="no a ingresado los generos a las emociones"
        else:
            dict_emociones = {}

            emociones = ['joy', 'anger', 'fear', 'disgust', 'surprise', 'sadness']

            for emocion in emociones:
                generos_emocion = GeneroEmocion.query.with_entities(getattr(GeneroEmocion, emocion)).filter(GeneroEmocion.user_id == user.id).all()
                generos_emocion = [genero[0] for genero in generos_emocion]
                
                # Agregar al diccionario si hay géneros asociados a la emoción
                if generos_emocion:
                    dict_emociones[emocion] = generos_emocion
            print(dict_emociones)
            
            listareco=[dict_emociones[emocion1[0]],dict_emociones[emocion1[1]]]
            listareco=[listareco[0][0],listareco[1][0]]
            print(listareco)#lista en ingles de la emociones del usuario
            listatotal=animeven.getlistanime(listareco)
            anime1=listatotal[0]
            descripcion1=traductor.espanolyingles(animeven.getinfor(anime1)[:500])
            imagen1=animeven.getimagen(anime1)
            anime2={
                'id': 2,
                'nombre': anime1,
                'imagen': imagen1,
                'descripcion': descripcion1
            }

            if 'user_id' in session:
                            recomendacion_actual = Recomendacion(nombre=anime1, imagen=imagen1, descripcion=descripcion1, user_id=user.id)
                            db.session.add(recomendacion_actual)
                            user.recomendaciones.append(recomendacion_actual)
                            db.session.commit()

            
            server_response=server_response+anime1+"desea otra recomendacion?"
            respuesta2=2
            conteando=0
    elif server_response=="estos son los generos disponibles:Acción,Aventura,Comedia,Drama,Ecchi,Fantasía,Harem,Histórico,Josei,Mecha,Música,Misterio,Parodia,Romance,Shounen,Slice of life,Terror,":
        if user.generos_emociones:
            server_response="ya tienes los generos ingresados a la cuenta"
            respuesta2=0
        else:
            server_response=server_response+" genero para la emocion "+str(emociones[0])+": "
            respuesta2=3
            conteando=0
    elif server_response=="Por favor ingresa una cuenta:":
            
            respuesta2=1
    elif server_response=="deseas la descripcion del ultimo anime?":
        
            respuesta2=4
    elif server_response=="estas seguro de reiniciar tus generos? esto eliminaria los anteriores":
        respuesta2=5

    print(respuesta2)


     # Recomendaciones pasadas (suponiendo que sea una lista de diccionarios con información)
    if user.recomendaciones:
        # Recomendación actual (suponiendo que sea un diccionario con información)
        latest_recommendation = user.recomendaciones[-1]  # Última recomendación

        recomendacion_actual = {
            'id': latest_recommendation.id,
            'nombre': latest_recommendation.nombre,
            'imagen': latest_recommendation.imagen,
            'descripcion': latest_recommendation.descripcion
            }
        
        recomendaciones_pasadas = []

                # Construir una lista con todas las recomendaciones del usuario
        for recomendacion in user.recomendaciones:
            recomendaciones_pasadas.append({
                'id': recomendacion.id,
                'nombre': recomendacion.nombre,
                'imagen': recomendacion.imagen,
                'descripcion': recomendacion.descripcion
                })
    else:
        recomendacion_actual={}
        recomendaciones_pasadas=[]

    
        #pruebas
        

    # Envía las recomendaciones al frontend
    response = {
        'server_response': server_response,
        'recomendacion_actual': recomendacion_actual,
        'recomendaciones_pasadas': recomendaciones_pasadas
    }
    return jsonify(response)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
