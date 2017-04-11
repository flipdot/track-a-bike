#!/usr/bin/env bash
# Get date
gd() {
    date --date="${1%%.*}" +%s
}

cd dumps
# Last date via file name
ld=$(gd $(basename $(find -type f -name '*.tar.xz' | sort | tail -1)))

# Transfer
rsync -a ajvar:~/konraddump/*.tar.xz .

for f in *.tar.xz; do
    # File date
    fd=$(gd "$(basename $f)")
    [[ $((fd-ld)) -gt 0 ]] && unp "$f.tar.xz"
done
true
