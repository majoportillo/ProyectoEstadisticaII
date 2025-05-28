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

    # ¿Cuentas con redes sociales?
    df1 = pd.read_excel(os.path.join(UPLOAD_FOLDER, 'Cuentas_con_redes.xlsx')) #lee el arcihvo de excel
    series1 = df1.iloc[0] #toma la primera fila
    plot1 = generar_plot(series1, '¿Cuentas con redes sociales?', ['green', 'red']) #genera la grafica
    desc1 = "La mayoría de los encuestados indicaron si tener redes sociales." #genera la descripcion del grafico
    plot_descriptions.append((plot1, desc1)) # lo agrega a una listita

    # ¿Cuál red social usas con mayor frecuencia?
    df2 = pd.read_excel(os.path.join(UPLOAD_FOLDER, 'Red_Social_Frecuente.xlsx'))
    series2 = df2.iloc[0]
    plot2 = generar_plot(series2, 'Red Social de Uso Frecuente', 'blue')
    desc2 = "Instagram y Facebook son las redes más frecuentemente usadas."
    plot_descriptions.append((plot2, desc2))

    # ¿Cuántas horas al día usas redes sociales?
    df3 = pd.read_excel(os.path.join(UPLOAD_FOLDER, 'Horas_al_dia.xlsx'))
    series3 = df3.iloc[0]
    plot3 = generar_plot(series3, 'Horas al día en Redes Sociales', 'orange')
    desc3 = "La mayoría pasa entre 2 a 4 horas al día en redes sociales."
    plot_descriptions.append((plot3, desc3))

    # ¿Qué propósito principal tienes al usar redes sociales?
    df4 = pd.read_excel(os.path.join(UPLOAD_FOLDER, 'Proposito.xlsx'))
    series4 = df4.iloc[0]
    plot4 = generar_plot(series4, 'Propósito del Uso de Redes Sociales', 'purple')
    desc4 = "El entretenimiento es el propósito más común para usar redes sociales."
    plot_descriptions.append((plot4, desc4))

    #¿Publicas contenido regularmente?
    df5 = pd.read_excel(os.path.join(UPLOAD_FOLDER, 'Publicar_contenido.xlsx'))
    series5 = df5.iloc[0]
    plot5 = generar_plot(series5, '¿Publicas contenido regularmente?', ['teal', 'gray'])
    desc5 = "Una minoría de los encuestados publica contenido regularmente."
    plot_descriptions.append((plot5, desc5))

    return render_template('segunda.html', plot_descriptions=plot_descriptions)



if __name__ == '__main__':
    app.run(debug=True) # Ejecuta
