import soundfile as sf
import os
import torch

torch.set_num_threads(6)


class VAD:
    def __init__(self, fname, save_dir):
        self.save_dir = save_dir
        self.fname = fname

        self.wav, self.rate = sf.read(fname)

        self.model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                           model='silero_vad',
                                           force_reload=True)

        (_, _, _, self.state_generator, _, _) = utils
        self.time = []

    def scanning(self):
        counter = 0
        self.time = []
        for batch in self.state_generator(self.model, [self.fname], audios_in_stream=1):
            if batch:
                counter += 1
                self.time.append(*batch[0][0].keys())

            if batch and not counter % 2:
                self._write_file()
                self.time = []

    def _write_file(self):
        start, end = self.time
        start_f = start // self.rate
        end_f = end // self.rate

        fname = f'{start_f}-{end_f}.wav'
        sf.write(os.path.join(self.save_dir, fname), self.wav[start: end], self.rate)
