# Instrucciones
*  [Insertar imágenes](https://github.com/enriqueacosta/IllustrativeMath-GrupoLEMA/blob/main/instrucciones/Agregar-imagenes.md)


# Problemas comunes
### No agregar formato a un `<li>`
Hay `<li>` de dos tipos:
*  Tipo 1: `<li>` que es solo una frase: `<li> f r a s e </li>` (sin `<p>`s)
* Tipo2: `<li>` con algo más de una frase: adentro del `<li>....</li>` debe ir HTML válido, y todo HTML válido debe ir adentro de algún tag. Entonces, puede ser:
  ```xml
    <li>
        <p> ....</p>
        <p>....</p>
        <ol>
            ....
        </ol>
        <p> ... </p>
    </li>
  ```

Si se trata de usar tipo1 para algo que es tipo2, es posible que Pretext ignore el contenido para el output. 

#### Ejemplo:

Incorrecto:
```xml
 <li><m>24</m> personas. Ejemplos de respuestas:
    <ul>
      ...
    </ul>
 </li>
```

Correcto:
```xml
 <li>
    <p><m>24</m> personas. Ejemplos de respuestas:</p>
    <ul>
      ...
    </ul>
 </li>
```

#### Ejemplo concreto:

Código incorrecto:
```xml
 <solution> 
     <ol> 
       <li><m>24</m> personas. Ejemplos de respuestas: 
       <ul> 
         <li>Dividí <m>72</m> cubos encajables en <m>3</m> grupos y vi que hay <m>24</m> cubos en cada grupo.</li> 
         <li>Si ponemos <m>10</m> personas en cada autobús, eso son 30 personas. Si ponemos <m>10</m> personas más en cada autobús, eso son <m>60</m> personas, y hay <m>12</m> personas más que aún no están en un autobús. Al poner <m>4</m> personas más en cada autobús, ubicamos esas <m>12</m> personas. <m>10 + 10 + 4 = 24</m>.</li> 
         <li>Sé que <m>3</m> grupos de <m>20</m> son <m>60</m> y <m>3</m> grupos de <m>4</m> son <m>12</m>, así que <m>3</m> grupos de <m>24</m> son <m>72</m>.</li> 
       </ul> 
       </li> 
       <li><m>6</m> mesas. Ejemplos de respuestas: 
```

El problema ocurre en la línea `<li><m>24</m> personas. Ejemplos de respuestas: `, porque comienza un `<li>` complejo, sin un `<p>`.

El output se ve así:

<img width="400" alt="Screenshot 2024-09-22 at 4 12 16 PM" src="https://github.com/user-attachments/assets/f3464f33-e9ad-439e-8d43-7789ab748e55">

El arreglo:
```xml
 <li>
    <p><m>24</m> personas. Ejemplos de respuestas:</p>
    <ul>
      ...
    </ul>
 </li>
```
