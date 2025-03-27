# Componentes del source

El en source, para crear un elemento que solo 
*  ve el profesor, poner `component="profesor"`
*  ve el estudiante, poner `component="estudiante"`
*  se ve en la versión web, poner `component="web"`

Por ejemplo:
```xml
<objectives component="estudiante">
  <ul>
    <li>Exploremos las fichas de dos colores y los tableros de 5.</li>
  </ul>
</objectives>

<objectives component="profesor">
  <ul>
    <li>Usar fichas de dos colores y los tableros de 5.</li>
    <li>Parafrasear ideas matemáticas de un compañero.</li>
  </ul>
</objectives>

<ul>
  <li>fichas de dos colores</li>
  <li>tableros de 5 <url component="web" href="external/blm/pdf-source/tableros-de-5.pdf">(ver pdf)</url></li>
</ul>
```

## Componentes disponibles

*  `estudiante`: cosas que solo ve el estudiante. Aparecen en todos los documentos para el estudiante, entonces NO sirve para diferenciar entre distintos docs del estudiante (como por ejemplo libro rayable y no rayable).

*  `profesor`: cosas que solo ve el profesor. Aparecen en todos los documentos para el profesor, entonces NO sirve para diferenciar entre distintos docs del estudiante (como por ejemplo libro rayable y no rayable).

*  `cools`: solo para los cools. Cada tipo de documento puede incluir o no los cools de acuerdo a si se incluye este componente o no.

*  `warms`: calentamientos. Igual que los `cools`, cada tipo de documento puede incluir o no los warms de acuerdo a si se incluye este componente o no.

*  `no-libroTrabajo`: sirve para excluir cosas del libro de trabajo. Todos los documentos que no sean el libro de trabajo deben incluir este componente.

*  `libroTrabajo`: cosas que SOLO deben aparecer en el libro de trabajo. Solo los libros de trabajo deben incluir este componente.

*  `web`: cosas que SOLO deben aparecer en las versiones web (tanto para profesores como para estudiantes).

*  `est-goal`: solo para los student goals (las frases "resumen" al inicio de cada lección de estilo [Representemos situaciones de división con dibujos]). Cada tipo de documento puede incluir o no los cools de acuerdo a si se incluye este componente o no.