import os
import glob
from DataObj import DataObj
import os
from scipy import signal
import glob
# from direct_response import prepare_roi_mat, remove_stimulation_artifact, spikes_analysis
import viz
import utils
from pathlib import Path
from collections import defaultdict
import pandas as pd


"""Local path should consist two subfolders:
- aCSF
- Retina
where in each folder there are 16 redordings, recorded with same parameters but different stimulation channel.
"""
local_path = r'C:\Shani\SoftC prob\16Ch prob experiments\2025.01.08 E14\Retina2'
output_folder = r'outputs'

pattern = os.path.join(local_path, '**', '*.rhs*')
matching_files = glob.glob(pattern, recursive=True)
objects = []

for file in matching_files:
    obj = DataObj(file, output_folder)
    # sos = signal.butter(2, [300, 3000], btype='bandpass', fs=int(obj.sample_rate), output='sos')
    # obj.recording_data = signal.sosfiltfilt(sos, obj.recording_data)

    obj.parent_folder = next((p.name for p in Path(file).parents if 'Recordings' in p.name), None)
    obj.pulses = utils.get_recorded_pulses(stim_ind=obj.stimulation_indexes,
                                                     data=obj.recording_data, sample_rate=obj.sample_rate,
                                                     win_size=9)
    objects.append(obj)

objects_by_channel = defaultdict(list)
for obj in objects:
    objects_by_channel[obj.stimulation_channels].append(obj)
sorted_objects_by_channel = [group for _, group in sorted(objects_by_channel.items())]

# plot artifact
for items in sorted_objects_by_channel:
    viz.plot_overlay_pulses(items)

# Find saturation
results = []
for obj in objects:
    recording_data = obj.recording_data
    rows_with_max_gt_6300 = [i for i, row in enumerate(abs(recording_data)) if row.max() > 6300]
    results.append({
        "stimulation_channels": obj.stimulation_channels,
        "parent_folder": obj.parent_folder,
        "row": rows_with_max_gt_6300
    })

# Convert the results list to a DataFrame
df = pd.DataFrame(results)
df = df.sort_values(by="stimulation_channels")

