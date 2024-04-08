import pandas as pd
import joblib
from datetime import datetime
import common
import sqlite3

def predict(date):
    print(f"Loading model")
    # loading model
    model = joblib.load('./models/temperature.model')
    list=[
           date+' '+'00:00:00',
          date+' '+'03:00:00',
          date+' '+'06:00:00',
          date+' '+'09:00:00',
          date+' '+'12:00:00',
          date+' '+'15:00:00',
          date+' '+'18:00:00',
          date+' '+'21:00:00']
    datetime_df = pd.DataFrame(list, columns=['time'])
    datetime_df['time']=pd.to_datetime(datetime_df['time'])
    datetime_df=datetime_df.set_index('time')
    print(f"Making predictions")
    predictions = model.predict(start=datetime_df.index[0], end=datetime_df.index[-1])
    #Saving prediction into database
    print(f"Saving predictions into database")
    prediction_df = pd.DataFrame(columns=['time','predictions','model_name'])
    prediction_df['predictions']=predictions
    prediction_df['time']=list
    prediction_df['model_name']=f'Sarimax'+'_'+f'(4,1,5)'
    with sqlite3.connect(common.DB_PATH) as con:
        prediction_df.to_sql(name='predictions', con=con, if_exists="replace")
    #getting predicting from database
    print(f"getting predicting from database")

    con = sqlite3.connect(common.DB_PATH)
    get_predictions = pd.read_sql('SELECT * FROM predictions', con)
    con.close()
    print(get_predictions)
    #print(get_predictions['time'][1])
    #print(get_predictions['predictions'][1])
    #print(predictions[0])
    #print(predictions.index[1])
    #print(f"displaying predictions")
    #print(predictions)
    return predictions


if __name__ == "__main__":
    date ='2024-01-01'
    predict(date)


