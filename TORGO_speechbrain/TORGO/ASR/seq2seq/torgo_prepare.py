"""
Data preparation for torgo, modified from LibriSpeech recipe

Author
------
Sathvik Udupa 2022
"""

import os
import csv
import random
import shutil
from tqdm import tqdm
from collections import Counter
import logging
import torchaudio
from pathlib import Path
from speechbrain.utils.data_utils import download_file, get_all_files
from speechbrain.dataio.dataio import (
    load_pkl,
    save_pkl,
    merge_csvs,
)
num_dev = 200
logger = logging.getLogger(__name__)
OPT_FILE = "opt_librispeech_prepare.pkl"
SAMPLERATE = 16000
sets = {'train1':["F01", "F03", "M01", "M02", "M03", "M04"],
        "train2":["FC01", "FC02", "MC01", "MC02", "MC03"],
        "test1":["F04", "M05"],
        "test2":["FC03", "MC04"]}


def read_prompts(folder):
    dict_ = {}
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r') as f:
            lines = f.read().split('\n')
        lines = [l for l in lines if len(l)>0 and '[' not in l and '.jpg' not in l]
        assert len(lines) <= 1
        if len(lines) == 1: dict_[filename[:-4]] = lines[0]
    return dict_

def prepare_torgo(
    data_folder,
    save_folder,
    tr_splits=[],
    dev_splits=[],
    te_splits=[],
    select_n_sentences=None,
    merge_lst=[],
    merge_name=None,
    create_lexicon=False,
    skip_prep=False,
):

    if skip_prep:
        return
    data_folder = data_folder
    splits = tr_splits + dev_splits + te_splits
    save_folder = save_folder
    select_n_sentences = select_n_sentences
    conf = {
        "select_n_sentences": select_n_sentences,
    }

    # Other variables
    # Saving folder
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    save_opt = os.path.join(save_folder, OPT_FILE)

    # Check if this phase is already done (if so, skip it)
    if skip(splits, save_folder, conf):
        logger.info("Skipping preparation, completed in previous run.")
        # return
    else:
        logger.info("Data_preparation...")

    # create csv files for each split
    all_texts = {}
    savefolder_ = 'renamed_data'
    if not os.path.exists(savefolder_):
        os.mkdir(savefolder_)
    else:
        logger.info("Data found, skipping prep")
        return
    for key in sets:
        audio_text_dict = {}
        for subject in tqdm(sets[key]):
            subject_path = os.path.join(data_folder, subject)
            print(subject_path)
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
                                newnamepath = os.path.join(savefolder_, newname)
                                if not os.path.exists(newnamepath):
                                    shutil.copy(oldnamepath, newnamepath)
                                audio_text_dict[newnamepath] = promptdict[oldname[:-4]]
        text_dict = {Path(l).stem:audio_text_dict[l] for l in audio_text_dict}
        create_csv(
            save_folder, list(audio_text_dict.keys()), text_dict, key, len(audio_text_dict),
        )

    with open(os.path.join(save_folder, 'train1.csv'), 'r') as f:
        lines = f.read().split('\n')[:-1]
    ids = lines[0]
    lines = lines[1:]
    random.shuffle(lines)
    with open(os.path.join(save_folder, 'dev1.csv'), 'w') as f:
        f.write(ids+'\n')
        for l in lines[:num_dev]:
            f.write(l+'\n')
    with open(os.path.join(save_folder, 'train1.csv'), 'w') as f:
        f.write(ids+'\n')
        for l in lines[num_dev:]:
            f.write(l+'\n')


    with open(os.path.join(save_folder, 'train2.csv'), 'r') as f:
        lines = f.read().split('\n')[:-1]
    ids = lines[0]
    lines = lines[1:]
    random.shuffle(lines)
    with open(os.path.join(save_folder, 'dev2.csv'), 'w') as f:
        f.write(ids+'\n')
        for l in lines[:num_dev]:
            f.write(l+'\n')
    with open(os.path.join(save_folder, 'train2.csv'), 'w') as f:
        f.write(ids+'\n')
        for l in lines[num_dev:]:
            f.write(l+'\n')

    with open(os.path.join(save_folder, 'train1.csv'), 'r') as f:
        lines2 = f.read().split('\n')[:-1]
    ids = lines2[0]
    lines2 = lines2[1:]
    with open(os.path.join(save_folder, 'train.csv'), 'w') as f:
        f.write(ids+'\n')
        for l in lines[num_dev:]+lines2:
            f.write(l+'\n')
    with open(os.path.join(save_folder, 'dev1.csv'), 'r') as f:
        lines2 = f.read().split('\n')[:-1]
    ids = lines2[0]
    lines2 = lines2[1:]
    with open(os.path.join(save_folder, 'dev.csv'), 'w') as f:
        f.write(ids+'\n')
        for l in lines[:num_dev]+lines2:
            f.write(l+'\n')
    with open(os.path.join(save_folder, 'test1.csv'), 'r') as f:
        lines1 = f.read().split('\n')[:-1]
    ids = lines2[0]
    lines1 = lines1[1:]
    with open(os.path.join(save_folder, 'test2.csv'), 'r') as f:
        lines2 = f.read().split('\n')[:-1]
    lines2 = lines2[1:]
    with open(os.path.join(save_folder, 'test.csv'), 'w') as f:
        f.write(ids+'\n')
        for l in lines1+lines2:
            f.write(l+'\n')
    # Merging csv file if needed
    # if merge_lst and merge_name is not None:
    #     merge_files = [split_libri + ".csv" for split_libri in merge_lst]
    #     merge_csvs(
    #         data_folder=save_folder, csv_lst=merge_files, merged_csv=merge_name,
    #     )

    # Create lexicon.csv and oov.csv
    if create_lexicon:
        create_lexicon_and_oov_csv(all_texts, data_folder, save_folder)

    # saving options
    save_pkl(conf, save_opt)

