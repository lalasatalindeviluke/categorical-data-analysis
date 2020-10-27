import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

os.chdir("E:\\類別資料分析")

titanic = pd.read_csv("E:\\類別資料分析\\titanic.csv", usecols=[1,9,10])
# titanic["parch"].isna().sum() = 900
titanic = titanic.dropna()
titanic["survived"] = titanic["survived"].replace(["no", "yes"], [0, 1])


parch_unique = titanic['parch'].unique()

parch_gender_group_titanic = titanic.groupby(["parch", "gender"])

def print_groups(group_object):
    for name, group in group_object:
        print(name)
        print(group)

print_groups(parch_gender_group_titanic)

titanic_group = parch_gender_group_titanic.agg(np.mean)
titanic_group = titanic_group.rename(columns={"survived":"survival_rate"})

matrix_titanic = titanic_group.unstack(["parch"])

plt.figure(figsize=(16,10))
plt.tick_params(axis="both", labelsize=18)
sns.heatmap(matrix_titanic, annot=True)
