#This script is not supposed to imitate UnitTests. It's for internal usage only!
source prepare.sh

./kraken.py crackme --verbose hexdump
./kraken.py crackme --verbose edit --address 0x8049d10 --bytes 1A 23 51 --output crackme2
./kraken.py crackme --verbose disassemble
