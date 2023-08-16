import pandas as pd
import datetime
import matplotlib.pyplot as plt

def save_to_csv(dataframe):
    csv_file_name = "ice_cream_data.csv"
    dataframe.to_csv(csv_file_name, index=False)
    print("\nDataFrame:")
    print(dataframe)
    print(f"\nDataFrame saved to {csv_file_name}")

def add_entry(existing_df):
    now = datetime.datetime.now()
    
    id = len(existing_df) + 1
    helado = input(f"¿Qué sabor? ").capitalize()
    cantidad = int(input("¿Cantidad? "))
    operacion = input("¿Entrada o salida? ").capitalize()

    if helado in existing_df["Helado"].values:
        stock = existing_df[existing_df["Helado"] == helado]["Stock"].iloc[-1]
    else:
        nuevo_sabor = input(f"El {helado} no existe en tu stock, ¿crear nuevo sabor? (s / n)")
        if nuevo_sabor.lower() != 's':
            return existing_df
        stock = 0

    new_entry = {
        "ID": id,
        "Helado": helado,
        "Cantidad": cantidad,
        "Operacion": operacion,
        "Stock": stock,
        "Fecha": now.strftime("%Y-%m-%d"),
        "Hora": now.strftime("%H:%M:%S"),
        "Hora numero": now.hour * 3600 + now.minute * 60 + now.second
    }
    
    return existing_df.append(new_entry, ignore_index=True)

def plot_graph(existing_df):
    plt.figure(figsize=(10, 6))

    unique_helados = existing_df['Helado'].unique()

    for helado in unique_helados:
        helado_df = existing_df[existing_df['Helado'] == helado]
        plt.step(helado_df['Hora numero'], helado_df['Stock'], where='post', label=helado)

    plt.xlabel('Time')
    plt.ylabel('Stock')
    plt.title('Stock vs Time')

    hora_labels = existing_df.groupby('Hora numero')['Hora'].first().reset_index(drop=True)
    hora_ticks = existing_df['Hora numero'].unique()
    plt.xticks(hora_ticks, hora_labels, rotation=45)

    plt.legend()
    plt.tight_layout()
    plt.show()

def display_stocks(existing_df):
    unique_helados = existing_df['Helado'].unique()

    for helado in unique_helados:
        last_stock = existing_df[existing_df["Helado"] == helado]["Stock"].iloc[-1]
        print(f"{helado}: {last_stock}")

def main():
    print("Hello to the Terraza Miramar")

    csv_file_name = "ice_cream_data.csv"
    existing_df = pd.read_csv(csv_file_name)
    
    while True:
        programa = input("¿Qué quieres: movimiento / grafico / stocks / salir? ").capitalize()

        if programa == "Movimiento":
            existing_df = add_entry(existing_df)
            save_to_csv(existing_df)
        elif programa == "Grafico":
            plot_graph(existing_df)
        elif programa == "Stocks":
            display_stocks(existing_df)
        elif programa == "Salir":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, elige una opción válida.")

if __name__ == "__main__":
    main()