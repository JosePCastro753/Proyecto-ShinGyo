# Proyecto Shin DMS
Shin DMS es un proyecto que busca desarrollar un sitema multi-agente capas de tomar deciciones sobre una simulacion realista de una linea de produccion, implicando todas las situaciones imprevistas y aleatorias presentes en una, sean productos defectuosos, paros de maquina no pronosticada, reprocesos, entre otros.<br>
Tambien busca dotar al sistema de la cualidad humana del "apetito de riesgo", entrenando a los modelos del sistema para que asuman mas o menos riesgos a la hora de tomar decisiones sobre la linea de produccion.

## Estado Actual 
Actualmente `./Shin_DMS/` ha demostrado que el proyecto es factible de realizarse y es en si mismo un sistema funcional, mas no uno confiable, ni optimo.<br>
actualmente el proyecto se puede considerar en una etapa de desarrollo con un norte definido y una base sobre la cual mejorar.
#### Grafica de aprendizaje de Shin DMS
<img src="/Shin_DMS/Reultados_1/grafica_aprendizaje.jpeg" height="250px" width="400px" ><br>
_Datos tomados de una corrida de aprendizaje de 1000 episodios.<br>
Muestra el puntaje obtenido por cada episodio._

## Cambios Planeados
`./Shin^2_DMS/` [Shin Shin DMS] toma como base a su antecesor, y busca robustecer sus algoritmos de aprendizaje tanto a nivel de codigo como estadistico, balancear su ecosistema, sofisticar y personalizar tanto sus agentes como los modeles relacionados a estos y corregir errores de su antecesor.<br>
Actualmente existen los siguiente cambios planeados:
- Balancear los porcentajes de piezas defectuosas y reprocesos en la simulacion, asi como las recompensas asociados a los resultados de la misma. Esto dado que se noto que los valores actuales no coinciden aportan correctamente a orientar al sistema en la direccion deseada.
- Transformar el ciclo de ejecucion de episodios actual, a un ciclo donde en cada episodio se generar un ecosistema aleatorio y se realizaran multiples iteraciones sobre un este antes de pasar al siguiente episodio. Esto con el fin de enseñar al sistemaa resolver una situacion antes de cambiarla, esto dado que entre ecosistemas, la forma de abordarlos y las soluciones optimas varian considerablemente.
- Reservar una mayor cantidad de recursos para ejecutar multiples corridas de aprendizaje a modo de prueba o exploracion, con mayor cantidad de episodios por corrida e iteraciones por episodio.

El objetivo último del proyecto es obtener una herramienta que pueda ser implementada en una línea de producción real y tomar variedad de decisiones sobre ella, siguiendo un apetito de riesgo dictado, siendo supervisada por un experto humano pero lo suficientemente confiable y adaptable para no requerir mayor intervencion por parte de este.
