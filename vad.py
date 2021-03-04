from itertools import chain
import soundfile as sf
import numpy as np
import os


class VAD:
    def __init__(self, fname, save_dir, mode: int = 0):
        self.save_dir = save_dir
        self.fname = fname
        self.mode = mode

        self.wav, self.rate = sf.read(fname)

        if not self.mode:
            self.size = self.rate // 4
            self.stop_iter = 5
            self.threshold_coefficient = 1.2

        elif self.mode == 1:
            self.size = self.rate // 2
            self.stop_iter = 8
            self.threshold_coefficient = 1.2

        elif self.mode == 2:
            self.size = self.rate
            self.stop_iter = 10
            self.threshold_coefficient = 1.1

        self.num_slice = len(self.wav) // self.size

        self.audio_frames = []
        self.rec = False
        self.iter_file = 0
        self.sample = 0
        self.counter = 0
        self.start = 0

    def _value_analysis(self):
        self.threshold = np.mean(np.abs(self.wav)) * self.threshold_coefficient

    def _detected(self):
        if self.value > self.threshold and not self.rec:
            self.start = self.counter * self.size
            self.rec = True
            self.sample += 1
            self.stop_iter = 20
            self.audio_frames.append(self.data)
        elif self.rec and self.value > self.threshold:
            self.audio_frames.append(self.data)
        elif self.rec and self.value < self.threshold:
            self.audio_frames.append(self.data)
            self.stop_iter -= 1

        if self.rec and self.stop_iter < 0:
            self.audio_frames.append(self.data)
            if len(self.audio_frames) > 4:
                self._write_file()
                self.audio_frames = []
                self.iter_file += 1
                self.rec = False
                self.sample = 0

    def scanning(self):
        self._value_analysis()

        for idx in range(self.num_slice):
            start = idx * self.size
            end = start + self.size
            self.data = self.wav[start: end]
            self.value = np.mean(np.abs(self.data))
            self.counter += 1
            self._detected()

    def _write_file(self):
        lenght = len(self.audio_frames)
        lenght_time = lenght * self.size / self.rate
        time_end = (self.counter * self.size) / self.rate
        time_start = time_end - lenght_time

        time_fragment_start = int(time_start)
        time_fragment_end = int(time_end)
        fname = f'{time_fragment_start}-{time_fragment_end}.wav'
        sf.write(os.path.join(self.save_dir, fname), list(chain(*self.audio_frames)), self.rate)