#band-pass filter (8-30 Hz) and compare before/after
import matplotlib.pyplot as plt
import mne
from mne.datasets import eegbci

path=eegbci.load_data(1, [4])[0]
raw=mne.io.read_raw_edf(path, preload=True)

eegbci.standardize(raw)
raw.set_montage(mne.channels.make_standard_montage("standard_1005"))
raw_filt=raw.copy().filter(l_freq=8.0, h_freq=30.0, fir_design="firwin")
raw.compute_psd(fmax=60).plot()
raw_filt.compute_psd(fmax=60).plot()

times=raw.times
mask=times<10
before=raw.get_data(picks="C3")[0]*1e6
after=raw_filt.get_data(picks="C3")[0]*1e6

fig, axes=plt.subplots(2, 1, sharex=True, figsize=(10, 5))
axes[0].plot(times[mask], before[mask])
axes[0].set_title("C3 raw")
axes[1].plot(times[mask], after[mask])
axes[1].set_title("C3 filtered 8-30 Hz")
axes[1].set_xlabel("Time (s)")
for ax in axes:
    ax.set_ylabel("uV")
plt.tight_layout()
plt.show()
