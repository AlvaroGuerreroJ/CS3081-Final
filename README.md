# Ingenieria de Software 1 - Examen Final

Para limitar el valor máximo enviado por día se debe revisar antes de hacer una transacción de que la suma a transferir no nos haga superar el límite diario.

Esta verificación es factible con los datos ya almacenados pero para evitar tener que leer el historial y seleccionar los envios de dinero correspondientes al presente día se podría guardar cuánto dinero ha enviado cada usuario el día actual. Esta variable debería ser actualizada después de cada transferencia exitosa y reiniciada a 0 al inicio de un nuevo día.

El código a modificar debería ser el de inicialización de la BD para guardar el nuevo campo del saldo diario usado por cada usuario (también podría añadirse a la clase de `Cuenta`). También se debe modificar el código de `transferir` para actualizar el monto diario usado. Se podría añadir también al historial para que el usuario pueda ver su monto diario usado. Por último, se debe reiniciar el monto diario usado para cada usuario al iniciar un nuevo día, esto puede ser una tarea programada diariamente o se puede verificar si ya se dio el reinicio diario (y de no ser así realizar el reinicio) antes de efectuar una transferencia.

El caso de prueba más saliente a implementar es el de revisar que efectivamente no se permitan transacciones totalizando más del monto permitido en un mismo día. Se debe verificar que no se permita una transacción individual que exceda el permitido así como que no se permita excederlo realizando múltiples transacciones pequeñas.

No considero que el cambio sea riesgoso. En su mayoría, este consta del añadido de una nueva condicional a la lógica de validación de `transferir`. Creo que el riesgo mayor sería que el código relacionado al límite diario sea defectuoso y permita transacciones que excedan el límite; esto no representaría una disminución de funcionalidad con respecto a la versión anterior de la aplicación.
