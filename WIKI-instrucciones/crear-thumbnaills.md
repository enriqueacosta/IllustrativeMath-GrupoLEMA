## Ejemplo básico
```
magick -density 150 centro-bingo-imagenes-tablero.pdf centro-bingo-imagenes-tablero.png
```

## Para un pdf de act, que sale con transparencia
```
magick -density 100 act-siSeQueEntoncesSeQue.pdf -background white -alpha remove -alpha off act-siSeQueEntoncesSeQue.png
```
