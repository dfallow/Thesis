#!/bin/sh

EKHANDLE=0x810100ee
AKHANDLE=0x810100aa

echo "Removing existing keys"
tpm2_evictcontrol -Q -c $EKHANDLE
tpm2_evictcontrol -Q -c $AKHANDLE

echo "Removing temporary objects"
tpm2_flushcontext -Q -t
tpm2_flushcontext -Q -s
tpm2_flushcontext -Q -l


echo "Creating directory where files will be stored"
dir=$(mktemp -d /tmp/machine.XXXXXX)

# Generate EK and AK
echo "Creating EK and AK"
tpm2_createek -c $EKHANDLE -G rsa -u $dir/ek.pub
tpm2_createak -C $EKHANDLE -c $dir/ak.ctx -G rsa -g sha256 -s rsassa -u $dir/ak.pub -f pem -n $dir/ak.name
tpm2_evictcontrol -c $dir/ak.ctx $AKHANDLE

echo "Creating PEM and data files"
tpm2_readpublic -Q -c $EKHANDLE -o $dir/ek.pem -f pem
tpm2_readpublic -Q -c $AKHANDLE -o $dir/ak.pem -f pem

echo "Removing temporary objects"
tpm2_flushcontext -Q -t
tpm2_flushcontext -Q -s
tpm2_flushcontext -Q -l

echo "Persistent handles: "
tpm2_getcap handles-persistent

echo "Files that have been created: "
ls -l $dir