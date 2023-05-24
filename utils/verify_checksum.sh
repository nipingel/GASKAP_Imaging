#!/bin/bash
if [ ! -f "$1.checksum" ]; then
  echo "No checksum file for $1"
  exit 1
fi
if [ -z $(diff <(cat "$1.checksum") <(./calc_checksum.sh "$1")) ]; then
  echo "Matches"
  exit 0
else
  echo "Differs"
  exit 1
fi
