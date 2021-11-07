import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib import pyplot as plt
sns.set(style='darkgrid')


out_dir = "../images"
data_dir = "../data"

files_to_process = [("DeepZ", False, 800),
                    ("ENCFF480UVM_hg19", True, 1800),
                    ("ENCFF933JKX_hg19", True, 4000),
                    ("zhunt", False, 60)
                   ]

for filename, includes_name_and_score, max_len in files_to_process:
    path = f"{data_dir}/{filename}.bed"
    if includes_name_and_score:
        col_names = ["chrom", "start", "end", "name", "score"]
    else:
        col_names = ["chrom", "start", "end"]

    df = pd.read_csv(path, sep="\t", names=col_names, header=None)
    df.drop_duplicates()
    f = plt.figure()
    lens = df["end"] - df["start"]
    to_filter = lens < max_len
    df_filtered = df[to_filter]

    plt.title(f"{filename} - filtered, number of peaks: {np.sum(to_filter)}")
    plt.hist(lens[to_filter], bins=30)
    plt.yscale("log")
    f.savefig(f"{out_dir}/{filename}-filtered-len-hist.pdf", bbox_inches="tight")
    f.savefig(f"{out_dir}/{filename}-filtered-len-hist.png", bbox_inches="tight")

    df_filtered.sort_values(by=["chrom", "start"])
    df_filtered.to_csv(f"{data_dir}/{filename}-filtered.bed", header=None, sep="\t", index=None)
