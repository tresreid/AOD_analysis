import os, sys
rootprefix="root://cmseos.fnal.gov//store/user/mreid/standaloneComp/"
with open('lifetime/ctau300.txt') as f:
        rootfiles1 = f.readlines()
commands = ["xrdcp root://cmseos.fnal.gov//store/user/mreid/standaloneComp/%s root://cmseos.fnal.gov//store/user/mreid/standaloneComp/SIDM/%s"%(x.strip(),x.strip()) for x in rootfiles1]
print commands
for cmd in commands:
	os.system(cmd)