def create_csv(
    save_folder, wav_lst, text_dict, split, select_n_sentences,
):
    """
    Create the dataset csv file given a list of wav files.

    Arguments
    ---------
    save_folder : str
        Location of the folder for storing the csv.
    wav_lst : list
        The list of wav files of a given data split.
    text_dict : list
        The dictionary containing the text of each sentence.
    split : str
        The name of the current data split.
    select_n_sentences : int, optional
        The number of sentences to select.

    Returns
    -------
    None
    """
    # Setting path for the csv file
    csv_file = os.path.join(save_folder, split + ".csv")

    # Preliminary prints
    msg = "Creating csv lists in  %s..." % (csv_file)
    logger.info(msg)

    csv_lines = [["ID", "duration", "wav", "spk_id", "wrd"]]

    snt_cnt = 0
    # Processing all the wav files in wav_lst
    for wav_file in wav_lst:
        snt_id = wav_file.split("/")[-1].replace(".wav", "")
        spk_id = "-".join(snt_id.split("-")[0:1])
        wrds = text_dict[snt_id]

        signal, fs = torchaudio.load(wav_file)
        signal = signal.squeeze(0)
        duration = signal.shape[0] / SAMPLERATE
        csv_line = [
            snt_id,
            str(duration),
            wav_file,
            spk_id,
            str(" ".join(wrds.split("_"))),
        ]

        #  Appending current file to the csv_lines list
        csv_lines.append(csv_line)
        snt_cnt = snt_cnt + 1

        if snt_cnt == select_n_sentences:
            break

    # Writing the csv_lines
    with open(csv_file, mode="w") as csv_f:
        csv_writer = csv.writer(
            csv_f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )

        for line in csv_lines:
            csv_writer.writerow(line)

    # Final print
    msg = "%s successfully created!" % (csv_file)
    logger.info(msg)


def skip(splits, save_folder, conf):
    """
    Detect when the librispeech data prep can be skipped.

    Arguments
    ---------
    splits : list
        A list of the splits expected in the preparation.
    save_folder : str
        The location of the seave directory
    conf : dict
        The configuration options to ensure they haven't changed.

    Returns
    -------
    bool
        if True, the preparation phase can be skipped.
        if False, it must be done.
    """

    # Checking csv files
    skip = True

    for split in splits:
        if not os.path.isfile(os.path.join(save_folder, split + ".csv")):
            skip = False

    #  Checking saved options
    save_opt = os.path.join(save_folder, OPT_FILE)
    if skip is True:
        if os.path.isfile(save_opt):
            opts_old = load_pkl(save_opt)
            if opts_old == conf:
                skip = True
            else:
                skip = False
        else:
            skip = False

    return skip


def text_to_dict(text_lst):
    """
    This converts lines of text into a dictionary-

    Arguments
    ---------
    text_lst : str
        Path to the file containing the librispeech text transcription.

    Returns
    -------
    dict
        The dictionary containing the text transcriptions for each sentence.

    """
    # Initialization of the text dictionary
    text_dict = {}
    # Reading all the transcription files is text_lst
    for file in text_lst:
        with open(file, "r") as f:
            # Reading all line of the transcription file
            for line in f:
                line_lst = line.strip().split(" ")
                text_dict[line_lst[0]] = "_".join(line_lst[1:])
    return text_dict
