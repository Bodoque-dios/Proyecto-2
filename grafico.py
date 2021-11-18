from matplotlib.figure import Figure
import matplotlib
from io import BytesIO
import base64

from datetime  import datetime

from oauth2client.service_account import ServiceAccountCredentials
import gspread


credential = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", ["https://spreadsheets.google.com/feeds",
                                                                                    "https://www.googleapis.com/auth/spreadsheets",
                                                                                    "https://www.googleapis.com/auth/drive.file",
                                                                                    "https://www.googleapis.com/auth/drive"])


client = gspread.authorize(credential)
Proyecto_2_db = client.open('Proyecto-2-db')

entradas = Proyecto_2_db.get_worksheet(1).get_all_records()[1::]
fechas_entradas_usuario = []
fechas_limpias = []

def grafico(id):
	
	fechas_entradas_usuario = []
	fechas_limpias = []
	fechas = []

	for i, entrada in enumerate(entradas):
		if entrada['id usuario'] == id:
			fechas_entradas_usuario.append(entrada['Fecha'])

	for fecha in fechas_entradas_usuario:
		fechas_limpias.append(datetime.strptime(fecha, '%d/%m/%Y'))

	fechas = matplotlib.dates.date2num(fechas_limpias )

	""" plt.plot(fechas,[i for i in range(len(fechas), 0 ,-1)])
	plt.plot_date(fechas,[i for i in range(len(fechas), 0 ,-1)])
	plt.grid()
	plt.gcf().autofmt_xdate()
 	"""
	fig = Figure()
	ax = fig.subplots()
	ax.plot(fechas,[i for i in range(len(fechas), 0 ,-1)])
	ax.plot_date(fechas,[i for i in range(len(fechas), 0 ,-1)])
	#ax.gcf().autofmt_xdate()
	ax.grid()
	# Save it to a temporary buffer.
	buf = BytesIO()
	fig.savefig(buf, format="png")
	# Embed the result in the html output.
	data = base64.b64encode(buf.getbuffer()).decode("ascii")
	return f"<img src='data:image/png;base64,{data}'/>", len(fechas_limpias)
