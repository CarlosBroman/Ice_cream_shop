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

    def generate_popup(self, title, content_widgets, num_columns):
        popup_content = GridLayout(cols=num_columns)
        for widget in content_widgets:
            popup_content.add_widget(widget)
            
        popup = Popup(title=title, content=popup_content, size_hint=(None, None), size=(400, 400))
        
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
        self.generate_popup(title, content_widgets, num_columns)

    def update_button_and_close_dropdown(self, dropdown, button, selected_value, selected_value_attr):
        button.text = selected_value
        
        if selected_value_attr == "selected_helado":
             self.selected_helado = selected_value
        elif selected_value_attr == "selected_quantity":
            self.selected_quantity = selected_value
        elif selected_value_attr == "selected_operation":
            self.selected_operation = selected_value
        
        dropdown.dismiss()

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
            self.existing_df.to_csv(CSV_FILE_NAME, index=False)
            self.message_popup(message)

# GENERATE MOVEMENT BUTTON       
    def show_movement_popup(self):
        title = "New movement"
        content_widgets = [
            self.create_helado_dropdown(),
            self.create_quantity_dropdown(),
            self.create_operation_dropdown(),
            Label(size_hint_y=None, height=30),
            Button(text="Generate", size_hint=(None, None), size=(100, 50), on_release=self.generate_entry),
        ]
        num_columns = 1
        self.generate_popup(title, content_widgets, num_columns)

    def create_dropdown(self, values, button_text, selected_value_attr):
        dropdown = DropDown()
        text = button_text
        button = Button(text=text, size_hint=(None, None), size=(150, 50), on_release=dropdown.open)
        
        for value in values:
            btn = Button(text=value, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.update_button_and_close_dropdown(dropdown, button, btn.text, selected_value_attr))
            dropdown.add_widget(btn)

        setattr(self, selected_value_attr, button.text)
        return button

    def create_helado_dropdown(self):
        x = self.existing_df["Helado"].unique()
        button_name = "Sabor de helado"
        attribute = "selected_helado"
        return self.create_dropdown(x, button_name, attribute)

    def create_quantity_dropdown(self):
        x = [str(number) for number in range(1, 10)]
        button_name = "Cantidad"
        selected_quantity = "selected_quantity"
        return self.create_dropdown(x,  button_name, selected_quantity)

    def create_operation_dropdown(self):
        x = ["Entrada", "Salida"]
        button_name = "Entrada o salida"
        selected_operation = "selected_operation"
        return self.create_dropdown(x,  button_name, selected_operation)

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
        helado_text_input = TextInput(hint_text="Enter Ice Cream Flavor", size_hint=(None, None), size=(150, 30))
        add_button = Button(text="Add Flavor", size_hint=(None, None), size=(150, 40))
        add_button.bind(on_release=lambda _: self.add_new_flavour(helado_text_input))
        
        title = "Añadir nuevo sabor"
        content_widgets = [helado_text_input, add_button]
        num_columns=1
        self.generate_popup(title, content_widgets, num_columns) 
        
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
        self.generate_popup(title, content_widgets, num_columns)
        
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