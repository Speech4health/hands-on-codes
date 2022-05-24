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

def gen_files(savefolder, dict_):
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
    audiofolder = os.path.join(path, 'audio')
    textfolder = os.path.join(path, 'mlf')
    controlaudiofolder = os.path.join(path, 'audio', 'control')
    print(audiofolder)
    dy_audio = []
    c_audio = []
    textdata = {}
    for filename in os.listdir(audiofolder):
        if filename.startswith('index.html'): continue
        if filename == 'control': continue
        assert  filename in dy_subs
        dy_audio.extend([os.path.join(audiofolder, filename, l) for l in os.listdir(os.path.join(audiofolder, filename))])
    for filename in os.listdir(controlaudiofolder):
        if filename.startswith('index.html'): continue
        assert  filename in c_subs
        c_audio.extend([os.path.join(controlaudiofolder, filename, l) for l in os.listdir(os.path.join(controlaudiofolder, filename))])
    for filename in os.listdir(textfolder):
        if filename not in subs: continue
        mlf_file = [os.path.join(textfolder, filename, f) for f in os.listdir(os.path.join(textfolder, filename)) if f.endswith('.mlf')][0]
        with open(mlf_file, 'r') as f:
            lines = f.read().replace('#!MLF!#\n', '').split('.\n')
        # assert lines[0] == '#!MLF!#'
        datadict = {l.split('\n')[0].replace('*/','').strip('"')[:-4]:l.split('\n')[1] for l in lines if len(l)>0}
        textdata = {**textdata, **datadict}

        # exit()
        # exit()

    print(f'{len(dy_audio)} dysarthric files found')

    print(f'{len(c_audio)} control files found')
    c_dict = {l:textdata[Path(l).stem] for l in c_audio if Path(l).stem in textdata}
    dy_dict = {l:textdata[Path(l).stem] for l in dy_audio if Path(l).stem in textdata}
    print(f'{len(c_dict)} control matched files found')
    print(f'{len(dy_dict)} dysarthric matched files found')
    c_train_dict = {l:c_dict[l] for l in c_dict if 'B1' in Path(l).stem or 'B3' in Path(l).stem}
    c_test_dict = {l:c_dict[l] for l in c_dict if 'B2' in Path(l).stem}
    print(f'{len(c_train_dict)} control matched train files found')
    print(f'{len(c_test_dict)} control matched test files found')
    dy_train_dict = {l:dy_dict[l] for l in dy_dict if 'B1' in Path(l).stem or 'B3' in Path(l).stem}
    dy_test_dict = {l:dy_dict[l] for l in dy_dict if 'B2' in Path(l).stem}
    print(f'{len(dy_train_dict)} dysarthric matched train files found')
    print(f'{len(dy_test_dict)} dysarthric matched test files found')
    for savefolder, audio_text_dict in zip([trainsavefolder1, trainsavefolder2, testsavefolder1, testsavefolder2], [dy_train_dict, c_train_dict, dy_test_dict, c_test_dict]):
        gen_files(savefolder, audio_text_dict)

if __name__ == '__main__':
    assert len(sys.argv) > 3
    path = sys.argv[1]
    trainsavefolder1 = sys.argv[2]
    trainsavefolder2 = sys.argv[3]
    testsavefolder1 = sys.argv[4]
    testsavefolder2 = sys.argv[5]
    subs = sys.argv[3:]
    dy_subs = [s for s in subs if s[0] != 'C']
    c_subs = [s for s in subs if s[0] == 'C']
    trainset = ['B1', 'B3']
    testset = ['B2']
    main()
