# itba-TME-examenResistor
Pequeño programa para practicar los codigos de colores de las tablas de tolerancia del 10% (E12), 5% 2% y 1% (E24, E48, E96)

### OJO! Este README esta desactualizado!

## Guia de uso
1. Escribir con el teclado el valor de la resistencia respetando la [Guia de Formato](#guia-de-formato)
2. Presionar Enter, el programa mostrara si la respuesta fue correcta o incorrecta
3. Volver a presionar Enter para obtener un nuevo valor de resistencia
- Para invertir el orden de los colores de la resistencia, presione "Girar"

## Guia de formato
Formato:
1. Numero de 1 a 3 digitos (maximo), con punto '.' para decimales (si corresponde)
2. espacio
3. Tolerancia (Ya no es necesario el '%') puede ser en numero o letra (si corresponde)

Ejemplos:
- `3.9     0.05%` &emsp; (Naranja, Blanco, Dorado, Gris)
- `820     1%`  &emsp;  (Gris, Rojo, Marron, Marron)
- `2.7M    F`  &emsp; (Rojo, Violeta, Verde, Plateado)
- `150K    2%` &emsp;  (Marron, Verde, Amarillo, Rojo]
- `0.18    D` &emsp; (Marron, Gris, Plateadi, Verde)

Multiplicadores: 
- M, K, G
- Para los mili-ohms, colocar con punto

## Aclaraciones
- Los valores de la tabla E12, el multiplicador y la tolerancia de la resistencia se eligen aleatoriamente
- Por defecto, existe un 20% de probabilidad de que los colores de la resistencia esten invertidos (Este parametro se puede modificar)

## Dependencias
- [Python 3.9 o superior](https://www.python.org/downloads/)
- [Pygame](https://www.pygame.org/wiki/GettingStarted)
- [numpy](https://pypi.org/project/numpy/)

## Contacto (Por favor si encuentran un error avisenme)
rdalzotto@gmail.com