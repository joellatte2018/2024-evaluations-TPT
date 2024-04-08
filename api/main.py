from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from datetime import date,datetime
import pandas as pd
import joblib
import common
import sqlite3
app = FastAPI()

class PredictionInput(BaseModel):
    posted_date: date

@app.post("/generating_predictions/")
async def predict(PredictionInput:PredictionInput):
    date=PredictionInput.posted_date
    date=f"{date}"
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

    prediction_df = get_predictions.drop(columns=['time'])
    return {"predictions effectuées": prediction_df}

@app.post("/recovering_predictions/")
async def recover(PredictionInput:PredictionInput):
    date=PredictionInput.posted_date
    date=f"{date}"
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

    get_predictions = get_predictions.drop(columns=['index'])
    return {"predictions effectuées": get_predictions}

#recuperation des preditions et des donnees reelles observées


def realdata_predictions(date,df):
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
    df = df.rename(columns={'mean_temperature': 'real_data'})
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

    return df,prediction_df
    #return {"Real Data": df}

@app.post("/recovering_realdata_predictions/")
async def recover_realdata_predictions(PredictionInput:PredictionInput):
    date = PredictionInput.posted_date
    date = f"{date}"
    load_missing_data = common.load_missing_data(common.DB_PATH)
    prepocessed_data = common.preprocess_data(load_missing_data)
    results=realdata_predictions(date, prepocessed_data)
    return {"predictions & real data":results}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1",
                port=8000, reload=True)
