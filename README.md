# Cosinor_Analysis
Un conjunto de funciones que permite calcular características <<interesantes>> de funciones sinusoidales. El punto de esto es
obtener información sobre series de tiempo de experimentos de eventos circadianos.

## Descripción

En esta versión del programa, utilizo una clase llamada ```Cosinor``` en la que se puede implementar métodos para hacer el 
análisis. Estos métodos y las otras funciones están definidas en otros archivos cual módulos para no ocupar un solo archivo de mil 
líneas, sino simplemente implementar las cosas en uno más breve importando las funciones de los otros. Cada uno de los módulos, 
```reading.py``` y ```analysis.py``` tiene una cláusula al final de la definición de funciones en la que, de correr el módulo 
directamente, hace una verificación de que todo corra bien. La carpeta de archivos ```read``` es parte de la verificación del 
módulo de lectura.

El último archivo, ```cosinor.py```, importa los otros dos módulos y trabaja con ellos.

## Uso

    
    $ python cosinor.py datos.csv
    

El archivo ```datos.csv``` debe estar contenido en el directorio donde están los archivos ```cosinor.py``` y los dos módulos.
En la primer columna se indica la hora con respecto a la cual se va a hacer el ajuste. El resto de las columnas indican las 
mediciones. El programa genera una lista de objetos tipo ```time_series```, donde el elemento $n$-ésimo contiene la columna de 
tiempo del archivo ```.csv``` y la $n$-ésima columna de datos. Posteriormente, pregunta qué se quiere analizar (por el momento
funciona solo con el número de la columna, aunque quiero hacer que funcione con el nombre del experimento) y calcula el coseno que
ajusta mejor a los datos. Eso regresa los parámetros de ajuste, y un valor de R$^2$ que representa el *goodness of fit*. Además, grafica la serie de tiempo contra su ajuste para guardar la figura.

Al terminar de analizar, se puede analizar un nuevo conjunto de columnas si así se desea, o terminar el programa, con la opción de 
escribir los análisis realizados en un archivo ```.txt``` con el nombre deseado.
