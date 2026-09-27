import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def bar_countprop_plot(df: pd.DataFrame, col_name: str, hue_col_name: str = "y") -> None:
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    sns.countplot(data=df, x=col_name, hue=hue_col_name, ax=ax1)
    ax1.set_title(f"{col_name} — Contagem")
    ax1.tick_params(axis="x", rotation=45)

    sns.histplot(data=df, x=col_name, hue=hue_col_name, multiple="fill", stat="proportion", ax=ax2)
    ax2.set_title(f"{col_name} — Proporção")
    ax2.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.show()
