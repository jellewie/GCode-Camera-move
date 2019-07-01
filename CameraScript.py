import re

inpfilename=input("enter file name: ")
if inpfilename == "":inpfilename="input.gcode"			##If no name is given use this

if "." not in inpfilename:
	inpfilename = inpfilename + ".gcode"				##If no extension was given add this extension

##IndentationError: expected an indented block

try: file=open(inpfilename)
except: quit()

outfile=open("C_" + inpfilename,"w")					##Create output file

attention=0

while True:
	line=file.readline()
	outfile.write(line)
	line=line.rstrip()
	if line==";End of Gcode": break						##Stop if we find this line
	content=line.split()
	try: tester=content[0]
	except: continue
	if content[0]=="G0":
		coords=line
		attention=1
	if re.search("^;LAYER:",line):														##This would indicate a layer change
		outfile.write("G91\n" + 		##Use relative Positioning
		"G1 F6000 E-8\n" + 				##Pull in filement
		"G1 F6000 Z1\n" + 				##Do a Z-hop
		"G90\n" + 						##Use Absolute Positioning
		"G1 F6000 X10 Y233\n" + 		##Move almost to the edge
		"G1 Y235 F50\n" + 				##Move (slowly) and push the button
		"G0 F6000\n")					##Set the feedrate back (else the code seems to go slow??) NEEDS TO BE CHECKED
		if attention==1: outfile.write(coords+"\n")										##Move back to last position before this code (if there is any)
		outfile.write("G91\n" + 		##Use relative Positioning
		"G1 F6000 E8\n" + 				##Z-hop back
		"G1 F6000 Z-1\n" + 				##Undo the Z hop
		"G90\n" )						##Use Absolute Positioning
print('Done!')