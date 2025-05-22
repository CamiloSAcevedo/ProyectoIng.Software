# scripts/clustering.py

from sklearn.cluster import KMeans
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from administrador.models import Vacante

def agrupar_vacantes(n_clusters=5):
    vacantes = Vacante.objects.all().values(
        'id', 'ubicacion', 'experiencia', 'salario', 'modalidad', 'industria'
    )
    
    df = pd.DataFrame(list(vacantes))

    # Llenar vacíos y codificar categorías
    df.fillna('', inplace=True)
    encoder = OneHotEncoder()
    cat_features = encoder.fit_transform(df[['ubicacion', 'experiencia', 'modalidad', 'industria']]).toarray()

    # Convertir features categóricas a DataFrame con columnas como string
    cat_df = pd.DataFrame(cat_features)
    cat_df.columns = cat_df.columns.astype(str)
    
    # Convertir salario a DataFrame
    salario_df = df[['salario']].fillna(0).astype(float).reset_index(drop=True)

    # Concatenar y asegurar que todas las columnas sean string
    final_data = pd.concat([cat_df, salario_df], axis=1)
    final_data.columns = final_data.columns.astype(str)

    # Aplicar clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['grupo'] = kmeans.fit_predict(final_data)

    # Actualizar vacantes en base de datos
    for index, row in df.iterrows():
        Vacante.objects.filter(id=row['id']).update(grupo=row['grupo'])

    print("Clustering completado.")
