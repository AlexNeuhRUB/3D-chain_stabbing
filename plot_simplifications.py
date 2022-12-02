import json
import os
import numpy as np
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

for d in dirs_stab:
    print(f"{stab_path}/{d}/results.json")
    with open(f"{stab_path}/{d}/results.json", "r") as f:
        content = json.load(f)
        for i in range(len(content['Track ID'])):
            if content['Track ID'][i] in exp_stab_dict:
                exp_stab_dict[content['Track ID'][i]].append({'inp': [content['Input lattitude'][i], content['Input longitude'][i]], 'out': [content['Output lattitude'][i], content['Output longitude'][i]]})
            else:
                exp_stab_dict[content['Track ID'][i]] = [{'inp': [content['Input lattitude'][i], content['Input longitude'][i]], 'out': [content['Output lattitude'][i], content['Output longitude'][i]]}]

tracks = list(exp_fred_dict.keys())

for track in tracks:

    plt.plot(exp_fred_dict[track][0]['inp'][0], exp_fred_dict[track][0]['inp'][1])
    plt.plot(exp_fred_dict[track][0]['out'][0], np.array(exp_fred_dict[track][0]['out'][1]), "--")

    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_axis_off()

    plt.savefig(f"fred_track{track}.pdf",bbox_inches='tight',pad_inches = 0)
    plt.close()

for track in tracks:

    fig, axs = plt.subplots(3, 3)
    for i in range(3):
        for j in range(3):
            axs[i,j].plot(exp_stab_dict[track][3*i+j]['inp'][0], exp_stab_dict[track][3*i+j]['inp'][1])
            axs[i,j].plot(exp_stab_dict[track][3*i+j]['out'][0], np.array(exp_stab_dict[track][3*i+j]['out'][1]), "--")

            axs[i,j].get_xaxis().set_visible(False)
            axs[i,j].get_yaxis().set_visible(False)
            axs[i,j].set_axis_off()

    plt.savefig(f"stabbing_track{track}.pdf",bbox_inches='tight',pad_inches = 0)
    plt.close()


