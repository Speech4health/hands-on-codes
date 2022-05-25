#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

use_lm=true #do you want to use a language model or not
asr_config=conf/train_asr_transformer.yaml  #specify acoustic model config
lm_config=conf/train_lm_transformer.yaml #specify language model config
train_set=train1  #specify train split
dev_set=dev1 #specify dev split
token=char  #char or bpe, with bpe, vary "nbpe" param
exp_name="default_transformer_model" #specify a custom tag

./asr.sh \
    --lang en \
    --use_lm $use_lm \
    --token_type $token \
    --asr_config "${asr_config}" \
    --lm_config "${lm_config}" \
    --train_set $train_set \
    --valid_set $dev_set \
    --test_sets "test1 test2" \
    --speed_perturb_factors "0.9 1.0 1.1"\
    --asr_tag $exp_name \
