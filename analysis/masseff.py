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
# open file (you can use 'edmFileUtil -d /store/whatever.root' to get the physical file name)

#rootprefix="root://cmseos.fnal.gov//store/user/mreid/standaloneComp/iDM/tar/M_6_dM_1_mZD_15/"
#with open('filelist/M_6_dM_1_mZD_15.txt') as f:
#with open('filelist/tar_6_1_15.txt') as f:
#	rootfiles = f.readlines()
#rootfiles1 = [rootprefix+"%s"%(x.strip()) for x in rootfiles if ("_AOD" in x and "_Wchi2-10000p23_" in x) ]
#rootfiles2 = [rootprefix+"%s"%(x.strip()) for x in rootfiles if ("_AOD" in x and "_Wchi2-100002p3_" in x) ]
#rootfiles3 = [rootprefix+"%s"%(x.strip()) for x in rootfiles if ("_AOD" in x and "_Wchi2-1000023_" in x) ]
#rootfiles4 = [rootprefix+"%s"%(x.strip()) for x in rootfiles if ("_AOD" in x and "_Wchi2-10000230_" in x) ]
#rootfiles5 = [rootprefix+"%s"%(x.strip()) for x in rootfiles if ("_AOD" in x and "_Wchi2-100002300_" in x) ]

rootprefix="root://cmseos.fnal.gov//store/user/mreid/standaloneComp/iDM/"

with open('filelist/tar_60_10_150.txt') as f:
	rootfiles2 = f.readlines()
rootfiles2 = [rootprefix+"tar/M_60_dM_10_mZD_150/%s"%(x.strip()) for x in rootfiles2 if ("_AOD" in x)]# and "_Wchi2-100002300_" in x)]
with open('filelist/tar_5p25_0p5_15.txt') as f:
	rootfiles3 = f.readlines()
rootfiles3 = [rootprefix+"tar/M_5p25_dM_0p5_mZD_15/%s"%(x.strip()) for x in rootfiles3 if ("_AOD" in x)]# and "_Wchi2-100002300_" in x)]
with open('filelist/tar_52p5_5_150.txt') as f:
	rootfiles4 = f.readlines()
rootfiles4 = [rootprefix+"tar/M_52p5_dM_5_mZD_150/%s"%(x.strip()) for x in rootfiles4 if ("_AOD" in x)]# and "_Wchi2-100002300_" in x)]
with open('filelist/tar_6_1_15.txt') as f:
	rootfiles1 = f.readlines()
rootfiles1 = [rootprefix+"tar/M_6_dM_1_mZD_15/%s"%(x.strip()) for x in rootfiles1 if ("_AOD" in x)]# and "_Wchi2-100002300_" in x)]

with open('filelist/M_60_dM_10_mZD_150.txt') as f:
	rootfiles5 = f.readlines()
rootfiles2 + [rootprefix+"M_60_dM_10_mZD_150/%s"%(x.strip()) for x in rootfiles5 if ("_AOD" in x)]# and "_Wchi2-100002300_" in x)]
with open('filelist/M_5p25_dM_0p5_mZD_15.txt') as f:
	rootfiles6 = f.readlines()
rootfiles3 + [rootprefix+"M_5p25_dM_0p5_mZD_15/%s"%(x.strip()) for x in rootfiles6 if ("_AOD" in x)]# and "_Wchi2-100002300_" in x)]
with open('filelist/M_52p5_dM_5_mZD_150.txt') as f:
	rootfiles7 = f.readlines()
rootfiles4 + [rootprefix+"M_52p5_dM_5_mZD_150/%s"%(x.strip()) for x in rootfiles7 if ("_AOD" in x)]# and "_Wchi2-100002300_" in x)]
with open('filelist/M_6_dM_1_mZD_15.txt') as f:
	rootfiles8 = f.readlines()
