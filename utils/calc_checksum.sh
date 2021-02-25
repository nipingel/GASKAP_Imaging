#!/usr/bin/python

import sys
import binascii
import hashlib

crc = None
sha1 = hashlib.sha1()
fsize = 0x00000000

chunksize = 65536

with open(sys.argv[1], "rb") as fin:
  while True:
    chunk = fin.read(chunksize)
    if chunk:
      if crc is None:
        crc = binascii.crc32(chunk)
      else:
        crc = binascii.crc32(chunk, crc)
      sha1.update(chunk);
      fsize += len(chunk);
    else:
      break

if crc is None:
  crc = 0

fin.close()

if crc < 0:
  crc = crc + (1 << 32)

sys.stdout.write(format(crc, '08x') + " " + sha1.hexdigest() + " " + format(fsize, 'x'))

