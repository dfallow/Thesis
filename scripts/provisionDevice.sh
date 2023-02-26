#!/bin/sh

EKHANDLE=0x810100ee
AKHANDLE=0x810100aa


#tpm2_evictcontrol -Q -c $EKHANDLE
#tpm2_evictcontrol -Q -c $AKHANDLE

#tpm2_flushcontext -Q -t
#tpm2_flushcontext -Q -s
#tpm2_flushcontext -Q -l


file=$(mktemp -t deviceInfo.XXXXXX)
echo "Writing file $file"
echo "My Contents" >> $file