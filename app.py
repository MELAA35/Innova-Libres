from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'clave-secreta'  # Necesaria para usar session

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/clasificacion', methods=['GET', 'POST'])
def clasificacion():
    if 'rondas' not in session:
        session['rondas'] = []
        session['ganadores'] = []

    rondas = session['rondas']
    ganadores = session['ganadores']

    if request.method == 'POST':
        if not rondas:
            # Primera vez: cargar jugadores
            jugadores = [request.form.get(f'player{i}', f'Jugador {i}') for i in range(1, 33)]
            primera_ronda = [(jugadores[i], jugadores[i+1]) for i in range(0, 32, 2)]
            rondas = [primera_ronda]
            session['rondas'] = rondas
        else:
            # Procesar ronda actual
            ronda_actual = rondas[len(ganadores)]
            ganadores_ronda = []
            for i, (j1, j2) in enumerate(ronda_actual):
                ganador = request.form.get(f'ganador{len(ganadores)}_{i}')
                if ganador:
                    ganadores_ronda.append(ganador)

            if ganadores_ronda:
                ganadores.append(ganadores_ronda)
                session['ganadores'] = ganadores

                if len(ganadores_ronda) > 1:
                    nueva_ronda = [(ganadores_ronda[i], ganadores_ronda[i+1]) for i in range(0, len(ganadores_ronda), 2)]
                    rondas.append(nueva_ronda)
                    session['rondas'] = rondas
                else:
                    # Final
                    rondas.append([(ganadores_ronda[0], "")])
                    session['rondas'] = rondas
                    session['ganador'] = ganadores_ronda[0]

    return render_template('clasificacion.html', rondas=rondas, ganadores=ganadores)

@app.route('/ganador')
def ganador():
    return render_template('ganador.html', ganador=session.get('ganador', ''))

@app.route('/reiniciar')
def reiniciar():
    session.clear()
    return redirect(url_for('clasificacion'))

if __name__ == '__main__':
    app.run(debug=True)
