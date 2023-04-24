import pandas as pd
import numpy as np
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt
import scipy.stats as ss

# Detecta outliers de un dataframe


def get_outliers(df):
    """
    Detecta outliers de un conjunto de series o de un dataframe

    args:
        list_series: lista de series o dataframes

    reutrns:
        lista de diccionarios. Primer diccionario con la cantidad de outliers por columna.
                                Segundo diccionario con la lista de outliers por columna.

    """
    outliers = {}
    outliers_len = {}
    for col in df.columns:
        if df[col].dtype == object or (col == "Codigo_municipio") or (col == "Codigo_provincia"):
            pass
        else:
            outliers_col = []
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            minimum = Q1 - (1.5 * IQR)
            maximum = Q3 + (1.5 * IQR)
            for data in df[col]:
                if data < minimum or data > maximum:
                    outliers_col.append(data)
            outliers[col] = outliers_col
            outliers_len[col] = len(outliers_col)
    output = [outliers_len, outliers]
    return output


# Cambia los outliers de un dataframe
def change_outliers(df):
    """
    Transforma los outliers en la media de cada columna

    args:
        list_series: lista de series o dataframes

    reutrns:
        Copia del DataFrame sin outliers

    """
    df_copy = df.copy()
    for col in df_copy.columns:
        if (df_copy[col].dtype == object) or (col == "Codigo_municipio") or (col == "Codigo_provincia"):
            pass
        else:
            Q1 = df_copy[col].quantile(0.25)
            Q3 = df_copy[col].quantile(0.75)
            IQR = Q3 - Q1
            minimum = Q1 - (1.5 * IQR)
            maximum = Q3 + (1.5 * IQR)
            media_col = df_copy[col].mean()
            df_copy[col] = df_copy[col].transform(
                lambda x: np.where(x < minimum or x > maximum, media_col, x))

    return df_copy

# Obtiene el análisis univariante de un dataframe


def get_univariate_analysis(df, df_no_outliers):
    """
    Obtiene el análisis univariante de un dataframe

    args:
        list_series: lista de series o dataframes

    returns:
        DataFrame con el análisis univariante de cada columna
    """
    normal_var = 0
    no_normal_var = 0
    univar_analysis = pd.DataFrame(
        {}, columns=["Media", "Mediana", "Moda", "Varianza", "Desviacion_estandar", "Percentil_25", "Percentil_75", "K_test", "p_value", "Distribución"])

    for col in df.columns:
        print(f"\033[1mAnálisis univariante de {col}:\033[0m")
        # Realiza un análisis si la variable es categórica
        if (df[col].dtype == object) or ((col == "Codigo_municipio") or (col == "Codigo_provincia")):
            print(f"Variable categórica:")
            print(f"-Valores únicos:\n{df[col].value_counts()}")
            print(f"-Número de valores únicos: {df[col].nunique()}")
            print("\n\n\n")

        # Realiza un análisis si la variable es numérica
        else:
            # Crea un histograma y un boxplot de la variable
            fig, axes = plt.subplots(1, 2, figsize=(10,4));
            sns.histplot(df_no_outliers[col], kde=True, ax= axes[0]);
            axes[0].set_title("Histograma");
            sns.boxplot(df_no_outliers[col], ax= axes[1]);
            axes[1].set_title("Boxplot");
            fig.suptitle(f"Análisis de {col}");
            plt.show();

            # Comprueba estadisticamente con el test Kolmogorov-Smirnov si la variable sigue una distribución normal
            stat, p = ss.kstest(df[col], 'norm')
            alpha = 0.05

            # Añade los datos al DataFrame dependiendo de si se acepta H0 o no
            if p < alpha:
                no_normal_var += 1
                univar_analysis = univar_analysis.append({"Municipio": col, "Media": df[col].mean(), "Mediana": df[col].median(
                ), "Moda": df[col].mode().iloc[0], "Varianza": df[col].var(), "Desviacion_estandar": df[col].std(), "Percentil_25": df[col].quantile(0.25), "Percentil_75": df[col].quantile(0.75), "K_test": stat, "p_value": p, "Distribución": "No normal"}, ignore_index=True)
                print(f"La columna {col} no presenta una distribución normal\n\n\n")

            else:
                normal_var += 1
                univar_analysis = univar_analysis.append({"Municipio": col, "Media": df[col].mean(), "Mediana": df[col].median(
                ), "Moda": df[col].mode().iloc[0], "Varianza": df[col].var(), "Desviacion_estandar": df[col].std(), "Percentil_25": df[col].quantile(0.25), "Percentil_75": df[col].quantile(0.75), "K_test": stat, "p_value": p, "Distribución": "Normal"}, ignore_index=True)
                print(f"La columna {col} presenta una distribución normal\n\n\n")

    # Establece la columna Municipio como índice
    univar_analysis.set_index("Municipio", inplace=True)

    # Imprime el número de variables que siguen una distribución normal y el que no
    print(
        f"\033[1mNúmero de variables que siguen una distribución normal:\033[0m {normal_var}")
    print(
        f"\033[1mNúmero de variables que no siguen una distribución normal:\033[0m {no_normal_var}")
    return univar_analysis

