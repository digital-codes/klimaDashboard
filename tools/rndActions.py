import random
import pandas as pd
import numpy as np

sections = ["A","B","C","D","E"]

results = pd.DataFrame()

def mkItems(n=5,total=100,usefloat=True):
    v = np.random.uniform(total/(10*n), total/n, n)
    scale = total / v.sum()
    if usefloat:
        v = np.array([(x * scale) for x in v])
    else:
        v = np.array([round(x * scale) for x in v])
    if v.sum() > total:
        v[np.argmax(v)] -= v.sum() - total
    elif v.sum() < total:
        v[np.argmin(v)] += total - v.sum()
    return v   

def mkGroup(name, count):
    grp = []
    cost = mkItems(n = count,total = 20000000)
    savings = mkItems(n = count,total = 10000)
    # state choices are: dropped, undefined, delayed, on time, done
    for i in range(count):
        item = {
            "section":name,
            "name":f"{name}_{(i+1):02d}",
            "cost":cost[i],
            "savings":savings[i],
            "state":random.choice(range(5))
            }
        grp.append(item)
    return grp

fields = mkItems(len(sections),75, False)    
print(fields.sum(),fields)

for i, field in enumerate(fields):
    grp = mkGroup(sections[i],field)
    r = pd.DataFrame(grp)
    if results.empty:
        results = r
    else:
        results = pd.concat([results,r],ignore_index=True)

# practions for cost and savings
totalCost = results.cost.sum()
totalSavings = results.savings.sum()

results["costFraction"] = round(results.cost/totalCost*100,2)
results["savingsFraction"] = round(results.savings/totalSavings*100,2)

results.to_csv("rndActions.csv",index=False)

# extract sums by sector and state
g2 = results.groupby(by=["section","state"])
g2.sum(numeric_only=True).to_csv("rndActionsSums.csv",index=True)

