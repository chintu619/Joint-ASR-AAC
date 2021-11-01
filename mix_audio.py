#!/usr/bin/env python3

import argparse
import re
import soundfile as sf
from tqdm import tqdm
import numpy as np
import os
import shutil
from itertools import cycle
np.random.seed(123456)

def normalize(arr):
    return arr/max(1e-10, np.max(np.abs(arr)))
def mix_arrays(arr1, arr2):
    if len(arr1) < len(arr2):
        return mix_arrays(arr2, arr1)
    else:
        start_ix = np.random.randint(len(arr1)-len(arr2)+1)
        arr1[start_ix:start_ix+len(arr2)] += arr2
        return normalize(arr1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('speech_dirs', type=str, help="path to speech wav data directory")
    parser.add_argument('captioned_dir', type=str, help="path to captioned wav data directory")
    parser.add_argument('mixing_weight', type=float, help="mixing weight of captioned audio in [0,1] range")
    args = parser.parse_args()

    speech_dirs = args.speech_dirs # "train_si284 test_dev93 test_eval92"
    captioned_dir = args.captioned_dir # train_audiocaps
    weight = args.mixing_weight
    out_dirtag = f"mixnospwav{weight}" # mixnospwav

    with open(f"data/{captioned_dir}/wav.scp") as f:
        permuted_lines = np.random.permutation(f.readlines())
        id_captionedpaths = [line[:-1].split() for line in permuted_lines]
    with open(f"data/{captioned_dir}/text") as f:
        id2captionedtexts = {line[:-1].split()[0]:' '.join(line[:-1].split()[1:]) for line in f.readlines()}
        id2captionedtexts_nosp = {key:val for key,val in id2captionedtexts.items() if 'SPEAK' not in val and 'TALK' not in val}
        id_captionedpaths_nosp = [file_id for file_id in id_captionedpaths if file_id[0] in id2captionedtexts_nosp]
        print(f'filtered {len(id2captionedtexts_nosp)} non-speech files from {len(id2captionedtexts)} captioned files')

    id_captionedpaths_nosp_tr = cycle(id_captionedpaths_nosp[:-600])
    id_captionedpaths_nosp_te = cycle(id_captionedpaths_nosp[-600:])

    datadirs = speech_dirs.split()
    for datadir in datadirs:
        savedir = f"corpora/wsj_{out_dirtag}/{datadir}"
        save_datadir = f"data/{f'_{out_dirtag}_'.join(datadir.split('_'))}"
        print(f"saving wav files to: {savedir} and kaldi data-dir at: {save_datadir}")
        if not os.path.isdir(savedir): os.makedirs(savedir)
        if not os.path.isdir(save_datadir): os.makedirs(save_datadir)
        wavdir=f"data/{'_wav_'.join(datadir.split('_'))}"
        with open(f"{wavdir}/wav.scp") as f:
            id2speechpaths = {line[:-1].split()[0]:line[:-1].split()[1] for line in f.readlines()}
        with open(f"{wavdir}/text") as f:
            id2speechtexts = {line[:-1].split()[0]:' '.join(line[:-1].split()[1:]) for line in f.readlines()}
        shutil.copyfile(f"{wavdir}/utt2spk", f"{os.path.join(save_datadir,'utt2spk')}")
        shutil.copyfile(f"{wavdir}/spk2utt", f"{os.path.join(save_datadir,'spk2utt')}")
        shutil.copyfile(f"{wavdir}/text",    f"{os.path.join(save_datadir,'text_nocaptions')}")
        shutil.copyfile(f"{wavdir}/text",    f"{os.path.join(save_datadir,'text_spk1')}")

        id2mixedpaths = {}; id2mixedtexts = {}; id2mixedrevtexts = {}
        for speech_id,mix_path1 in tqdm(id2speechpaths.items(), mininterval=60):
            x1,f = sf.read(mix_path1)
            found_good_captioned_file = False
            while not found_good_captioned_file:
                if 'train' in datadir: captioned_id, mix_path2 = next(id_captionedpaths_nosp_tr)
                elif 'test' in datadir: captioned_id, mix_path2 = next(id_captionedpaths_nosp_te)
                else: raise ValueError(f"{datadir} doesn't have train or test")
                try:
                    x2,f = sf.read(mix_path2)
                    if len(x2)/f >= 1: found_good_captioned_file = True
                except:
                    pass
            x_mix = mix_arrays(normalize(x1), weight*normalize(x2))
            mix_id = f"{speech_id}_{captioned_id.split('_')[-1]}"
            savepath = os.path.join(savedir, f'{mix_id}.wav')
            sf.write(savepath, x_mix, f)
            savetext = ' <CAPTION> '.join([id2speechtexts[speech_id],id2captionedtexts_nosp[captioned_id]])
            saverevtext = ' <CAPTION> '.join([id2captionedtexts_sp[captioned_id],dummpy_speechtext])
            id2mixedpaths[speech_id] = savepath
            id2mixedtexts[speech_id] = savetext
            id2mixedrevtexts[speech_id] = saverevtext

        with open(os.path.join(save_datadir,'wav.scp'),'w') as f:
            for key,val in id2mixedpaths.items():
                f.write(f"{key} {os.path.realpath(val)}\n")
        with open(os.path.join(save_datadir,'text'),'w') as f:
            for key,val in id2mixedtexts.items():
                f.write(f"{key} {val}\n")
        with open(os.path.join(save_datadir,'text_revcaptions'),'w') as f:
            for key,val in id2mixedrevtexts.items():
                f.write(f"{key} {val}\n")
        with open(os.path.join(save_datadir,'text_spk2'),'w') as f:
            for key,val in id2mixedtexts.items():
                f.write(f"{key} {val.split(' <CAPTION> ')[-1]}\n")
        with open(os.path.join(save_datadir,'text_onlycaptions'),'w') as f:
            for key,val in id2mixedtexts.items():
                f.write(f"{key} {val.split(' <CAPTION> ')[-1]}\n")
