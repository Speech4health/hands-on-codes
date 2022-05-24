#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

for folder in exp/* ; do
  if [ -f "$folder/RESULTS.md" ]; then
    echo $folder
    grep -iA 8 CER "$folder/RESULTS.md" | grep -B 4 TER | tail -n4 | head -n2 | awk '{split($0,a,"|"); print substr(a[2],length(a[2])-4) , a[9]}'
    echo '~~~'
fi
done
