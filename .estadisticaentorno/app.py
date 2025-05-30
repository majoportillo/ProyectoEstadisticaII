from flask import Flask, render_template, request
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import uuid
import numpy as np
from scipy.stats import norm

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PLOT_FOLDER = 'static/plots'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOT_FOLDER, exist_ok=True)

# --------- Función para gráficas de barras ---------
def generar_plot(series, titulo, color, rotacion=0):
    fig, ax = plt.subplots()
    series.plot(kind='bar', ax=ax, color=color)
    ax.set_title(titulo)
    ax.set_ylabel('Cantidad')
    if rotacion:
        ax.set_xticklabels(series.index, rotation=rotacion, ha='right')
    fig.tight_layout()
    filename = f"{uuid.uuid4()}.png"
    filepath = os.path.join(PLOT_FOLDER, filename)
    fig.savefig(filepath)
    plt.close(fig)
    return f'plots/{filename}'

# --------- Función para la curva normal ---------
def calcular_aproximacion_normal(n, x1, x2, p):
    q = 1 - p
    mu = n * p
    sigma = np.sqrt(n * p * q) if n > 0 else 0.0001
    z1 = (x1 - mu) / sigma
    z2 = (x2 - mu) / sigma
    probabilidad = norm.cdf(z2) - norm.cdf(z1)
    return probabilidad, z1, z2, mu, sigma

def graficar_curva(mu, sigma, z1, z2, tipo):
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 500)
    y = norm.pdf(x, mu, sigma)
    fig, ax = plt.subplots()
    ax.plot(x, y, 'b-', label='Curva Normal')
    ax.set_title('Curva Normal Binomial')
    ax.set_xlabel('Número de éxitos')
    ax.set_ylabel('Densidad')
    if tipo == 'exacto' or tipo == 'entre':
        x_fill = np.linspace(mu + z1*sigma, mu + z2*sigma, 300)
        ax.fill_between(x_fill, norm.pdf(x_fill, mu, sigma), color='skyblue', alpha=0.5)
    elif tipo == 'mayor':
        x_fill = np.linspace(mu + z1*sigma, mu + 4*sigma, 300)
        ax.fill_between(x_fill, norm.pdf(x_fill, mu, sigma), color='lightgreen', alpha=0.5)
    elif tipo == 'menor':
        x_fill = np.linspace(mu - 4*sigma, mu + z2*sigma, 300)
        ax.fill_between(x_fill, norm.pdf(x_fill, mu, sigma), color='salmon', alpha=0.5)
    filename = f"{uuid.uuid4()}.png"
    filepath = os.path.join(PLOT_FOLDER, filename)
    fig.tight_layout()
    fig.savefig(filepath)
    plt.close(fig)
    return f'plots/{filename}'

# --------- Portada y Datos Demográficos ---------
@app.route('/')
def index():
    excel_file = os.path.join(UPLOAD_FOLDER, 'Datos_demograficos.xlsx')
    df = pd.read_excel(excel_file)
    row = df.iloc[0]
    plots = []
    plots.append(generar_plot(row[['Masculino', 'Femenino']], 'Distribución por Género', ['skyblue', 'lightpink']))
    plots.append(generar_plot(row[['Menor de 15 años', '15-18 años', '19-24 años', '25 años o más']], 'Distribución por Edad', 'lightgreen'))
    plots.append(generar_plot(row[['San pedro pinula', 'Jalapa', 'monjas', 'San manuel chaparron',
                                   'San carlos alzatate', 'San luis jilotepeque', 'mataquescuintla']],
                              'Distribución por Zona', 'orange', rotacion=45))
    return render_template('index.html', plots=plots)

# --------- Gráficas de preguntas generales ---------
@app.route('/segunda')
def segunda():
    plot_descriptions = []
    archivos = [
        ("Cuentas_con_redes.xlsx", "¿Cuentas con redes sociales?", ['green', 'red'], "La mayoría de los encuestados indicaron sí tener redes sociales."),
        ("Frecuencia_Tiktok.xlsx", "¿Utiliza TikTok con mayor frecuencia?", 'blue', "TikTok es una de las redes más frecuentemente utilizadas."),
        ("Concentracion.xlsx", "¿Crees que las redes sociales afectan negativamente tu concentración al estudiar?", 'red', "Muchos creen que las redes sociales afectan su concentración al estudiar."),
        ("Instagram_frecuencia.xlsx", "¿Utiliza Instagram con mayor frecuencia?", 'purple', "Instagram destaca como una de las redes favoritas."),
        ("Redes_Noche.xlsx", "¿Usas redes sociales por la noche?", 'orange', "Una gran cantidad de personas usa redes sociales por la noche."),
        ("Frecuencia_horas.xlsx", "¿Usas redes sociales con una frecuencia mayor a 3 horas?", 'cyan', "El uso superior a 3 horas al día es común entre los encuestados."),
        ("Publicas_contenido.xlsx", "¿Publicas contenido regularmente?", ['teal', 'gray'], "Una minoría de los encuestados publica contenido regularmente."),
        ("Entretenimiento.xlsx", "¿Usas redes sociales principalmente para entretenimiento?", 'pink', "El entretenimiento es el principal motivo de uso."),
        ("Educativo.xlsx", "¿Consume frecuentemente contenido educativo en redes sociales?", 'lightblue', "Algunos usuarios consumen contenido educativo con frecuencia.")
    ]
    for archivo, titulo, color, descripcion in archivos:
        path = os.path.join(UPLOAD_FOLDER, archivo)
        df = pd.read_excel(path)
        series = df.iloc[0]
        plot = generar_plot(series, titulo, color)
        plot_descriptions.append((plot, descripcion))
    return render_template('segunda.html', plot_descriptions=plot_descriptions)

