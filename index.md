## Description
This page provides details of our paper Joint Speech Recognition and Audio Captioning, submitted to ICASSP 2022. 
For better model interpretability and holistic understanding of real-world audio samples, we aim to bring together the growing field of automated audio captioning (AAC) and the well studied automatic speech recognition (ASR), in an end-to-end manner.
The goal of AAC is to generate natural language descriptions of contents in audio samples, while ASR extracts a transcript of speech content.
An exemplar output from our jointly trained models as compared to independently trained ASR and AAC models is shown below.

<p align="left">
<!-- <iframe width="560" height="315" src="https://www.youtube.com/embed/8hSarhQXJbg?start=30" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> -->
</p>

<table>
<colgroup>
<col width="30%" />
<col width="70%" />
</colgroup>
<thead>
<tr class="header">
<th>Method</th>
<th>Generated Output(s)</th>
</tr>
</thead>
<tbody>
<tr>
<td markdown="span">ASR-only</td>
<td markdown="span"><span style="color:blue;">n. e. scale now that's a break job</span></td>
</tr>
<tr>
<td markdown="span">AAC-only</td>
<td markdown="span"><span style="color:magenta;">a train approaches and blows a horn</span></td>
</tr>
<tr>
<td markdown="span">Cat-AAC-ASR<br>(concatenating AAC & ASR outputs)</td>
<td markdown="span"><span style="color:blue;">nice giel now that's a break job</span><br><span style="color:magenta;">a gun fires and a person whistles</span></td>
</tr>
<tr>
<td markdown="span">Dual-decoder</td>
<td markdown="span"><span style="color:blue;">nise feel now that's a break job</span><br><span style="color:magenta;">gunshots fire and male voices with gunshots and blowing while a duck quacks in the background</span></td>
</tr>
<tr>
<td markdown="span">Human Generated</td>
<td markdown="span"><span style="color:blue;">nice kill, now that's a great shot</span><br><span style="color:magenta;">a man speaking and gunshots ringing out</span></td>
</tr>
</tbody>
</table>

## Mixing Samples from WSJ and AudioCaps
A major hurdle in evaluating joint ASR AAC models is the lack of labeled audio datasets with both speech transcriptions and audio captions. 
Therefore we create a multi-task dataset (see below instructions) by mixing the clean speech Wall Street Journal corpus with multiple levels of background noises chosen from the AudioCaps dataset. 

### Requirements
  ```bash
  pip install youtube-dl
  ```

### Clone the repository
  ```bash
  git clone https://github.com/chintu619/Joint-ASR-AAC.git
  cd Joint-ASR-AAC
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
