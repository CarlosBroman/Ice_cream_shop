import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput

import pandas as pd
import datetime

CSV_FILE_NAME = "ice_cream_data.csv"
EMPTY_STOCK_THRESHOLD = 2

class icecream(App):
    
# CREATE LAYOUT OF INITIAL SCREEN    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.existing_df = pd.read_csv(CSV_FILE_NAME)
        self.selected_helado = None
        self.selected_quantity = None
        self.selected_operation = None
        self.helado_text_input = None
    
    def build(self):
        layout = self.create_layout()
        return layout

    def create_layout(self):
        layout = BoxLayout(orientation='vertical')
        self.add_title(layout)
        self.add_buttons(layout)
        return layout

    def add_title(self, layout):
        title = Label(
            text="Heladeria Terraza Miramar",
            font_size=64,
            color=(0.92, 0.45, 0)
        )
        layout.add_widget(title)

    def add_buttons(self, layout):
        buttons = [
            ("Entrada / salida helado existente", lambda _: self.show_movement_popup()),
            ("Añadir nuevo sabor", lambda _: self.add_new_flavour_popup()),
            ("Stocks", self.show_stocks)
        ]
        for button_text, callback in buttons:
            button = Button(text=button_text, font_size=32, size=(100, 50))
            button.bind(on_release=callback)
            layout.add_widget(button)

# ADD FUNCTIONALITY TO BUTTONS

    def generate_popup(self, title, content_widgets, num_columns, size):
        popup_content = GridLayout(cols=num_columns)
        for widget in content_widgets:
            popup_content.add_widget(widget)
            
        popup = Popup(title=title, content=popup_content, size_hint=(None, None), size=size)
        
        cancel_button = Button(text="Cerrar", size_hint=(None, None), size=(100, 40))
        cancel_button.bind(on_release=lambda _: popup.dismiss())
        popup_content.add_widget(cancel_button)
        
        
        popup.open()
    
    def message_popup(self, message):
        title = "Movimiento"
        content_widgets = [
            Label(text=message),
        ]
        num_columns = 1
        size = (450, 200)
        self.generate_popup(title, content_widgets, num_columns, size)

    def update_button_and_close_dropdown(self, button, dropdown, new_text):
        button.text = new_text
        dropdown.dismiss()
            
        if button is self.helado_button:
            self.selected_helado = new_text
        elif button is self.quantity_button:
            self.selected_quantity = new_text
        elif button is self.operation_button:
            self.selected_operation = new_text

    def create_new_entry(self, helado, cantidad, operacion, stock, message):
            now = datetime.datetime.now()
            id = len(self.existing_df["ID"].tolist())
                    
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
            
            self.existing_df = pd.concat([self.existing_df, pd.DataFrame([new_entry])])
            print(self.existing_df)
            self.existing_df.to_csv(CSV_FILE_NAME, index=False)
            self.message_popup(message)

# GENERATE MOVEMENT BUTTON       
    def show_movement_popup(self):
        popup_content = GridLayout(cols=1)
        
        helado_dropdown = DropDown()
        unique_helados = self.existing_df["Helado"].unique()
        for helado in unique_helados:
            btn = Button(text=helado, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.update_button_and_close_dropdown(self.helado_button, helado_dropdown, btn.text))
            helado_dropdown.add_widget(btn)
            
        self.helado_button = Button(text="Sabor del helado", size_hint=(None, None), size=(150, 50))
        self.helado_button.bind(on_release=helado_dropdown.open)
        popup_content.add_widget(self.helado_button)
        
        
        quantity_dropdown = DropDown()
        for quantity in range(1, 10):
            btn = Button(text=str(quantity), size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.update_button_and_close_dropdown(self.quantity_button, quantity_dropdown, btn.text))
            quantity_dropdown.add_widget(btn)
            
        self.quantity_button = Button(text="Seleccionar cantidad", size_hint=(None, None), size=(150, 50))
        self.quantity_button.bind(on_release=quantity_dropdown.open)
        popup_content.add_widget(self.quantity_button)
        
        
        operation_dropdown = DropDown()
        for operation in ["Entrada", "Salida"]:
            btn = Button(text=operation, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.update_button_and_close_dropdown(self.operation_button, operation_dropdown, btn.text))
            operation_dropdown.add_widget(btn)
            
        self.operation_button = Button(text="Seleccionar operacion", size_hint=(None, None), size=(150, 50))
        self.operation_button.bind(on_release=operation_dropdown.open)
        popup_content.add_widget(self.operation_button)
        
        empty_space = Label(size_hint_y=None, height=30)
        popup_content.add_widget(empty_space)
        
        generate_button = Button(text="Añadir movimiento", size_hint=(None, None), size=(150, 50))
        generate_button.bind(on_release=self.generate_entry)
        popup_content.add_widget(generate_button)
        
        cancel_button = Button(text="Cerrar", size_hint=(None, None), size=(100, 40))
        cancel_button.bind(on_release=lambda _: self.popup.dismiss())
        popup_content.add_widget(cancel_button)
        
        
        self.popup = Popup(title="Nuevo movimiento", content=popup_content, size_hint=(None, None), size=(200, 350))
        self.popup.open()
        
    def generate_entry(self, instance):
        # Functionality to generate entry based on selected values
        helado = self.selected_helado
        cantidad = int(self.selected_quantity)
        operacion = self.selected_operation
        stock = self.existing_df[self.existing_df["Helado"] == helado]["Stock"].iloc[-1]
        
        if operacion == "Entrada":
            stock = stock + cantidad
        elif operacion == "Salida":
            stock = stock - cantidad
            
        message = f"Se ha hecho una {operacion} de {cantidad} unidades de {helado}"
        self.create_new_entry(helado, cantidad, operacion, stock, message)
        
# ADD FLAVOUR BUTTON   
    def add_new_flavour_popup(self):
        helado_text_input = TextInput(hint_text="Nuevo Sabor de helado: ", size_hint=(None, None), size=(150, 30))
        add_button = Button(text="Añadir sabor", size_hint=(None, None), size=(150, 40))
        add_button.bind(on_release=lambda _: self.add_new_flavour(helado_text_input))
        
        title = "Añadir nuevo sabor"
        content_widgets = [helado_text_input, add_button]
        num_columns=1
        size = (200, 200)
        self.generate_popup(title, content_widgets, num_columns, size) 
        
    def add_new_flavour(self, helado_text_input):
        helado = helado_text_input.text
        cantidad = 0
        operacion = "Nuevo sabor"
        stock = 0
        message = f"Se ha introducido {helado} a la base de datos"
        
        self.create_new_entry(helado, cantidad, operacion, stock, message)

# SHOW STOCKS
    def show_stock_popup(self, stock_info, restock_info):
        title = "Stocks"
        content_widgets = [
            Label(text=stock_info),
            Label(text=restock_info)
        ]
        num_columns = 2
        size = (400, 400)
        self.generate_popup(title, content_widgets, num_columns, size)
        
    def show_stocks(self, instance):
        stock_info = "STOCK\n\n"
        restock_info ="EMPTY STOCK\n\n"
        
        unique_helados = self.existing_df['Helado'].unique()

        for helado in unique_helados:
            last_stock = self.existing_df[self.existing_df["Helado"] == helado]["Stock"].iloc[-1]
            if last_stock > EMPTY_STOCK_THRESHOLD:
                stock_info += f"{helado}: {last_stock}\n"
            else:
                restock_info += f"{helado}: {last_stock}\n"        
        
        self.show_stock_popup(stock_info, restock_info)
        
app = icecream()
app.run()