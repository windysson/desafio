import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import glob, os

DATABASE_URI = "mysql+pymysql://root:password@localhost:3307/aeroporto"
engine = create_engine(DATABASE_URI)


def preprocess_data(file_path):
    df = pd.read_csv(file_path)
    
    if 'Unnamed: 27' in df.columns:
        df.drop(columns=['Unnamed: 27'], inplace=True)

    numeric_columns = [
        'DEP_TIME', 'DEP_DELAY', 'TAXI_OUT', 'WHEELS_OFF', 'WHEELS_ON',
        'TAXI_IN', 'ARR_TIME', 'ARR_DELAY', 'CANCELLED', 'DIVERTED',
        'ACTUAL_ELAPSED_TIME', 'AIR_TIME', 'CARRIER_DELAY', 'WEATHER_DELAY',
        'NAS_DELAY', 'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY', 'CRS_ELAPSED_TIME',
        'CRS_ARR_TIME', 'CRS_DEP_TIME'
    ]
    df[numeric_columns] = df[numeric_columns].fillna(0)

    categorical_columns = ['CANCELLATION_CODE']
    df[categorical_columns] = df[categorical_columns].fillna("UNKNOWN")

    df['CANCELLATION_CODE'] = df['CANCELLATION_CODE'].apply(lambda x: x if len(str(x)) <= 1 else None)

    df['createdAt'] = datetime.now()

    return df



def insert_row_by_row(df, table_name):
    try:
        df.to_sql(table_name, con=engine, if_exists='append', index=False)

        print("Dados inseridos com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")


for file_path in glob.glob(os.path.join("../data/", "*.csv")):
    print(f"Processando arquivo: {file_path}")

    table_name = "passengers"

    df = preprocess_data(file_path)
    insert_row_by_row(df, table_name)