# Obtiene el análisis bivariante de un dataframe


def get_bivariate_analysis(df):
    """
    Obtiene el análisis bivariante de un dataframe

    args:
        list_series: lista de series o dataframes
    """
    principal_df = df.filter(regex=r'\bInmuebles_totales\b|\b\w+2021\b')
    sns.heatmap(principal_df.corr());
    sns.pairplot(principal_df, diag_kind='kde');

# Obtiene la correlación entre dos o mas variables no paramétricas de un dataframe


def get_significance_friedman(df, regex):
    """
    Determina si existe una diferencias significativas en al menos una de las variables, seleccionadas mediante un regex, de un dataframe pasado como argumento.
    Las variables deben de ser no paramétricas, puesto que se utiliza la prueba de Friedman.

    args:
        df: dataframe
        regex: regex para seleccionar variables
    """
    total_stats_data = []
    df_alq_time = df.filter(regex=regex)
    for col in df_alq_time.columns:
        total_stats_data.append(df_alq_time[col].values)

    f_statistic, p_value = ss.friedmanchisquare(*total_stats_data)
    p_value

    nivel_de_significacion = 0.05
    if p_value < nivel_de_significacion:
        print("A menos uno de los años presenta diferencias significativas con el resto.")
    else:
        print("No hay evidencia suficiente para concluir que hay diferencias significativas entre los grupos.")


def get_difference_in_terms(df, df_no_outliers, list_columns, column_depend):
    """
    Obtiene si existen diferencias significativas entre dos variables dependientes de una tercera.

    args:
        df: dataframe
        list_columns: Lista con las columnas a comprobar si existe diferencias significativas
        column_depend: Columna de la que se quiere comprobar si depende las otras dos variables
    """
    # Crea un boxplot
    plt.figure(figsize=(10, 5));
    sns.boxplot(
        df_no_outliers[[list_columns[0], list_columns[1], column_depend]]);

    # Crea un pairplot de las variables
    sns.pairplot(
        df_no_outliers[[list_columns[0], list_columns[1], column_depend]]);

    variables_name = [list_columns[0], list_columns[1], column_depend]

    # Realiza una correlación de Spearman de todas las variables
    counter = 1
    for col in variables_name:
        if counter <= 3:
            for col2 in variables_name:
                if (col != col2) & (col2 != list_columns[0]):
                    sp, p_value = ss.spearmanr(df[col], df[col2])
                    alpha = 0.05
                    if sp > alpha:
                        print(
                            f"La correlación de Spearman entre {col} y {col2} es significativa")
                    else:
                        print(
                            f"La correlación de Spearman entre {col} y {col2} no es significativa")
                else:
                    pass
            counter += 1
        else:
            break

    df_pvalue = pd.DataFrame(
        {}, columns=variables_name, index=variables_name)
    df_differences = pd.DataFrame(
        {}, columns=variables_name, index=variables_name)
    alpha = 0.05
    # Se calcula si existen diferencias significativas entre ambos grupos a comparar con un tet de Mann-Whitney
    for col1 in variables_name:
        for col2 in variables_name:
            mw, p_value = ss.mannwhitneyu(df[col1], df[col2])
            df_pvalue.loc[col1, col2] = p_value
            if p_value < alpha:
                df_differences.loc[col1, col2] = "Diferencia significativa"
            else:
                df_differences.loc[col1, col2] = "Diferencia no significativa"

    # Df con los valores únicos de la columna a estudiar la dependencia
    unique_valors_tourism = df[column_depend].unique()

    # Lista con todos los p valores a calculados
    p_values_total = []
    # se estudia la diferencia significativa de los datos de las dos variables a comparar que corresponden a los valores únicos de la columna a estudiar la dependencia
    for valor in unique_valors_tourism:
        valor_tour_liv = df[df[column_depend] == valor][list_columns[0]]
        valor_rent_liv = df[df[column_depend] == valor][list_columns[1]]
        mw, p_value = ss.mannwhitneyu(valor_tour_liv, valor_rent_liv)
        p_values_total.append(p_value)

    # Determina si al menos algún grupo de datos comparados tienen una diferencia significativa
    significative = False
    # Guarda todos los p valores de los grupos de datos comparados que tienen una diferencia significativa
    significative_pvalue = []

    for p_value in p_values_total:
        if p_value < alpha:
            significative = True
            significative_pvalue.append(p_value)

    if significative == False:
        print(
            f"Ninguna muestra es significativamente diferente dependiendo de {column_depend}")
    else:
        print(
            f"Al menos una muestra es significativamente diferente dependiendo de {column_depend}")

    print(
        f"Número de muestras paquetes de muestras que son significativamente diferentes y dependientes de {column_depend}: {len(significative_pvalue)}")
    print(
        f"Porcentaje del número de muestras paquetes de muestras que son significativamente diferentes y dependientes de {column_depend} respecto del total: {len(significative_pvalue)*100/len(p_values_total)} %")
    print(
        f"Media de los p-value de cada paquete de muestras a explorar en el test: {pd.Series(p_values_total).mean()}")

    return (df_pvalue, df_differences)
