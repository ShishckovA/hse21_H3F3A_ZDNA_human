import pandas as pd
import seaborn as sns

from matplotlib import pyplot as plt
sns.set(style='darkgrid')


out_dir = "../images"
data_dir = "../data"

files_to_process = [("DeepZ", False), ("ENCFF480UVM_hg19", True), ("ENCFF933JKX_hg19", True), ("zhunt", False), ("ZDNA-merge", False)]

for filename, includes_name_and_score in files_to_process:
    path = f"{data_dir}/{filename}.bed"
    if includes_name_and_score:
        col_names = ["chrom", "start", "end", "name", "score"]
    else:
        col_names = ["chrom", "start", "end"]

    df = pd.read_csv(path, sep="\t", names=col_names, header=None)
    f = plt.figure()
    plt.title(f"{filename}, number of peaks: {len(df)}")
    lens = df["end"] - df["start"]
    plt.hist(lens, bins=30)
    plt.yscale("log")
    f.savefig(f"{out_dir}/{filename}-len-hist.pdf", bbox_inches="tight")
    f.savefig(f"{out_dir}/{filename}-len-hist.png", bbox_inches="tight")
