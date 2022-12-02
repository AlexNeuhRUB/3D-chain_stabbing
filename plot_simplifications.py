import json
import os
import matplotlib.pyplot as plt

fred_path = "./fred"
stab_path = "./stabbing"

dirs_fred = [dirn for dirn in os.listdir(fred_path) if "Track" in dirn]

dirs_stab = [dirn for dirn in os.listdir(stab_path) if "Track" in dirn]

exp_fred_dict = dict()
exp_stab_dict = dict()


for d in dirs_fred:
    print(f"{fred_path}/{d}/results.json")
    with open(f"{fred_path}/{d}/results.json", "r") as f:
        content = json.load(f)
        for i in range(len(content['Track ID'])):
            if content['Track ID'][i] in exp_fred_dict:
                exp_fred_dict[content['Track ID'][i]].append({'inp': [content['Input lattitude'][i], content['Input longitude'][i]], 'out': [content['Output lattitude'][i], content['Output longitude'][i]]})
            else:
                exp_fred_dict[content['Track ID'][i]] = [{'inp': [content['Input lattitude'][i], content['Input longitude'][i]], 'out': [content['Output lattitude'][i], content['Output longitude'][i]]}]


tracks = list(exp_fred_dict.keys())

for track in tracks:

    plt.plot(exp_fred_dict[track][0]['inp'][0], exp_fred_dict[track][0]['inp'][1])
    plt.plot(exp_fred_dict[track][0]['out'][0], exp_fred_dict[track][0]['out'][1], "--")

    plt.show()
