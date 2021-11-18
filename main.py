from flask.sessions import SessionInterface
from flask import Flask, render_template, request, redirect, session, flash

from oauth2client.service_account import ServiceAccountCredentials
import gspread

from validate_email import validate_email
from newsapi import NewsApiClient
from datetime import date

from sort import get_ranking

#Noticias
newsapi = NewsApiClient(api_key='ffa1123e4add4b7c9e5e95f1ce806f8b')
headlines = newsapi.get_everything(language='es',  sort_by="publishedAt", page_size=30, q='(biodegradable AND reutilizar) OR (reutilizar AND reciclaje)')

#Flask
app = Flask(__name__)
app.secret_key = 'no revelar clave'

#Drive
credential = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", ["https://spreadsheets.google.com/feeds",
                                                                                    "https://www.googleapis.com/auth/spreadsheets",
                                                                                    "https://www.googleapis.com/auth/drive.file",
                                                                                    "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credential)
Proyecto_2_db = client.open('Proyecto-2-db')

# objetos de drive 
users_gs = Proyecto_2_db.get_worksheet(0)
data_gs = Proyecto_2_db.get_worksheet(1)
opciones_gs= Proyecto_2_db.get_worksheet(2)
posiciones_gs = Proyecto_2_db.get_worksheet(4) #no se usa


@app.route('/')
def hello_world():

    noticias = headlines['articles']

    ranking_ = get_ranking()[:10:]

    return render_template('inicio.html', noticias=noticias, ranking= ranking_)

@app.route('/revisar', methods=['POST'])
def check():
    users = users_gs.get_all_records()
    
    
    for user in users:
        if user['usuario'] == request.form['usuario'] and str(user['contrasena']) == str(request.form['contraseña']):
            session['id'] = user['id']
            session['usuario'] = user['usuario']
            session['nombre'] = user['nombre']
            session['mail'] = user['mail']
            session['fdn'] = user['fdn']
            session['region/comuna'] = user['region/comuna']
            session['img'] = user['img']
            session['active'] = True

            noticias = headlines['articles']
            
            return redirect('/')#cambiar a pagina de inicio

    flash('Usuario o Clave erronea')
    return redirect("/signin.html") #esto pendiente

@app.route('/ranking')
def ranking():
    
    registros = []
    registros = get_ranking()
    return render_template('/ranking.html', registros = registros)


@app.route('/signin.html')
def signin():
    return render_template('/signin.html')


@app.route('/signup.html')
def signup():

    return render_template('/signup.html')


@app.route('/pregunta')
def pregunta():
    print("dfasd")
    return render_template('/pregunta.html')

    
@app.route('/opcion' , methods=['POST'])
def opcion():
    opciones = opciones_gs.get_all_records()
    users_new_id = session['id']
    relleno = 'relleno'
    row = [users_new_id,request.form['objetivo1'], request.form['recordar1'],relleno, request.form['frecuencia1']]
    opciones_gs.insert_row(row,2)
    return redirect('/')
##,request.form['Recordatorio'],request.form['Fechas'],request['Frecuencia']

@app.route('/salir')
def logout():
    session.clear()
    return redirect('/')

@app.route("/perfil")#Aqui lo deje asi no mas, me falta cambiarlo a mi al otro link de perfil(pipe)
def perfil():
    posiciones = []
    posiciones = get_ranking()
    return render_template('/perfil_.html',  posiciones = posiciones)


@app.route('/tips_y_consejos')
def consejos():
    return render_template('/tips_y_consejos.html')

@app.route('/tips/<titulo>')
def tip(titulo):

    return render_template('/tip.html', titulo=titulo)

@app.route('/progreso')
def progresos():
    from grafico import grafico
    entradas = []
    entradas = data_gs.get_all_records()[1::]

    return render_template('/progreso.html', entradas=entradas, plot=grafico(session['id']))


@app.route('/puntos')
def puntos():
    return render_template('/puntos.html')

@app.route('/metas')
def metas():
    opciones= opciones_gs.get_all_records()
    for opcion in opciones:
        if session['id']== opcion['id usuario']:
            session['objetivo'] = opcion['Objetivo']
            session['Recordatorio'] = opcion['Recordatorio']
            session['Frecuencia'] = opcion['Frecuencia']
            
    return render_template('/mismetaseste.html')

@app.route('/nosotros')
def nosotros():
    return render_template('/nosotros.html')

@app.route('/formulario_puntos')
def formulario():
    return render_template('/formulario_puntos.html')

@app.route('/vidrio')
def consejos():
    return render_template('/vidrio.html')

@app.route('/vcartonpapel')
def consejos():
    return render_template('/vcartonpapel.html')
@app.route('/vlatas')
def consejos():
    return render_template('/vlatas.html')

@app.route('/vtetra')
def consejos():
    return render_template('/vtetra.html')

@app.route('/vresiduo')
def consejos():
    return render_template('/vresiduo.html')

@app.route('/vplastico')
def consejos():
    return render_template('/vplastico.html')
   

@app.route('/registrar', methods=['POST'])
def register():
    if request.form['contraseña1'] != request.form['contraseña2']:
        flash('Claves no iguales')
        return redirect('/signup.html')
    users = users_gs.get_all_records()
    users_new_id = int(users[0]['id'] + 1)
    imagen = 'https://picsum.photos/id/'+str(users_new_id)+'/64/64'
    row = [users_new_id,request.form['nombre'],request.form['usuario'],request.form['contraseña1'],request.form['email'],request.form['fdn'],request.form['region/comuna'],imagen]

    users_gs.insert_row(row,2)

    session['id'] =  users_new_id
    session['usuario'] = request.form['usuario']
    session['nombre'] = request.form['nombre']
    session['mail'] = request.form['email']
    session['fdn'] = request.form['fdn']
    session['region/comuna'] = request.form['region/comuna']
    session['img'] = imagen 
    session['active'] = True
    return redirect('/pregunta')

@app.route('/obtener_puntos', methods=['POST'])
def obtener_puntos():

    vidrio_chico = int(request.form['vidrio_chico'])
    vidrio_grande = int(request.form['vidrio_grande'])

    tetra_chico = int(request.form['tetra_chico'])
    tetra_grande = int(request.form['tetra_grande'])
    
    plastico_chico = int(request.form['plastico_chico'])
    plastico_grande = int(request.form['plastico_grande'])

    carton_chico = int(request.form['carton_chico'])
    carton_grande = int(request.form['carton_grande'])

    latas_chico = int(request.form['latas_chico'])
    latas_grande = int(request.form['latas_grande'])

    org_kilo = int(request.form['org_kilo'])
    org_litro = int(request.form['org_litro'])

    descripcion = request.form['descripcion']

    #imagen = request.form['imagen']
    entradas = data_gs.get_all_records()[1::]
    
    entrada_new_id = int(entradas[0]['id entrada'] + 1)
    fecha = date.today().strftime("%d/%m/%Y")

    suma_puntos = (tetra_grande*4 + tetra_chico) + (vidrio_grande*4 + vidrio_chico*2) + (plastico_grande*3 + plastico_chico) + (carton_grande*5 + carton_chico*1) + (latas_grande*2 + latas_chico) + (org_litro*4 + org_kilo*4)
    info = [
        session['id'], entrada_new_id, fecha,
        descripcion, vidrio_grande, vidrio_chico,
        tetra_grande, tetra_chico, plastico_grande,
        plastico_chico, carton_grande ,carton_chico,
        latas_grande, latas_chico, org_kilo + org_litro,
        suma_puntos
        ]
    data_gs.insert_row(info, 3)
    return redirect('/metas')
    