# --------- Módulo de Probabilidad ---------
@app.route('/probabilidad', methods=['GET', 'POST'])
def probabilidad():
    preguntas = [
        ("¿Cuentas con redes sociales?", "¿Cuentas con redes sociales?"),
        ("¿Utiliza TikTok con mayor frecuencia?", "¿Utiliza TikTok con mayor frecuencia?"),
        ("¿Crees que las redes sociales afectan negativamente tu concentración al estudiar?", "¿Crees que las redes sociales afectan negativamente tu concentración al estudiar?"),
        ("¿Utiliza Instagram con mayor frecuencia?", "¿Utiliza Instagram con mayor frecuencia?"),
        ("¿Usas redes sociales por en la noche?", "¿Usas redes sociales por en la noche?"),
        ("¿Usas redes sociales con una frecuencia mayor a 3 horas?", "¿Usas redes sociales con una frecuencia mayor a 3 horas?"),
        ("¿Publicas contenido regularmente?", "¿Publicas contenido regularmente?"),
        ("¿Usas redes sociales principalmente para entretenimiento?", "¿Usas redes sociales principalmente para entretenimiento?"),
        ("¿Consume frecuentemente contenido educativo en redes sociales?", "¿Consume frecuentemente contenido educativo en redes sociales?")
    ]
    zonas = [
        "Todos", "Jalapa", "San Pedro Pinula", "Monjas", "San Manuel Chaparron",
        "San Carlos Alzatate", "San Luis Jilotepeque", "Mataquescuintla"
    ]
    resultado = None
    plot_path = None
    advertencia = None

    if request.method == 'POST':
        pregunta = request.form['pregunta']
        tipo = request.form['tipo']
        x1 = int(request.form['x1'])
        x2 = int(request.form.get('x2', 0))
        genero = request.form['genero']
        zona = request.form['zona']

        df = pd.read_excel("uploads/Redes Sociales 1 (respuestas).xlsx")

        if genero != "Todos":
            df = df[df['¿Cuál es tu Género?'] == genero]
        if zona != "Todos":
            df = df[df['¿En dónde vives?'] == zona]

        n = len(df)
        if n == 0:
            p = 0
        else:
            p = (df[pregunta].str.lower().isin(['sí', 'si'])).mean()

        if n == 0:
            advertencia = "No hay datos para el subgrupo seleccionado."
        elif n * p < 5 or n * (1 - p) < 5:
            advertencia = "¡Advertencia! La aproximación normal NO es adecuada para este subgrupo (n·p < 5 o n·q < 5). Por favor, seleccione un grupo más grande."
        else:
            if tipo == "exacto":
                lim_inf = x1 - 0.5
                lim_sup = x1 + 0.5
            elif tipo == "mayor":
                lim_inf = x1 + 0.5
                lim_sup = n + 0.5
            elif tipo == "menor":
                lim_inf = -0.5
                lim_sup = x1 - 0.5
            elif tipo == "entre":
                lim_inf = x1 - 0.5
                lim_sup = x2 + 0.5
            else:
                lim_inf = lim_sup = 0

            prob, z1, z2, mu, sigma = calcular_aproximacion_normal(n, lim_inf, lim_sup, p)
            plot_path = graficar_curva(mu, sigma, z1, z2, tipo)
            resultado = {
                "probabilidad": prob * 100,
                "z1": z1,
                "z2": z2,
                "mu": mu,
                "sigma": sigma,
                "n": n,
                "p": p
            }

    return render_template("probabilidad.html", preguntas=preguntas, zonas=zonas, resultado=resultado, plot=plot_path, advertencia=advertencia)

if __name__ == '__main__':
    app.run(debug=True)
