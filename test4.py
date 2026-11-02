#cut the filter signal into epoch around T1/T2 events
import matplotlib.pyplot as plt
import mne
from mne.datasets import eegbci

path=eegbci.load_data(1, [4])[0]
raw=mne.io.read_raw_edf(path, preload=True)

eegbci.standardize(raw)
raw.set_montage(mne.channels.make_standard_montage("standard_1005"))

raw.filter(l_freq=8.0, h_freq=30.0, fir_design="firwin")

events, _=mne.events_from_annotations(raw, event_id={"T1": 1, "T2": 2})
eventid={"left_hand": 1, "right_hand": 2}

epochs = mne.Epochs(
    raw,
    events,
    event_id=eventid,
    tmin=0.0,
    tmax=4.0,
    baseline=None,
    preload=True,
    picks="eeg",
)

print(epochs)
print("Data shape (trial, channel,sample):", epochs.get_data().shape)
for name in eventid:
    print(f"{name}: {len(epochs[name])} trials")

epochs["left_hand"].plot_image(picks="C3", title="C3 - left hand")
epochs["right_hand"].plot_image(picks="C3", title="C3 - right hand")
plt.show()
