# Cosinor_Analysis
Un conjunto de funciones que permite calcular características <<interesantes>> de funciones sinusoidales. El punto de esto es
obtener información sobre series de tiempo de experimentos de eventos circadianos.

## Uso

    
    python OA_Cosinor.py datos.csv
    

El archivo ```datos.csv``` debe estar contenido en el directorio donde está el script ```OA_Cosinor.py```. En la primer columna
se indica la hora con respecto a la cual se va a hacer el ajuste. El resto de las columnas indican las mediciones. El programa
transforma la hora de hora militar a minutos para poder hacer los cálculos apropiados. Se ingresan las columnas que se quiere
evaluar, y el programa calcula acrofase, magnitud y mesor. Genera una figura con los datos experimentales y el ajuste. Al terminar
de analizar todas las columnas, se puede analizar otro conjunto de columnas.

Después de analizar todas las columnas, se puede escribir un archivo de texto que indica el valor de la columna y sus parámetros
de ajuste. En caso de no querer guardar los datos, basta con escribir ```c```cuando el prompt lo indique.
