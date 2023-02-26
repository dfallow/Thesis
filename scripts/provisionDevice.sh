#!/bin/sh

EKHANDLE=0x810100ee
AKHANDLE=0x810100aa


tpm2_evictcontrol -Q -c $EKHANDLE
tpm2_evictcontrol -Q -c $AKHANDLE

tpm2_flushcontext -Q -t
tpm2_flushcontext -Q -s
tpm2_flushcontext -Q -l


dir=$(mktemp -d /tmp/machine.XXXXXX)

# Generate EK and AK
tpm2_createek -c $EKHANDLE -G rsa -u $dir/ek.pub
tpm2_createak -C $EKHANDLE -c $dir/ak.ctx -G rsa -g sha256 -s rsassa -u $dir/ak.pub -f pem -n $dir/ak.name
tpm2_evictcontrol -c $dir/ak.ctx $AKHANDLE


file=$(mktemp -t deviceInfo.XXXXXX)
echo "Writing file $file"
echo "My Contents" >> $file