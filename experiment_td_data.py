import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import acctelemetry
from ldparser import ldparser


####

data = pd.read_csv('./data/Austin.csv').to_numpy()

min_x = abs(data[:, 0].min())
min_y = abs(data[:, 1].min())

max_x = data[:, 0].max() + min_x
max_y = data[:, 1].max() + min_y

data[:, 0] = (data[:, 0] + min_x) / max_x
data[:, 1] = (data[:, 1] + min_y) / max_y

data[:, 2] = data[:, 2] / 500
data[:, 3] = data[:, 3] / 500

rights = []
lefts = []
vectors = []

for i in range(0, data.shape[0], 2):
    p1 = data[i, :2]
    if i + 1 >= data.shape[0]:
        p2 = data[0, :2]
    else:
        p2 = data[i + 1, :2]
    
    width_right = data[i, 2]
    width_left = data[i, 3]
    
    vector = p2 - p1
    vector = vector / np.linalg.norm(vector)
    vector = np.array([-vector[1], vector[0]])
    vectors.append(vector)
    
    right_p1 = p1 + width_right * vector
    left_p1 = p1 - width_left * vector
    
    rights.append(right_p1)
    lefts.append(left_p1)
    
rights = np.array(rights)
lefts = np.array(lefts)
vectors = np.array(vectors)

plt.plot(data[:, 0], data[:, 1])
plt.plot(rights[:, 0], rights[:, 1])
plt.plot(lefts[:, 0], lefts[:, 1])


#####
file_path = "./data/Barcelona-bmw.ld"
#file_path = "./data/cota-porsche_992_gt3_r-1-2023.10.15-14.43.56.ld"

data = acctelemetry.getData(file_path)

head_, chans = ldparser.read_ldfile(file_path)
laps = np.array(acctelemetry.laps(file_path))

ds = acctelemetry.LDDataStore(
    chans, laps,
    acc=head_.event != 'AC_LIVE'
)

df_ = ds.get_data_frame(data["lap"][0])

td_data = np.stack([df_.x.values, df_.y.values]).T


min_x = abs(td_data[:, 0].min())
min_y = abs(td_data[:, 1].min())

max_x = td_data[:, 0].max() + min_x
max_y = td_data[:, 1].max() + min_y

td_data[:, 0] = (td_data[:, 0] + min_x) / max_x
td_data[:, 1] = (td_data[:, 1] + min_y) / max_y

# td_data[:, 2] = td_data[:, 2] / 500
# td_data[:, 3] = td_data[:, 3] / 500

plt.plot(td_data[:,0], td_data[:, 1])
plt.savefig("mygraph.png")