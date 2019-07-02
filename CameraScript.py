Feedrate = 6000		##mm/min speed 
FeedrateSlow = 300	##mm/min speed to move slowly
PosX = 10			##X pos to go to when pausing
PosY = 235			##Y pos to go to when pausing
Zhop = 1			##Amount to Zhop 
Retract = 8			##Distance to retract
PosSlowY = 5 		##Amount to slowly move of the PosY to pres the button
EndCharacter = ";End of Gcode" ##This marks the end of the file, WARNING if non found, the program would freeze! 
LayerChar = "^;LAYER:"	##This would indicate a layer

##Do not change things below this line unles you know what you are doing.

inpfilename=input("enter file name: ")
if inpfilename == "":
	inpfilename="input.gcode"					##If no name is given use this
if "." not in inpfilename:
	inpfilename = inpfilename + ".gcode"		##If no extension was given add this extension
import os.path
if not os.path.isfile(inpfilename):				##If this file does not exist
	print('"' + str(inpfilename) + '" is not a valid input file')
	quit()
InFile=open(inpfilename)						##Open the file for use
OutFile=open("C_" + inpfilename,"w")			##Create output file
ReturnCoordsFlag=0								##Reset the flag that markes that we have coords to return to
import re
while True:
	line=InFile.readline()						##Read a line from the input file
	OutFile.write(line)							##Write the line to the output file
	line=line.rstrip()							##remove any trailing characters (DO WE NEED THIS?)
	if line==EndCharacter: break				##Stop if we find this line
	content=line.split()						##Split the line at each space, stored in the array
	try: tester=content[0]						##If this is a emthy line
	except: continue							##Just ignore it and continue
	if content[0]=="G0":						##If this line starts with a G0 command
		coords=line								##Save the coords in case we need it later
		ReturnCoordsFlag=1						##Flag that we have a location to return to 
	if re.search(LayerChar,line):				##This would indicate a layer change
		OutFile.write("G91\n" + 												##Use relative Positioning
		"G1 F" + str(Feedrate) + " E-" + str(Retract) + "\n"					##Pull in filement
		"G1 F" + str(Feedrate) + " Z" + str(Zhop) + "\n" + 						##Do a Z-hop
		"G90\n" + 																##Use Absolute Positioning
		"G1 F" + str(Feedrate) + " X" + str(PosX) + " Y" + str(PosY-PosSlowY) + "\n" + 	##Move almost to the edge
		"G1 F" + str(FeedrateSlow) + " Y" + str(PosY) + "\n" + 					##Move (slowly) and push the button
		"G0 F" + str(Feedrate) + "\n")											##Set the feedrate back (else the code seems to go slow??) NEEDS TO BE CHECKED
		if ReturnCoordsFlag==1: OutFile.write(coords+"\n")						##Move back to last position before this code (if there is any)
		OutFile.write("G91\n" + 												##Use relative Positioning
		"G1 F" + str(Feedrate) + " E" + str(Retract) + "\n" 					##Z-hop back
		"G1 F" + str(Feedrate) + " Z-" + str(Zhop) + "\n" + 					##Undo the Z hop
		"G90\n" )																##Use Absolute Positioning
print('Done!')