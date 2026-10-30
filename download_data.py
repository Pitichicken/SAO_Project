from mne.datasets import eegbci

SUBJECTS=range(1, 16)
RUNS=[4, 6, 8, 10, 12, 14]

for s in SUBJECTS:
    print(f"\nsubject {s}/{len(SUBJECTS)}\n")
    eegbci.load_data(s, RUNS)

print("stored in ./data/")
