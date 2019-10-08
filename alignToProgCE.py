#!/usr/bin/python

# Authors: Manuel + Vincent
# Project: Genome Harvest

# This script generates an XML input file for the ProgCE network inference program
# This program needs as input a set of sequences from individuals (e.g. varieties in the context of the GH project)
# that are assigned to species (here subspecies in the GH project).
# The inference program can accept a network to start from (given in a file)
#

import numpy as np
import sys
import os
import re
from sys import exit as sys_exit
if len(sys.argv) !=6 :
	print("""Thanks for giving following parameters (in order):
			1 - The varieties x SNPs matrix, 
			2 - The file indicating to which network leaf is assigned each variety
			3 - The XML template file (containing header and footer of ProgCE's input file)
			4 - The file containing the network/tree in Newick format
			5 - The name of the output file for this script""")
	sys.exit(1)
fichSNP=open(sys.argv[1], "r")
liste2=open(sys.argv[2], "r")
newick=open(sys.argv[4], "r")
Matrice=[]
Relation=[]
for j in fichSNP:
	Matrice.append(j.split())
for l in liste2:
	Relation.append(l.split())


# Reads only the first network/tree in the Newick file
nwkString = newick.readline().rstrip()
#Newck=[]
#for n in newick:
#	Newck.append(n.split())
#Nwk=np.asarray(Newck)


Mat=np.asarray(Matrice)
Rel=np.asarray(Relation)
#print (Matrice)
#print (Relation)

Listefinale=[]
for i in range(len(Matrice)):
	for k in range(len(Relation)):
		if Mat[i][0]==Rel[k][0]:  # variety name
			Listefinale.append(Mat[i][0])  # variety name
			Listefinale.append(Rel[k][1])  # name of corresponding species
			Listefinale.append(Mat[i][1])  # corresponding sequence of SNPs 

# Builds the list of subspecies
ListeSousEspeces = {} # empty dictionary
for k in range(len(Relation)):
	ListeSousEspeces[Relation[k][1]] = " " # says which subspecies is present
ListeRelation = ListeSousEspeces.keys()

#print(ListeRelation[0])
#print(Relation[2][1])
#print(ListeRelation)

xml= open(sys.argv[3],"r")
lignesXML = xml.readlines()


fXMLresultat = open(sys.argv[5], "w")
# Copies the header of the XML template file
# until we meet "</rawdata>"
l = 0
while (re.search("^\s*</rawdata>",lignesXML[l]) is None):
	fXMLresultat.write(lignesXML[l])
	l += 1

# Write the SNP matrix part
for k in range(len(Matrice)):
	fXMLresultat.write('\t\t<sequence id="')
	fXMLresultat.write(Listefinale[3*k])
	fXMLresultat.write('" taxon="')
	fXMLresultat.write(Listefinale[3*k+1])
	fXMLresultat.write('_')
	fXMLresultat.write(Listefinale[3*k])
	fXMLresultat.write('" totalcount="2"> ')
	fXMLresultat.write(Listefinale[3*k+2])
	fXMLresultat.write(' </sequence>')
	fXMLresultat.write('\n')

# Write the line containing </rawdata>
fXMLresultat.write(lignesXML[l])
l += 1

# Write which subspecies contains which variety
for k in ListeRelation:
	fXMLresultat.write('<taxonset id="'+k)
	fXMLresultat.write('" spec="TaxonSet">')
	fXMLresultat.write('\n')
	for j in range(len(Relation)):
		if k==Relation[j][1]:
			fXMLresultat.write('\t<taxon id="'+k)
			fXMLresultat.write('_'+Relation[j][0]) 
			fXMLresultat.write('" spec="Taxon"/>') 
			fXMLresultat.write('\n')	
	fXMLresultat.write('</taxonset>')
	fXMLresultat.write('\n')

# Write lines until we find that contenaing the markup attribute of the network
while (re.search("newick=",lignesXML[l]) is None):
	fXMLresultat.write(lignesXML[l])
	l += 1

# extract the beginning and end of the liune (anything except the network itself)
res = re.search(r'^(.*newick=").*(".*)$',lignesXML[l])
if res is None or len(res.group())<3:
	print("Impossible to find the newick form in the XML header_footer file")
	#print len(res.group())
	sys.exit()
debLigneReseau =  res.group(1)
finLigneReseau =  res.group(2)
# rewrites the line with the new network instead
ligneReseau = debLigneReseau + nwkString + finLigneReseau 
fXMLresultat.write(ligneReseau)

# Write remaining lines of the XML template file
l += 1 # skips the line we just replaced

baseName = os.path.splitext(os.path.basename(sys.argv[5]))[0] #os.path.splitext(sys.argv[5])[0]
#print("basename is ",baseName)

for ftL in range(l,len(lignesXML)):
	# Change the name of log files
	res=re.search(r'^(.*fileName=").*trees(".*)$',lignesXML[ftL])
	if (res is not None):
		#print(lignesXML[ftL])
		fXMLresultat.write(res.group(1)+baseName+".nex"+res.group(2))
	else:
		res=re.search(r'^(.*fileName=").*(log".*)$',lignesXML[ftL])
		if res is not None:
			#print(res.group(1))
			#print(res.group(2))
			#print(lignesXML[ftL])
			fXMLresultat.write(res.group(1)+baseName+"."+res.group(2))
			#sys.exit()
		else:
			fXMLresultat.write(lignesXML[ftL])

fXMLresultat.close()
