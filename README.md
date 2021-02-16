# Cosinor_Analysis
Un conjunto de funciones que permite calcular características <<interesantes>> de funciones sinusoidales. El punto de esto es
obtener información sobre series de tiempo de experimentos de eventos circadianos.

## Descripción

En esta versión del programa, utilizo una clase llamada ```time_series``` en la que se puede implementar métodos para hacer el 
análisis. Estos métodos y las otras funciones están definidas en otros archivos cual módulos para no ocupar un solo archivo de mil 
líneas, sino simplemente implementar las cosas en uno más breve importando las funciones de los otros. Cada uno de los módulos, 
```reading.py``` y ```analysis.py``` tiene una cláusula al final de la definición de funciones en la que, de correr el módulo 
directamente, hace una verificación de que todo corra bien. La carpeta de archivos ```read``` es parte de la verificación del 
módulo de lectura.

El último archivo, ```cosinor.py```, importa los otros dos módulos y trabaja con ellos.

## Uso

    
    $ python[3] [direccion/a/programa/]cosinor.py datos.xls [int]
    

El archivo ```datos.xls``` debe estar contenido en el directorio donde están los archivos ```cosinor.py``` y los dos módulos, a
menos de que se especifique la dirección completa o relativa del archivo. En otras palabras, el programa no es un programa global
(a menos de que se cambie el PATH del sistema a que incluya el PATH donde se encuentran los programas). La extensión del archivo
puede ser también ```.xlsx```.

El archivo de Excel debe contener primero una columna con la hora de la medición, seguida de columnas de datos. Se pide que las
columnas estén alineadas en la parte superior izquierda del archivo, *i.e.* empezando en la celda A1. Adicionalmente, se pide
que no haya filas o columnas en blanco entre filas o columnas de datos, ya que esto causará un problema. Fuera de eso, se le
puede dar formato de negritas o color o alguno otro deseado.

Finalmente, el valor opcional ```int``` del final especifica qué libro del archivo se va a leer. De no ser especificado, se asume
que es 0 y por ende el primer libro. El resto de los libros se puede especificar enumerando su posición empezando desde cero.

Lo primero que se va a ver al correr el programa es un *prompt* que pregunta sobre las columnas que se quiere analizar. A éste
se puede responder de tres maneras distintas:
* con la opción "-h", que indica el nombre de todas las columnas.
* con la opción "all", que analiza todas las columnas.
* con una lista de nombres de columna que se quiere analizar, con cada elemento separado por comas. Por ejemplo, si los nombres
de las columnas son "Control", "Ayuno" y "Dieta", y se quiere estudiar únicamente el control y el ayuno, la respuesta puede ser

  ```Control, Ayuno```

  Cabe resaltar que el nombre tiene que estar escrito exactamente como está escrito en el documento. De lo contrario, volverá a
salir el *prompt*.

De aquí en adelante, el programa da indicaciones y las opciones para responder preguntas. En el caso de que se desee guardar la
información obtenida en un archivo de texto, se pide que el nombre no contenga caracteres especiales. Si se desea agregar la
extensión ```.xlsx``` o no a la respuesta al prompt es irrelevante, ya que siempre se guardará un archivo de ese formato, con una
sola extensión.
