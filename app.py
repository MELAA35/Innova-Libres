from flask import Flask, render_template, jsonify, request, url_for, redirect
from pathlib import Path
import json, uuid

app = Flask(__name__)
DATA_PATH = Path("data/bracket.json")

# ------- Utilidades ---------
DEFAULT_PLAYERS = [f"Jugador {i+1}" for i in range(32)]

def init_bracket():
    """Crea un JSON con llaves vacías si no existe"""
    rounds = 5  # 32→16→8→4→2→1 campeón
    bracket = {"players": DEFAULT_PLAYERS, "matches": {}}
    match_id = 1
    size = 32
    for r in range(rounds):
        for m in range(size // 2):
            bracket["matches"][str(match_id)] = {
                "round": r + 1,
                "teamA": None,
                "teamB": None,
                "winner": None,
            }
            match_id += 1
        size //= 2
    DATA_PATH.parent.mkdir(exist_ok=True)
    DATA_PATH.write_text(json.dumps(bracket, indent=2, ensure_ascii=False))

if not DATA_PATH.exists():
    init_bracket()

# ------- Rutas ---------------
@app.route("/")
def index():
    return render_template("inicio.html")

equipos=[]
@app.route('/clasificacion')
def clasificacion():
    equipos_ordenados = sorted(equipos, key=lambda x: x['puntos'], reverse=True)
    return render_template('clasificacion.html', equipos=equipos_ordenados)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    puntos = request.form['puntos']
    if nombre and puntos.isdigit():
        equipo_existente = next((e for e in equipos if e['nombre'] == nombre), None)
        if not equipo_existente:
            equipos.append({'nombre': nombre, 'puntos': int(puntos)})
    return redirect(url_for('clasificacion'))

@app.route('/eliminar/<nombre>')
def eliminar(nombre):
    global equipos
    equipos = [e for e in equipos if e['nombre'] != nombre]
    return redirect(url_for('clasificacion'))

@app.route('/actualizar/<nombre>', methods=['POST'])
def actualizar(nombre):
    nuevos_puntos = int(request.form['puntos'])
    for equipo in equipos:
        if equipo['nombre'] == nombre:
            equipo['puntos'] = nuevos_puntos
            break
    return redirect(url_for('clasificacion'))

@app.route('/ganador')
def ganador():
    if equipos:
        equipo_ganador = max(equipos, key=lambda e: e['puntos'])
        return render_template('ganador.html', nombre=equipo_ganador['nombre'])
    return render_template('ganador.html', nombre="(sin equipos)")


if __name__ == "__main__":
    app.run(debug=True)