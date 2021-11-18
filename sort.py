
from oauth2client.service_account import ServiceAccountCredentials
import gspread


credential = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", ["https://spreadsheets.google.com/feeds",
                                                                                    "https://www.googleapis.com/auth/spreadsheets",
                                                                                    "https://www.googleapis.com/auth/drive.file",
                                                                                    "https://www.googleapis.com/auth/drive"])


client = gspread.authorize(credential)
Proyecto_2_db = client.open('Proyecto-2-db')

users_gs = Proyecto_2_db.get_worksheet(0)
ranking_gs = Proyecto_2_db.get_worksheet(1)

entradas = ranking_gs.get_all_records()[1::]
usuarios = users_gs.get_all_records()

total_puntos = {}
ranking = []

def get_total_puntos():

	for kk in total_puntos.keys():
		total_puntos[kk] = 0
	for  entrada in entradas:
		
		if entrada['id usuario'] in total_puntos:
			total_puntos[entrada['id usuario']] += entrada['Puntos']
		else:
			total_puntos[entrada['id usuario']] = entrada['Puntos']

	return total_puntos


def get_ranking():

	ranking = []
	total_puntos = get_total_puntos()
	sorted_keys = sorted(total_puntos, key=total_puntos.get)[::-1]

	for key in sorted_keys:
		#(id, img, Usuario, puntaje)
		user = info_usuario(key)
		ranking.append(user)
	
	return ranking

def info_usuario(key):
	
	for usuario in usuarios:
		if usuario['id'] == key:
			return key, usuario['img'], usuario['usuario'], total_puntos[key]
