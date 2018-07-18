# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()
#
## load FWlite python libraries
from DataFormats.FWLite import Handle, Events

triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","","HLT")
triggerObjects, triggerObjectLabel  = Handle("std::vector<pat::TriggerObjectStandAlone>"), "slimmedPatTrigger"
triggerPrescales, triggerPrescaleLabel  = Handle("pat::PackedTriggerPrescales"), "patTrigger"
tracks,tracklabel = Handle("vector<reco::Track>"),("displacedStandAloneMuons","","RECO")
genmu,genmulabel = Handle("vector<reco::GenParticle>"),("genParticles","","HLT")
genmet,genmetlabel = Handle("vector<reco::GenMET>"),("genMetTrue","","HLT")
genjet,genjetlabel = Handle("vector<reco::GenJet>"),("ak4GenJets","","HLT")
met,metlabel = Handle("vector<reco::PFMET>"),("pfMet","","RECO")
jet,jetlabel = Handle("vector<reco::PFJet>"),("ak4PFJets","","RECO")
###############################################################################################################################
#################Choose configuration to run
###############################################################################################################################
run_masses = False
run_lifetimes12 = True
run_lifetimes1000 = False



##################################################################################################################
################SETUP FILES FOR LIFETIME COMPARISON
##################################################################################################################
# open files 
if run_lifetimes12:
	mass_split = "5p25_dMchi-0p5_mZD-15"
	rootprefix="root://cmseos.fnal.gov//store/user/mreid/standaloneComp/iDM/ctau3_12/"
	with open('filelist/ctau/ctau12_3.txt') as f:
		rootfilesx = f.readlines()
#	rootfilesx = rootfilesx[:40] + rootfilesx[246:270]+ rootfilesx[275:300] + rootfilesx[305:340] + rootfilesx[637:653]
	rootfiles = [x.strip() for x in rootfilesx if ("_AOD" in x and mass_split in x)]
	rootfiles1 = [rootprefix+"%s"%(x.strip()) for x in rootfiles if ("_ctau-1p20e-03_" in x) ]
	rootfiles2 = [rootprefix+"%s"%(x.strip()) for x in rootfiles if ("_ctau-0p01_" in x) ]
	rootfiles3 = [rootprefix+"%s"%(x.strip()) for x in rootfiles if ("_ctau-0p12_" in x) ]
	rootfiles4 = [rootprefix+"%s"%(x.strip()) for x in rootfiles if ("_ctau-1p2_" in x) ]
	rootfiles5 = [rootprefix+"%s"%(x.strip()) for x in rootfiles if ("_ctau-12p0_" in x) ]
	print rootfiles1	
	print rootfiles2
	print rootfiles3
	print rootfiles4
	print rootfiles5
	events1 = Events(rootfiles1)
	events2 = Events(rootfiles2)
	events3 = Events(rootfiles3)
	events4 = Events(rootfiles4)
	events5 = Events(rootfiles5)
if run_lifetimes1000:
	mass_split = "5p25_dMchi-0p5_mZD-15"
	rootprefix="root://cmseos.fnal.gov//store/user/mreid/standaloneComp/iDM/ctau_1000/"
	with open('filelist/ctau/ctau1000.txt') as f:
		rootfilesx = f.readlines()
	rootfilesx = rootfilesx + rootfilesx+ rootfilesx + rootfilesx + rootfilesx
	rootfiles = [x.strip() for x in rootfilesx if ("_AOD" in x and mass_split in x)]
	rootfiles1 = [rootprefix+"%s"%(x.strip()) for x in rootfiles if ("_ctau-0p1_" in x) ]
	rootfiles2 = [rootprefix+"%s"%(x.strip()) for x in rootfiles if ("_ctau-1_" in x) ]
	rootfiles3 = [rootprefix+"%s"%(x.strip()) for x in rootfiles if ("_ctau-10_" in x) ]
	rootfiles4 = [rootprefix+"%s"%(x.strip()) for x in rootfiles if ("_ctau-100_" in x) ]
	rootfiles5 = [rootprefix+"%s"%(x.strip()) for x in rootfiles if ("_ctau-1000_" in x) ]
	print rootfiles1	
	print rootfiles2
	print rootfiles3
	print rootfiles4
	print rootfiles5
	events1 = Events(rootfiles1)
	events2 = Events(rootfiles2)
	events3 = Events(rootfiles3)
	events4 = Events(rootfiles4)
	events5 = Events(rootfiles5)
	
