import pandas as pd
df = pd.read_csv("klimadata_3.csv",sep=";",decimal=",")
print(df.keys())

def makeTag(x):
    return x.split(" ")[0].replace("/","_")

df["TAG"] = df.MERKMAL.apply(makeTag)

grouped = df.groupby('THEMENBEREICH')
for id, group in grouped:
    group.to_csv(f'topic_{id}.csv', index=False)

grouped = df.groupby('TAG')
for id, group in grouped:
    group.to_csv(f'tag_{id}.csv', index=False)
    group.to_json(f'tag_{id}.json', orient="records")

