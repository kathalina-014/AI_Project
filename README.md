# Sistema de recomendación de productos

## 1. Nombre y descripción del proyecto

**Nombre:** Sistema de recomendación de productos.

Este proyecto es una aplicación inicial en Python que recomienda productos de
un catálogo de ejemplo según categorías y palabras clave proporcionadas por la
persona usuaria. Utiliza similitud entre textos para ordenar los productos y
permite limitar los resultados por precio.

> **Captura 1 — Repositorio y proyecto:** insertar aquí una captura real de la
> página del repositorio en GitHub o del proyecto abierto en Visual Studio Code.

## 2. Objetivo

El objetivo es construir una demostración sencilla de un sistema de
recomendación basado en contenido. El modelo representa las descripciones y
características de cada producto como vectores; luego compara esos vectores
con las preferencias indicadas para sugerir los productos más relacionados.

El catálogo incluido es ilustrativo. No representa inventario ni datos de
compras de una tienda real.

## 3. Herramientas utilizadas

- **GitHub:** alojamiento y gestión del repositorio del proyecto.
- **GitHub Copilot:** asistencia para redactar y desarrollar el código.
- **Visual Studio Code:** editor para trabajar con el repositorio y el archivo
  Python.
- **Python:** lenguaje en el que está implementada la aplicación.
- **Pandas:** creación y manipulación del catálogo como tabla de productos.
- **NumPy:** procesamiento de las puntuaciones de similitud y validación de
  valores numéricos.
- **Scikit-learn:** vectorización de texto con TF-IDF y búsqueda de productos
  cercanos mediante `NearestNeighbors`.

> **Captura 2 — Herramientas:** insertar aquí una captura real de Visual Studio
> Code con el proyecto abierto. Si se desea mostrar Copilot, incluir una
> captura real de la interacción utilizada, ocultando cualquier dato privado.

## 4. Creación del repositorio en GitHub

Para organizar el proyecto, se puede crear un repositorio en GitHub y añadir
una descripción breve, por ejemplo: “Sistema de recomendación de productos
basado en contenido con Python y scikit-learn”.

Al crear el repositorio, se obtiene su dirección de clonación. Usa la URL real
que muestra GitHub; no se incluye aquí una dirección para evitar asumir cuál
se utilizó.

> **Captura 3 — Creación del repositorio:** insertar una captura real de la
> página del repositorio en GitHub. Si aún no se ha creado o no está disponible,
> realizar esta etapa antes de añadir la captura.

## 5. Clonación del repositorio en Visual Studio Code

En Visual Studio Code, selecciona **Clonar repositorio** desde la paleta de
comandos o la vista de control de código fuente, pega la URL del repositorio
real y elige una carpeta local. Después, abre la carpeta clonada como espacio
de trabajo.

También se puede clonar desde una terminal con Git:

```bash
git clone <URL_REAL_DEL_REPOSITORIO>
```

Reemplaza el marcador por la URL de clonación proporcionada por GitHub.

> **Captura 4 — Clonación:** insertar una captura real de Visual Studio Code
> mostrando el repositorio clonado y abierto. No incluir credenciales ni tokens.

## 6. Creación del archivo `recommendation_system.py`

Dentro de la carpeta del proyecto se crea el archivo
[`recommendation_system.py`](./recommendation_system.py). El archivo reúne el
catálogo de ejemplo, el entrenamiento del modelo, la función de recomendación
y un ejemplo de ejecución directa.

> **Captura 5 — Archivo Python:** insertar una captura real del archivo abierto
> en Visual Studio Code, procurando que se vean las partes principales del
> código.

## 7. Generación del código con GitHub Copilot

GitHub Copilot puede asistir en la generación y revisión del código a partir
de instrucciones en lenguaje natural. Para esta actividad, la solicitud puede
describir el catálogo de productos, las bibliotecas requeridas, el modelo de
similitud, la función de recomendaciones y la necesidad de explicar el código
en español.

El código propuesto debe revisarse antes de ejecutarlo: conviene comprobar que
las dependencias estén declaradas, que las preferencias se procesen de forma
coherente y que los resultados respeten los filtros solicitados. Copilot es
una herramienta de asistencia y no sustituye la revisión ni las pruebas.

> **Captura 6 — Asistencia de Copilot:** insertar una captura real de la
> interacción o sugerencia de Copilot relacionada con el código. Si no se
> conservó una captura de la sesión, no reconstruirla ni presentarla como real.

## 8. Funcionamiento del sistema de recomendación

El archivo sigue este flujo:

1. Define un catálogo de ejemplo con identificador, nombre, categoría,
   descripción, características y precio.
2. Combina los campos de texto de cada producto.
3. Usa `TfidfVectorizer` de Scikit-learn para convertir esos textos en
   vectores numéricos.
4. Entrena `NearestNeighbors` con distancia coseno para encontrar productos
   próximos en el espacio de vectores.
5. La función `recomendar_productos(preferencias, cantidad=5)` transforma las
   categorías y palabras clave indicadas por el usuario y calcula similitudes.
6. Si se proporciona `precio_maximo`, excluye los productos que superan ese
   límite. Devuelve una tabla ordenada con los productos recomendados y su
   puntuación de similitud.

Ejemplo de uso desde otro archivo Python:

```python
from recommendation_system import recomendar_productos

preferencias = {
    "categorias": ["tecnologia"],
    "palabras_clave": ["audio", "inalámbrico"],
    "precio_maximo": 100,
}

recomendaciones = recomendar_productos(preferencias, cantidad=5)
print(recomendaciones)
```

La puntuación de similitud es una medida relativa basada en el texto y no una
garantía de que el producto sea adecuado para cada persona.

> **Captura 7 — Código de recomendación:** insertar una captura real donde se
> aprecie la función o el ejemplo de preferencias.

## 9. Instalación de dependencias y ejecución

Se requiere Python instalado y disponible desde la terminal. Instala las
bibliotecas necesarias desde la carpeta del proyecto:

```bash
python -m pip install pandas numpy scikit-learn
```

Ejecuta el ejemplo incluido en el archivo:

```bash
python recommendation_system.py
```

El programa imprime las recomendaciones correspondientes a las preferencias
de ejemplo definidas al final del script. El resultado depende del catálogo y
de los datos del código; no se documenta aquí una salida específica.

> **Captura 8 — Instalación y ejecución:** insertar una captura real de la
> terminal mostrando los comandos ejecutados y su salida. Asegurarse de que la
> captura corresponda a una ejecución real y no contenga información privada.

## 10. Conclusión

La actividad reúne herramientas de desarrollo y aprendizaje automático para
crear una demostración funcional de recomendación basada en contenido. El
ejemplo muestra cómo transformar texto de productos en vectores, medir+++
similitud y aplicar preferencias como categoría, palabras clave y presupuesto.

Para evolucionar el proyecto, se podría reemplazar el catálogo de ejemplo por
datos reales autorizados, incorporar valoraciones de usuarios, añadir pruebas
automatizadas y evaluar la calidad de las recomendaciones. Esos pasos no
forman parte del prototipo documentado aquí.
