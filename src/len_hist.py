import pandas as pd
import seaborn as sns
sns.set(style='darkgrid')
from matplotlib import pyplot as plt

out_dir = "../images"
data_dir = "../data"

files_to_process = [("DeepZ", False), ("ENCFF480UVM_hg19", True), ("ENCFF933JKX_hg19", True), ("zhunt", False)]

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
    f.savefig(f"{out_dir}/{filename}-len-hist.pdf", bbox_inches="tight")