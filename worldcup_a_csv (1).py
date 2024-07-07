import sqlite3
import pandas as pd

#Conectamos con a la base de datos
ruta_base = 'worldcup.db'
conexion = sqlite3.connect(ruta_base)
cursor = conexion.cursor()


cursor.execute("SELECT * FROM worldcup")
data = cursor.fetchall()

#Obtenenemos los nombres de las columnas
columnas = [description[0] for description in cursor.description]

#Creamos un DataFrame con los datos obtenidos
df = pd.DataFrame(data, columns=columnas)

#Guarda el DataFrame en un archivo CSV
df.to_csv('worldcup_data.csv', index=False)

#Terminamos la conexión a la base de datos
conexion.close()