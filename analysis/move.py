import os, sys
rootprefix="root://cmseos.fnal.gov//store/user/mreid/standaloneComp/"
with open('filelist/M_60_dM_10_mZD_150.txt') as f:
        rootfiles1 = f.readlines()
commands = ["xrdcp root://cmseos.fnal.gov//store/user/mreid/standaloneComp/%s root://cmseos.fnal.gov//store/user/mreid/standaloneComp/iDM/M_60_dM_10_mZD_150/%s"%(x.strip(),x.strip()) for x in rootfiles1]
print commands
for cmd in commands:
	os.system(cmd)
