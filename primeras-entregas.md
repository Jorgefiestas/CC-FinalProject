# Aplicacion de prediccion de acciones:

- jorge.fiestas@utec.edu.pe	
- fernando.delosheros@utec.edu.pe

## Por que este proyecto?

Debido a el alto volumen ventas de cualquier accion, poder preveer los cambios de precio diarios es una muy util habilidad, ya que nos da una impresionante capacidad de ganancias al poder hacer esto, debido a la manera en que funcionan los mercados capitales.

## Cloud

Nuestra aplicacion esta basada en una arquitectura basada en kubernetes, permitiendo asi la computacion distribuida de los datos que se tienen, lo cual se dificulta al tratar de ejecutarlo en una computadora tradicional. Nosotros proponemos correr diferentes parted de la arqiutectura en containers de kubernetes, como por ejemplo la infulxdb, para poder mejorar la modularidad del funcionanmineto del proyecto.

## Funcionalidad

Nuestro modelo depende de 4 vairables: Open, close, Daily high y Daily low.
Basado en los datos historicos que se tienen sobre el movimiento de los precios, el algoritmo trata de estimar cuales seran estos para el dia proximo del mercado.

# Requerimientos

1. La aplicaccion es capaz de predecir algun precio para el dia siguiente, posiblemente como complemento informacional para los indicadores que un comprador tiende a tener, para mejorar la cantidad de informacion que se tiene.
2. La aplicacion permite tener una lista de acciones seguidas, para poder obtener informacion sobre los posibles movimientos de esta a futuro de manera simple y sencilla.Idealmente, se podria encontrar un resumen de las features caracteristicas de una accion en un solo vistaso
3. Visualizacion grafica de datos: La aplicacion podra mostrar graficamente los datos que se requieren, mostrandolos de manera que el usuatio pueda extraer de ellos la mayor cantidad de informacion posible.
## Pasos para ejecucion
1. Terminar la aplicaccion localmente
2. Deployear en minikube
3. Deployear en google cloud
