from datetime import datetime
import sys
import ast
 
def getWord(b, k, n=4):
	return sum(list(map(lambda c: b[k+c]<<(c*8),range(n))))

def findPattern(p, t, addr, size):
	pattern = []
	for i in range(size):
		pattern += [getWord(p, addr + i*4, 4)]
	k = 0
	# not a perfect pattern search, but most likely good enough
	for i in range(0, len(t), 4):
		candidate = getWord(t, i, 4)
		if candidate == pattern[k]:
			if k+1 == size:
				return i-k*4
			else:
				k += 1
		elif candidate == pattern[0]:
			k = 1
		else:
			k = 0
	return None

def outputConstantsTxt(d):
	out="[\n"
	for k in d:
		out+="(\""+k[0]+"\", \""+str(k[1])+"\"),\n"
	out+="]\n"
	return out

if len(sys.argv)<4:
	print("use : "+sys.argv[0]+" <proto_code.bin> <target_code.bin> <code_base_addr> <proto_ropdb_file> <output.txt>")
	exit()

l = ast.literal_eval(open(sys.argv[-2],"r").read())

base = int(sys.argv[3], 0)
proto = bytearray(open(sys.argv[1], "rb").read())
target = bytearray(open(sys.argv[2], "rb").read())

out = []

for entry in l:
	if len(entry) == 3:
		# gadget search
		(name, in_addr, in_size) = entry
		print(name)
		out_addr = findPattern(proto, target, in_addr - base, in_size) + base
		out += [(name, hex(out_addr))]
	if len(entry) == 4:
		# const ptr search
		(name, in_addr, in_size, in_offset) = entry
		out_addr = findPattern(proto, target, in_addr - base, in_size)
		out_addr = getWord(target, out_addr + in_offset*4, 4)
		out += [(name, hex(out_addr))]

open(sys.argv[-1],"w").write(outputConstantsTxt(out))
