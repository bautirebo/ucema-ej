from flask import Flask, jsonify, request
import pandas as pd
import requests
import sqlite3
import db_worldcup
from db_worldcup import get_worldcup, add_worldcup_2, create_tables, update_worldcup, delete_worldcup_2

# URL de la API
api_football_url = "https://api.sportmonks.com/v3/football/referees"

# Headers (incluyendo el token de autorización)
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'ah2IMULuqqt0ENs5ds8fyLagpeErsqfG0opPwrT7Z4FJFsnZaXVg3WyGbLUt'  # Reemplaza con tu token real
}

# Hacer la solicitud a la API
# Función para obtener árbitros de la API de terceros
def get_referee():
    response = requests.get(api_football_url, headers=headers)
    if response.status_code == 200:
        referees_data = response.json().get('data', [])
        return [referee['common_name'] for referee in referees_data]
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

referees = get_referee()

# Verifica que los árbitros se hayan agregado correctamente a la lista, osea imprime la lista
#print(referees)

# Nos devuelve los nombres de los referees

app = Flask(__name__)

# Datos en DataFrame
data = {
    "Year": [2022, 2018, 2014, 2010, 2006, 2002, 1998, 1994, 1990, 1986, 1982, 1978, 1974, 1970, 1966, 1962, 1958, 1954, 1950, 1938, 1934, 1930],
    "Host": ["Qatar", "Russia", "Brazil", "South Africa", "Germany", "Korea Republic", "France", "United States", "Italy", "Mexico", "Spain", "Argentina", "Germany", "Mexico", "England", "Chile", "Sweden", "Switzerland", "Brazil", "France", "Italy", "Uruguay"],
    "Teams": [32, 32, 32, 32, 32, 32, 32, 24, 24, 24, 24, 16, 16, 16, 16, 16, 16, 16, 13, 15, 16, 13],
    "Champion": ["Argentina", "France", "Germany", "Spain", "Italy", "Brazil", "France", "Brazil", "West Germany", "Argentina", "Italy", "Argentina", "West Germany", "Brazil", "England", "Brazil", "Brazil", "Germany", "Uruguay", "Italy", "Italy", "Uruguay"],
    "Runner-Up": ["France", "Croatia", "Argentina", "Netherlands", "France", "Germany", "Brazil", "Italy", "Argentina", "West Germany", "West Germany", "Netherlands", "Netherlands", "Italy", "West Germany", "Czechoslovakia", "Sweden", "Hungary", "Brazil", "Hungary", "Czechoslovakia", "Argentina"],
    "TopScorer": ["Kylian Mbappé", "Harry Kane", "James Rodríguez", "Wesley Sneijder", "Miroslav Klose", "Ronaldo - 8", "Davor Šuker", "Hristo Stoichkov", "Salvatore Schillaci", "Gary Lineker - 6", "Paolo Rossi - 6", "Mario Kempes", "Grzegorz Lato", "Gerd Müller", "Eusébio - 9", "Leonel Sánchez", "Just Fontaine", "Sándor Kocsis", "Ademir - 8", "Leônidas - 7", "Oldřich Nejedlý", "Guillermo Stábile"],
    "Attendance": [3404252, 3031768, 3429873, 3178856, 3352605, 2705337, 2903477, 3587538, 2516215, 2394031, 2109723, 1545791, 1865753, 1603975, 1563135, 893172, 819810, 768607, 1045246, 375700, 363000, 590549],
    "AttendanceAv": [53191, 47371, 53592, 49670, 52384, 42271, 45367, 68991, 48389, 46039, 40572, 40679, 49099, 50124, 48848, 27912, 23423, 29562, 47511, 20872, 21353, 32808],
    "Matches": [64, 64, 64, 64, 64, 64, 64, 52, 52, 52, 52, 38, 38, 32, 32, 32, 35, 26, 22, 18, 17, 18]
}
# Todo lo de data es lo que sacamos del csv, que más adelante vamos a sacar del repositorio de GitHub (va a estar el csv en el repositorio)

# A recordar, teams es la cantidad de equipos en cada mundial

df = pd.DataFrame(data)

@app.route("/")
def hello():
    return "Hola!, esta es nuestra api"

# Endpoint para obtener toda la tabla, osea todos los mundiales
@app.route('/api/worldcup', methods=['GET'])
def get_data():
    return jsonify(df.to_dict(orient='records'))