###############################################################################################################
############3SETUP FILES FOR MASS COMPARISON
###############################################################################################################
if run_masses:
	rootprefix="root://cmseos.fnal.gov//store/user/mreid/standaloneComp/iDM/"
	
	with open('/uscms/home/mreid/gridpacks/analysis/filelist/tar_60_10_150.txt') as f:
		rootfiles2 = f.readlines()
	rootfiles2 = [rootprefix+"tar/M_60_dM_10_mZD_150/%s"%(x.strip()) for x in rootfiles2 if ("_AOD" in x)]# and "_Wchi2-100002300_" in x)]
	with open('/uscms/home/mreid/gridpacks/analysis/filelist/tar_5p25_0p5_15.txt') as f:
		rootfiles3 = f.readlines()
	rootfiles3 = [rootprefix+"tar/M_5p25_dM_0p5_mZD_15/%s"%(x.strip()) for x in rootfiles3 if ("_AOD" in x)]# and "_Wchi2-100002300_" in x)]
	with open('/uscms/home/mreid/gridpacks/analysis/filelist/tar_52p5_5_150.txt') as f:
		rootfiles4 = f.readlines()
	rootfiles4 = [rootprefix+"tar/M_52p5_dM_5_mZD_150/%s"%(x.strip()) for x in rootfiles4 if ("_AOD" in x)]# and "_Wchi2-100002300_" in x)]
	with open('/uscms/home/mreid/gridpacks/analysis/filelist/tar_6_1_15.txt') as f:
		rootfiles1 = f.readlines()
	rootfiles1 = [rootprefix+"tar/M_6_dM_1_mZD_15/%s"%(x.strip()) for x in rootfiles1 if ("_AOD" in x)]# and "_Wchi2-100002300_" in x)]
	
	with open('/uscms/home/mreid/gridpacks/analysis/filelist/M_60_dM_10_mZD_150.txt') as f:
		rootfiles5 = f.readlines()
	rootfiles2 + [rootprefix+"M_60_dM_10_mZD_150/%s"%(x.strip()) for x in rootfiles5 if ("_AOD" in x)]# and "_Wchi2-100002300_" in x)]
	with open('/uscms/home/mreid/gridpacks/analysis/filelist/M_5p25_dM_0p5_mZD_15.txt') as f:
		rootfiles6 = f.readlines()
	rootfiles3 + [rootprefix+"M_5p25_dM_0p5_mZD_15/%s"%(x.strip()) for x in rootfiles6 if ("_AOD" in x)]# and "_Wchi2-100002300_" in x)]
	with open('/uscms/home/mreid/gridpacks/analysis/filelist/M_52p5_dM_5_mZD_150.txt') as f:
		rootfiles7 = f.readlines()
	rootfiles4 + [rootprefix+"M_52p5_dM_5_mZD_150/%s"%(x.strip()) for x in rootfiles7 if ("_AOD" in x)]# and "_Wchi2-100002300_" in x)]
	with open('/uscms/home/mreid/gridpacks/analysis/filelist/M_6_dM_1_mZD_15.txt') as f:
		rootfiles8 = f.readlines()
	rootfiles1 + [rootprefix+"M_6_dM_1_mZD_15/%s"%(x.strip()) for x in rootfiles8 if ("_AOD" in x)]# and "_Wchi2-100002300_" in x)]

	print rootfiles1
	print rootfiles2
	print rootfiles3
	print rootfiles4
	events1 = Events(rootfiles1)
	events2 = Events(rootfiles2)
	events3 = Events(rootfiles3)
	events4 = Events(rootfiles4)
###################################################################################################################################################
def setrange(h1,h2,h3,h4,h5=None):
	max1 = max([h1.GetMaximum(),h2.GetMaximum(),h3.GetMaximum(),h4.GetMaximum()]) if h5 is None else max([h1.GetMaximum(),h2.GetMaximum(),h3.GetMaximum(),h4.GetMaximum(),h5.GetMaximum()])
	min1 = min([h1.GetMinimum(),h2.GetMinimum(),h3.GetMinimum(),h4.GetMinimum()]) if h5 is None else min([h1.GetMinimum(),h2.GetMinimum(),h3.GetMinimum(),h4.GetMinimum(),h5.GetMinimum()])
	h1.SetMaximum(max1*1.15)
	h1.SetMinimum(min1*0.85)
