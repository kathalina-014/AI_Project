
"""Sistema inicial de recomendación de productos basado en contenido."""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


# Catálogo pequeño de ejemplo. En un proyecto real, estos datos podrían venir
# de una base de datos o de un archivo CSV.
PRODUCTOS = pd.DataFrame(
    [
        {
            "id": 1,
            "nombre": "Auriculares inalámbricos",
            "categoria": "tecnologia",
            "descripcion": "Auriculares bluetooth con cancelación de ruido y sonido envolvente",
            "caracteristicas": "audio música inalámbrico batería larga",
            "precio": 89.99,
        },
        {
            "id": 2,
            "nombre": "Altavoz portátil",
            "categoria": "tecnologia",
            "descripcion": "Altavoz bluetooth resistente al agua para escuchar música",
            "caracteristicas": "audio música inalámbrico portátil",
            "precio": 59.99,
        },
        {
            "id": 3,
            "nombre": "Teclado mecánico",
            "categoria": "tecnologia",
            "descripcion": "Teclado mecánico retroiluminado para jugar y trabajar",
            "caracteristicas": "computación gaming accesorios",
            "precio": 74.50,
        },
        {
            "id": 4,
            "nombre": "Reloj inteligente",
            "categoria": "tecnologia",
            "descripcion": "Reloj inteligente con seguimiento de actividad y ritmo cardíaco",
            "caracteristicas": "salud deporte notificaciones batería",
            "precio": 129.00,
        },
        {
            "id": 5,
            "nombre": "Cafetera espresso",
            "categoria": "hogar",
            "descripcion": "Cafetera compacta para preparar espresso y café con leche",
            "caracteristicas": "cocina café bebidas",
            "precio": 149.99,
        },
        {
            "id": 6,
            "nombre": "Lámpara de escritorio LED",
            "categoria": "hogar",
            "descripcion": "Lámpara LED regulable para leer y trabajar en el escritorio",
            "caracteristicas": "iluminación lectura oficina",
            "precio": 34.99,
        },
        {
            "id": 7,
            "nombre": "Botella térmica",
            "categoria": "deporte",
            "descripcion": "Botella reutilizable que mantiene las bebidas frías o calientes",
            "caracteristicas": "hidratación gimnasio exterior",
            "precio": 24.00,
        },
        {
            "id": 8,
            "nombre": "Esterilla de yoga",
            "categoria": "deporte",
            "descripcion": "Esterilla antideslizante para yoga, estiramientos y ejercicio",
            "caracteristicas": "bienestar entrenamiento fitness",
            "precio": 39.95,
        },
        {
            "id": 9,
            "nombre": "Mochila urbana",
            "categoria": "accesorios",
            "descripcion": "Mochila ligera con compartimento acolchado para portátil",
            "caracteristicas": "viaje oficina transporte",
            "precio": 54.90,
        },
        {
            "id": 10,
            "nombre": "Cámara instantánea",
            "categoria": "tecnologia",
            "descripcion": "Cámara compacta que imprime fotografías al instante",
            "caracteristicas": "fotografía creatividad viajes",
            "precio": 99.00,
        },
    ]
)


def entrenar_modelo(productos):
    """Convierte las descripciones en vectores y entrena el buscador de similitud."""
    # Se combinan los campos de texto para representar cada producto.
    textos = (
        productos["categoria"].fillna("")
        + " "
        + productos["nombre"].fillna("")
        + " "
        + productos["descripcion"].fillna("")
        + " "
        + productos["caracteristicas"].fillna("")
    )

    # TF-IDF da más peso a los términos informativos del catálogo.
    vectorizador = TfidfVectorizer(stop_words=None)
    matriz_productos = vectorizador.fit_transform(textos)

    # El modelo busca los productos más cercanos usando distancia coseno.
    modelo = NearestNeighbors(metric="cosine", algorithm="brute")
    modelo.fit(matriz_productos)
    return vectorizador, modelo, matriz_productos


# El entrenamiento se realiza al cargar el programa.
VECTORIZADOR, MODELO, MATRIZ_PRODUCTOS = entrenar_modelo(PRODUCTOS)


def recomendar_productos(preferencias, cantidad=5):
    """
    Recomienda productos similares a las preferencias indicadas.

    preferencias debe ser un diccionario con "categorias" y/o "palabras_clave".
    También puede incluir "precio_maximo" para limitar los resultados.
    """
    if not isinstance(preferencias, dict):
        raise TypeError("Las preferencias deben proporcionarse como un diccionario.")
    if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 1:
        raise ValueError("La cantidad de recomendaciones debe ser un entero positivo.")

    # Se aceptan tanto listas de términos como un único término en texto.
    partes_consulta = []
    for campo in ("categorias", "palabras_clave"):
        valores = preferencias.get(campo, [])
        if isinstance(valores, str):
            valores = [valores]
        elif not isinstance(valores, (list, tuple, set)):
            raise TypeError(f"El campo '{campo}' debe ser texto o una lista de textos.")
        partes_consulta.extend(str(valor).strip() for valor in valores if str(valor).strip())

    if not partes_consulta:
        raise ValueError("Indica al menos una categoría o palabra clave.")

    precio_maximo = preferencias.get("precio_maximo")
    candidatos = PRODUCTOS.copy()
    if precio_maximo is not None:
        try:
            precio_maximo = float(precio_maximo)
        except (TypeError, ValueError) as error:
            raise ValueError("'precio_maximo' debe ser un número.") from error
        if not np.isfinite(precio_maximo) or precio_maximo < 0:
            raise ValueError("'precio_maximo' debe ser un número finito no negativo.")
        candidatos = candidatos[candidatos["precio"] <= precio_maximo]

    if candidatos.empty:
        return pd.DataFrame(columns=["id", "nombre", "categoria", "precio", "similitud"])

    # Se obtiene la similitud frente al texto que resume las preferencias.
    consulta = VECTORIZADOR.transform([" ".join(partes_consulta)])
    distancias, indices = MODELO.kneighbors(
        consulta, n_neighbors=len(PRODUCTOS)
    )
    puntuaciones = np.clip(1 - distancias[0], 0, 1)

    resultados = PRODUCTOS.iloc[indices[0]].copy()
    resultados["similitud"] = puntuaciones
    resultados = resultados[resultados["id"].isin(candidatos["id"])]

    return (
        resultados.sort_values("similitud", ascending=False)
        .head(cantidad)[["id", "nombre", "categoria", "precio", "similitud"]]
        .reset_index(drop=True)
    )


if __name__ == "__main__":
    # Ejemplo: buscar tecnología de audio dentro del presupuesto indicado.
    preferencias_usuario = {
        "categorias": ["tecnologia"],
        "palabras_clave": ["audio", "inalámbrico"],
        "precio_maximo": 100,
    }

    print("Recomendaciones para tus preferencias:")
    print(recomendar_productos(preferencias_usuario, cantidad=5).to_string(index=False))
