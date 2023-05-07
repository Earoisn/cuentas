Un programita que usé hasta hace poco para llevar las cuentas de mi trabajo usando un bloc de notas almacenado localmente porque no se me ocurrió otra forma de hacerlo con los conocimientos que tenía y me pareció que para el uso que le iba a dar estaba bien.
Originalmente anotaba las clases que me debían a mano y creé mi propio código de cómo hacerlo:
{Nombre del alumno} ${dinero} {d}/{m}/{a}. En caso de tener plata a favor, la agregaba entre paréntesis con un "+": (+${dinero}) y sin fecha asociada y todas las clases correspondientes a ese alumno se anotaban una a continuación de la otra. 
Con esto como punto de partida me propuse automatizar lo máximo posible el proceso. Tuve que usar regular expressions para hacer el parsing.
Es el primer programa mínimamente complejo que escribí y le tengo cariño. Me sirvió para reforzar todos los conceptos básicos del curso py4e de Charles Severance y lo usé todos los días hasta hace poco, en que pude juntar varios proyectitos en uno solo que está aca: https://github.com/Earoisn/calmgr.
No creo que le sirva a nadie más, es para quien quiera ver por curiosidad.
