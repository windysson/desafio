import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

DATABASE_URI = "mysql+pymysql://root:password@localhost:3307/aeroporto"
engine = create_engine(DATABASE_URI)

def plot_bar_chart(data):
    plt.figure(figsize=(20, 10))
    sns.barplot(data=data, x="ORIGIN", y="MÉDIA_DELAY", hue="AIRLINE", dodge=True, palette="tab20")
    plt.xticks(rotation=90)
    plt.title("Média de Delay por Origem e Linha Aérea", fontsize=16)
    plt.xlabel("Origem", fontsize=14)
    plt.ylabel("Média de Delay", fontsize=14)
    plt.legend(title="Linha Aérea", loc="upper right", fontsize=10)
    plt.tight_layout()
    plt.savefig("media_delay_por_origem_e_linha_aerea.png")
    plt.show()

def plot_scatter_chart(data):
    plt.figure(figsize=(20, 10))
    scatter = sns.scatterplot(
        data=data,
        x="ORIGIN",
        y="AIRLINE",
        size="CANCELLED",
        hue="FLIGHT_NUMBER",
        sizes=(20, 200),
        palette="coolwarm",
        alpha=0.8,
    )
    scatter.legend(bbox_to_anchor=(1.05, 1), loc="upper left", title="Número do Voo")
    plt.title("Origem vs Linha Aérea com Status de Cancelamento", fontsize=16)
    plt.xlabel("Origem", fontsize=14)
    plt.ylabel("Linha Aérea", fontsize=14)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("origem_linha_aerea_cancelamento.png")
    plt.show()

def main():
    query = """
    SELECT ORIGIN, AIRLINE, FLIGHT_NUMBER, AVG_DELAY AS MÉDIA_DELAY, CANCELLED
    FROM flight_statistics
    """
    data = pd.read_sql(query, con=engine)

    bar_chart_data = (
        data.groupby(["ORIGIN", "AIRLINE"])
        .agg(MÉDIA_DELAY=("MÉDIA_DELAY", "mean"))
        .reset_index()
    )

    scatter_chart_data = data

    plot_bar_chart(bar_chart_data)
    plot_scatter_chart(scatter_chart_data)

if __name__ == "__main__":
    main()
