import pandas as pd
import joblib
from datetime import datetime
import common
import sqlite3
import matplotlib.pyplot as plt
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (25, 5)

def load_missing_data(path):
    print(f"Reading missing data from the database: {path}")
    con = sqlite3.connect(path)
    train_missing_data = pd.read_sql('SELECT * FROM train_missing_data', con)
    #train_missing_data = pd.read_sql('SELECT * FROM train_missing_data', con)
    con.close()
    #fixed index
    train_missing_data = train_missing_data.set_index('time')
    #train_missing_data = train_missing_data.set_index('time')
    return train_missing_data
def visualizations(date,df):
    #periode de predictions 3 jours

    print(f"Loading model")
    # loading model
    model = joblib.load('./models/temperature.model')
    print(f"setting date format")
    date_debut=date+' '+'00:00:00'
    #getting index for starting date
    df.reset_index(inplace=True)
    index_date_debut = df.index[df['time'] == date_debut]
    df=df.loc[index_date_debut[0]:index_date_debut[0]+23]
    #saving column time for predictions
    print(f"saving data from column time")
    time_save=df['time'].tolist()
    #fixing datetime as the index
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    #create a new data frame for predictions
    datetime_df = pd.DataFrame(time_save, columns=['time'])
    datetime_df['time'] = pd.to_datetime(datetime_df['time'])
    datetime_df = datetime_df.set_index('time')
    print(f"Making predictions")
    predictions = model.predict(start=datetime_df.index[0], end=datetime_df.index[-1])
    #saving prediction into a dataframe
    print(f"Saving predictions into dataframe")
    prediction_df = pd.DataFrame(columns=['time', 'predictions'])
    prediction_df['predictions'] = predictions
    prediction_df['time'] = time_save
    prediction_df['time'] =pd.to_datetime(prediction_df['time'])
    prediction_df = prediction_df.set_index('time')
    #plotting
    plt.figure()
    plt.plot(df.index, df.values, label='real data')
    best_order='_(4,1,5)'
    plt.plot(prediction_df.index, prediction_df.values, label='SARIMAX'+best_order+' '+'forecast')
    plt.legend(loc='best')
    plt.title('SARIMAX Forecast\n {}'.format(best_order))
    plt.show()

    #print(prediction_df)


    # list of concatenating index date
    #making predictions
    #

    return df

if __name__ == "__main__":
    date ='2024-01-01'
    load_missing_data = load_missing_data(common.DB_PATH)
    prepocessed_data = common.preprocess_data(load_missing_data)
    visualizations(date,prepocessed_data)