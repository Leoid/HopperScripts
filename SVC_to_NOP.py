doc = Document.getCurrentDocument()
# alertbox: doc.message("title",["OK"])

seg = doc.getCurrentSegment()
adr = doc.getCurrentAddress()
instr = seg.getInstructionAtAddress(adr)

start, end = doc.getSelectionAddressRange()
instr_len = instr.getInstructionLength()
b = seg.readByte(adr)    
#if seg.readByte(adr) == 128 and seg.readByte(adr + 1) == 21:

def svcCall_old(seg, adr):
    #(0x80 == 128) (0xDF == 223)
    seg = doc.getCurrentSegment()
    b = seg.readByte(adr)    
    if seg.readByte(adr) == 1 and seg.readByte(adr + 1) == 16 and seg.readByte(adr + 2) == 0 and seg.readByte(adr + 3) == 212:
		return True
    return False

def svcCall(seg, adr):
    #(0x80 == 128) (0xDF == 223)
    seg = doc.getCurrentSegment()
    b = seg.readByte(adr)
    if seg.readByte(adr) == 48 and seg.readByte(adr + 1) == 4 and seg.readByte(adr + 2) == 128 and seg.readByte(adr + 3) == 210:
		return True
    return False

def to_nop(adr):
	print("[+] Patching: "+str(hex(adr)))
	seg.writeByte(adr+0, 0x1F)
	seg.writeByte(adr+1, 0x20)
	seg.writeByte(adr+2, 0x03)
	seg.writeByte(adr+3, 0xD5)
	seg.markAsCode(adr)

def to_null(adr):
	print("[+] Patching: "+str(hex(adr)))
	seg.writeByte(adr+0, 0x10)
	seg.writeByte(adr+1, 0x0)
	seg.writeByte(adr+2, 0x80)
	seg.writeByte(adr+3, 0xd2)
	seg.markAsCode(adr)


print("[+] Start Patching..!")
counter = 0
for seg_id in range(0, doc.getSegmentCount()):
    seg = doc.getSegment(seg_id)

    seg_start = seg.getStartingAddress()
    seg_stop = seg_start + seg.getLength()

    adr = seg_start
    
    while adr + 1 <= seg_stop:
        if svcCall_old(seg, adr):
            #print("[+] found at: ", hex(adr))
            to_nop(adr)
            counter += 1
        adr += 1

print("[+] Total Patched Count: "+str(counter))

print("[+] End of Patching..!")
