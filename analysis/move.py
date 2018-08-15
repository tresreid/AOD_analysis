import os, sys
#rootprefix="root://cmseos.fnal.gov//store/user/mreid/standaloneComp/test"
with open('filelist/move.txt') as f:
        rootfiles1 = f.readlines()

commands10000 = ["xrdcp root://cmseos.fnal.gov//store/user/mreid/standaloneComp/iDM/redone/%s root://cmseos.fnal.gov//store/user/mreid/iDM/lifetime_10000mm/%s"%(x.strip(),x.strip()) for x in rootfiles1 if ("ctau-10000_" in x and "_AOD" in x)]
commands1000 = ["xrdcp root://cmseos.fnal.gov//store/user/mreid/standaloneComp/iDM/redone/%s root://cmseos.fnal.gov//store/user/mreid/iDM/lifetime_1000mm/%s"%(x.strip(),x.strip()) for x in rootfiles1 if ("ctau-1000_" in x and "_AOD" in x)]
commands100 = ["xrdcp root://cmseos.fnal.gov//store/user/mreid/standaloneComp/iDM/redone/%s root://cmseos.fnal.gov//store/user/mreid/iDM/lifetime_100mm/%s"%(x.strip(),x.strip()) for x in rootfiles1 if ("ctau-100_" in x and "_AOD" in x)]
commands10 = ["xrdcp root://cmseos.fnal.gov//store/user/mreid/standaloneComp/iDM/redone/%s root://cmseos.fnal.gov//store/user/mreid/iDM/lifetime_10mm/%s"%(x.strip(),x.strip()) for x in rootfiles1 if ("ctau-10_" in x and "_AOD" in x)]
commands1 = ["xrdcp root://cmseos.fnal.gov//store/user/mreid/standaloneComp/iDM/redone/%s root://cmseos.fnal.gov//store/user/mreid/iDM/lifetime_1mm/%s"%(x.strip(),x.strip()) for x in rootfiles1 if ("ctau-1_" in x and "_AOD" in x)]
commands = commands1+commands10+commands100+commands1000+commands10000
print commands
for cmd in commands:
	os.system(cmd)