def norm(histogram):
	if histogram.Integral() != 0:
		n = 1/histogram.Integral()
		histogram.Scale(n)
	else:
		print "pass"
def drawall(hist1,hist2,hist3,hist4,hist5=None):
	c = ROOT.TCanvas("c","c",800,800)
	c.cd
	#format titles
	name = "outputlife3/all_%s.png"%(hist1.GetName())
	namepdf = "outputlife3/all_%s.pdf"%(hist1.GetName())
	xtitle = 'pt [GeV]' if ('pt' in name or 'eff' in name) else ('eta' if ('eta' in name) else ('phi' if ('phi' in name) else 'unknown'))
	xtitle = xtitle if ('vertex' not in name) else ('dxy [cm]' if 'vxy' in name else ('dz [cm]' if 'vz' in name else 'v unknown'))
	hist1.GetXaxis().SetTitle(xtitle)

	hist1.SetLineColor(2)
	hist2.SetLineColor(3)
	hist3.SetLineColor(4)
	hist4.SetLineColor(5)
	if (hist5 is not None):
		hist5.SetLineColor(6)
		#setrange(hist01,hist1,hist10,hist50,hist100,hist300)
	hist1.SetMaximum(1.0)
	hist1.SetMinimum(0.0)
	#hist1.GetYaxis().SetTitle("Efficiency")
	hist1.SetMarkerColorAlpha(2,.6)
	hist2.SetMarkerColorAlpha(3,.6)
	hist3.SetMarkerColorAlpha(4,.6)
	hist4.SetMarkerColorAlpha(5,.6)
	if hist5 is not None:
		hist5.SetMarkerColorAlpha(6,.6)
		
	hist1.SetMarkerStyle(8)
	hist2.SetMarkerStyle(8)
	hist3.SetMarkerStyle(8)
	hist4.SetMarkerStyle(8)
	if hist5 is not None:
		hist5.SetMarkerStyle(8)
	if 'eff' in name:
		print "eff: ",name 		
		hist1.GetYaxis().SetTitle("Efficiency")
		hist1.Draw('E1')
		hist2.Draw('E1 Same')
		hist3.Draw('E1 Same')
		hist4.Draw('E1 Same')
		if hist5 is not None:
			hist5.Draw('E1 Same')
	if 'eff' not in name:
		print "not eff: ", name 		
		hist1.GetYaxis().SetTitle("Counts (normalized)")	
		norm(hist1)
		norm(hist2)
		norm(hist3)
		norm(hist4)
		if hist5 is not None:
			norm(hist5)
		setrange(hist1,hist2,hist3,hist4) if hist5 is None else setrange(hist1,hist2,hist3,hist4,hist5)
		hist1.Draw('HIST')
		hist2.Draw('HIST Same')
		hist3.Draw('HIST Same')
		hist4.Draw('HIST Same')
		if hist5 is not None:
			hist5.Draw('HIST Same')
#	else:
#		norm(hist1)
#		norm(hist2)
#		norm(hist3)
#		norm(hist4)
#		if hist5 is not None:
#			norm(hist5)
#		setrange(hist01,hist1,hist10,hist100) if hist1000 is None else setrange(hist01,hist1,hist10,hist100,hist1000)#,hist300)
#		hist01.Draw('HIST')
#		hist1.Draw('HIST SAME')
#		hist10.Draw('HIST SAME')
#		hist100.Draw('HIST SAME')
#		if hist1000 is not None:
#			 hist1000.Draw('HIST SAME')

	if hist5 is not None:
		leg = ROOT.TLegend(.75,.75,.95,.95)
		leg.AddEntry(hist1,"0.1 cm","f")
		leg.AddEntry(hist2,"1 cm","f")
		leg.AddEntry(hist3,"10 cm","f")
		leg.AddEntry(hist4,"100 cm","f")
		leg.AddEntry(hist5,"1000 cm","f")
	else:
		leg = ROOT.TLegend(.75,.75,.95,.95)
		leg.AddEntry(hist1,"M=6+/-1 .5","f")
		leg.AddEntry(hist2,"M=60 +/- 5","f")
		leg.AddEntry(hist3,"M=5.25 +/- 0.25 ","f")
		leg.AddEntry(hist4,"M=52.5 +/- 2.5","f")
	leg.Draw()
	c.Update()
	c.SaveAs(name)
	c.SaveAs(namepdf)
	del c
