
from struct import *
import pdb


a = ""
count = 0
while len(a) < 204800:
    a+=str(count)
    count+=1

packet = pack('!c204800s','t',a)

type,padding = unpack('!c204800s',packet)
print type,padding[:10]
