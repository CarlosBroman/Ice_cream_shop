import pandas as pd
import datetime
import matplotlib.pyplot as plt


language = input("Select language: Español / English ").capitalize()

if language == "Español":
    welcome = "Bienvenido a la Terraza Miramar"
    options = "¿Qué quieres: movimiento / grafico / stocks? "
    chose_flavour = "¿Qué sabor? "
    chose_quantity = "¿Cantidad? "
    chose_operation = "¿Entrada o salida? "
    unexisting_stock_statement =  "no existe en tu stock, ¿crear nuevo sabor? (s / n) "
    more_entries = "¿Quieres ingresar otra entrada? (s/n): "

elif language =="English":
    welcome = "Welcome to Terraza Miramar"
    options = "Choose: movement / chart / stocks"
    chose_flavour = "What flavor? "
    chose_quantity = "Quantity? "
    chose_operation = "Input or output? "
    unexisting_stock_statement =  "it does not exist in your stock, create a new flavor? (y / n) "
    more_entries = "Do you want to enter another record? (y/n): "


csv_file_name = "ice_cream_data.csv"

print(welcome)

existing_df = pd.read_csv(csv_file_name)
ids = existing_df["ID"].tolist()
helados = existing_df["Helado"].tolist()
cantidades = existing_df["Cantidad"].tolist() 
operaciones = existing_df["Operacion"].tolist() 
stocks = existing_df["Stock"].tolist()
dates = existing_df["Fecha"].tolist()
horas = existing_df["Hora"].tolist()
# Group the DataFrame by "Helado" and sum the "Stock" values for each flavorespañ
ice_cream_stock = existing_df.groupby("Helado")["Stock"].sum().reset_index()

program = input(options).capitalize()

if program == "Movimiento" or program == "Movement":
    now = datetime.datetime.now()
    while True:
        
        id = len(ids)
        helado = input(chose_flavour).capitalize()
        cantidad = int(input(chose_quantity))
        operacion = input(chose_operation).capitalize()
        
        if helado in existing_df["Helado"].values:
            stock = existing_df[existing_df["Helado"] == helado]["Stock"].iloc[-1]
        else:
            nuevo_sabor = input(f"{helado} {unexisting_stock_statement}")
            if nuevo_sabor.lower() != 's':
                continue
            stock = 0      

        ids.append(id)
        helados.append(helado)
        operaciones.append(operacion)
        cantidades.append(cantidad)
        
        if operacion == "Entrada" or operacion == "Input":
            stock = stock + cantidad
        elif operacion == "Salida" or operacion =="Output":
            stock = stock - cantidad
        stocks.append(stock)
        
        date = now.strftime("%Y-%m-%d")  # Format the current date and time
        hora = now.strftime("%H:%M:%S")
        dates.append(date)
        horas.append(hora)
        
        another_entry = input(more_entries)
        if another_entry.lower() != 's':
            break

    # Create a dictionary from the lists
    data = {
        "ID": ids,
        "Helado": helados,
        "Cantidad": cantidades,
        "Operacion": operaciones,
        "Stock": stocks,
        "Fecha": dates,
        "Hora" : horas,
    }

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)

    # Save DataFrame to an Excel file
    csv_file_name = "ice_cream_data.csv"
    df.to_csv(csv_file_name, index=False)

    print("\nDataFrame:")
    print(df)
    print(f"\nDataFrame saved to {csv_file_name}")


elif program == "Grafico" or program =="Chart":

    plt.figure(figsize=(8, 8))
    plt.pie(ice_cream_stock["Stock"], labels=ice_cream_stock["Helado"], autopct="%1.1f%%", startangle=140)
    plt.title("Ice Cream Stocks")
    plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

elif program == "Stocks":
    print(ice_cream_stock )