import requests
import pandas as pd
import sqlite3
import common
def upload_missing_data():
    print(f"Upload missing data")
    # Effectuer une requête GET à l'API
    response = requests.get(
        'https://archive-api.open-meteo.com/v1/archive?latitude=5.3544&longitude=-4.0017&start_date=2024-01-01&end_date=2024-03-25&hourly=temperature_2m&timezone=GMT')
    # Vérifier si la requête a réussi (code de statut 200)
    if response.status_code == 200:
        # Convertir la réponse JSON en un dictionnaire Python
        data_dict = response.json()
        # Créer un DataFrame à partir du dictionnaire
        df = pd.DataFrame(data_dict)
        # Afficher le DataFrame
        print(df)
    else:
        # Afficher un message d'erreur si la requête a échoué
        print('La requête à l\'API a échoué avec le code de statut :', response.status_code)

def convert_to_datetime(df):
    new_df = pd.DataFrame(columns=['time', 'temperature_2m'])
    new_df['time'] = df['hourly']['time']
    new_df['temperature_2m'] = df['hourly']['temperature_2m']
    new_df['time'] = pd.to_datetime(new_df['time'])
    #fixed column time to index
    new_df = new_df.set_index('time')
    return new_df

def insert_into_DB(df):
    print(f"inserted into the database: {common.DB_PATH}")
    with sqlite3.connect(common.DB_PATH) as con:
        df.to_sql(name='train_missing_data', con=con, if_exists="replace")
    return 'inserted with success'

if __name__ == "__main__":

    missing_df= upload_missing_data()
    converted_df = convert_to_datetime(missing_df)
    inserted_df = insert_into_DB(converted_df)


