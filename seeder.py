import csv
import random

# Número de usuarios
num_users = 100000

# Generar datos de ejemplo y escribir al archivo CSV
with open('data.csv', 'w', newline='') as csvfile:
    fieldnames = ['usuario', 'pelicula1', 'pelicula2', 'pelicula3']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Escribir encabezados
    writer.writeheader()

    # Generar datos aleatorios
    for user_id in range(1, num_users + 1):
        row_data = {
            'usuario': f'User{user_id}',
            'pelicula1': random.randint(1, 5),
            'pelicula2': random.randint(1, 5),
            'pelicula3': random.randint(1, 5)
        }
        writer.writerow(row_data)

print('Archivo CSV generado con éxito: data.csv')
