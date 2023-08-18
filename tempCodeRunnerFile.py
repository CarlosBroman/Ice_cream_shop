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
            global existing_df
            now = datetime.datetime.now()
            id = len(existing_df["ID"].tolist())
                    
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
            
            existing_df = pd.concat([existing_df, pd.DataFrame([new_entry])])
            existing_df.to_csv(CSV_FILE_NAME, index=False)
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
        x = existing_df["Helado"].unique()
        button_name = "Select Helado"
        attribute = "selected_helado"
        return self.create_dropdown(x, button_name, attribute)

    def create_quantity_dropdown(self):
        x = [str(number) for number in range(1, 10)]
        button_name = "Select quantity"
        selected_quantity = "selected_quantity"
        return self.create_dropdown(x,  button_name, selected_quantity)

    def create_operation_dropdown(self):
        x = ["Entrada", "Salida"]
        button_name = "Select operation"
        selected_operation = "selected_operation"
        return self.create_dropdown(x,  button_name, selected_operation)

    def generate_entry(self, instance):
        # Functionality to generate entry based on selected values
        global existing_df
        helado = self.selected_helado
        cantidad = int(self.selected_quantity)
        operacion = self.selected_operation
        stock = existing_df[existing_df["Helado"] == helado]["Stock"].iloc[-1]
        
        if operacion == "Entrada":
            stock = stock + cantidad
        elif operacion == "Salida":
            stock = stock - cantidad
            
        message = f"Se ha hecho una {operacion.lower()} de {cantidad} unidades de {helado}"
        self.create_new_entry(helado, cantidad, operacion, stock, message)