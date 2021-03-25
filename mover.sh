#!/bin/bash

declare daydir
declare DATADIR="/opt/atom_webcam/data"

for file in "$DATADIR"/*.jpg; do
	[ ! -f "$file" ] && continue
	daydir="$(date -d @$(echo $file | cut -d'.' -f2) +%d%m%y)"
	echo $DATADIR/$daydir
	mkdir -p "$DATADIR/$daydir"
	mv "$file" "$DATADIR/$daydir"
done
