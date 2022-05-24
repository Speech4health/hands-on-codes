#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail


asr_config=conf/train_asr_transformer2.yaml

./asr.sh \
    --lang en \
    --use_lm true \
    --token_type "char" \
    --train_set "train1" \
    --asr_config "${asr_config}" \
    --pretrained_model "exp/asr_control_only_12epoch_nospecaug_uselm/valid.acc.best.pth" \
    --valid_set "dev1" \
    --test_sets "test1" \
    --lm_tag "both_set_text" \
    --lm_train_text "data/text" \
    --asr_tag "dy_ft_only_12epoch_noscheduler_nospecaug_uselm"
