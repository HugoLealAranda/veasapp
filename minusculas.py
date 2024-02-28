import pandas as pd

# Ruta del archivo CSV original
archivo_original = r'C:\Users\hugol\OneDrive\Desktop\RENTALVEAS\DataFrameveas.csv'

# Leer el archivo CSV en un DataFrame
df = pd.read_csv(archivo_original, header=None)

# Convertir todas las letras del DataFrame a minúsculas
df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)

# Ruta para guardar el nuevo archivo CSV
archivo_nuevo = r'C:\Users\hugol\OneDrive\Desktop\RENTALVEAS\veas_minusculas.csv'

# Guardar el DataFrame modificado en un nuevo archivo CSV
df.to_csv(archivo_nuevo, index=False, header=False)

print("El nuevo archivo CSV 'veas_minusculas.csv' ha sido creado con éxito.")

