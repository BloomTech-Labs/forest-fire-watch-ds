"""
All the DS stuff we need.
"""
# DS Logic imports
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
from pandas.util import hash_pandas_object

# joblib to load model
from sklearn.externals import joblib
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer

# database imports
from .models import db, Fire, FrameHash

# time conversion import
import datetime, time

# the source of our live data!
modis_url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6/csv/MODIS_C6_USA_contiguous_and_Hawaii_24h.csv"


def pull_modis(url=modis_url):
    """
    Get latest modis data.
    """
    print("pulling modus - sleep for 1")
    time.sleep(1)

    df = pd.read_csv(url, sep=",")
    print("got dataframe ", df.shape)
    return df


def process_live_data(original_df):
    """
    Pre processes live data to match pipeline expectations.
    """
    print("process_live_data!")
    df = original_df.copy()
    # process satellite labels
    df["satellite"] = df["satellite"].replace({"T": "Terra", "A": "Aqua"})

    # process time features
    df["acq_time"] = (df["acq_time"] // 100) * 60 + (df["acq_time"] % 100)
    df["timestamp"] = df.apply(
        lambda x: datetime.datetime.strptime(x["acq_date"], "%Y-%m-%d")
        + datetime.timedelta(minutes=x["acq_time"]),
        axis=1,
    )
    df["month"] = df["timestamp"].dt.month
    df["week"] = df["timestamp"].dt.weekofyear
    df.drop(columns=["acq_date", "acq_time"], inplace=True)

    return df


xgb_path = "/app/fire_data_api/xgb_pipeline_baseline_full_v2.pkl"

dtc_path = "/app/fire_data_api/dtc_pipeline_baseline_full_v2.pkl"

path = xgb_path


def load_model(path=path):
    """
    Loads our trained classification model pipeline. 
    Must define a custom FunctionTransformer method before loading trained pipeline.
    """

    print("loading_model: ", path)
    return joblib.load(path)


def check_model(path=path):
    """
    Returns the path to the loaded model. Tell us what model is running.
    """
    return str(path)


def classify_fires(original_df):
    """
    Predict fire labels for live data using our trained model.
    Predictions are appended to dataframe in the 'fire' feature.
    We then return a dataframe that can be appended to our SQL DB.
    """
    print("classify_fires")
    model = load_model()

    df = original_df.copy()

    df["fire"] = model.predict(df)

    # List of the features we want to store in our database
    results = ["latitude", "longitude", "fire", "timestamp"]

    return df[results]


def add_fires(df):
    """
    Adds predictions to our database.
    """
    # assumes df has the shape of results,
    # i.e. ['latitude', 'longitude', 'acq_date', 'fire', 'timestamp']

    print("add_fires")

    for row in df.values:
        pred = Fire(
            latitude=str(round(row[0], 2)),
            longitude=str(round(row[1], 2)),
            fire=str(row[2]),
            timestamp=(row[3]),
        )

        db.session.add(pred)

    db.session.commit()


def add_hash(df_hash):
    """
    Adds a new hash to our hash table.
    """
    ts = datetime.datetime.now()
    print("add_hash")
    # print('timestamp: ', ts)
    # print('datatype: ', type(ts))

    hash = FrameHash(hash=str(df_hash), timestamp=ts)

    db.session.add(hash)
    db.session.commit()


def check_new_df():
    """
    Pulls a new df from modis and compares it to previous data pulls
    """
    print("check_new_df")
    new_df = pull_modis()
    time.sleep(1)

    # hash new dataframe to check if we have already added it.
    df_hash = str(hash_pandas_object(new_df).sum())
    print("latest df_hash: ", df_hash)

    # get all existing db hashes
    print("getting ready to query the db for hashes.")
    try:
        hash_query = FrameHash.query.all()
        time.sleep(3)

    except Exception as e:
        print("Hash query failed: ", e)
        hash_query = []

    print(len(hash_query))
    hashes = [x.hash for x in hash_query]
    print("existing hashes", hashes)

    if df_hash in hashes:
        print("Not adding hash/updating data")
        return 1
    else:
        add_hash(df_hash)
        return new_df
