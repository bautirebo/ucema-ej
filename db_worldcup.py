import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def create_tables():
    conn = sqlite3.connect('worldcup.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS worldcup')
    c.execute('''
              CREATE TABLE worldcup
              (Year INTEGER PRIMARY KEY AUTOINCREMENT,
              Host TEXT,
              Teams INTEGER,
              Champion TEXT,
              RunnerUp TEXT,
              TopScorer TEXT,
              Attendance INTEGER,
              AttendanceAv INTEGER,
              Matches INTEGER,
              Referee TEXT)
              ''')
    conn.commit()
    conn.close()

create_tables()

def get_worldcup():
    conn = sqlite3.connect('worldcup.db')
    c = conn.cursor()
    c.execute('SELECT * FROM worldcup')
    worldcup = c.fetchall()
    conn.close()
    return worldcup

def add_worldcup_2(year, host, teams, champion, runner_up, top_scorer, attendance, attendance_av, matches, referee):
    conn = sqlite3.connect('worldcup.db')
    c = conn.cursor()
    c.execute('INSERT INTO worldcup (Year, Host, Teams, Champion, RunnerUp, TopScorer, Attendance, AttendanceAv, Matches, Referee) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (year, host, teams, champion, runner_up, top_scorer, attendance, attendance_av, matches, referee))  
    conn.commit()
    conn.close()

def update_worldcup(year, host, teams, champion, runner_up, top_scorer, attendance, attendance_av, matches, referee):
    conn = sqlite3.connect('worldcup.db')
    c = conn.cursor()
    c.execute('''
              UPDATE worldcup
              SET Host = ?, Teams = ?, Champion = ?, RunnerUp = ?, TopScorer = ?, Attendance = ?, AttendanceAv = ?, Matches = ?, Referee = ?
              WHERE Year = ?
              ''', (host, teams, champion, runner_up, top_scorer, attendance, attendance_av, matches, referee, year))
    conn.commit()
    conn.close()


# Función para eliminar un mundial de la base de datos
def delete_worldcup_2(year):
    conn = sqlite3.connect('worldcup.db')
    c = conn.cursor()
    c.execute('DELETE FROM worldcup WHERE Year = ?', (year,))
    conn.commit()
    conn.close()