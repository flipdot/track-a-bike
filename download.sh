#!/usr/bin/env bash
cd dumps
rsync ajvar:~/konraddump/*.tar.xz .
# TODO: unp only new tars
unp *.tar.xz