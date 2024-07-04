import pandas as pd
import locale
import sys

locale.setlocale(locale.LC_ALL, ("de_DE","UTF-8"))
df = pd.read_csv("KSK_Kennzahlen_Werte_2024-light_tbl1.csv",sep=";",decimal=",")
df.rename(columns={"Unnamed: 1":"Topic",
                   "Unnamed: 4":"Einheit",
                   "Unnamed: 21":"Kommentar"},inplace=True)


# fillna
df["Maßnahme"].fillna(method="ffill",inplace=True)
df["Ziffer"].fillna(method="ffill",inplace=True)
df["Ziffer"].fillna("Basics",inplace=True)
df["Topic"].fillna(method="ffill",inplace=True)
df["Topic"].fillna("",inplace=True)
df["Einheit"].fillna("",inplace=True)
df["Topic"] = df["Ziffer"] + "-" + df["Topic"] + "|" +  df["Maßnahme"]

# drop empty lines after fillna !
df.drop(index=df[df["Jahr"].isna()].index,inplace=True)

df.to_csv("ksk.csv")

subset_columns = [str(x) for x in range(2010,2024)]
df["na_count"] = df[subset_columns].isna().sum(axis=1)
df["valid"] = (df["2023"].notna() | df["2022"].notna()) & (df["na_count"] <= 10)

df = df[df["valid"]==True]
#df["Jahr"] = df["Jahr"] + "|" + df["Maßnahme"] +"|" + df["Einheit"]
#df.drop(columns=["Topic","Maßnahme","Einheit","Ziffer","valid","na_count"],inplace=True)
#df.drop(columns=["Topic","valid","na_count"],inplace=True)
df.drop(columns=["Maßnahme","Ziffer","valid","na_count"],inplace=True)
df.to_csv("ksk1.csv")

df.drop(columns=["Datenquelle","Bemerkungen","Kommentar"],inplace=True)
dft = df.set_index("Jahr").T.rename_axis("Jahr")
dft.to_csv("ksk1T.csv")
