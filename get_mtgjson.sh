#!/bin/bash

mkdir -p cards
cd cards

filelist=(
    AllCards
    Keywords
)

for file in ${filelist[@]}; do
    if [ -f $file.json ]; then
        echo $file exists
        continue
    fi
    echo $file
    curl -LO https://www.mtgjson.com/files/$file.json.bz2
    bunzip2 $file.json.bz2
done
