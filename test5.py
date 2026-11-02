#compare mu-band (8-12 Hz) on C3 C4 btwn lef/right
import matplotlib.pyplot as plt
import mne
import numpy as np
from mne.datasets import eegbci

mne.set_log_level("WARNING")

SUBJECT=1
RUNS=[4, 8, 12]
event_id={"left_hand": 1, "right_hand": 2}

epochs_list = []
for run in RUNS:
    path=eegbci.load_data(SUBJECT, [run])[0]
    raw=mne.io.read_raw_edf(path, preload=True)
    eegbci.standardize(raw)
    raw.set_montage(mne.channels.make_standard_montage("standard_1005"))
    raw.filter(l_freq=8.0, h_freq=30.0, fir_design="firwin")

    events, _=mne.events_from_annotations(raw, event_id={"T1": 1, "T2": 2})
    epochs_list.append(
        mne.Epochs(raw, events, event_id=event_id, tmin=0.0, tmax=4.0,baseline=None, preload=True, picks="eeg"))

epochs=mne.concatenate_epochs(epochs_list)
labels=epochs.events[:, 2]
print("Total trial:", len(epochs))
for name, code in event_id.items():
    print(f"{name}: {(labels == code).sum()} trial")

channels=["C3", "C4"]
psd=epochs.compute_psd(fmin=8.0, fmax=12.0, picks=channels)
mu_power=10*np.log10(psd.get_data().mean(axis=2))

fig, ax=plt.subplots(figsize=(6, 4))
width=0.35
for i, (name, code) in enumerate(event_id.items()):
    values=mu_power[labels == code]
    mean=values.mean(axis=0)
    sem=values.std(axis=0) / np.sqrt(len(values))
    ax.bar(np.arange(len(channels)) + i * width, mean, width, yerr=sem,capsize=4, label=name)
    print(f"{name}: "+", ".join(f"{ch}={m:.2f} dB" for ch, m in zip(channels, mean)))

ax.set_xticks(np.arange(len(channels)) + width / 2)
ax.set_xticklabels(channels)
ax.set_ylabel("Mu power (dB)")
ax.set_title(f"Mu power by class (subject {SUBJECT}, mean +/- SEM)")
ax.legend()
plt.tight_layout()
plt.show()
