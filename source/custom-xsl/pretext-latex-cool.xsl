<?xml version='1.0'?> <!-- As XML file -->

<!--********************************************************************
Copyright 2024 Enrique Acosta

xsl stylesheet to process cool-down activities into standalone text files

*  Assumes cool-down is in a separate .ptx file only containing a <project> 
*  Uses pretext-latex.xsl to process the statement into latex
*  latex-preamble-cool is built out of what pretext-latex produces, but tries 
   to be minimal. Simplification is possible (as long as the <statement> latex 
   always compiles.

Usage:
xsltproc <path to this xsl file>.xsl gra3-uni4-secB-lec10-cool.ptx > output.tex

*********************************************************************-->

<!-- http://pimpmyxslt.com/articles/entity-tricks-part2/ -->
<!DOCTYPE xsl:stylesheet [
    <!ENTITY % entities SYSTEM "entities.ent">
    %entities;
]>

<!-- Identify as a stylesheet -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:xml="http://www.w3.org/XML/1998/namespace"
    xmlns:exsl="http://exslt.org/common"
    xmlns:date="http://exslt.org/dates-and-times"
    xmlns:str="http://exslt.org/strings"
    xmlns:pi="http://pretextbook.org/2020/pretext/internal"
    extension-element-prefixes="exsl date str"
>

<!-- load pretext-latex.xsl to process the <statement>-->
<xsl:import href="./pretext-latex.xsl"/>

<!-- Intended output for rendering by pdflatex -->
<xsl:output method="text" encoding="UTF-8"/>

<!-- ############## -->
<!-- Entry Template -->
<!-- pick up the <project> -->
<!-- ############## -->
<xsl:template match="/">
    <xsl:apply-templates select="project"/>
</xsl:template>


<!-- Create tex file -->
<xsl:template match="project">
    
    <!-- document class and options -->
    <xsl:text>\documentclass[</xsl:text>
    <!-- <xsl:call-template name="sidedness"/> -->
    <xsl:text>,</xsl:text>
    <xsl:text>]{article}&#xa;</xsl:text>

    <!-- load custom cool-down latex preamble (defined below) -->
    <xsl:call-template name="latex-preamble-cool" />

    <!-- load <title> (into \title{} command) using pretext-latex.xsl template -->
    <xsl:call-template name="title-page-info-article" />

    <!-- begin document -->
    <xsl:text>\begin{document}&#xa;</xsl:text>

    <!-- alternate loading of <title> element -->
    <xsl:text>\section*{</xsl:text>
        <xsl:value-of select="title"/>
    <xsl:text>}&#xa;</xsl:text>

    <!-- Call the pretext-latex.xsl "statement" template to create the statement tex code -->
    <xsl:apply-templates select="statement"/>

    <!-- End document -->
    <xsl:text>\end{document}&#xa;</xsl:text>
</xsl:template>


<!-- Custom cool-down latex preamble -->
<xsl:template name="latex-preamble-cool">
    <xsl:text>\usepackage{tcolorbox}&#xa;</xsl:text>
    <xsl:text>\tcbuselibrary{skins}&#xa;</xsl:text>
    <xsl:text>\tcbuselibrary{breakable}&#xa;</xsl:text>
    <xsl:text>\tcbuselibrary{raster}&#xa;</xsl:text>
    <xsl:text>\newtcolorbox[auto counter]{project-distinct}{}&#xa;</xsl:text>
    <xsl:text>\tcbset{ bwminimalstyle/.style={size=minimal, boxrule=-0.3pt, frame empty,&#xa;</xsl:text>
    <xsl:text>colback=white, colbacktitle=white, coltitle=black, opacityfill=0.0} }&#xa;</xsl:text>
    <xsl:text>\tcbset{ runintitlestyle/.style={fonttitle=\blocktitlefont\upshape\bfseries, attach title to upper}, coltitle=black }&#xa;</xsl:text>
    <xsl:text>\tcbset{ exercisespacingstyle/.style={before skip={1.5ex plus 0.5ex}} }&#xa;</xsl:text>
    <xsl:text>\tcbset{ blockspacingstyle/.style={before skip={2.0ex plus 0.5ex}} }&#xa;</xsl:text>
    <xsl:text>\tcbuselibrary{xparse}&#xa;</xsl:text>
    <xsl:text>\usetikzlibrary{calc}&#xa;</xsl:text>
    <xsl:text>\tcbuselibrary{hooks}&#xa;</xsl:text>
    <xsl:text>\usepackage{amsmath}&#xa;</xsl:text>
    <xsl:text>\usepackage{amscd}&#xa;</xsl:text>
    <xsl:text>\usepackage{amssymb}&#xa;</xsl:text>
    <xsl:text>\tcbset{ imagestyle/.style={bwminimalstyle} }&#xa;</xsl:text>
    <xsl:text>\NewTColorBox{tcbimage}{mmm}{imagestyle,left skip=#1\linewidth,width=#2\linewidth}&#xa;</xsl:text>
    <xsl:text>\NewDocumentEnvironment{image}{mmmm}{\notblank{#4}{\leavevmode\nopagebreak\vspace{#4}}{}\begin{tcbimage}{#1}{#2}{#3}}{\end{tcbimage}}&#xa;</xsl:text>
    <xsl:text>\usepackage{multicol}&#xa;</xsl:text>
    <xsl:text>\usepackage{enumitem}&#xa;</xsl:text>
    <xsl:text>\usepackage{longtable}&#xa;</xsl:text>
    <xsl:text>\tcbset{ projectstyle/.style={blockspacingstyle, after title={\space}, before upper app={\setlength{\parindent}{\normalparindent}}, } }&#xa;</xsl:text>
    <xsl:text>\newtcolorbox[use counter from=project-distinct]{project}[3]{title={{#1~\thetcbcounter\notblank{#2}{\space\space#2}{}}}, phantomlabel={#3}, breakable, after={\par}, projectstyle, }&#xa;</xsl:text>
    <xsl:text>\NewDocumentEnvironment{paragraphs}{mm}&#xa;</xsl:text>
    <xsl:text>{\subparagraph*{#1}\label{#2}\hypertarget{#2}{}}{}&#xa;</xsl:text>
    <xsl:text>\usepackage{tikz, pgfplots}&#xa;</xsl:text>
    <xsl:text>\usetikzlibrary{positioning,matrix,arrows}&#xa;</xsl:text>
    <xsl:text>\usetikzlibrary{shapes,decorations,shadows,fadings,patterns}&#xa;</xsl:text>
    <xsl:text>\usetikzlibrary{decorations.markings}&#xa;</xsl:text>
    <xsl:text>\tcbset{ sbsstyle/.style={raster before skip=2.0ex, raster equal height=rows, raster force size=false} }&#xa;</xsl:text>
    <xsl:text>\tcbset{ sbspanelstyle/.style={bwminimalstyle, fonttitle=\blocktitlefont} }&#xa;</xsl:text>
    <xsl:text>\NewDocumentEnvironment{sidebyside}{mmmm}&#xa;</xsl:text>
        <xsl:text>  {\begin{tcbraster}&#xa;</xsl:text>
        <xsl:text>    [sbsstyle,raster columns=#1,&#xa;</xsl:text>
        <xsl:text>    raster left skip=#2\linewidth,raster right skip=#3\linewidth,raster column skip=#4\linewidth]}&#xa;</xsl:text>
        <xsl:text>  {\end{tcbraster}}&#xa;</xsl:text>
    <xsl:text>\NewTColorBox{sbspanel}{mO{top}}{sbspanelstyle,width=#1\linewidth,valign=#2}&#xa;</xsl:text>
    <xsl:text>\newcommand{\alert}[1]{\textbf{\textit{#1}}}&#xa;</xsl:text>
    <xsl:text>\usepackage[export]{adjustbox}% 'export' allows adjustbox keys in \includegraphics&#xa;</xsl:text>
    <xsl:text>%% Indentación párrafos &#xa;</xsl:text>
    <xsl:text>\setlength{\parskip}{\smallskipamount}&#xa;</xsl:text>
    <xsl:text>\setlength{\parindent}{0pt}&#xa;</xsl:text>
    <xsl:text>%% Márgenes &#xa;</xsl:text>
    <xsl:text>\usepackage{geometry}&#xa;</xsl:text>
    <xsl:text>\geometry{verbose,top=2.5cm,bottom=1.7cm,lmargin=3.5cm,rmargin=3.5cm,headheight=3cm,headsep=0.3cm,footskip=0cm}&#xa;</xsl:text>
    <xsl:text>%% Headings y footers&#xa;</xsl:text>
    <xsl:text>\usepackage{fancyhdr}&#xa;</xsl:text>
    <xsl:text>\pagestyle{fancy}&#xa;</xsl:text>
    <xsl:text>\fancyfoot[C]{} %Remove default Latex numbering&#xa;</xsl:text>
    <xsl:text>\fancyhead[C]{\begin{tikzpicture}[remember picture,overlay] \node[yshift=-0.5cm] at (current page.north west) {\begin{tikzpicture}[remember picture, overlay] \includegraphics[width=\paperwidth]{barra-colorGrupoLEMA.png}\end{tikzpicture}};\end{tikzpicture}} % Paper-Wide header&#xa;</xsl:text>
    <xsl:text>\fancyfoot[L]{{\small Grupo LEMA (www.grupolema.org), \the\year{}. Licencia de uso CC-BY-NC Internacional 4.0.}\\{\scriptsize Adaptado de IM K–5 Math v.I, © 2021 Illustrative Mathematics ® illustrativemathematics.org en su versión en español en im.kendallhunt.com y de Open Up Resources © 2022, openupresources.org, publicadas bajo una licencia Creative Commons CC BY 4.0. Detalles: https://creativecommons.org/licenses/by/4.0/deed.es}}&#xa;</xsl:text>
    <xsl:text>\fancyhead[R]{}&#xa;</xsl:text>
    <xsl:text>\fancyfoot[R]{}&#xa;</xsl:text>
    <xsl:text>\fancyfootoffset{2cm}&#xa;</xsl:text>
    <xsl:text>\fancypagestyle{plain}{}  % Redefine the plain page style (style used in title pages)&#xa;</xsl:text>
    <xsl:text>\renewcommand{\footrulewidth}{1pt}  % Agregar linea all footer&#xa;</xsl:text>
    <xsl:text>\renewcommand{\headrulewidth}{0pt}  % Quitar linea del header&#xa;</xsl:text>
    <xsl:text>%% Colores y estilo de los headings&#xa;</xsl:text>
    <xsl:text>\usepackage{graphicx}&#xa;</xsl:text>
    <xsl:text>\usepackage{xcolor}&#xa;</xsl:text>
    <xsl:text>\PassOptionsToPackage{usenames,dvipsnames,svgnames,table}{xcolor}&#xa;</xsl:text>
    <xsl:text>%% Fuente sans-serif&#xa;</xsl:text>
    <xsl:text>\renewcommand{\familydefault}{\sfdefault}&#xa;</xsl:text>
    <xsl:text>%% quitar hyphenation&#xa;</xsl:text>
    <xsl:text>\usepackage[none]{hyphenat}&#xa;</xsl:text>
</xsl:template>


<!-- override image generation -->
<!-- REMOVE once using a custom pretext-latex.xsl (which will implement the same thing) -->
<!-- adds options [max width=\linewidth, center] to \includegraphics to display images at default size if possible -->
<xsl:template match="image[@source|@pi:generated]" mode="image-inclusion">
    <xsl:variable name="extension">
        <xsl:call-template name="file-extension">
            <xsl:with-param name="filename">
                <xsl:choose>
                    <xsl:when test="@pi:generated">
                        <xsl:value-of select="@pi:generated" />
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="@source" />
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:with-param>
        </xsl:call-template>
    </xsl:variable>
    <xsl:text>\includegraphics[max width=\linewidth</xsl:text>
    <xsl:text>,center</xsl:text>
    <xsl:if test="@rotate">
      <xsl:text>,angle=</xsl:text>
      <xsl:value-of select="@rotate"/>
      <xsl:text>,origin=c</xsl:text>
    </xsl:if>
    <xsl:text>]{</xsl:text>
    <xsl:choose>
        <xsl:when test="@pi:generated">
            <xsl:text>../</xsl:text>
            <xsl:value-of select="$generated-directory"/>
            <xsl:value-of select="@pi:generated"/>
        </xsl:when>
        <xsl:otherwise>
            <!-- empty when not using managed directories -->
            <xsl:text>../</xsl:text>
            <xsl:value-of select="$external-directory"/>
            <xsl:value-of select="@source"/>
        </xsl:otherwise>
    </xsl:choose>
    <xsl:if test="$extension = ''">
        <xsl:text>.pdf</xsl:text>
    </xsl:if>
    <xsl:text>}&#xa;</xsl:text>
</xsl:template>

</xsl:stylesheet>
