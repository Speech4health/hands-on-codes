"""
author: Sathvik Udupa
affiation: SPIRE Lab, Indian Institute of Science (2022)
contact: sathvikudupa66@gmail.com
"""

import os, sys
from pathlib import Path
import shutil
from tqdm import tqdm

def read_prompts(folder):
    dict_ = {}
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r') as f:
            lines = f.read().split('\n')
        lines = [l for l in lines if len(l)>0 and '[' not in l and '.jpg' not in l]
        assert len(lines) <= 1
        if len(lines) == 1: dict_[filename[:-4]] = lines[0]
    return dict_

def save_files(data):
    if isinstance(data, dict):
        for path_ in data:
            with open(path_, 'w') as f:
                for line in data[path_]:
                    f.write(line+'\n')
    else:
        raise NotImplementedError

def gen_files(dict_):
    wav2scp, text, utt2spk = [], [], []
    for path in dict_:
        id = Path(path).stem
        speaker = id.split('-')[0]
        wav2scp.append(id + ' ' + path)
        text.append(id + ' ' + dict_[path].upper())
        utt2spk.append(id + ' ' + speaker)
    save_files({os.path.join(savefolder, 'wav.scp'):wav2scp,
                os.path.join(savefolder, 'text'):text,
                os.path.join(savefolder, 'utt2spk'):utt2spk})

def main():
    audio_text_dict = {}
    if not os.path.exists(os.path.join(savefolder, 'audio')):
        os.mkdir(os.path.join(savefolder, 'audio'))
    for subject in tqdm(subs):
        subject_path = os.path.join(path, subject)
        for folder in os.listdir(subject_path):
            if folder.startswith('Session'):
                session_path = os.path.join(subject_path, folder)
                promptfolder = os.path.join(subject_path, folder, "prompts")
                promptdict = read_prompts(promptfolder)
                if not os.path.exists(promptfolder):
                    raise Exception(f'{promptfolder} not found')
                for subfolder in os.listdir(session_path):
                    if subfolder.startswith('wav'):
                        wav_path = os.path.join(session_path, subfolder)
                        wavfiles = os.listdir(wav_path)
                        id = f'{subject}-{folder}-{subfolder}-'
                        savenames = [id+w for w in wavfiles]
                        for (oldname, newname) in zip(wavfiles, savenames):
                            if oldname[:-4] not in promptdict:
                                continue
                            oldnamepath = os.path.join(wav_path, oldname)
                            newnamepath = os.path.join(savefolder, 'audio', newname)
                            if not os.path.exists(newnamepath):
                                shutil.copy(oldnamepath, newnamepath)
                            audio_text_dict[newnamepath] = promptdict[oldname[:-4]]
    print(subs)
    print(f'{len(audio_text_dict)} pairs found')
    gen_files(audio_text_dict)
    
if __name__ == '__main__':
    assert len(sys.argv) > 4
    path = sys.argv[1]
    savefolder = sys.argv[2]
    subs = sys.argv[3:]

    main()
