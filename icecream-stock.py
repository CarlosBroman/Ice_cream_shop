import pandas as pd

print("hello to the Terraza Miramar")
nombre = input("¿Cómo te llamas? ")
helado = input(f"Hola, {nombre}, ¿Qué helado acabas de poner?")

data = {
    "Nombre" : [nombre],
    "Helado" : [helado]
}

df = pd.DataFrame(data)

print("\nDataFrame:")
print(df)