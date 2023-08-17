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
NEW_FLAVOR_OPERATION = "Nuevo sabor"
EMPTY_STOCK_THRESHOLD = 1

existing_df = pd.read_csv(CSV_FILE_NAME)

class icecream(App):
    
# CREATE LAYOUT OF INITIAL SCREEN    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_helado = None
        self.selected_quantity = None
        self.selected_operacion = None
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
            ("Generar movimiento", self.generate_movement),
            ("Añadir nuevo sabor", self.add_new_flavor),
            ("Stocks", self.show_stocks)
        ]
        for button_text, callback in buttons:
            button = Button(text=button_text, font_size=32, size=(100, 50))
            button.bind(on_release=callback)
            layout.add_widget(button)

# ADD FUNCTIONALITY TO BUTTONS

# GENERATE MOVEMENT BUTTON
    def generate_movement(self, instance):
        self.show_movement_popup()
        
    def show_movement_popup(self):
        popup_content = GridLayout(cols=1, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        helado_dropdown = DropDown()
        unique_helados = existing_df["Helado"].unique()
        for helado in unique_helados:
            btn = Button(text=helado, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.update_button_and_close_dropdown(self.helado_button, helado_dropdown, btn.text))
            helado_dropdown.add_widget(btn)
            helado_dropdown.bind(on_select=self.update_button_and_close_dropdown)
            
        self.helado_button = Button(text="Select Helado", size_hint=(None, None), size=(150, 50))
        self.helado_button.bind(on_release=helado_dropdown.open)
        popup_content.add_widget(self.helado_button)

        quantity_dropdown = DropDown()
        for quantity in range(1, 10):
            btn = Button(text=str(quantity), size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.update_button_and_close_dropdown(self.quantity_button, quantity_dropdown, btn.text))
            quantity_dropdown.add_widget(btn)
            
        self.quantity_button = Button(text="Select Quantity", size_hint=(None, None), size=(150, 50))
        self.quantity_button.bind(on_release=quantity_dropdown.open)
        popup_content.add_widget(self.quantity_button)

        operation_dropdown = DropDown()
        for operation in ["Entrada", "Salida"]:
            btn = Button(text=operation, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.update_button_and_close_dropdown(self.operation_button, operation_dropdown, btn.text))
            operation_dropdown.add_widget(btn)
            
        self.operation_button = Button(text="Select Operation", size_hint=(None, None), size=(150, 50))
        self.operation_button.bind(on_release=operation_dropdown.open)
        popup_content.add_widget(self.operation_button)
        
        empty_space = Label(size_hint_y=None, height=30)
        popup_content.add_widget(empty_space)
        
        generate_button = Button(text="Generate", size_hint=(None, None), size=(100, 50))
        generate_button.bind(on_release=self.generate_entry)
        popup_content.add_widget(generate_button)
        
        close_button = Button(text="Close", size_hint=(None, None), size=(100, 50))
        close_button.bind(on_release=self.dismiss_popup)
        popup_content.add_widget(close_button)
        
        self.popup = Popup(title="New movement", content=popup_content, size_hint=(None, None), size=(300, 350))
        self.popup.open()

    def generate_entry(self, instance):
        # Functionality to generate entry based on selected values
        global existing_df
        now = datetime.datetime.now()
        id = len(existing_df["ID"].tolist())
        helado = self.selected_helado
        cantidad = self.selected_quantity
        operacion = self.selected_operacion
        stock = existing_df[existing_df["Helado"] == helado]["Stock"].iloc[-1]
        
        if operacion == "Entrada":
            stock = stock + cantidad
        elif operacion == "Salida":
            stock = stock - cantidad
                
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
        
        existing_df = icecream.save_to_csv(pd.concat([existing_df, pd.DataFrame([new_entry])]))
        message = f"Se ha hecho una {operacion.lower()} de {cantidad} de {helado}"
        self.show_message_popup("Movimiento", message)

    def show_message_popup(self, title, message):
        popup_content = GridLayout(cols = 1)
        popup_content.add_widget(Label(text=message))
        
        close_button = Button(text="Close", size_hint=(None, None), size=(100, 50))
        close_button.bind(on_release=self.dismiss_message_popup)
        popup_content.add_widget(close_button)
        
        self.message_popup = Popup(title=title, content=popup_content, size_hint=(None, None), size=(300, 200))
        self.message_popup.open()
        
    def dismiss_message_popup(self, instance):
        self.message_popup.dismiss()
        
    def update_button_and_close_dropdown(self, button, dropdown, new_text):
        self.update_button_text(button, new_text)
        dropdown.dismiss()
        
        if button is self.helado_button:
            self.selected_helado = new_text
        elif button is self.quantity_button:
            self.selected_quantity = int(new_text)
        elif button is self.operation_button:
            self.selected_operacion = new_text
        
    def update_button_text(self, button, new_text):
       button.text = new_text

# ADD FLAVOUR BUTTON
  
    def add_new_flavor(self, instance):
        self.add_new_flavour_popup()
        
    def add_new_flavour_popup(self):
        popup_content = GridLayout(cols = 1)
        self.helado_text_input = TextInput(hint_text="Enter Ice Cream Flavor", size_hint=(None, None), size=(150, 30))
        popup_content.add_widget(self.helado_text_input)
        
        add_button = Button(text="Add Flavor", size_hint=(None, None), size=(150, 40))
        add_button.bind(on_release=self.add_the_flavour)  # Bind to the function that adds the flavor
        popup_content.add_widget(add_button)
                
        cancel_button = Button(text="Cancel", size_hint=(None, None), size=(100, 40))
        cancel_button.bind(on_release=self.dismiss_popup)  # Bind to dismiss the popup
        popup_content.add_widget(cancel_button)
        
        self.popup = Popup(title="Add New Flavor", content=popup_content, size_hint=(None, None), size=(300, 200))
        self.popup.open()
        
    def add_the_flavour(self, instance):
        global existing_df
        now = datetime.datetime.now()
        id = len(existing_df["ID"].tolist())
        helado = self.helado_text_input.text
        cantidad = 0
        operacion = "Nuevo sabor"
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
        
        existing_df = icecream.save_to_csv(pd.concat([existing_df, pd.DataFrame([new_entry])]))
        message = f"Se ha introducido {helado} a la base de datos"
        self.show_message_popup("Movimiento", message)

    def show_stocks(self, instance):
        stock_info = "STOCK\n\n"
        restock_info ="EMPTY STOCK\n\n"
        unique_helados = existing_df['Helado'].unique()

        for helado in unique_helados:
            last_stock = existing_df[existing_df["Helado"] == helado]["Stock"].iloc[-1]
            if last_stock >1:
                stock_info += f"{helado}: {last_stock}\n"
            else:
                restock_info += f"{helado}: {last_stock}\n"
        
        
        
        self.show_stock_popup(stock_info, restock_info)
        
    def show_stock_popup(self, stock_info, restock_info):
        popup_content = GridLayout(cols = 2)
        popup_content.add_widget(Label(text=stock_info))
        popup_content.add_widget(Label(text=restock_info))
        close_button = Button(text="Close", size_hint=(None, None), size=(100, 50))
        close_button.bind(on_release=self.dismiss_popup)
        popup_content.add_widget(close_button)
        
        self.popup = Popup(title="Stocks", content=popup_content, size_hint=(None, None), size=(400, 400))
        self.popup.open()
        
    def dismiss_popup(self, instance):
        self.popup.dismiss()
    
    @staticmethod
    def save_to_csv(dataframe):
        CSV_FILE_NAME = "ice_cream_data.csv"
        dataframe.to_csv(CSV_FILE_NAME, index=False)
        return dataframe

app = icecream()
app.run()