import pandas as pd
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
import joblib

DATABASE_URI = "mysql+pymysql://root:password@localhost:3307/aeroporto"
engine = create_engine(DATABASE_URI)

def train_unsupervised_model(sample_size=30000000, n_clusters=5):

    print("Carregando dados da tabela flight_statistics...")

    query = f"""
    SELECT AVG_DELAY, TOTAL_AIR_TIME, TOTAL_DELAY
    FROM flight_statistics
    LIMIT {sample_size}
    """

    df = pd.read_sql(query, con=engine)

    features = df[["AVG_DELAY", "TOTAL_AIR_TIME", "TOTAL_DELAY"]].fillna(0)

    print(f"Treinando modelo K-Means com {len(df)} amostras e {n_clusters} clusters...")

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(features)

    df["CLUSTER"] = kmeans.labels_

    cluster_summary = df.groupby("CLUSTER").agg(
        AVG_DELAY=("AVG_DELAY", "mean"),
        TOTAL_AIR_TIME=("TOTAL_AIR_TIME", "mean"),
        TOTAL_DELAY=("TOTAL_DELAY", "mean"),
        COUNT=("CLUSTER", "count")
    )
    print("Resumo dos clusters:")
    print(cluster_summary)

    model_path = "cancellation_model.pkl"
    joblib.dump(kmeans, model_path)
    print(f"Modelo K-Means salvo como {model_path}")

    return kmeans

if __name__ == "__main__":
    train_unsupervised_model()
