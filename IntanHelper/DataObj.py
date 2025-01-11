import os
import pyintan
import numpy as np
import scipy


class DataObj:
    def __init__(self, path, output_folder):
        self.path = path
        self.output_folder = self.create_output_folder(output_folder)

        if path[-3:] == 'rhs':
            file = pyintan.File(path)
            self.start_time = file.datetime
            self.file_name = file.fname
            self.sample_rate = int(file.sample_rate)
            self.recording_data = file.analog_signals[0].signal
            self.recording_channels = file.analog_signals[0].channel_names[0]
            try:
                self.stimulation_data = file.stimulation[0].signal
                self.stimulation_channels = file.stimulation[0].channels
                self.stimulation_indexes = self.get_stimulation_indexes(self.stimulation_data, path[-3:])
                self.stimulation_trials = self.get_stimulation_trials(self.stimulation_data, path[-3:])

            except Exception:
                print('No stimulation found')
                self.stimulation_data = None
                self.stimulation_channels = None
                self.stimulation_indexes = None

    @staticmethod
    def get_stimulation_indexes(stim, file_type):
        if file_type == 'rhs':
            peaks, _ = scipy.signal.find_peaks(stim, height=0.9, distance=30)
            crossings = np.where(np.diff(stim < -0.01))[0]
            crossings = crossings + 1
            crossings = crossings[::2]
            return crossings
        if file_type == 'rhd':
            crossings = np.where(np.diff(np.sign(stim - 0.9)))[0]
            sample_interval = 4
            filtered_crossings = crossings[::sample_interval]
            return filtered_crossings

    @staticmethod
    def get_stimulation_trials(stim, file_type):
        if file_type == 'rhs':
            peaks, _ = scipy.signal.find_peaks(stim, height=0.9, distance=30)
            peaks_diff = np.diff(peaks)
            most_common_val = np.argmax(np.bincount(peaks_diff))
            indices_greater_than_3x = np.where(peaks_diff > 3 * most_common_val)[0]
            trails_indices = peaks[indices_greater_than_3x]
            return trails_indices
        if file_type == 'rhd':
            print('not supported yet')

    @staticmethod
    def create_output_folder(output_folder):
        # output_folder = path.split(os.path.sep)[-1][:-4]
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        # now = datetime.now()
        # now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        # now_output_folder = os.path.join(output_folder, now_str)
        # if not os.path.exists(now_output_folder):
        #     os.makedirs(now_output_folder)
        # return now_output_folder
        return output_folder
