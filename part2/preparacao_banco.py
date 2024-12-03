import pandas as pd
from sqlalchemy import create_engine, text

# Configuração do banco de dados
DATABASE_URI = "mysql+pymysql://root:password@localhost:3307/aeroporto"
engine = create_engine(DATABASE_URI)

def process_flight_statistics():
    batch_size = 10000000

    create_flight_statistics_table()

    offset = 0
    has_data = True

    while has_data:
        print(f"Processando lote a partir do offset {offset}...")

        query = f"""
            SELECT * 
            FROM passengers
            LIMIT {batch_size} OFFSET {offset}
        """
        chunk = pd.read_sql(query, con=engine)

        if chunk.empty:
            has_data = False
            print("Todos os dados foram processados.")
            break

        chunk["TOTAL_DELAY"] = chunk[[
            "CARRIER_DELAY", "WEATHER_DELAY", "NAS_DELAY", 
            "SECURITY_DELAY", "LATE_AIRCRAFT_DELAY"
        ]].sum(axis=1)


        grouped = chunk.groupby(["OP_CARRIER", "OP_CARRIER_FL_NUM", "ORIGIN"])
        stats = grouped.agg(
            AVG_DELAY=pd.NamedAgg(column="TOTAL_DELAY", aggfunc="mean"),
            TOTAL_AIR_TIME=pd.NamedAgg(column="AIR_TIME", aggfunc="sum"),
            TOTAL_DELAY=pd.NamedAgg(column="TOTAL_DELAY", aggfunc="sum")
        ).reset_index()

        stats.rename(columns={"OP_CARRIER": "AIRLINE", "OP_CARRIER_FL_NUM": "FLIGHT_NUMBER"}, inplace=True)

        stats.to_sql("flight_statistics", con=engine, if_exists="append", index=False)
        print(f"Processado lote com {len(chunk)} linhas.")

        offset += batch_size


def create_flight_statistics_table():
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS flight_statistics (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                AIRLINE VARCHAR(5),
                FLIGHT_NUMBER INT,
                ORIGIN VARCHAR(3),
                AVG_DELAY FLOAT,
                TOTAL_AIR_TIME FLOAT,
                TOTAL_DELAY FLOAT,
                CANCELLED BOOL
            )
        """))

if __name__ == "__main__":
    process_flight_statistics()
