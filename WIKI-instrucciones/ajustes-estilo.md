## Soluciones que son listas de respuestas separadas por puntos deben cambiarse a listas de viñetas.
Ejemplo: Cool-down [Encuentra el producto desconocido] de 3.4.9:

<img width="500" alt="Screenshot 2025-01-13 at 4 01 26 PM" src="https://github.com/user-attachments/assets/fc10a8eb-e158-459b-a597-7930c896e05a" />

(debería ser un `ul`).

## Los warm que son listas deben ser `<ol>` con estilo `A.`, `B.`, etc.
Muchos de esos son listas de viñetas en la material original y se ven así:

<img width="320" alt="Screenshot 2025-01-13 at 4 37 27 PM" src="https://github.com/user-attachments/assets/f9d46e5c-7712-46e3-8c32-4fccdbcc2169" />

deben quedar así:

<img width="350" alt="Screenshot 2025-01-13 at 4 38 55 PM" src="https://github.com/user-attachments/assets/35606bf4-b31b-46d3-901b-2fe0322789d0" />

El código para esto se ve así:
```xml
<ol marker="A.">
  <li><m>4\times 10</m></li>
  <li><m>40\div 40</m></li>
  <li><m>40\div 10</m></li>
  <li><m>60\div 6</m></li>
</ol>
```