rootfiles1 + [rootprefix+"M_6_dM_1_mZD_15/%s"%(x.strip()) for x in rootfiles8 if ("_AOD" in x)]# and "_Wchi2-100002300_" in x)]
#with open('lifetime/ctau300.txt') as f:
#	rootfiles6 = f.readlines()
#rootfiles6 = [rootprefix+"%s"%(x.strip()) for x in rootfiles6 if "_AOD" in x]
print rootfiles1
print rootfiles2
print rootfiles3
print rootfiles4
#print rootfiles5
#print rootfiles6

events1 = Events(rootfiles1)
events2 = Events(rootfiles2)
events3 = Events(rootfiles3)
events4 = Events(rootfiles4)
#events5 = Events(rootfiles5)
#events6 = Events(rootfiles2)
def setrange(h1,h2,h3,h4,h5=None):#,h6):
	max1 = max([h1.GetMaximum(),h2.GetMaximum(),h3.GetMaximum(),h4.GetMaximum()]) if h5 is None else max([h1.GetMaximum(),h2.GetMaximum(),h3.GetMaximum(),h4.GetMaximum(),h5.GetMaximum()])#,h6.GetMaximum()])
	#min1 = min([h1.GetMinimum(),h2.GetMinimum(),h3.GetMinimum(),h4.GetMinimum(),h5.GetMinimum()])#,h6.GetMinimum()])
	min1 = min([h1.GetMinimum(),h2.GetMinimum(),h3.GetMinimum(),h4.GetMinimum()]) if h5 is None else min([h1.GetMinimum(),h2.GetMinimum(),h3.GetMinimum(),h4.GetMinimum(),h5.GetMinimum()])#,h6.GetMinimum()])
	h1.SetMaximum(max1*1.15)
	h1.SetMinimum(min1*0.85)
def norm(histogram):
	if histogram.Integral() != 0:
		n = 1/histogram.Integral()
		histogram.Scale(n)
	else:
		print "pass"
def drawall(hist01,hist1,hist10,hist100,hist1000=None):#,hist300):
	c = ROOT.TCanvas("c","c",800,800)
	c.cd
	#format titles
	name = "output/all_%s.pdf"%(hist01.GetName())
	xtitle = 'pt [GeV]' if ('pt' in name or 'eff' in name) else ('eta' if ('eta' in name) else ('phi' if ('phi' in name) else 'unknown'))
	xtitle = xtitle if ('vertex' not in name) else ('dxy [cm]' if 'vxy' in name else ('dz [cm]' if 'vz' in name else 'v unknown'))
	hist01.GetXaxis().SetTitle(xtitle)

	hist01.SetLineColor(2)
	hist1.SetLineColor(3)
	hist10.SetLineColor(4)
	hist100.SetLineColor(5)
	if (hist1000 is not None):
		hist1000.SetLineColor(6)
	#hist300.SetLineColor(7)

	if 'eff' in name:
		#setrange(hist01,hist1,hist10,hist50,hist100,hist300)
		hist01.SetMaximum(1.0)
		hist01.SetMinimum(0.0)
		hist01.GetYaxis().SetTitle("Efficiency")
		#hist01.SetMarkerColor(2)
		#hist1.SetMarkerColor(3)
		#hist10.SetMarkerColor(4)
		#hist50.SetMarkerColor(5)
		#hist100.SetMarkerColor(6)
		#hist300.SetMarkerColor(7)
		hist01.SetMarkerColorAlpha(2,.6)
		hist1.SetMarkerColorAlpha(3,.6)
		hist10.SetMarkerColorAlpha(4,.6)
		hist100.SetMarkerColorAlpha(5,.6)
		if hist1000 is not None:
			hist1000.SetMarkerColorAlpha(6,.6)
		#hist300.SetMarkerColorAlpha(7,.6)
		
		hist01.SetMarkerStyle(8)
		hist1.SetMarkerStyle(8)
		hist10.SetMarkerStyle(8)
		hist100.SetMarkerStyle(8)
		if hist1000 is not None:
			hist1000.SetMarkerStyle(8)
		#hist300.SetMarkerStyle(8)
		
		hist01.Draw('B')
		hist1.Draw('Same')
		hist10.Draw('Same')
		hist100.Draw('Same')
		if hist1000 is not None:
			hist1000.Draw('Same')
		#hist300.Draw('Same')
		
	else:
		norm(hist01)
		norm(hist1)
		norm(hist10)
		norm(hist100)
		if hist1000 is not None:
			norm(hist1000)
		#norm(hist300)
		setrange(hist01,hist1,hist10,hist100) if hist1000 is None else setrange(hist01,hist1,hist10,hist100,hist1000)#,hist300)
		#hist01.SetMaximum(maxy)
		#hist01.SetMinimum(miny)
		hist01.Draw('HIST')
		hist1.Draw('HIST SAME')
		hist10.Draw('HIST SAME')
		hist100.Draw('HIST SAME')
		if hist1000 is not None:
			 hist1000.Draw('HIST SAME')
		#hist300.Draw('HIST SAME')

	if hist1000 is not None:
		leg = ROOT.TLegend(.75,.75,.95,.95)
		leg.AddEntry(hist01,"0.1 cm","f")
		leg.AddEntry(hist1,"1 cm","f")
		leg.AddEntry(hist10,"10 cm","f")
		leg.AddEntry(hist100,"100 cm","f")
		leg.AddEntry(hist1000,"1000 cm","f")
	else:
		leg = ROOT.TLegend(.75,.75,.95,.95)
		leg.AddEntry(hist01,"M=6+/-1 .5","f")
		leg.AddEntry(hist1,"M=60 +/- 5","f")
		leg.AddEntry(hist10,"M=5.25 +/- 0.25 ","f")
		leg.AddEntry(hist100,"M=52.5 +/- 2.5","f")
	#leg.AddEntry(hist300,"300 cm","f")
	leg.Draw()
	#ROOT.gStyle.SetOptStat(0)
	c.Update()
	c.SaveAs(name)

