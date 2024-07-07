import requests

Referees = ['Craig Alexander Thomson', 'Robert Madden', 'Peter Munch Larsen', 'Michael Johansen', 'Jorgen Daugbjerg Burchardt',
            'Steven McLean', 'Lars Christoffersen', 'Mads-Kristoffer Kristoffersen', 'Sandi Putros', 'Peter Kjaersgaard-Andersen',
            'Anders Poulsen', 'Morten Krogh', 'Michael Tykgaard', 'Mads Kristoffer Kristoffersen', 'Peter Rasmussen',
            'Dennis Mogensen', 'Jens Maae', 'Jorgen Daugbjerg Nielsen', 'Jens Grabski Maae', 'O. Kronlykke', 'J. Daugbjerg Burchardt',
            'E. Boric', 'A. Poulsen', 'J. Rosenkrands Vinther', 'D. Rasmussen']

class WorldCup:
    def __init__(self, year, host, teams, champion, runner_up, top_scorer, attendance, attendance_av, matches):
        self.year = year
        self.host = host
        self.teams = teams
        self.champion = champion
        self.runner_up = runner_up
        self.top_scorer = top_scorer
        self.attendance = attendance
        self.attendance_av = attendance_av
        self.matches = matches

def obtener_worldcups(base_url):
    url = f"{base_url}/api/worldcup"
    response = requests.get(url)
    if response.status_code == 200:
        worldcups = response.json()
        return [crear_worldcup(wc) for wc in worldcups]
    else:
        print(f"Error al obtener los datos: {response.status_code}")
        return None

def crear_worldcup(data):
    return WorldCup(
        data["Year"], data["Host"], data["Teams"], data["Champion"],
        data["Runner-Up"], data["TopScorer"], data["Attendance"],
        data["AttendanceAv"], data["Matches"]
    )

def agregar_worldcup(base_url, worldcup):
    url = f"{base_url}/api/worldcup/agregar"
    data = {
        "Year": worldcup.year,
        "Host": worldcup.host,
        "Teams": worldcup.teams,
        "Champion": worldcup.champion,
        "Runner-Up": worldcup.runner_up,
        "TopScorer": worldcup.top_scorer,
        "Attendance": worldcup.attendance,
        "AttendanceAv": worldcup.attendance_av,
        "Matches": worldcup.matches
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print("World Cup agregada exitosamente")
    else:
        print(f"Error al agregar la World Cup: {response.status_code}")

def actualizar_worldcup(base_url, year, updates):
    url = f"{base_url}/api/worldcup/update/{year}"
    response = requests.put(url, json=updates)
    if response.status_code == 200:
        print("World Cup actualizada exitosamente")
    else:
        print(f"Error al actualizar la World Cup: {response.status_code}")

def eliminar_worldcup(base_url, year):
    url = f"{base_url}/api/worldcup/delete/{year}"
    response = requests.delete(url)
    if response.status_code == 200:
        print("World Cup eliminada exitosamente")
    else:
        print(f"Error al eliminar la World Cup: {response.status_code}")

def agregar_arbitro(base_url, year, referee):
    url = f"{base_url}/api/worldcup/update/{year}"
    updates = {"Referee": referee}
    response = requests.put(url, json=updates)
    if response.status_code == 200:
        print("Árbitro agregado exitosamente")
    else:
        print(f"Error al agregar el árbitro: {response.status_code}")

def main():
    base_url = "http://127.0.0.1:4000"
    while True:
        print("Opciones")
        print("1: Ver todas las Copas del Mundo")
        print("2: Ver una Copa del Mundo por año")
        print("3: Agregar una nueva Copa del Mundo")
        print("4: Actualizar una Copa del Mundo existente")
        print("5: Eliminar una Copa del Mundo existente")
        print("6: Agregar un Árbitro a un mundial existente")
        print("7: Salir")

        option = int(input("Selecciona una opción: "))

        if option == 1:
            worldcups = obtener_worldcups(base_url)
            if worldcups:
                for wc in worldcups:
                    print(f"Año: {wc.year}, Sede: {wc.host}, Campeón: {wc.champion}, Subcampeón: {wc.runner_up}, Goleador: {wc.top_scorer}")

        elif option == 2:
            year = int(input("Ingresa el año de la Copa del Mundo: "))
            worldcups = obtener_worldcups(base_url)
            wc = next((wc for wc in worldcups if wc.year == year), None)
            if wc:
                print(f"Año: {wc.year}, Sede: {wc.host}, Campeón: {wc.champion}, Subcampeón: {wc.runner_up}, Goleador: {wc.top_scorer}")
            else:
                print("Copa del Mundo no encontrada")

        elif option == 3:
            year = int(input("Año: "))
            host = input("Sede: ")
            teams = int(input("Equipos: "))
            champion = input("Campeón: ")
            runner_up = input("Subcampeón: ")
            top_scorer = input("Goleador: ")
            attendance = int(input("Asistencia: "))
            attendance_av = int(input("Promedio de asistencia: "))
            matches = int(input("Partidos: "))
            new_worldcup = WorldCup(year, host, teams, champion, runner_up, top_scorer, attendance, attendance_av, matches)
            agregar_worldcup(base_url, new_worldcup)

        elif option == 4:
            year = int(input("Año de la Copa del Mundo a actualizar: "))
            updates = {}
            print("Ingresa los nuevos valores (deja en blanco para no cambiar)")
            host = input("Sede: ")
            if host:
                updates["Host"] = host
            champion = input("Campeón: ")
            if champion:
                updates["Champion"] = champion
            runner_up = input("Subcampeón: ")
            if runner_up:
                updates["Runner-Up"] = runner_up
            top_scorer = input("Goleador: ")
            if top_scorer:
                updates["TopScorer"] = top_scorer
            attendance = input("Asistencia: ")
            if attendance:
                updates["Attendance"] = int(attendance)
            attendance_av = input("Promedio de asistencia: ")
            if attendance_av:
                updates["AttendanceAv"] = int(attendance_av)
            matches = input("Partidos: ")
            if matches:
                updates["Matches"] = int(matches)
            actualizar_worldcup(base_url, year, updates)

        elif option == 5:
            year = int(input("Año de la Copa del Mundo a eliminar: "))
            eliminar_worldcup(base_url, year)

        elif option == 6:
            year = int(input("Año de la Copa del Mundo: "))
            print("Selecciona un árbitro:")
            for i, referee in enumerate(Referees):
                print(f"{i + 1}: {referee}")
            referee_index = int(input("Número del árbitro: ")) - 1
            referee = Referees[referee_index]
            agregar_arbitro(base_url, year, referee)

        elif option == 7:
            break

main()