# Endpoint para obtener el top scorer de cada año
@app.route('/api/topscorer', methods=['GET'])
def get_topscorer():
    topscorers = df[['Year', 'TopScorer']].to_dict(orient='records')
    return jsonify(topscorers)

# Endpoint para obtener la cantidad de partidos jugados en cada país
@app.route('/api/matches', methods=['GET'])
def get_matches():
    matches = df[['Year', 'Host', 'Matches']].to_dict(orient='records')
    return jsonify(matches)

# Endpoint para agregar un nuevo mundial
@app.route("/api/worldcup/agregar", methods=["POST"])
def add_worldcup():
    worldcup_details = request.get_json()
    
    new_worldcup = {
        "Year": worldcup_details["Year"],
        "Host": worldcup_details["Host"],
        "Teams": worldcup_details["Teams"],
        "Champion": worldcup_details["Champion"],
        "Runner-Up": worldcup_details["Runner-Up"],
        "TopScorer": worldcup_details["TopScorer"],
        "Attendance": worldcup_details["Attendance"],
        "AttendanceAv": worldcup_details["AttendanceAv"],
        "Matches": worldcup_details["Matches"]
    }
    
    
    referee = worldcup_details.get("Referee", "Desconocido")
    
    # Agregar el nuevo mundial a la base de datos usando add_worldcup_2
    add_worldcup_2(
        new_worldcup["Year"],
        new_worldcup["Host"],
        new_worldcup["Teams"],
        new_worldcup["Champion"],
        new_worldcup["Runner-Up"],
        new_worldcup["TopScorer"],
        new_worldcup["Attendance"],
        new_worldcup["AttendanceAv"],
        new_worldcup["Matches"],
        referee
    )
    
    global df
    df = df._append(new_worldcup, ignore_index=True)  
    
    return jsonify({"message": "World Cup successfully added"}), 201

@app.route("/api/worldcup/delete/<int:Year>", methods=["DELETE"])
def delete_worldcup_endpoint(Year):
    global df
    if Year in df['Year'].values:
        df = df[df['Year'] != Year]
        
        # Elimina el mundial de la base de datos
        delete_worldcup_2(Year)
        
        return jsonify({"message": "World Cup successfully deleted"}), 200
    else:
        return jsonify({"message": "World Cup not found"}), 404

@app.route("/api/worldcup/update/<int:Year>", methods=["PUT"])
def update_worldcup_endpoint(Year):
    worldcup_details = request.get_json()
    
    global df
    for index, row in df.iterrows():
        if row["Year"] == Year:
            host = worldcup_details.get("Host", row["Host"])
            teams = worldcup_details.get("Teams", row["Teams"])
            champion = worldcup_details.get("Champion", row["Champion"])
            runner_up = worldcup_details.get("Runner-Up", row["Runner-Up"])
            top_scorer = worldcup_details.get("TopScorer", row["TopScorer"])
            attendance = worldcup_details.get("Attendance", row["Attendance"])
            attendance_av = worldcup_details.get("AttendanceAv", row["AttendanceAv"])
            matches = worldcup_details.get("Matches", row["Matches"])
            referee = worldcup_details.get("Referee", "Desconocido")  

            # Actualiza el DataFrame
            df.at[index, "Host"] = host
            df.at[index, "Teams"] = teams
            df.at[index, "Champion"] = champion
            df.at[index, "Runner-Up"] = runner_up
            df.at[index, "TopScorer"] = top_scorer
            df.at[index, "Attendance"] = attendance
            df.at[index, "AttendanceAv"] = attendance_av
            df.at[index, "Matches"] = matches
            
            # Actualiza la base de datos
            update_worldcup(Year, host, teams, champion, runner_up, top_scorer, attendance, attendance_av, matches, referee)

            return jsonify({"message": "World Cup successfully updated"}), 200

    return jsonify({"message": "World Cup not found"}), 404



if __name__ == "__main__":
    create_tables()
    
    # Agrega todos los datos del DataFrame a la base de datos
    for index, row in df.iterrows():
        add_worldcup_2(
            row["Year"],
            row["Host"],
            row["Teams"],
            row["Champion"],
            row["Runner-Up"],
            row["TopScorer"],
            row["Attendance"],
            row["AttendanceAv"],
            row["Matches"],
            "Desconocido"  
        )
    
    app.run(debug=True, port=4000)