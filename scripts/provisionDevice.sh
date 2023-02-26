#!/bin/sh

EKHANDLE=0x810100ee
AKHANDLE=0x810100aa


tpm2_evictcontrol -Q -c $EKHANDLE
tpm2_evictcontrol -Q -c $AKHANDLE

tpm2_flushcontext -Q -t
tpm2_flushcontext -Q -s
tpm2_flushcontext -Q -l

# Generate EK and AK
tpm2_createek -c $EKHANDLE -G rsa -u /tmp/ek.pub
tpm2_createak -C $EKHANDLE -c /tmp/ak.ctx -G rsa -g sha256 -s rsassa -u /tmp/ak.pub -f pem -n /tmp/ak.name
tpm2_evictcontrol -c /tmp/ak.ctx $AKHANDLE


file=$(mktemp -t deviceInfo.XXXXXX)
echo "Writing file $file"
echo "My Contents" >> $file