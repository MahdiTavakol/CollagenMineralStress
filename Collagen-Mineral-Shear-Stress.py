#!/usr/bin/env python
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from math import sqrt
from math import pi
import csv
import os

Sims = ["1-Series1","2-Series2","3-Series3","4-Series4","5-Series5"]
volPerBead = 0

TimeStep  = []
CStress   = []
MStress   = []

for sim in Sims:
	tsVector             = []
	CollagenStressVector = []
	MineralStressVector  = []
	CollagenBeads        = 0
	MineralBeads         = 0
	#dumpPath = os.path.join(path,sim)
	dumpPath = os.path.join(sim,"dump/dump.defo.lammpstrj")
	with open(dumpPath, 'r') as dumpFile :
		dump = dumpFile.readlines()
	tsFound = False
	numAtoms = 0
	xmin = xmax = ymin = ymax = zmin = zmax = 0.0
	for i in range(len(dump)):
		line = dump[i]
		if "ITEM: TIMESTEP" in line:
			ts = int(dump[i+1])
			i = i + 1
			print "Reading timestep: ", ts
			tsFound = True
			if (ts != 0):
				volPerAtom = float(pi*100*100*(zmax-zmin)/float(numAtoms))
				collVol  = volPerAtom*collagenBeads
				minerVol = volPerAtom*mineralBeads
				collagenStress = collagenStress/collVol
				mineralStress  = mineralStress/minerVol
				tsVector.append(ts)
				CollagenStressVector.append(collagenStress/10000)
				MineralStressVector.append(mineralStress/10000)
			volPerAtom = 0.0
			collagenStress = 0.0
			mineralStress  = 0.0
			collagenBeads  = 0
			mineralBeads   = 0 
		elif "ITEM: NUMBER OF ATOMS" in line:
			numAtoms = int(dump[i+1])
			i = i + 1
		elif "ITEM: BOX BOUNDS" in line:
			line = dump[i+1].split()
			i = i + 1
			xmin = float(line[0])
			xmax = float(line[1])
			line = dump[i+1].split()
			i = i + 1
			ymin = float(line[0])
			ymax = float(line[1])
			line = dump[i+1].split()
			i = i + 1
			zmin = float(line[0])
			zmax = float(line[1])
		elif "ITEM: ATOMS" in line:
			if tsFound == False :
				i = i + numAtoms
			else :
				for j in range(numAtoms):
					#print j
					i = i + 1
					line  = dump[i].split()
					pType  = int(line[2])
					strs  = abs(float(line[7]))
					if (pType == 1):
						collagenStress += strs
						collagenBeads  += 1
					if (pType == 2):
						mineralStress  += strs
						mineralBeads   += 1

	TimeStep.append(tsVector)
	CStress.append(CollagenStressVector)
	MStress.append(MineralStressVector)
  

lens = []
for i in range(len(TimeStep)):
	lens.append(TimeStep[i])
for i in range(len(TimeStep)):
	if (len(TimeStep[i]) > max(lens)):
		for j in range(len(TimeStep[i]),max(lens)):
			CStress[i].append(0.0)
			MStress[i].append(0.0)


timestep = TimeStep[TimeStep.index(max(lens))]


with open('Collagen-Mineral-Shear-Stress.csv', 'w') as csvfilew:
	plotsw = csv.writer(csvfilew,delimiter=',')
	plotsw.writerow(["Timestep","c-1","c-2","c-3","c-4","m-1","m-2","m-3","m-4"])
	plotsw.writerows(zip(timestep,CStress[0],CStress[1],CStress[2],CStress[3],MStress[0],MStress[1],MStress[2],MStress[3]))


