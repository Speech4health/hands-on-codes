#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail


asr_config=conf/train_asr_transformer.yaml

./asr.sh \
    --lang en \
    --token_type "char"\
    --train_set "train1" \
    --asr_config "${asr_config}" \
    --valid_set "dev1" \
    --test_sets "test1" \
    --asr_tag "default"
#    --speed_perturb_factors "0.9 1.0 1.1"\
#    --nbpe "38"
