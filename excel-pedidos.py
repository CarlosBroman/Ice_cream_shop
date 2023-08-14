import pandas as pd

print("Hello to the Terraza Miramar")

csv_file_name = "ice_cream_data.csv"
existing_df = pd.read_csv(csv_file_name)
ids = existing_df["ID"].tolist()
helados = existing_df["Helado"].tolist()
cantidades = existing_df["Cantidad"].tolist() 
operaciones = existing_df["Operacion"].tolist() 
stocks = existing_df["Stock"].tolist()


while True:
    id = len(ids)
    helado = input(f"¿Qué sabor? ")
    cantidad = int(input("¿Cantidad? "))
    operacion = input("¿Entrada o salida? ")
    stock = existing_df[existing_df["Helado"] == helado]["Stock"].iloc[-1]

    ids.append(id)
    helados.append(helado)
    operaciones.append(operacion)
    cantidades.append(cantidad)
    
    if operacion == "entrada":
        stock = stock + cantidad
    elif operacion == "salida":
        stock = stock - cantidad
    stocks.append(stock)
    
    another_entry = input("¿Quieres ingresar otra entrada? (s/n): ")
    if another_entry.lower() != 's':
        break

# Create a dictionary from the lists
data = {
    "ID": ids,
    "Helado": helados,
    "Cantidad": cantidades,
    "Operacion": operaciones,
    "Stock": stocks
}

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

# Save DataFrame to an Excel file
csv_file_name = "ice_cream_data.csv"
df.to_csv(csv_file_name, index=False)

print("\nDataFrame:")
print(df)
print(f"\nDataFrame saved to {csv_file_name}")