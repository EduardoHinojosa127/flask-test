# app.py
from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from scipy.spatial.distance import minkowski, euclidean, cityblock
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    data = pd.read_csv('data.csv', names=['usuario', 'pelicula1', 'pelicula2', 'pelicula3'])

    data[['pelicula1', 'pelicula2', 'pelicula3']] = data[['pelicula1', 'pelicula2', 'pelicula3']].apply(pd.to_numeric, errors='coerce')

    media_pelicula1 = data['pelicula1'].mean()
    media_pelicula2 = data['pelicula2'].mean()
    media_pelicula3 = data['pelicula3'].mean()

    distancia_minkowski = minkowski([media_pelicula1, media_pelicula2, media_pelicula3], [0, 0, 0], 1.5)
    distancia_euclidiana = euclidean([media_pelicula1, media_pelicula2, media_pelicula3], [0, 0, 0])
    distancia_manhattan = cityblock([media_pelicula1, media_pelicula2, media_pelicula3], [0, 0, 0])

    x = [0, distancia_manhattan, 0, 0]
    y = [0, 0, distancia_euclidiana, 0]
    minkowski_curve = [0, 0, distancia_minkowski, 0]

    plt.figure(figsize=(18, 5))

    plt.subplot(1, 2, 1)
    plt.bar(['Pelicula1', 'Pelicula2', 'Pelicula3'], [media_pelicula1, media_pelicula2, media_pelicula3], color=['skyblue', 'lightgreen', 'lightcoral'])
    for i, v in enumerate([media_pelicula1, media_pelicula2, media_pelicula3]):
        plt.text(i, v, f' {v:.4f}', ha='center', va='bottom', color='black', fontweight='bold')
    plt.xlabel('Películas')
    plt.ylabel('Media')
    plt.title('Media de Cada Película')

    plt.subplot(1, 2, 2)
    plt.plot(x[:3], y[:3], linestyle='-', color='red', label='Línea Manhattan')
    plt.plot(x[1:], y[1:], linestyle='-', color='red', label='Línea Euclidiana')
    plt.scatter(x, y, color='red')
    plt.text(distancia_manhattan / 2, -0.1, f'Distancia Manhattan: {distancia_manhattan:.4f}', ha='center', va='top', color='black', fontweight='bold')
    plt.text(distancia_manhattan + 0.1, distancia_euclidiana / 2, f'Distancia Euclidiana: {distancia_euclidiana:.4f}', ha='left', va='center', color='black', fontweight='bold')
    plt.text(distancia_manhattan / 2, distancia_euclidiana + 0.1, f'Distancia Minkowski: {distancia_minkowski:.4f}', ha='center', va='bottom', color='black', fontweight='bold')
    plt.xlabel('Distancia')
    plt.ylabel('Valor')
    plt.title('Distancias entre Medias de Películas')
    plt.legend()

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
