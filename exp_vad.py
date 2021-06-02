import torchaudio
import torch
import os

torch.set_num_threads(6)


class VAD:
    def __init__(self, fname, save_dir=None):
        self.save_dir = save_dir
        self.fname = fname

        self.model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                           model='silero_vad',
                                           force_reload=False)

        (self.get_speech_ts,
         get_speech_ts_adaptive,
         save_audio,
         self.read_audio,
         state_generator,
         single_audio_stream,
         collect_chunks) = utils
        self.speech_timestamps = []

        self.wav = self.read_audio(fname)

    def scanning(self):
        self.speech_timestamps = self.get_speech_ts(
            self.wav, self.model,
            visualize_probs=False,  # True для графиков
            trig_sum=0.13,  # мин порог активации голоса 0.15
            neg_trig_sum=0.11,  # макс порог шума 0.13
            min_speech_samples=10000,  # мин продолж. речи 13000
            min_silence_samples=5000,  # мин. продолж паузы в речи 5000
            # num_samples_per_window=4000,  # number of samples in each window
            # num_steps=8,  # number of overlapping windows to split audio chunk into (we recommend 4 or 8)
        )
        if self.save_dir:
            self._write_file()
        return self.speech_timestamps

    def _write_file(self):
        for idx, timestamp in enumerate(self.speech_timestamps):
            start = timestamp['start']
            end = timestamp['end']
            torchaudio.save(os.path.join(self.save_dir, f'{idx}.wav'), self.wav[start: end], 16000)