def draw(histogram):
	c = ROOT.TCanvas("c","c",800,800)
	c.cd
	name = "outputlife3/%s.png"%(histogram.GetName())
	namepdf = "outputlife3/%s.pdf"%(histogram.GetName())
	xtitle = 'pt [GeV]' if ('pt' in name or 'eff' in name) else ('eta' if ('eta' in name) else ('phi' if ('phi' in name) else 'unknown'))
	xtitle = xtitle if ('vertex' not in name) else ('dxy [cm]' if 'vxy' in name else ('dz [cm]' if 'vz' in name else 'v unknown'))
	histogram.GetXaxis().SetTitle(xtitle)
	if 'eff' in name:
		histogram.GetYaxis().SetTitle("Efficiency")
		histogram.Draw('E')
	else:
		histogram.Draw('B')
	c.SaveAs(name)
	c.SaveAs(namepdf)

def makehist(events):
	# SET UP HISTOGRAMS
	hist_pt_met = ROOT.TH1F("histptmet","gen MET pt", 100,0,200)
	hist_eta_met = ROOT.TH1F("histetamet","gen Met eta", 40,-6,6)
	hist_phi_met = ROOT.TH1F("histphimet","gen Met phi", 40,-6,6)
	hist_pt_jet = ROOT.TH1F("histptjet","gen Jet pt", 100,0,100)
	hist_eta_jet = ROOT.TH1F("histetajet","gen Jet eta", 40,-6,6)
	hist_phi_jet = ROOT.TH1F("histphijet","gen Jet phi", 40,-6,6)
	hist_pt_mu = ROOT.TH1F("histptmu","gen Mu pt", 100,0,50)
	hist_eta_mu = ROOT.TH1F("histetamu","gen Mu eta", 40,-6,6)
	hist_phi_mu = ROOT.TH1F("histphimu","gen Mu phi", 40,-6,6)
	hist_vxy_mu = ROOT.TH1F("histvertexvxymu","gen Mu vxy", 50,0,0.6)
	hist_vz_mu = ROOT.TH1F("histvertexvzmu","gen Mu vz", 50,-10,10)
	hist_trigeff_denom1 = ROOT.TH1F("histtrigeffdenom1","trigeff denominator", 50,120,200)
	hist_trigeff_num1 = ROOT.TH1F("histtrigeffnum1","trigefficiency HLT_PFMET120_PFMHT120", 50,120,200)
	hist_trigeff_denom2 = ROOT.TH1F("histtrigeffdenom2","trigeff denominator", 50,0,80)
	hist_trigeff_num2 = ROOT.TH1F("histtrigeffnum2","trigefficiency HLT_DoubleMu3_DCA_PFMET50_PFMHT60", 50,0,80)
	hist_trigeff_denom3 = ROOT.TH1F("histtrigeffdenom3","trigeff denominator", 50,0,80)
	hist_trigeff_num3 = ROOT.TH1F("histtrigeffnum3","trigefficiency HLT_DoubleMu3_DZ_PFMET50_PFMHT60", 50,0,80)
	hist_recoeff_denom_mu = ROOT.TH1F("histrecoeffdenommu","recoeff mu denominator", 50,0,50)
	hist_recoeff_num_mu = ROOT.TH1F("histrecoeffnummu","recoefficiency mu", 50,0,50)
	hist_recoeff_denom_met = ROOT.TH1F("histrecoeffdenommet","recoeff met denominator", 50,0,200)
	hist_recoeff_num_met = ROOT.TH1F("histrecoeffnummet","recoefficiency met", 50,0,200)
	hist_pt_met.Sumw2()
	hist_eta_met.Sumw2()
	hist_phi_met.Sumw2()
	hist_pt_jet.Sumw2()
	hist_eta_jet.Sumw2()
	hist_phi_jet.Sumw2()
	hist_pt_mu.Sumw2()
	hist_eta_mu.Sumw2()
	hist_phi_mu.Sumw2()
	hist_vxy_mu.Sumw2()
	hist_vz_mu.Sumw2()
	hist_trigeff_denom1.Sumw2()
	hist_trigeff_num1.Sumw2()
	hist_trigeff_denom2.Sumw2()
	hist_trigeff_num2.Sumw2()
	hist_trigeff_denom3.Sumw2()
	hist_trigeff_num3.Sumw2()
	hist_recoeff_denom_mu.Sumw2()
	hist_recoeff_num_mu.Sumw2()
	hist_recoeff_denom_met.Sumw2()
	hist_recoeff_num_met.Sumw2()
	
	#Run over events
	for iev,event in enumerate(events):
		if (iev %100 ==0):
			print "Event %d: run %6d, lumi %4d, event %12d" % (iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
		# setup trigger and reconstruction counters and bools
		denominator_trig1 = False # 
		numerator_trig1 = False # 
		denominator_trig2 = False # 
		numerator_trig2 = False # 
		denominator_trig3 = False # 
		numerator_trig3 = False # 
		trig2_ht = False
		trig2_met = False
		trig2_mu = False
		num_count_reco_mu=0
		num_count_reco_met=0
		trig2_mucount = 0	
		denom_count_trig_mu = 0
		denom_count_reco_mu =0
		denom_count_trig_met = 0
		denom_count_reco_met =0
		denominator_reco_mu = False # 
		numerator_reco_mu = False #  
		denominator_reco_met = False #
		numerator_reco_met = False #
		#get all objects for this event 
	    	event.getByLabel(triggerBitLabel,triggerBits)
		event.getByLabel(triggerObjectLabel,triggerObjects)
		event.getByLabel(triggerPrescaleLabel,triggerPrescales)
		event.getByLabel(tracklabel,tracks)
		event.getByLabel(genmulabel,genmu)
		event.getByLabel(genmetlabel,genmet)
		event.getByLabel(genjetlabel,genjet)
		event.getByLabel(metlabel,met)
		event.getByLabel(jetlabel,jet)
		# pick out list of generated muons (also makes a list containing the met and jet information)
		genmutracks = [x for x in genmu.product() if abs(x.pdgId())==13]
		genmettracks = [x for x in genmet.product()]
		genjettracks = [x for x in genjet.product()]
		mettracks = [x for x in met.product()]
		jettracks = [x for x in jet.product()]
		ht = 0.0

		#fill histograms for generated muon, jet and met information. Check denom for trigger and reco efficiency for met and mu
		for gmutrack in genmutracks:
	#		print "gtrack: ", gtrack.pt(), gtrack.eta()
			if abs(gmutrack.eta())<2.5 and gmutrack.pt()>3.0:
				denom_count_reco_mu +=1
			hist_pt_mu.Fill(gmutrack.pt())
			hist_eta_mu.Fill(gmutrack.eta())
			hist_phi_mu.Fill(gmutrack.phi())
			hist_vxy_mu.Fill(float(gmutrack.vx()**2 + gmutrack.vy()**2)**(0.5))
			hist_vz_mu.Fill(gmutrack.vz())
		for gjtrack in genjettracks:
	#		print "gtrack: ", gtrack.pt(), gtrack.eta()
			hist_pt_jet.Fill(gjtrack.pt())
			hist_eta_jet.Fill(gjtrack.eta())
			hist_phi_jet.Fill(gjtrack.phi())
		for gmtrack in genmettracks:
	#		print "gtrack: ", gtrack.pt(), gtrack.eta()
			hist_pt_met.Fill(gmtrack.pt())
			hist_eta_met.Fill(gmtrack.eta())
			hist_phi_met.Fill(gmtrack.phi())

			if gmtrack.pt()>20.0:
				denom_count_reco_met +=1
		#run over jet information to add up ht information
		for jtrack in jettracks:
			#print jtrack.pt()
			if jtrack.pt() > 20.0 and (jtrack.eta() < 5.2):
				ht += jtrack.pt()
		if ht >60 :
			trig2_ht = True
		#run over met information 
		for mtrack in mettracks:
			if mtrack.pt()> 50:
				trig2_met = True
			if abs(mtrack.eta())<2.4:
				if mtrack.pt() > 120.0 and ht > 120:
					denominator_trig1 = True
			#match met information to generated met information
			for cur,gmettrack in enumerate(genmettracks):
				if (gmettrack.pt() > 20) and (abs( ((gmettrack.eta()**2+gmettrack.phi()**2)**(0.5)) - ((mtrack.eta()**2 + mtrack.phi()**2)**(0.5))) <= 0.5) and ((abs(gmettrack.pt()-mtrack.pt())/gmettrack.pt()) <= 1.0):
					num_count_reco_met +=1
					del genmettracks[cur]
					break
			
		if denom_count_reco_mu >=2:
			denominator_reco_mu = True
		if denom_count_reco_met >=1:
			denominator_reco_met = True
			
		for track in tracks.product():
			if track.eta()<2.5 and track.pt()>3.0:
				trig2_mucount +=1
			
				#match reco mu to gen muons (maxdeltaR = .5 maxdeltapt/pt = 1.0)
				for cur,gtrack in enumerate(genmutracks):
					if (abs( ((gtrack.eta()**2+gtrack.phi()**2)**(0.5)) - ((track.eta()**2 + track.phi()**2)**(0.5))) <= 0.5) and ((abs(gtrack.pt()-track.pt())/gtrack.pt()) <= 1.0):
						num_count_reco_mu +=1
						del genmutracks[cur]
						break
			
		if denominator_reco_mu and num_count_reco_mu >= 2:
			numerator_reco_mu = True
		if denominator_reco_met and num_count_reco_met >= 1:
			numerator_reco_met = True
		if trig2_mucount >= 2:
			trig2_mu = True
		if trig2_mu and trig2_ht and trig2_met:
			denominator_trig2 = True
			denominator_trig3 = True
	


	# trigger efficiency
	#	print "\n === TRIGGER PATHS ==="
	    	names = event.object().triggerNames(triggerBits.product())
	    	for i in xrange(triggerBits.product().size()):
			if "HLT_PFMET120_PFMHT120_IDTight_v16" in names.triggerName(i):
	        		#print "Trigger ", names.triggerName(i), ": ", ("PASS" if triggerBits.product().accept(i) else "fail (or not run)")
	        		#if triggerBits.product().accept(i):
		#			print "Trigger ", names.triggerName(i), ": ", ("PASS" if denominator_trig1 else "fail (denom)")
				if triggerBits.product().accept(i) and denominator_trig1:
					numerator_trig1 = True
			#	elif denominator_trig1:
		#			print "bad hit 1"
			if "HLT_DoubleMu3_DCA_PFMET50_PFMHT60_v6" in names.triggerName(i):
	        		#print "Trigger ", names.triggerName(i), ": ", ("PASS" if triggerBits.product().accept(i) else "fail (or not run)")
	        	#	if triggerBits.product().accept(i):
		#			print "Trigger ", names.triggerName(i), ": ", ("PASS" if denominator_trig2 else "fail (denom) %s %s %s"%(ht,trig2_met,trig2_mucount))
				if triggerBits.product().accept(i) and denominator_trig2:
					numerator_trig2 = True
			#	elif denominator_trig2:
		#			print "bad hit 2"
			if "HLT_DoubleMu3_DZ_PFMET50_PFMHT60_v6" in names.triggerName(i):
	        		#print "Trigger ", names.triggerName(i), ": ", ("PASS" if triggerBits.product().accept(i) else "fail (or not run)")
	        	#	if triggerBits.product().accept(i):
		#			print "Trigger ", names.triggerName(i), ": ", ("PASS" if denominator_trig2 else "fail (denom) %s %s %s"%(ht,trig2_met,trig2_mucount))
				if triggerBits.product().accept(i) and denominator_trig3:
					numerator_trig3 = True
			#	elif denominator_trig3:
		#			print "bad hit 3"
		#Fill efficiency plots
		for track in mettracks:
			#fill trigger eff plots
			if denominator_trig1:
				hist_trigeff_denom1.Fill(track.pt())
			if numerator_trig1:
				hist_trigeff_num1.Fill(track.pt())
			if denominator_reco_met:
				hist_recoeff_denom_met.Fill(track.pt())
			if numerator_reco_met:
				hist_recoeff_num_met.Fill(track.pt())
		for track in tracks.product():
			if denominator_trig3:
				hist_trigeff_denom3.Fill(track.pt())
			if numerator_trig3:
				hist_trigeff_num3.Fill(track.pt())
			if denominator_trig2:
				hist_trigeff_denom2.Fill(track.pt())
			if numerator_trig2:
				hist_trigeff_num2.Fill(track.pt())
			#fill reco eff plots
			if denominator_reco_mu:
				hist_recoeff_denom_mu.Fill(track.pt())
			if numerator_reco_mu:
				hist_recoeff_num_mu.Fill(track.pt())

	hist_trigeff1 = hist_trigeff_num1.Clone("trigefficiency1")
	hist_trigeff1.Sumw2()
	hist_trigeff1.Divide(hist_trigeff_denom1)
	hist_trigeff2 = hist_trigeff_num2.Clone("trigefficiency2")
	hist_trigeff2.Sumw2()
	hist_trigeff2.Divide(hist_trigeff_denom2)
	hist_trigeff3 = hist_trigeff_num3.Clone("trigefficiency3")
	hist_trigeff3.Sumw2()
	hist_trigeff3.Divide(hist_trigeff_denom3)
	hist_recoeff_mu = hist_recoeff_num_mu.Clone("recoefficiencymu")
	hist_recoeff_mu.Sumw2()
	hist_recoeff_mu.Divide(hist_recoeff_denom_mu)
	hist_recoeff_met = hist_recoeff_num_met.Clone("recoefficiencymet")
	hist_recoeff_met.Sumw2()
	hist_recoeff_met.Divide(hist_recoeff_denom_met)
	ROOT.gStyle.SetOptStat(0)
	return (hist_pt_met,hist_eta_met,hist_phi_met,hist_pt_jet,hist_eta_jet,hist_phi_jet,hist_pt_mu,hist_eta_mu,hist_phi_mu,hist_vxy_mu,hist_vz_mu,hist_trigeff1,hist_trigeff2,hist_trigeff3,hist_recoeff_mu,hist_recoeff_met)

(hist_pt_met1,hist_eta_met1,hist_phi_met1,hist_pt_jet1,hist_eta_jet1,hist_phi_jet1,hist_pt_mu1,hist_eta_mu1,hist_phi_mu1,hist_vxy_mu1,hist_vz_mu1,hist_trigeffmet1,hist_trigeffdca1,hist_trigeffdz1,hist_recoeff_mu1,hist_recoeff_met1) = makehist(events1)
(hist_pt_met2,hist_eta_met2,hist_phi_met2,hist_pt_jet2,hist_eta_jet2,hist_phi_jet2,hist_pt_mu2,hist_eta_mu2,hist_phi_mu2,hist_vxy_mu2,hist_vz_mu2,hist_trigeffmet2,hist_trigeffdca2,hist_trigeffdz2,hist_recoeff_mu2,hist_recoeff_met2) = makehist(events2)
(hist_pt_met3,hist_eta_met3,hist_phi_met3,hist_pt_jet3,hist_eta_jet3,hist_phi_jet3,hist_pt_mu3,hist_eta_mu3,hist_phi_mu3,hist_vxy_mu3,hist_vz_mu3,hist_trigeffmet3,hist_trigeffdca3,hist_trigeffdz3,hist_recoeff_mu3,hist_recoeff_met3) = makehist(events3)
(hist_pt_met4,hist_eta_met4,hist_phi_met4,hist_pt_jet4,hist_eta_jet4,hist_phi_jet4,hist_pt_mu4,hist_eta_mu4,hist_phi_mu4,hist_vxy_mu4,hist_vz_mu4,hist_trigeffmet4,hist_trigeffdca4,hist_trigeffdz4,hist_recoeff_mu4,hist_recoeff_met4) = makehist(events4)

if run_lifetimes12 or run_lifetimes1000:
	(hist_pt_met5,hist_eta_met5,hist_phi_met5,hist_pt_jet5,hist_eta_jet5,hist_phi_jet5,hist_pt_mu5,hist_eta_mu5,hist_phi_mu5,hist_vxy_mu5,hist_vz_mu5,hist_trigeffmet5,hist_trigeffdca5,hist_trigeffdz5,hist_recoeff_mu5,hist_recoeff_met5) = makehist(events5)

	drawall(hist_pt_met1,hist_pt_met2,hist_pt_met3,hist_pt_met4,hist_pt_met5)
	drawall(hist_eta_met1,hist_eta_met2,hist_eta_met3,hist_eta_met4,hist_eta_met5)
	drawall(hist_phi_met1,hist_phi_met2,hist_phi_met3,hist_phi_met4,hist_phi_met5)
	drawall(hist_pt_jet1,hist_pt_jet2,hist_pt_jet3,hist_pt_jet4,hist_pt_jet5)
	drawall(hist_eta_jet1,hist_eta_jet2,hist_eta_jet3,hist_eta_jet4,hist_eta_jet5)
	drawall(hist_phi_jet1,hist_phi_jet2,hist_phi_jet3,hist_phi_jet4,hist_phi_jet5)
	drawall(hist_pt_mu1,hist_pt_mu2,hist_pt_mu3,hist_pt_mu4,hist_pt_mu5)
	drawall(hist_eta_mu1,hist_eta_mu2,hist_eta_mu3,hist_eta_mu4,hist_eta_mu5)
	drawall(hist_phi_mu1,hist_phi_mu2,hist_phi_mu3,hist_phi_mu4,hist_phi_mu5)
	drawall(hist_vxy_mu1,hist_vxy_mu2,hist_vxy_mu3,hist_vxy_mu4,hist_vxy_mu5)
	drawall(hist_vz_mu1,hist_vz_mu2,hist_vz_mu3,hist_vz_mu4,hist_vz_mu5)
	drawall(hist_trigeffmet1,hist_trigeffmet2,hist_trigeffmet3,hist_trigeffmet4,hist_trigeffmet5)
	drawall(hist_trigeffdca1,hist_trigeffdca2,hist_trigeffdca3,hist_trigeffdca4,hist_trigeffdca5)
	drawall(hist_trigeffdz1,hist_trigeffdz2,hist_trigeffdz3,hist_trigeffdz4,hist_trigeffdz5)
	drawall(hist_recoeff_mu1,hist_recoeff_mu2,hist_recoeff_mu3,hist_recoeff_mu4,hist_recoeff_mu5)
	drawall(hist_recoeff_met1,hist_recoeff_met2,hist_recoeff_met3,hist_recoeff_met4,hist_recoeff_met5)

else:
	drawall(hist_pt_met1,hist_pt_met2,hist_pt_met3,hist_pt_met4,None)
	drawall(hist_eta_met1,hist_eta_met2,hist_eta_met3,hist_eta_met4,None)
	drawall(hist_phi_met1,hist_phi_met2,hist_phi_met3,hist_phi_met4,None)
	drawall(hist_pt_jet1,hist_pt_jet2,hist_pt_jet3,hist_pt_jet4,None)
	drawall(hist_eta_jet1,hist_eta_jet2,hist_eta_jet3,hist_eta_jet4,None)
	drawall(hist_phi_jet1,hist_phi_jet2,hist_phi_jet3,hist_phi_jet4,None)
	drawall(hist_pt_mu1,hist_pt_mu2,hist_pt_mu3,hist_pt_mu4,None)
	drawall(hist_eta_mu1,hist_eta_mu2,hist_eta_mu3,hist_eta_mu4,None)
	drawall(hist_phi_mu1,hist_phi_mu2,hist_phi_mu3,hist_phi_mu4,None)
	drawall(hist_vxy_mu1,hist_vxy_mu2,hist_vxy_mu3,hist_vxy_mu4,None)
	drawall(hist_vz_mu1,hist_vz_mu2,hist_vz_mu3,hist_vz_mu4,None)
	drawall(hist_trigeffmet1,hist_trigeffmet2,hist_trigeffmet3,hist_trigeffmet4,None)
	drawall(hist_trigeffdca1,hist_trigeffdca2,hist_trigeffdca3,hist_trigeffdca4,None)
	drawall(hist_trigeffdz1,hist_trigeffdz2,hist_trigeffdz3,hist_trigeffdz4,None)
	drawall(hist_recoeff_mu1,hist_recoeff_mu2,hist_recoeff_mu3,hist_recoeff_mu4,None)
	drawall(hist_recoeff_met1,hist_recoeff_met2,hist_recoeff_met3,hist_recoeff_met4,None)
