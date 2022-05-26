#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

./asr.sh \
    --lang en \
    --stage 11 \
    --stop_stage 13 \
    --token_type "bpe" \
    --nbpe "38" \
    --train_set train1 \
    --valid_set "dev1" \
    --test_sets "test1 test2" \
    --asr_config "conf/train_asr.yaml" \
    --ast_tag "transfer_from_ftshijt_espnet2_asr_dsing_transformer" \
    --pretrained_model "ftshijt_espnet2_asr_dsing_transformer.pth" \
    --ignore_init_mismatch "true" \
    --use_lm "false" \
    --inference_asr_model "valid.acc.ave_10best.pth"
