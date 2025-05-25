from flask import Flask, render_template, request
import pandas as pd
import os
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PLOT_FOLDER = 'static/plots'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    plots = []
    resultado = None
    grafica_prob = None
    data_uploaded = False

    if request.method == 'POST':
        if 'file' in request.files and request.files['file'].filename != '':
            # Carga de archivo
            file = request.files['file']
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            df = pd.read_excel(filepath)
            data_uploaded = True

            for col in df.select_dtypes(include='number').columns:
                fig, ax = plt.subplots()
                df[col].hist(ax=ax)
                ax.set_title(f'Distribución de {col}')
                plot_name = f"{uuid.uuid4()}.png"
                plot_path = os.path.join(PLOT_FOLDER, plot_name)
                fig.savefig(plot_path)
                plt.close(fig)
                plots.append(f'plots/{plot_name}')

        elif 'calcular' in request.form:
            # Cálculo de probabilidad
            tipo = request.form['tipo']
            media = float(request.form['media'])
            desv = float(request.form['desviacion'])
            x = np.linspace(media - 4*desv, media + 4*desv, 1000)
            y = stats.norm.pdf(x, media, desv)

            fig, ax = plt.subplots()
            ax.plot(x, y, label='Distribución Normal')

            if tipo == 'exacto':
                valor = float(request.form['valor'])
                resultado = stats.norm.pdf(valor, media, desv)
                ax.fill_between(x, y, where=(np.abs(x - valor) < 0.01), color='red')
            elif tipo == 'mayor':
                valor = float(request.form['valor'])
                resultado = 1 - stats.norm.cdf(valor, media, desv)
                ax.fill_between(x, y, where=(x > valor), color='skyblue')
            elif tipo == 'menor':
                valor = float(request.form['valor'])
                resultado = stats.norm.cdf(valor, media, desv)
                ax.fill_between(x, y, where=(x < valor), color='orange')
            elif tipo == 'entre':
                a = float(request.form['valor_min'])
                b = float(request.form['valor_max'])
                resultado = stats.norm.cdf(b, media, desv) - stats.norm.cdf(a, media, desv)
                ax.fill_between(x, y, where=(x > a) & (x < b), color='green')

            ax.set_title('Distribución Normal')
            plot_name = f"{uuid.uuid4()}.png"
            plot_path = os.path.join(PLOT_FOLDER, plot_name)
            fig.savefig(plot_path)
            plt.close(fig)
            grafica_prob = f'plots/{plot_name}'

    return render_template('index.html', plots=plots, resultado=resultado, grafica_prob=grafica_prob, data_uploaded=data_uploaded)

if __name__ == '__main__':
    app.run(debug=True)
