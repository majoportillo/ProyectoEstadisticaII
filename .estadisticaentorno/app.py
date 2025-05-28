from flask import Flask, render_template #importar Flask y render_template
import pandas as pd # importar pandas para manejar datos en excel
import os
import matplotlib # importar matplotlib para graficar 
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads' # carpeta donde estan los archivos subidos
PLOT_FOLDER = 'static/plots' # carpeta donde estan los graficos
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # crear la carpeta si no existe
os.makedirs(PLOT_FOLDER, exist_ok=True) # crear la carpeta de graficos si no existe

def generar_plot(series, titulo, color, rotacion=0): # función para generar un gráfico de barras
    fig, ax = plt.subplots()
    series.plot(kind='bar', ax=ax, color=color)
    ax.set_title(titulo)
    ax.set_ylabel('Cantidad')
    if rotacion: 
        ax.set_xticklabels(series.index, rotation=rotacion, ha='right')
    fig.tight_layout() # ajusta el layout para que no choquen los elemento
    filename = f"{uuid.uuid4()}.png" 
    filepath = os.path.join(PLOT_FOLDER, filename) 
    fig.savefig(filepath) # guarda el gráfico en la carpeta de graficos
    plt.close(fig)
    return f'plots/{filename}' # devuelve la ruta del gráfico generado

@app.route('/')
def index():
    excel_file = os.path.join(UPLOAD_FOLDER, 'Datos_demograficos.xlsx') # ruta del archivo excel de datos demo 
    df = pd.read_excel(excel_file) #lee el excel
    row = df.iloc[0] # toma la primera fila

    plots = [] 

    # Genero
    plots.append(generar_plot(row[['Masculino', 'Femenino']], 'Distribución por Género', ['skyblue', 'lightpink']))
    plots.append(generar_plot(row[['Menor de 15 años', '15-18 años', '19-24 años', '25 años o más']],
                               'Distribución por Edad', 'lightgreen'))
    plots.append(generar_plot(row[['San pedro pinula', 'Jalapa', 'monjas', 'San manuel chaparron',
                                    'San carlos alzatate', 'San luis jilotepeque', 'mataquescuintla']],
                               'Distribución por Zona', 'orange', rotacion=45))

    return render_template('index.html', plots=plots) 

@app.route('/segunda') # ruta para la segunda página html
def segunda():
    excel_file = os.path.join(UPLOAD_FOLDER, 'Datos_demograficos.xlsx') # ruta del archivo excel de datos demo
    df = pd.read_excel(excel_file)
    row = df.iloc[0]

    plots = []

    # lista de gráficos para la segunda página
    plots.append(generar_plot(row[['Masculino', 'Femenino']], 'Repetición - Género', ['skyblue', 'lightpink']))
    plots.append(generar_plot(row[['Menor de 15 años', '15-18 años', '19-24 años', '25 años o más']],
                               'Repetición - Edad', 'purple'))
    plots.append(generar_plot(row[['Jalapa', 'San luis jilotepeque', 'mataquescuintla']],
                               'Zonas destacadas', 'salmon', rotacion=30))

    return render_template('segunda.html', plots=plots)

if __name__ == '__main__':
    app.run(debug=True) # Ejecuta la aplicación Flask en modo debug
