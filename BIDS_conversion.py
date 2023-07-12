#See https://mne.tools/mne-bids/stable/index.html


import mne
from mne_bids import write_raw_bids, BIDSPath
import os
from pathlib import Path
from mne_bids import print_dir_tree


metaproject_name = 'Dreamachine_META'
subproject_name = 'preprocessing/MNE_BIDS_pipeline'
dataset_name = 'ScienceDay27_Session3'

PROJDIR = os.path.expanduser(f"~/projects/{metaproject_name}")
DATADIR = os.path.join(PROJDIR,f'DATA/{dataset_name}/')
CODEDIR = os.path.join(PROJDIR,f'{subproject_name}')


#1. Read .set EEG files : read .set EEG data files using MNE's read_raw_eeglab() function.
set_files = [file for file in os.listdir(DATADIR) if file.endswith('.set')] #select only .set files
n_participants = len(set_files)
raws = []


for set_file in set_files: 
    raw = mne.io.read_raw_eeglab(DATADIR + set_file, preload=True)
    raws.append(raw)

# Check for events : print the number of events in each .set file
for i, raw in enumerate(raws, 1):
    events,events_id = mne.events_from_annotations(raw) #events variable is a 2D numpy array where the first column is the event time in samples, and the third column is the event id.
    if len(events) > 0:
        print(f"Participant {i} .set file contains {len(events)} events")
    else:
        print(f"Participant {i} .set file contains no events")

# #Create event_id dict
# event_id = {
#     'Impedance': 1,
#     'dmstart': 2,
#     'dmstop': 3,
#     'eegstart': 4,
#     'eegstop': 5,
#     'startpost': 6,
#     'startpre': 7,
#     'stoppost': 8,
#     'stoppre': 9,
#     'synch1': 10,
#     'synch2': 11,
# }



#2. Create BIDSPath : 

# Create the main BIDS directory if it does not exist
bids_dir = Path(f'{DATADIR}/BIDS')
bids_dir.mkdir(parents=True, exist_ok=True)

#Create a BIDSPath for each participant, which describes the naming structure.
bids_paths = []

for participant_id in range(1, n_participants+1):
    bids_path = BIDSPath(subject=str(participant_id), session='1', task='ScienceDay27', root=str(bids_dir))
    bids_paths.append(bids_path)


# 3. Write the raw data to BIDS format
for i in range(n_participants):
    # Define path for this participant's data
    participant_dir = bids_dir / f'sub-{bids_paths[i].subject}'
    
    # Check if data for this participant has already been converted
    if participant_dir.exists():
        print(f"BIDS data for participant {bids_paths[i].subject} already converted.")
    else:
        write_raw_bids(raws[i], bids_paths[i], event_id=events_id, format='BrainVision', allow_preload=True)


# 4. Check the BIDS dataset
print_dir_tree(str(bids_dir))