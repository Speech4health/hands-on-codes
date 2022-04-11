#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

./asr.sh \
    --lang en \
    --token_type "char" \
    --train_set train1 \
    --valid_set "dev1 dev2" \
    --test_sets "test1 test2" \
