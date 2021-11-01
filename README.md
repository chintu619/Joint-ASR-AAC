## Mixing Samples from WSJ and AudioCaps

### Requirements
  ```bash
  pip install youtube-dl
  ```

### Clone repository
  ```bash
  git clone https://github.com/chintu619/Joint-ASR-AAC.git
  ```

### Download AudioCaps data
  * Downloading YouTube audio using [`youtube-dl`](https://github.com/ytdl-org/youtube-dl) and `ffmpeg` package
  ```bash
  cat data/train_audiocaps/files_su.txt | ./download_audiocaps.sh
  ```
  * Expected directory structure:
  ```
  corpora/audiocaps_data
  │
  └───train
  │   │   000AjsqXq54.wav
  │   │   001_HxkADSI.wav
  │   │   004NnY1farU.wav
  │   │   ...
  ```

### Convert WSJ data to `.WAV` format
  * Convert WSJ (WSJ0, WSJ1) samples from original `.wv1` format to `.wav` format as follows:
  ```
  corpora/wsj_wav
  │
  └───train_si284
  │   │   011c0201.wav
  │   │   ...
  │
  │───test_dev93
  │   │   4k0c0301.wav
  │   │   ...
  │   
  │───test_eval92
  │   │   440c0401.wav
  │   │   ...
  ```

### Mix WSJ and AudioCaps samples
  * Mix samples from both datasets with specified mixing weight. Output samples will be saved to `corpora/wsj_mixnospwav{0.1,0.2,...}`
  ```bash
  mix_audio.py "train_si284 test_dev93 test_eval92" train_audiocaps 0.1
  mix_audio.py "train_si284 test_dev93 test_eval92" train_audiocaps 0.2
  ...
  ```

### Notes
  * Some of the audio files in YouTube might no longer be available (shown as `ERROR: Video unavailable` while downloading)
  * The audio samples in the AudioCaps dataset are not publicly available. Alternatively, one can use the Clotho-V2 dataset [available here](https://zenodo.org/record/4783391#.YXBTXtnMI-Q). We also provide a script to download and reformat this dataset using `./download_clothov2.sh`.
