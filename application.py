import pandas as pd
import datetime
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

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

def save_to_csv(dataframe):
    csv_file_name = "ice_cream_data.csv"
    dataframe.to_csv(csv_file_name, index=False)
    print("\nDataFrame:")
    print(dataframe)
    print(f"\nDataFrame saved to {csv_file_name}")
    return dataframe
   
def open_add_entry_window():
    def submit_entry():
        
        global existing_df
        now = datetime.datetime.now()
        id = len(existing_df["ID"].tolist())
        helado = helado_var.get().capitalize()
        cantidad = int(cantidad_var.get())
        operacion = operacion_var.get().capitalize()
        stock = existing_df[existing_df["Helado"] == helado]["Stock"].iloc[-1]
        
        if operacion == "Entrada":
            stock = stock + cantidad
        elif operacion == "Salida":
            stock = stock - cantidad
        stocks.append(stock)
                
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
        
        existing_df = save_to_csv(pd.concat([existing_df, pd.DataFrame([new_entry])]))
        messagebox.showinfo("Movimiento", "Entrada registrada exitosamente.")
        add_entry_window.destroy()
    
    add_entry_window = tk.Toplevel(root)
    add_entry_window.title("Registrar Movimiento")
    
    tk.Label(add_entry_window, text="Registrar Movimiento", font=("Helvetica", 16)).pack(pady=10)
    
    unique_helados = existing_df['Helado'].unique()
    helado_var = tk.StringVar(value=unique_helados[0])
    
    tk.Label(add_entry_window, text="Sabor de helado:").pack()
    tk.OptionMenu(add_entry_window, helado_var, *unique_helados).pack()
    
    cantidad_var = tk.StringVar()
    tk.Label(add_entry_window, text="Cantidad:").pack()
    tk.Entry(add_entry_window, textvariable=cantidad_var).pack()
    
    operacion_var = tk.StringVar(value="Entrada")
    tk.Label(add_entry_window, text="Operación (Entrada o Salida):").pack()
    tk.OptionMenu(add_entry_window, operacion_var, "Entrada", "Salida").pack()
    
    tk.Button(add_entry_window, text="Registrar", command=submit_entry).pack(pady=10)

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
    stock_info = ""
    unique_helados = existing_df['Helado'].unique()

    for helado in unique_helados:
        last_stock = existing_df[existing_df["Helado"] == helado]["Stock"].iloc[-1]
        stock_info += f"{helado}: {last_stock}\n"

    return stock_info

def handle_program_choice(choice):
    
    if choice == "Movimiento":
        open_add_entry_window()
    elif choice == "Grafico":
        plot_graph(existing_df)
    elif choice == "Stocks":
        stocks_info = display_stocks(existing_df)
        messagebox.showinfo("Stocks", stocks_info)
    elif choice == "Salir":
        root.destroy()
    else:
        messagebox.showerror("Error", "Opción no válida. Por favor, elige una opción válida.")

def main():
    global existing_df, root
    
    root = tk.Tk()
    root.title("Terraza Miramar App")

    csv_file_name = "ice_cream_data.csv"
    existing_df = pd.read_csv(csv_file_name)

    label = tk.Label(root, text="Bienvenido a Terraza Miramar", font=("Helvetica", 16))
    label.pack(pady=20)

    button_movimiento = tk.Button(root, text="Registrar Movimiento", command=lambda: handle_program_choice("Movimiento"))
    button_movimiento.pack()

    button_grafico = tk.Button(root, text="Mostrar Gráfico", command=lambda: handle_program_choice("Grafico"))
    button_grafico.pack()

    button_stocks = tk.Button(root, text="Mostrar Stocks", command=lambda: handle_program_choice("Stocks"))
    button_stocks.pack()

    button_salir = tk.Button(root, text="Salir", command=lambda: handle_program_choice("Salir"))
    button_salir.pack()

    root.mainloop()

if __name__ == "__main__":
    main()