#!/bin/bash

md5=$(md5sum "$1" | cut -d ' ' -f 1)
echo $md5
