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

    # Generar gráficos para cada categoría
    plots.append(generar_plot(row[['Masculino', 'Femenino']], 'Distribución por Género', ['skyblue', 'lightpink']))
    plots.append(generar_plot(row[['Menor de 15 años', '15-18 años', '19-24 años', '25 años o más']],
                               'Distribución por Edad', 'lightgreen'))
    plots.append(generar_plot(row[['San pedro pinula', 'Jalapa', 'monjas', 'San manuel chaparron',
                                    'San carlos alzatate', 'San luis jilotepeque', 'mataquescuintla']],
                               'Distribución por Zona', 'orange', rotacion=45))

    return render_template('index.html', plots=plots) 

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
        ("Educativo.xlsx", "¿Consumes frecuentemente contenido educativo en redes sociales?", 'lightblue', "Algunos usuarios consumen contenido educativo con frecuencia.")
    ]

    for archivo, titulo, color, descripcion in archivos:
        path = os.path.join(UPLOAD_FOLDER, archivo)
        df = pd.read_excel(path)
        series = df.iloc[0]
        plot = generar_plot(series, titulo, color)
        plot_descriptions.append((plot, descripcion))

    return render_template('segunda.html', plot_descriptions=plot_descriptions)



if __name__ == '__main__':
    app.run(debug=True) # Ejecuta
