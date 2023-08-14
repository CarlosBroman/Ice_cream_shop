import pandas as pd

print("Hello to the Terraza Miramar")

# Create empty lists to store data
nombres = []
helados = []

while True:
    nombre = input("¿Cómo te llamas? ")
    helado = input(f"Hola, {nombre}, ¿Qué helado acabas de poner? ")

    # Append data to lists
    nombres.append(nombre)
    helados.append(helado)

    another_entry = input("¿Quieres ingresar otra entrada? (s/n): ")
    if another_entry.lower() != 's':
        break

# Create a dictionary from the lists
data = {
    "Nombre": nombres,
    "Helado": helados
}

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

# Save DataFrame to an Excel file
excel_file_name = "ice_cream_data.xlsx"
df.to_excel(excel_file_name, index=False)

print("\nDataFrame:")
print(df)
print(f"\nDataFrame saved to {excel_file_name}")