def draw(histogram):
	c = ROOT.TCanvas("c","c",800,800)
	c.cd
	name = "output/%s.pdf"%(histogram.GetName())
	xtitle = 'pt [GeV]' if ('pt' in name or 'eff' in name) else ('eta' if ('eta' in name) else ('phi' if ('phi' in name) else 'unknown'))
	xtitle = xtitle if ('vertex' not in name) else ('dxy [cm]' if 'vxy' in name else ('dz [cm]' if 'vz' in name else 'v unknown'))
	histogram.GetXaxis().SetTitle(xtitle)
	if 'eff' in name:
		histogram.GetYaxis().SetTitle("Efficiency")
		histogram.Draw('E')
	else:
		histogram.Draw('B')
	c.SaveAs(name)

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
	hist_trigeff_denom1 = ROOT.TH1F("histtrigeffdenom1","trigeff denominator", 50,0,80)
	hist_trigeff_num1 = ROOT.TH1F("histtrigeffnum1","trigefficiency HLT_PFMET120_PFMHT120", 50,0,80)
	hist_trigeff_denom2 = ROOT.TH1F("histtrigeffdenom2","trigeff denominator", 50,0,200)
	hist_trigeff_num2 = ROOT.TH1F("histtrigeffnum2","trigefficiency HLT_DoubleMu3_DCA_PFMET50_PFMHT60", 50,0,200)
	hist_trigeff_denom3 = ROOT.TH1F("histtrigeffdenom3","trigeff denominator", 50,0,200)
	hist_trigeff_num3 = ROOT.TH1F("histtrigeffnum3","trigefficiency HLT_DoubleMu3_DZ_PFMET50_PFMHT60", 50,0,200)
	hist_recoeff_denom = ROOT.TH1F("histrecoeffdenom","recoeff denominator", 50,0,120)
	hist_recoeff_num = ROOT.TH1F("histrecoeffnum","recoefficiency", 50,0,120)
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
#	hist_recoeff_denom.Sumw2()
#	hist_recoeff_num.Sumw2()
	
	#Run over events
	for iev,event in enumerate(events):
		denominator_trig1 = False # 
		numerator_trig1 = False # 
		denominator_trig2 = False # 
		numerator_trig2 = False # 
		denominator_trig3 = False # 
		numerator_trig3 = False # 
		trig2_ht = False
		trig2_met = False
		trig2_mu = False
	#	denominator_reco = False # 4 gen muons with |eta| <2.4
	#	numerator_reco = False # 4 muons matched with gen muons (maxdeltaR = 0.5, maxdeltaPt/Pt =1.0)

	    	event.getByLabel(triggerBitLabel,triggerBits)
		event.getByLabel(triggerObjectLabel,triggerObjects)
		event.getByLabel(triggerPrescaleLabel,triggerPrescales)
		if (iev %100 ==0):
			print "Event %d: run %6d, lumi %4d, event %12d" % (iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
	    	
		denom_count_trig = 0
		denom_count_reco =0
		event.getByLabel(tracklabel,tracks)
		event.getByLabel(genmulabel,genmu)
		event.getByLabel(genmetlabel,genmet)
		event.getByLabel(genjetlabel,genjet)
		event.getByLabel(metlabel,met)
		event.getByLabel(jetlabel,jet)
		# pick out list of generated muons
		genmutracks = [x for x in genmu.product() if abs(x.pdgId())==13]
		genmettracks = [x for x in genmet.product()]
		genjettracks = [x for x in genjet.product()]
		mettracks = [x for x in met.product()]
		jettracks = [x for x in jet.product()]
		ht = 0.0
#		mht = 0.0

		for jtrack in jettracks:
			#print jtrack.pt()
			if jtrack.pt() > 20.0 and (jtrack.eta() < 5.2):
				ht += jtrack.pt()
	#	print "ht: ",ht
		if ht >60 :
			trig2_ht = True
		for mtrack in mettracks:
	#		print "met track pt, sumEt: ", mtrack.pt(), mtrack.sumEt()
			if mtrack.pt()> 50:
				trig2_met = True
			if abs(mtrack.eta())<2.4:
				if mtrack.pt() > 120.0 and ht > 120:
	#				print "demon pass", mtrack.pt(), ht
					denominator_trig1 = True
		#fill histograms for generated muon information. Check denom for trigger and reco efficiency
		for gmutrack in genmutracks:
	#		print "gtrack: ", gtrack.pt(), gtrack.eta()
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
			#hist_vxy_jet.Fill(float(gjtrack.vx()**2 + gjtrack.vy()**2)**(0.5))
			#hist_vz_jet.Fill(gjtrack.vz())
		for gmtrack in genmettracks:
	#		print "gtrack: ", gtrack.pt(), gtrack.eta()
			hist_pt_met.Fill(gmtrack.pt())
			hist_eta_met.Fill(gmtrack.eta())
			hist_phi_met.Fill(gmtrack.phi())

	#		if abs(gtrack.eta())<2.4:
	#			denom_count_reco +=1
	#			if gtrack.pt() >16.0:# and abs(gtrack.eta())<2.4:
	#				denominator_trig = True
	#			if gtrack.pt() >6.0:# and abs(gtrack.eta())<2.4:
	#				denom_count_trig +=1
			
#		if not (denominator_trig and (denom_count_trig > 3)):
#			denominator_trig =False
#		if denom_count_reco >=4:
#			denominator_reco = True
			
		#Reco Efficiency
		num_count_reco=0
		trig2_mucount = 0	
		for track in tracks.product():
			if track.eta()<2.5 and track.pt()>3.0:
				trig2_mucount +=1
			
	#		print "track: ", track.pt()
			#match reco mu to gen muons (maxdeltaR = .5 maxdeltapt/pt = 1.0)
	#		for cur,gtrack in enumerate(genmettracks):
	#			if (abs( ((gtrack.eta()**2+gtrack.phi()**2)**(0.5)) - ((track.eta()**2 + track.phi()**2)**(0.5))) <= 0.5) and ((abs(gtrack.pt()-track.pt())/gtrack.pt()) <= 1.0):
	#				num_count_reco +=1
	#				print " matched pt: %s vs %s" %(track.pt(),gtrack.pt())
	#				del genmettracks[cur]
	#				break
			
	#	if denominator_reco and num_count_reco >= 4:
	#		numerator_reco = True
		if trig2_mucount >= 2:
			trig2_mu = True
		if trig2_mu and trig2_ht and trig2_met:
			denominator_trig2 = True
			denominator_trig3 = True
	#	print "reco denominator: ", denominator_reco
	#	print "reco numerator: ",numerator_reco
	


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
			if denominator_trig3:
				hist_trigeff_denom3.Fill(track.pt())
			if numerator_trig3:
				hist_trigeff_num3.Fill(track.pt())
			if denominator_trig2:
				hist_trigeff_denom2.Fill(track.pt())
			if numerator_trig2:
				hist_trigeff_num2.Fill(track.pt())
		for track in tracks.product():
			if denominator_trig1:
				hist_trigeff_denom1.Fill(track.pt())
			if numerator_trig1:
				hist_trigeff_num1.Fill(track.pt())
			#fill reco eff plots
	#		if denominator_reco:
	#			hist_recoeff_denom.Fill(track.pt())
	#		if numerator_reco:
	#			hist_recoeff_num.Fill(track.pt())

	hist_trigeff1 = hist_trigeff_num1.Clone("trigefficiency1")
	hist_trigeff1.Sumw2()
	hist_trigeff1.Divide(hist_trigeff_denom1)
	hist_trigeff2 = hist_trigeff_num2.Clone("trigefficiency2")
	hist_trigeff2.Sumw2()
	hist_trigeff2.Divide(hist_trigeff_denom2)
	hist_trigeff3 = hist_trigeff_num3.Clone("trigefficiency3")
	hist_trigeff3.Sumw2()
	hist_trigeff3.Divide(hist_trigeff_denom3)
	hist_recoeff = hist_recoeff_num.Clone("recoefficiency")
	hist_recoeff.Sumw2()
	#hist_recoeff.Divide(hist_recoeff_denom)
	ROOT.gStyle.SetOptStat(0)
	return (hist_pt_met,hist_eta_met,hist_phi_met,hist_pt_jet,hist_eta_jet,hist_phi_jet,hist_pt_mu,hist_eta_mu,hist_phi_mu,hist_vxy_mu,hist_vz_mu,hist_trigeff1,hist_trigeff2,hist_trigeff3,hist_recoeff)

(hist_pt_met1,hist_eta_met1,hist_phi_met1,hist_pt_jet1,hist_eta_jet1,hist_phi_jet1,hist_pt_mu1,hist_eta_mu1,hist_phi_mu1,hist_vxy_mu1,hist_vz_mu1,hist_trigeffmet1,hist_trigeffdca1,hist_trigeffdz1,hist_recoeff1) = makehist(events1)
(hist_pt_met2,hist_eta_met2,hist_phi_met2,hist_pt_jet2,hist_eta_jet2,hist_phi_jet2,hist_pt_mu2,hist_eta_mu2,hist_phi_mu2,hist_vxy_mu2,hist_vz_mu2,hist_trigeffmet2,hist_trigeffdca2,hist_trigeffdz2,hist_recoeff2) = makehist(events2)
(hist_pt_met3,hist_eta_met3,hist_phi_met3,hist_pt_jet3,hist_eta_jet3,hist_phi_jet3,hist_pt_mu3,hist_eta_mu3,hist_phi_mu3,hist_vxy_mu3,hist_vz_mu3,hist_trigeffmet3,hist_trigeffdca3,hist_trigeffdz3,hist_recoeff3) = makehist(events3)
(hist_pt_met4,hist_eta_met4,hist_phi_met4,hist_pt_jet4,hist_eta_jet4,hist_phi_jet4,hist_pt_mu4,hist_eta_mu4,hist_phi_mu4,hist_vxy_mu4,hist_vz_mu4,hist_trigeffmet4,hist_trigeffdca4,hist_trigeffdz4,hist_recoeff4) = makehist(events4)
#(hist_pt5,hist_eta5,hist_phi5,hist_vxy5,hist_vz5,hist_trigeff5,hist_recoeff5) = makehist(events5)
#(hist_pt6,hist_eta6,hist_phi6,hist_vxy6,hist_vz6,hist_trigeff6,hist_recoeff6) = makehist(events6)


#draw(hist_pt1)
#draw(hist_pt5)
#draw(hist_eta1)
#draw(hist_phi1)
#draw(hist_vxy1)
#draw(hist_vz1)
##draw(hist_eff_num)
##draw(hist_eff_denom)
#draw(hist_trigeff1)
#draw(hist_recoeff1)
#drawall(hist_pt1,hist_pt2,hist_pt3,hist_pt4,hist_pt5)#,hist_pt6)
#drawall(hist_eta1,hist_eta2,hist_eta3,hist_eta4,hist_eta5)#,hist_eta6)
#drawall(hist_phi1,hist_phi2,hist_phi3,hist_phi4,hist_phi5)#,hist_phi6)
#drawall(hist_vxy1,hist_vxy2,hist_vxy3,hist_vxy4,hist_vxy5)#,hist_vxy6)
#drawall(hist_vz1,hist_vz2,hist_vz3,hist_vz4,hist_vz5)#,hist_vz6)
#drawall(hist_trigeff1,hist_trigeff2,hist_trigeff3,hist_trigeff4,hist_trigeff5)#,hist_trigeff6)
#drawall(hist_recoeff1,hist_recoeff2,hist_recoeff3,hist_recoeff4,hist_recoeff5)#,hist_recoeff6)
drawall(hist_pt_met1,hist_pt_met2,hist_pt_met3,hist_pt_met4,None)#,hist_pt6)
drawall(hist_eta_met1,hist_eta_met2,hist_eta_met3,hist_eta_met4,None)#,hist_eta6)
drawall(hist_phi_met1,hist_phi_met2,hist_phi_met3,hist_phi_met4,None)#,hist_phi6)
drawall(hist_pt_jet1,hist_pt_jet2,hist_pt_jet3,hist_pt_jet4,None)#,hist_pt6)
drawall(hist_eta_jet1,hist_eta_jet2,hist_eta_jet3,hist_eta_jet4,None)#,hist_eta6)
drawall(hist_phi_jet1,hist_phi_jet2,hist_phi_jet3,hist_phi_jet4,None)#,hist_phi6)
drawall(hist_pt_mu1,hist_pt_mu2,hist_pt_mu3,hist_pt_mu4,None)#,hist_pt6)
drawall(hist_eta_mu1,hist_eta_mu2,hist_eta_mu3,hist_eta_mu4,None)#,hist_eta6)
drawall(hist_phi_mu1,hist_phi_mu2,hist_phi_mu3,hist_phi_mu4,None)#,hist_phi6)
drawall(hist_vxy_mu1,hist_vxy_mu2,hist_vxy_mu3,hist_vxy_mu4,None)#,hist_vxy6)
drawall(hist_vz_mu1,hist_vz_mu2,hist_vz_mu3,hist_vz_mu4,None)#,hist_vz6)
drawall(hist_trigeffmet1,hist_trigeffmet2,hist_trigeffmet3,hist_trigeffmet4,None)#,hist_trigeff6)
drawall(hist_trigeffdca1,hist_trigeffdca2,hist_trigeffdca3,hist_trigeffdca4,None)#,hist_trigeff6)
drawall(hist_trigeffdz1,hist_trigeffdz2,hist_trigeffdz3,hist_trigeffdz4,None)#,hist_trigeff6)
drawall(hist_recoeff1,hist_recoeff2,hist_recoeff3,hist_recoeff4,None)#,hist_recoeff6)
