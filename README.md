# itba-TME-examenResistor
Pequeño programa para practicar los codigos de colores de la tabla de tolerancia del 10% (E12)

## Guia de uso
1. Escribir con el teclado el valor de la resistencia respetando la [Guia de Formato](#guia-de-formato)
2. Presionar Enter, el programa mostrara si la respuesta fue correcta o incorrecta
3. Volver a presionar Enter para obtener un nuevo valor de resistencia
- Para invertir el orden de los colores de la resistencia, presione "Girar"

## Guia de formato
Formato:
1. Numero de 1 a 3 digitos (maximo), con punto '.' para decimales (si corresponde)
2. espacio
3. Tolerancia con '%' (si es numero entero), o con decimales con punto y '%'
Ejemplos:
- 3.9 0.05%  (Naranja, Blanco, Dorado, Gris)
- 820 1%    (Gris, Rojo, Marron, Marron)
- 2.7M 1%   (Rojo, Violeta, Verde, Plateado)
- 150K 2%   (Marron, Verde, Amarillo, Rojo]
- 0.18    0.5% (Marron, Gris, Plateadi, Verde)

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