#ls -v /pnfs/psi.ch/cms/trivcat/store/user/nchernya/VBFZll/workflow/v25b/SingleElectron  > el_done.txt

import string

input = open("done.txt","rt")
output = open("missing_1.txt","wt")
lines = input.readlines()
max_num = 96
for i in range(0,max_num+1) :
	found = 0
	num = str(i)
	search_line = "TTbar_nanoAOD_RegressionPerJet_nanoAOD_2017JECv32_"+ num +".root\n"
	if search_line not in lines:
		output.write('%i\n'%i)

