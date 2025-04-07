#!/usr/bin/env python3

import os
import sys
import warnings

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from utils.log import log_info
from utils.path import expand_path

warnings.filterwarnings("ignore", category=FutureWarning)


def recall_vs_precision(key: str, key2: str = None, path: str = "", save_to: str = ""):
    log_info(f"Generating recall vs precision plot for key {key} and key2 {key2}")

    df = pd.read_csv(path)

    group_keys = [key] if key2 is None else [key, key2]

    # Group by key(s) and compute mean/std
    agg_df = (
        df.groupby(group_keys)
        .agg(
            {
                "recall": "mean",
                "recall_std": "mean",
                "precision": "mean",
                "precision_std": "mean",
            }
        )
        .reset_index()
    )

    # Melt value metrics
    plot_df = pd.melt(
        agg_df,
        id_vars=group_keys,
        value_vars=["recall", "precision"],
        var_name="metric",
        value_name="value",
    )

    # Melt stds in same order
    plot_df["std"] = pd.melt(
        agg_df,
        id_vars=group_keys,
        value_vars=["recall_std", "precision_std"],
        value_name="std",
    )["std"]

    # Compute y-axis limit
    plot_df["upper"] = plot_df["value"] + plot_df["std"]
    y_max = plot_df["upper"].max()
    y_lim = max(1.0, y_max + 0.05)

    plt.figure(figsize=(10, 6))

    if key2 is None:
        sns.barplot(
            data=plot_df,
            x=key,
            y="value",
            hue="metric",
            palette=["#66c2a5", "#fc8d62"],
            ci=None,
        )
    else:
        # Concatenate key and key2 for grouped x-axis
        plot_df["group"] = plot_df[key].astype(str) + " | " + plot_df[key2].astype(str)

        sns.barplot(
            data=plot_df,
            x="group",
            y="value",
            hue="metric",
            palette=["#66c2a5", "#fc8d62"],
            ci=None,
        )
        plt.xlabel(f"{key} | {key2}")

    # Add error bars manually
    ax = plt.gca()
    group_size = len(plot_df) // 2  # Because we have recall and precision per group
    for i in range(group_size):
        recall_row = plot_df.iloc[i * 2]
        precision_row = plot_df.iloc[i * 2 + 1]

        # Get the corresponding bar for recall and precision
        recall_bar = ax.patches[i * 2]  # First bar is recall
        precision_bar = ax.patches[i * 2 + 1]  # Second bar is precision

        # Add error bars
        ax.errorbar(
            recall_bar.get_x() + recall_bar.get_width() / 2,
            recall_bar.get_height(),
            yerr=recall_row["std"],
            fmt="none",
            c="black",
            capsize=5,
        )
        ax.errorbar(
            precision_bar.get_x() + precision_bar.get_width() / 2,
            precision_bar.get_height(),
            yerr=precision_row["std"],
            fmt="none",
            c="black",
            capsize=5,
        )

    plt.title("Recall vs. Precision")
    plt.ylabel("Score")
    plt.ylim(0, y_lim)
    plt.legend(title="Metric")
    plt.tight_layout()

    if save_to:
        log_info(f"Saving figure to: {save_to}")
        plt.savefig(save_to, dpi=300)
    else:
        plt.show()


if __name__ == "__main__":
    FUNC = os.environ.get("FUNC")
    if FUNC == "recall_vs_precision":
        argc = len(sys.argv)
        if argc == 5:
            recall_vs_precision(
                key=sys.argv[1],
                key2=sys.argv[2],
                path=expand_path(sys.argv[3]),
                save_to=expand_path(sys.argv[4]),
            )
        if argc == 4:
            recall_vs_precision(
                key=sys.argv[1],
                key2=None,
                path=expand_path(sys.argv[2]),
                save_to=expand_path(sys.argv[3]),
            )
