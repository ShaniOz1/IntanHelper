import numpy as np
import pyedflib
import pyintan
import os

folder_path = r'C:\Shani\SoftC prob\16Ch prob experiments\2025.01.12 E14\Stimulation'

# Traverse all subdirectories to find .rhs files
for root, _, files in os.walk(folder_path):
    for filename in files:
        if filename.endswith('.rhs'):
            try:
                file_path = os.path.join(root, filename)
                # Load the .rhs file
                file = pyintan.File(file_path)

                # Retrieve analog signals
                analog_signals = file.analog_signals[0]
                sig = analog_signals.signal

                try:
                    # Attempt to retrieve stimulation signals if available
                    stimulation = file.stimulation[0].signal
                    data = np.vstack((sig, stimulation))
                except Exception as e:
                    print(f"No stimulation signal in {filename}: {e}")
                    data = sig

                # Define the parameters for EDF file creation
                num_channels = len(data)
                sample_frequency = int(file.sample_rate)
                duration = len(data[0]) / sample_frequency

                # Create the EDF file path
                edf_file = f"{file_path[:-4]}.edf"
                pyedflib.highlevel.write_edf_quick(edf_file, data, sample_frequency)
                print(f"EDF file created successfully: {edf_file}")
            except Exception as e:
                print(f"File {filename} could not be converted: {e}")

