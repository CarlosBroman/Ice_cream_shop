helados = ["Chocolate", "Vainilla", "Banana Split"]

cantidad_por_sabor = {
    "Chocolate" : 0,
    "Vainilla" : 3,
    "Banana Split" : 0
}

while True:
    sabor = input("¿Qué sabor? ")
    
    if sabor in helados:
        cantidad = int(input("¿Qué cantidad? "))
        operacion = input("¿Qué operación (entrada / salida) ? ")
        
        if sabor in cantidad_por_sabor:
            if operacion == "salida":
                cantidad_por_sabor[sabor] -= cantidad
            elif operacion == "entrada":
                cantidad_por_sabor[sabor] += cantidad
        else:
            cantidad_por_sabor[sabor] = cantidad
    
        print(f"Sabor: {sabor}, Cantidad: {cantidad}, Operación: {operacion}")
        another_entry = input("¿Es correcto? (s/n): ")
        if another_entry.lower() == 's':
            break
    else: 
        print("Este sabor no existe")
    
print(cantidad_por_sabor)