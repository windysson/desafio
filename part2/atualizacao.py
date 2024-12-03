import pandas as pd
from sqlalchemy import create_engine, text
import joblib

DATABASE_URI = "mysql+pymysql://root:password@localhost:3307/aeroporto"
engine = create_engine(DATABASE_URI)

def update_cancellation_status(batch_size=1000000):
    print("Atualizando status de cancelamento na tabela flight_statistics...")

    model_path = "cancellation_model.pkl"
    try:
        model = joblib.load(model_path)
        print(f"Modelo K-Means carregado de {model_path}")
    except FileNotFoundError:
        print(f"Modelo não encontrado em {model_path}. Certifique-se de treinar o modelo antes.")
        return

    offset = 0
    has_data = True

    while has_data:
        print(f"Processando lote a partir do offset {offset}...")

        query = f"""
        SELECT ID, AVG_DELAY, TOTAL_AIR_TIME, TOTAL_DELAY
        FROM flight_statistics
        LIMIT {batch_size} OFFSET {offset}
        """
        chunk = pd.read_sql(query, con=engine)

        if chunk.empty:
            has_data = False
            print("Todos os status de cancelamento foram atualizados.")
            break

        features = chunk[["AVG_DELAY", "TOTAL_AIR_TIME", "TOTAL_DELAY"]].fillna(0)

        cluster_labels = model.predict(features)
        cancellation_status = determine_cancellation_status(cluster_labels)

        chunk["CANCELLED"] = cancellation_status

        with engine.connect() as connection:
            transaction = connection.begin()
            try:
                for _, row in chunk.iterrows():
                    connection.execute(
                        text("""
                        UPDATE flight_statistics
                        SET CANCELLED = :cancelled
                        WHERE ID = :id
                        """),
                        {
                            "cancelled": row["CANCELLED"],
                            "id": row["ID"]
                        }
                    )
                transaction.commit()
                print(f"Lote com {len(chunk)} linhas atualizado.")
            except Exception as e:
                transaction.rollback()
                print(f"Erro ao atualizar o lote: {e}")
                raise e

        offset += batch_size

def determine_cancellation_status(cluster_labels):

    cluster_to_status = {
        0: 0,  # Não cancelado
        1: 1,  # Cancelado
        2: 1,  # Cancelado
        3: 1,  # Cancelado
        4: 0   # Não cancelado
    }
    return [cluster_to_status[label] for label in cluster_labels]

if __name__ == "__main__":
    update_cancellation_status()
