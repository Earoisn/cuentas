Un programita que usé hasta hace poco para llevar las cuentas de mi trabajo usando un bloc de notas almacenado localmente porque no se me ocurrió otra forma de hacerlo con los conocimientos que tenía y me pareció que para el uso que le iba a dar estaba bien.
Originalmente anotaba las clases que me debían a mano así:

{Nombre del alumno} ${dinero adeudado} {día}/{mes} (+${dinero a favor}).

Todas las clases correspondientes a ese alumno una a continuación de la otra y cada alumno en un nuevo renglón. 
Todos los alumnos están nombrados {primer nombre} {nro} (el nro para diferenciar alumnos con el mismo nombre, sin número cuando es el único con ese nombre).

Con esto como punto de partida me propuse automatizar lo máximo posible el proceso. Usé regular expressions para hacer el parsing.
El programita permite hacer varias cosas:

*Ingresar clases de nuevos alumnos o agregar clases a los existentes usando opciones prefijadas de duraciones y precios y la fecha actual recuperada de forma automática para acelerar el proceso (pero también la opción de ingresar la información manualmente en caso de olvidar anotar una clase).

*Buscar información sobre uno o más alumnos, con fecha de las clases tomadas, precio y dinero total adeudado.

*Borrar selectivamente clases de un solo mes en caso de tener deudas que abarquen más meses y hayan pagado uno solo.

Es el primer programa mínimamente complejo que escribí y le tengo cariño. Me sirvió para reforzar todos los conceptos básicos del curso py4e de Charles Severance y lo usé todos los días durante un año, hasta que junté varios proyectitos en uno solo que hace todo esto y más interactuando con el calendario de Google. Está aca: https://github.com/Earoisn/calmgr.
No creo que le sirva a nadie más, queda de recuerdo acá.
