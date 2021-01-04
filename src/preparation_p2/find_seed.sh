#!/bin/bash


for SEED in {0..100}; do
    if ./src/preparation_p2/prepare_annotators.py --seed $SEED --no-save 2>1 1> /dev/null; then
        ONES=$(./src/preparation_p2/prepare_annotators.py --seed $SEED --no-save | tr -cd '1' | wc -c)
        if [[ $ONES -ge 236 ]]; then
            echo -e "$SEED\t$ONES"
        fi
    fi
done