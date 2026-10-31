import mne
from mne.datasets import eegbci

path = eegbci.load_data(1, [4])[0]
raw = mne.io.read_raw_edf(path, preload=True)

print(raw.info)
print("frequence echantillonnage:", raw.info["sfreq"], "Hz")
print("duree:", raw.times[-1], "s")
print("canaux:", raw.ch_names)
print()
print(raw.annotations)
print()

from collections import Counter
print(Counter(raw.annotations.description))

raw.plot(n_channels=10, duration=20, scalings="auto")
import matplotlib.pyplot as plt
plt.show()
