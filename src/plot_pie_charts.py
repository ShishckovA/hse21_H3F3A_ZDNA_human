import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib import pyplot as plt

out_dir = "../images"
data_dir = "../data"

files_to_process = [("DeepZ-filtered", False),
                    ("ENCFF480UVM_hg19-filtered", True),
                    ("ENCFF933JKX_hg19-filtered", True),
                    ("zhunt-filtered", False),
                    ("ZDNA-merge", False)
                   ]

for filename, includes_name_and_score in files_to_process:
    path = f"{data_dir}/{filename}-intersect.bed"
    if includes_name_and_score:
        col_names = ["chrom1", "start1", "end1", "name1", "score1", "type", "chrom2", "start2", "end2", "name2", "score2", "strend"]
    else:
        col_names = ["chrom1", "start1", "end1", "type", "chrom2", "start2", "end2", "name2", "score2", "strend"]

    df = pd.read_csv(path, sep="\t", names=col_names, header=None)
    df.drop_duplicates()
    counts = df["type"].value_counts()
    explode = 0.1 * np.ones(counts.shape)
    labels = [f"{name}: {100 * counts[name] / np.sum(counts):.2f}%" for name in counts.index]
    plt.figure(figsize=(10, 5))
    plt.title(f"{filename}")

    plt.pie(counts, labels=labels, explode=explode)