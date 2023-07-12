import os
import mne
import argparse
import mne_bids.config
import sys
print(sys.path)
print(dir(mne_bids.config))
# from mne_bids.config import BIDS_PATH
from mne_bids import BIDSPath

config_validation = 'warn'

metaproject_name = 'Dreamachine_META'
subproject_name = 'preprocessing/MNE_BIDS_pipeline'
dataset_name = 'ScienceDay27_Session3'

PROJDIR = os.path.expanduser(f"~/projects/{metaproject_name}")
CODEDIR = os.path.join(PROJDIR,f'{subproject_name}')

study_name = "ScienceDay27_Session3"


# Set the BIDS root
bids_root = os.path.join(PROJDIR,f'DATA/{dataset_name}/BIDS')
deriv_root = os.path.expanduser(f"~/projects/{metaproject_name}/DATA/{study_name}/derivatives/mne-bids-pipeline") #path where process output will be stored


# Find the --task option
args = [arg for arg in sys.argv if arg.startswith("--task") or not arg.startswith("-")]
parser = argparse.ArgumentParser()
parser.add_argument("ignored", nargs="*")
parser.add_argument(
    "--task", choices=("1"), required=True
)
# task = parser.parse_args(args).task #use this if we have more than one task/session

sessions = ["1"]
task = "ScienceDay27"

subjects = ["1", "2", "3"]

ch_types = ["eeg"]
interactive = False

raw_resample_sfreq = 250


eeg_template_montage = mne.channels.make_standard_montage("standard_1020")
eeg_bipolar_channels = {
    "HEOG": ("HEOG_left", "HEOG_right"),
    "VEOG": ("VEOG_lower", "FP2"),
}
drop_channels = ["HEOG_left", "HEOG_right", "VEOG_lower"]
eog_channels = ["HEOG", "VEOG"]

# Use EEG channels:
ch_types = ['eeg']

# Specify preprocessing options : used setups from Schwartzman et al.,2019
l_freq = 1  # High-pass filter cutoff (in Hz)
h_freq = 30  # Low-pass filter cutoff (in Hz)
notch_freq = 60



decode = True
decoding_time_generalization = True
decoding_time_generalization_decim = 2

find_breaks = True
min_break_duration = 10
t_break_annot_start_after_previous_event = 3.0
t_break_annot_stop_before_next_event = 1.5

ica_reject = dict(eeg=350e-6, eog=500e-6)
reject = "autoreject_global"

spatial_filter = "ica"
eeg_reference = 'average'

ica_max_iterations = 1000
ica_eog_threshold = 2
ica_decim = 2  # speed up ICA fitting

run_source_estimation = False

on_rename_missing_events = "ignore"

parallel_backend = "dask"
dask_worker_memory_limit = "2G"
n_jobs = 2

if task == "ScienceDay27":
    dask_open_dashboard = True
    task_is_rest = True
    conditions = None

