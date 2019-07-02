import re

inpfilename=input("enter file name: ")
if inpfilename == "":
	inpfilename="input.gcode"					##If no name is given use this

if "." not in inpfilename:
	inpfilename = inpfilename + ".gcode"		##If no extension was given add this extension

import os.path
if not os.path.isfile(inpfilename):				##If this file does not exist
	print('No valid input file given')
	quit()
	
InFile=open(inpfilename)						##Open the file for use
OutFile=open("C_" + inpfilename,"w")			##Create output file
ReturnCoordsFlag=0								##Reset the flag that markes that we have coords to return to



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
	if re.search("^;LAYER:",line):														##This would indicate a layer change
		outfile.write("G91\n" + 		##Use relative Positioning
		"G1 F6000 E-8\n" + 				##Pull in filement
		"G1 F6000 Z1\n" + 				##Do a Z-hop
		"G90\n" + 						##Use Absolute Positioning
		"G1 F6000 X10 Y230\n" + 		##Move almost to the edge
		"G1 F300 Y235\n" + 				##Move (slowly) and push the button
		"G0 F6000\n")					##Set the feedrate back (else the code seems to go slow??) NEEDS TO BE CHECKED
		outfile.write("G91\n" + 		##Use relative Positioning
		"G1 F6000 E8\n" + 				##Z-hop back
		"G1 F6000 Z-1\n" + 				##Undo the Z hop
		"G90\n" )						##Use Absolute Positioning
		ReturnCoordsFlag=1						##Flag that we have a location to return to 
		if ReturnCoordsFlag==1: OutFile.write(coords+"\n")						##Move back to last position before this code (if there is any)
print('Done!')