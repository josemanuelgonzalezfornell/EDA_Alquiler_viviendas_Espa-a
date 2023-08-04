# EDA_Alquiler_viviendas_España
  
----

## Se presenta un Análisis Exploratorio de Datos del precio del alquiler por metro cuadrado de viviendas colectivas y unifamiliares y rurales en España  

----

Las bases de datos utilizadas para la producción de este EDA fueron las siguientes:  

1. Datos de viviendas en alquiler por municipios:

    Cantidad de viviendas en alquiler por municipios en España desde 2015 hasta 2021, junto con sus precios expuestos de diferentes formas. Además, este Dataset clasifica las viviendas en dos conjuntos dependiendo de la superficie de esta: Colectiva y Unifamiliar o Rural.  

    Los datos han sido obtenidos a partir de las tributaciones de los contribuyentes, por lo que no incluye los datos de los municipios pertenecientes a los fueros de País Vasco ni de la Comunidad Foral de Navarra.

    [Link del Dataset](https://www.mitma.gob.es/vivienda/alquiler/indice-alquiler)

2. Relación de municipios con Comunidades autónomas:  

    Relaciona los municipios de España con las comunidades autónomas a las que pertenecen.
  
    [Link del Dataset](https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177031&menu=ultiDatos&idp=1254734710990)

3. Población por municipios españoles.  

    Población de los diferentes municipios españoles en total y por tramos de edad desde 2003 hasta 2022. También se incluye en este dataset los datos respecto a la población total nacional.

    [Link del Dataset](https://www.ine.es/jaxi/Tabla.htm?tpx=55200&L=0)

4. Censo de viviendas en España.

    Cantidad de edificios dedicados principal o exclusivamente a la vivienda en municipios de más de 2.000 habitantes hasta 2011 (fecha del último censo de viviendas realizado). En este Dataset se muestra además el estado de la vivienda y el año de construcción.

    [Link del Dataset](https://www.ine.es/jaxi/Tabla.htm?path=/t20/e244/edificios/p04/l0/&file=2mun00.px&L=0)

5. Censo de viviendas turísticas en España.  
  
    Cantidad de alquileres turísticos por municipios producidos en España en los meses de febrero y de agosto en los años 2020, 2021 y 2022. También se muestra las viviendas, las plazas por viviendas y solo las plazas turísticas.  

    Este Datasets fue obtenido mediante una técnica de Web Scraping en las 3 mayores páginas de alquiler turístico utilizadas.

    [Link del Dataset](https://www.ine.es/jaxiT3/Tabla.htm?t=39363)
  
6. Turismo internacional en España.

    Cantidad de turismo internacional recibida en España en los años 2020, 2021 y 2022 por municipio.

    Estos datos se obtuvieron a partir de la geolocaliación de dispositivos de telefonía móvil.

    [Link del Dataset](https://www.ine.es/dynt3/inebase/es/index.htm?padre=8578&capsel=8579)
  
Los DataSets obtenidos tras la depuración de datos fueron los siguientes:

 1. df_alquiler_processed.csv

     Contiene todos los datos necesarios para realizar el EDA.

 2. df_alquiler_no_outliers.csv

     Es igual que el anterior pero los outlirs que se encontraban por encima del máximo se igualaron al máximo y los que estaban por debajo del mínimo se igualaron al mínimo.

 3. df_alquiler_2020_21_processed.csv

     Contiene los datos necesarios para realizar el EDA pero solo de los años 2020 y 2021.

 4. df_alquiler_2020_21_no_outliers.csv

     Es igual que el anterior pero los outlirs que se encontraban por encima del máximo se igualaron al máximo y los que estaban por debajo del mínimo se igualaron al mínimo.
