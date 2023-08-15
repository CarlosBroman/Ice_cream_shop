import pandas as pd
import datetime
import matplotlib.pyplot as plt

print("Hello to the Terraza Miramar")

csv_file_name = "ice_cream_data.csv"
existing_df = pd.read_csv(csv_file_name)
ids = existing_df["ID"].tolist()
helados = existing_df["Helado"].tolist()
cantidades = existing_df["Cantidad"].tolist() 
operaciones = existing_df["Operacion"].tolist() 
stocks = existing_df["Stock"].tolist()
dates = existing_df["Fecha"].tolist()
horas = existing_df["Hora"].tolist()
horas_numero = existing_df["Hora numero"].tolist()

programa = input("¿Qué quieres: movimiento / grafico / stocks ").capitalize()

if programa == "Movimiento":
    now = datetime.datetime.now()
    while True:
        
        id = len(ids)
        helado = input(f"¿Qué sabor? ").capitalize()
        cantidad = int(input("¿Cantidad? "))
        operacion = input("¿Entrada o salida? ").capitalize()
        
        if helado in existing_df["Helado"].values:
            stock = existing_df[existing_df["Helado"] == helado]["Stock"].iloc[-1]
        else:
            nuevo_sabor = input(f"El {helado} no existe en tu stock, ¿crear nuevo sabor? (s / n)")
            if nuevo_sabor.lower() != 's':
                continue
            stock = 0
            

        ids.append(id)
        helados.append(helado)
        operaciones.append(operacion)
        cantidades.append(cantidad)
        
        if operacion == "Entrada":
            stock = stock + cantidad
        elif operacion == "Salida":
            stock = stock - cantidad
        stocks.append(stock)
        
        date = now.strftime("%Y-%m-%d")  # Format the current date and time
        hora = now.strftime("%H:%M:%S")
        hora_numero = time_numeric = now.hour * 3600 + now.minute * 60 + now.second
        horas_numero.append(hora_numero)
        dates.append(date)
        horas.append(hora)
        
        another_entry = input("¿Quieres ingresar otra entrada? (s/n): ")
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
        "Hora numero": horas_numero
    }

    # Create a DataFrame from the dictionary
    df = pd.DataFrame(data)

    # Save DataFrame to an Excel file
    csv_file_name = "ice_cream_data.csv"
    df.to_csv(csv_file_name, index=False)

    print("\nDataFrame:")
    print(df)
    print(f"\nDataFrame saved to {csv_file_name}")
    
elif programa == "Grafico":
    plt.figure(figsize=(10, 6))

    unique_helados = existing_df['Helado'].unique()

    for helado in unique_helados:
        helado_df = existing_df[existing_df['Helado'] == helado]
        plt.step(helado_df['Hora numero'], helado_df['Stock'], where='post', label=helado)

    plt.xlabel('Time')
    plt.ylabel('Stock')
    plt.title('Stock vs Time')

    # Customize the x-axis tick locations and labels
    hora_labels = existing_df.groupby('Hora numero')['Hora'].first().reset_index(drop=True)
    hora_ticks = existing_df['Hora numero'].unique()
    plt.xticks(hora_ticks, hora_labels, rotation=45)

    plt.legend()
    plt.tight_layout()
    plt.show()
    
elif programa == "Stocks":
    unique_helados = existing_df['Helado'].unique()

    for helado in unique_helados:
        last_stock = existing_df[existing_df["Helado"] == helado]["Stock"].iloc[-1]
        print(f"{helado}: {last_stock}")