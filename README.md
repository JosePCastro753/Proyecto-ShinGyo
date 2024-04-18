# Proyecto Shin DMS
Shin DMS es un proyecto que busca desarrollar un sistema multi-agente capaz de tomar decisiones sobre una simulación realista de una línea de producción, implicando todas las situaciones imprevistas y aleatorias presentes en una, sean productos defectuosos, paros de maquina no pronosticada, reprocesos, entre otros.<br>
También busca dotar al sistema de la cualidad humana del "apetito de riesgo", entrenando a los modelos del sistema para que asuman más o menos riesgos a la hora de tomar decisiones sobre la línea de producción.

## Estado Actual 
`./Shin_DMS/` ha demostrado que el proyecto es factible de realizarse y actualmente es en si mismo un sistema funcional, mas no uno confiable, ni optimo.<br>
El proyecto se puede considerar en una etapa de desarrollo con un norte definido y una base sobre la cual mejorar.
#### Grafica de aprendizaje de Shin DMS
<img src="/Shin_DMS/Reultados_1/grafica_aprendizaje.jpeg" height="250px" width="400px" ><br>
_Datos tomados de una corrida de aprendizaje de 1000 episodios.<br>
Muestra el puntaje obtenido por cada episodio._

## El Camino Frente a Nosotros
`./Shin^2_DMS/` [Shin Shin DMS] toma como base a su antecesor, y busca robustecer sus algoritmos de aprendizaje tanto a nivel de código como estadístico, balancear su ecosistema, sofisticar y personalizar tanto sus agentes como los modeles relacionados a estos y corregir errores de su antecesor.<br>
Actualmente existen los siguientes cambios planeados:
- Balancear los porcentajes de piezas defectuosas y reprocesos en la simulación, así como las recompensas asociadas a los resultados de esta. Esto dado que se notó que los valores actuales no coinciden aportan correctamente a orientar al sistema en la dirección deseada.
- Transformar el ciclo de ejecución de episodios actual, a un ciclo donde en cada episodio se generar un ecosistema aleatorio y se realizaran múltiples iteraciones sobre un este antes de pasar al siguiente episodio. Esto con el fin de enseñar al sistema resolver una situación antes de cambiarla, esto dado que, entre ecosistemas, la forma de abordarlos y las soluciones optimas varían considerablemente.
- Reservar una mayor cantidad de recursos para ejecutar múltiples corridas de aprendizaje a modo de prueba o exploración, con mayor cantidad de episodios por corrida e iteraciones por episodio.
- Arreglar la impresión de decisiones en el resumen del ecosistema.
- Separar y diferenciar los agentes segun sus funciones a realizar, iniciando por la funcion de activacion de las capas (actualmente 'relu' pero se deben definir funciones que optimizen el apredizaje segun la naturaleza de cada agente).
- Revisar, corregir y mejorar la forma de los datos y los datos en si que los agentes observan tanto para predecir como para aprender.

El objetivo último del proyecto es obtener una herramienta que pueda ser implementada como controladora de una línea de producción real y tomar variedad de decisiones de diferentes naturalezas sobre ella, siguiendo un apetito de riesgo dictado por el área administrativa; siendo supervisada por un experto humano pero lo suficientemente confiable y adaptable para no requerir mayor intervención por parte de este. Lograr un sistema de toma de decisiones calificado para hacerse cargo de las decisiones rutinarias y situaciones repentinas previamente consideradas, que supere a los supervisores de producción humanos, aventajándolos en tiempo de reacción, visión del panorama general, sesgos emocionales, entre otros.
