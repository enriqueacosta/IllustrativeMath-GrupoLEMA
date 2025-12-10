# Instrucciones para el curso de ingestión

## Encuentro 1

### Cuentas e instalaciones
1.  **Crear una cuenta en [github.com](github.com)**. ¡Piense muy bien el nombre de usuario! (es una decisión parecida a cuando uno seleccionó su usuario de gmail).
2.  **Instalar en el computador que va a usar:**  
     a.  [Github Desktop](https://desktop.github.com/download). Para poder usar git desde su computador.  
     b.  [Visual Studio Code](https://code.visualstudio.com/download). Para editar código. Es el editor de código más usado en el mundo (más información [acá](https://en.wikipedia.org/wiki/Visual_Studio_Code)).  
     c.  [Python 3](https://www.python.org/downloads). Para poder generar las páginas web del material. Descargue la versión más nueva que permita su sistema operativo (3.14 en este momento).
4.  **Configurar Github Desktop:** abrir github desktop y hacer el login con su cuenta de github.

### Revisión (auto evaluación)
1. Cuando va a [github.com](github.com), ¿le aparece su cuenta de usuario?
2.   
     a. ¿Puede abrir el app `Gitub Desktop` en su computador?  
     b. ¿Puede abrir el app `Visual Studio Code` en su computador?  
     c. Abra la terminal (command prompt en Windows, `applications/U tilities/Terminal.app` en Mac). Ejecute `python --version` y `python3 --version`. ¿qué mensaje le sale?

## Cultura General
1. [PreTexT](https://pretextbook.org) y repositorio de [github](https://github.com/PreTeXtBook/pretext)
2. [Git](https://en.wikipedia.org/wiki/Git) y repositorio de [github](https://github.com/git/git)
3. [LaTeX](https://en.wikipedia.org/wiki/LaTeX), sucesor de [TeX](https://en.wikipedia.org/wiki/TeX). Repositorio de [github](https://github.com/latex3/latex2e)
4. [MathJaX](https://www.mathjax.org) para mostrar formulas de LaTeX en la web. Repositorio de [github](https://github.com/mathjax/MathJax)

## Encuentro 2

### Configuración PreTeXt (lo vamos a hacer sincrónico) 
1. En VSCode, instalar la extensión de PreTeXt.
2. Reiniciar VSCode.
3. En la terminal de VSCode, instalar el PreTeXt CLI: `pip3 install pretext`

### Compilar una página web
1. En la terminal de VSCode, ejecutar `pretext build gra3-uni4-web-prof` y revisar que les diga `success` al final.
2. Abrir el `index.html` que se generó en `IllustrativeMath-GrupoLEMA/output/web-prof/gra3-uni4`
