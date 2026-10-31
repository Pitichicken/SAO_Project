import matplotlib.pyplot as plt
import mne
from mne.datasets import eegbci


#clean canals name + place electrodes
path = eegbci.load_data(1, [4])[0]
raw = mne.io.read_raw_edf(path, preload=True)

eegbci.standardize(raw)

raw.set_montage(mne.channels.make_standard_montage("standard_1005"))

print(raw.ch_names)
for ch in ["C3", "Cz", "C4"]:
    print(ch, "present :", ch in raw.ch_names)

raw.plot_sensors(show_names=True)
plt.show()
