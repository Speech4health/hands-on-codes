#!/usr/bin/env bash

# author: Sathvik Udupa
# affiation: SPIRE Lab, Indian Institute of Science (2022)
# contact: sathvikudupa66@gmail.com

data_loc=$1
ndev_utt=100
echo "Data path:"$data_loc

#define datasets
D_train="F01 F03 M01 M02 M03 M04"   #dysarthric train
C_train="FC01 FC02 MC01 MC02 MC03"  #control train
D_test="F04 M05"  #dysarthric test
C_test="FC03 MC04"  #control test


#rename audio files with metadata and create wav.scp, text and utt2spk files
rm -r data/{dev1,dev2}
mkdir -p data/{train1,train2,test1,test2,dev1,dev2}
echo "Renaming and creating required files.."
python3 local/data_prep.py $data_loc data/train1 $D_train
python3 local/data_prep.py $data_loc data/train2 $C_train
python3 local/data_prep.py $data_loc data/test1 $D_test
python3 local/data_prep.py $data_loc data/test2 $C_test

#sort and remove repeating entries from created files, also create spk2utt

for dataset in data/{train1,train2,test1,test2}; do
  sort $dataset/utt2spk | uniq -u > data/temp
  cp data/temp  $dataset/utt2spk
  utils/utt2spk_to_spk2utt.pl $dataset/utt2spk > $dataset/spk2utt
  sort $dataset/text | uniq -u > data/temp
  cp data/temp  $dataset/text
  sort $dataset/wav.scp | uniq -u > data/temp
  cp data/temp  $dataset/wav.scp
  rm data/temp
done

#create validation sets
mkdir -p data/{dev1,dev2}/audio
utils/subset_data_dir.sh --first data/train1 ${ndev_utt} data/dev1
n=$(($(wc -l < data/train1/text) - ndev_utt))
utils/subset_data_dir.sh --last data/train1 "${n}" "data/train1_"
for file in $(cat data/dev1/wav.scp  | awk '{split($0, a, " "); print a[2]}'); do mv "$file" data/dev1/audio/; done
mv data/train1_/* data/train1
rm -r data/train1_
sed -i 's/train1/dev1/' data/dev1/wav.scp

utils/subset_data_dir.sh --first data/train2 ${ndev_utt} data/dev2
n=$(($(wc -l < data/train2/text) - ndev_utt))
utils/subset_data_dir.sh --last data/train2 "${n}" "data/train2_"
for file in $(cat data/dev2/wav.scp  | awk '{split($0, a, " "); print a[2]}'); do mv "$file" data/dev2/audio/; done
mv data/train2_/* data/train2
rm -r data/train2_
sed -i 's/train2/dev2/' data/dev2/wav.scp
