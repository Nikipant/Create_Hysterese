# Create_Hysterese
Python Program to turn OOMMF .odt file into csv and png

This program turns complex formatted .odt files created by OOMMF into easy readable .csv files
and creates their hysterese loop in a .png format. It is reliable on the OOMMF format from 01.2022.
If something changes concerning the column names, this program might not be working correctly anymore.
In this case contact niklas.pantschitz@gmx.de for further help.

Reliable on: Python3, pandas, matplotlib, tkinter

#USER MANUAL - CREATE HYSTERESE

## Important:
- Name of the files
- if the simultations have been done at a specific angle, this must be stated in the filename.
Format: "..._angle_Grad.odt" or "..._angle_deg.odt". Otherwise the program can't handle the 
data accordingly.
- Columns
--The columns can't be identified just by the file and must be given specifically in the code.
This means if in future versions of OOMMF the column names might defer so the program needs
an adjustment.
- Files must have an individual name.
-- If a filename already consists in the saving folder it is not overwritten.

## Example Usecase:
1. Open Program
2. Press Load Button and select wanted files. (Files must be selected all at once)
3. Press "To png" or "To csv" to command actions.
4. Repeat step 2-3 if wanted.

## Open OOMMF .odt data in Excel
1.  Load .odt files into program 
2.  Create .csv files by pressing Button "To csv" and choosing folder
3.  In Excel:
	- go to "Data"
	- click "From Text/CSV" in left top corner
	- chose csv file 
	- confirm by pressing load
