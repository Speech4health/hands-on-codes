# hands-on-codes
How to use?
<br>
- install espnet with kaldi.
- clone repository and place folder inside espnet/egs2
- rename "data_path" in local/data.sh
- separate splits are created for healthy and control, specify the ones needed in run.sh

# Colab demo
- Data augmentation: https://colab.research.google.com/drive/1giatjCVXk0KpPqRr3civNUqCjKYgp6Nf?usp=sharing
- Inference colab: https://colab.research.google.com/drive/1FOJ00xYil7T1dH31K5kJv7NJbxKWmRRe?usp=sharing

# UASpeech
Expected results, without hyper parameter tuning-
 on UASpeech- 
 without LM 
 
 |trainset|control|dysarthric
 |---------|---------|---------|
 |UASpeech|92.6|98.3|
 |Transfer learning| 44.5 | 49.9 |
 
with LM

|trainset|control|dysarthric|
|---------|---------|---------|
|UASpeech| 83.4 |87.2 |
|Transfer learning| 47 | 55.7 |
