#!/usr/bin/env bash

# author: Sathvik Udupa
# affiation: SPIRE Lab, Indian Institute of Science (2022)
# contact: sathvikudupa66@gmail.com

data_loc=$1
ndev_utt=200
echo "Data path:"$data_loc

#define datasets
D_train="F02 F03 F04 F05 M01 M04 M05 M07 M08 M09 M10 M11 M12 M14 M16"   #dysarthric train
C_train="CF02 CF03 CF04 CF05 CM01 CM04 CM05 CM06 CM08 CM09 CM10 CM12 CM13"  #control train

#rename audio files with metadata and create wav.scp, text and utt2spk files
rm -r data/{dev1,dev2}
mkdir -p data/{train1,train2,test1,test2,dev1,dev2}
echo "Renaming and creating required files.."
python3 local/data_prep.py $data_loc data/train1 data/train2 data/test1 data/test2 $D_train $C_train

#remove very short utterences
# lines=$(awk -F" " '{print $2}' "data/test1/wav.scp")
# for line in $lines; do
#   dur=$(soxi -D $line)
#   if (( $(echo "$dur < 0.1" | bc -l) )); then
#     linename=$(basename "$line" | cut -d. -f1)
#     sed -i "/$linename/d" data/test1/wav.scp
#     sed -i "/$linename/d" data/test1/utt2spk
#     sed -i "/$linename/d" data/test1/text
#
# fi
# done



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

cat data/train1/text data/train2/text > data/text
sort data/text | uniq -u > data/temp
cp data/temp  data/text

#create validation sets
utils/subset_data_dir.sh --first data/train1 ${ndev_utt} data/dev1
n=$(($(wc -l < data/train1/text) - ndev_utt))
utils/subset_data_dir.sh --last data/train1 "${n}" "data/train1_"
mv data/train1_/* data/train1
rm -r data/train1_
sed -i 's/train1/dev1/' data/dev1/wav.scp

utils/subset_data_dir.sh --first data/train2 ${ndev_utt} data/dev2
n=$(($(wc -l < data/train2/text) - ndev_utt))
utils/subset_data_dir.sh --last data/train2 "${n}" "data/train2_"
mv data/train2_/* data/train2
rm -r data/train2_
sed -i 's/train2/dev2/' data/dev2/wav.scp
