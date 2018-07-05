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
tracks,tracklable = Handle("vector<reco::Track>"),("displacedStandAloneMuons","","RECO")
gen,genlable = Handle("vector<reco::GenParticle>"),("genParticles","","HLT")
# open file (you can use 'edmFileUtil -d /store/whatever.root' to get the physical file name)

rootfiles1=["root://cmseos.fnal.gov//store/user/mreid/standaloneComp/iDM_Mchi-52p5_dMchi-5p0_mZD-150_Wchi2-1000023_36370810_AOD.root"]
rootfiles2=["root://cmseos.fnal.gov//store/user/mreid/standaloneComp/iDM_Mchi-52p5_dMchi-5p0_mZD-150_Wchi2-1000023_18018284_AOD.root"]
#rootfiles3=["root://cmseos.fnal.gov//store/user/mreid/standaloneComp/SIDMmumu_Mps-200_MZp-1p2_ctau-10p0_%s_AOD.root"%(x) for x in ctau10]
#rootfiles4=["root://cmseos.fnal.gov//store/user/mreid/standaloneComp/SIDMmumu_Mps-200_MZp-1p2_ctau-50p0_%s_AOD.root"%(x) for x in ctau50]
#rootfiles5=["root://cmseos.fnal.gov//store/user/mreid/standaloneComp/SIDMmumu_Mps-200_MZp-1p2_ctau-100p0_%s_AOD.root"%(x) for x in ctau100]
#rootfiles6=["root://cmseos.fnal.gov//store/user/mreid/standaloneComp/SIDMmumu_Mps-200_MZp-1p2_ctau-300p0_%s_AOD.root"%(x) for x in ctau300]
#rootprefix="root://cmseos.fnal.gov//store/user/mreid/standaloneComp/SIDM/"
#with open('lifetime/ctau01.txt') as f:
#	rootfiles1 = f.readlines()
#rootfiles1 = [rootprefix+"%s"%(x.strip()) for x in rootfiles1 if "_AOD" in x]
#with open('lifetime/ctau1.txt') as f:
#	rootfiles2 = f.readlines()
#rootfiles2 = [rootprefix+"%s"%(x.strip()) for x in rootfiles2 if "_AOD" in x]
#with open('lifetime/ctau10.txt') as f:
#	rootfiles3 = f.readlines()
#rootfiles3 = [rootprefix+"%s"%(x.strip()) for x in rootfiles3 if "_AOD" in x]
#with open('lifetime/ctau50.txt') as f:
#	rootfiles4 = f.readlines()
#rootfiles4 = [rootprefix+"%s"%(x.strip()) for x in rootfiles4 if "_AOD" in x]
#with open('lifetime/ctau100.txt') as f:
#	rootfiles5 = f.readlines()
#rootfiles5 = [rootprefix+"%s"%(x.strip()) for x in rootfiles5 if "_AOD" in x]
#with open('lifetime/ctau300.txt') as f:
#	rootfiles6 = f.readlines()
#rootfiles6 = [rootprefix+"%s"%(x.strip()) for x in rootfiles6 if "_AOD" in x]
#print rootfiles1
#print rootfiles2
#print rootfiles3
#print rootfiles4
#print rootfiles5
#print rootfiles6

events1 = Events(rootfiles1)
events2 = Events(rootfiles2)
events3 = Events(rootfiles1)
events4 = Events(rootfiles2)
events5 = Events(rootfiles1)
events6 = Events(rootfiles2)
def setrange(h1,h2,h3,h4,h5,h6):
	max1 = max([h1.GetMaximum(),h2.GetMaximum(),h3.GetMaximum(),h4.GetMaximum(),h5.GetMaximum(),h6.GetMaximum()])
	min1 = min([h1.GetMinimum(),h2.GetMinimum(),h3.GetMinimum(),h4.GetMinimum(),h5.GetMinimum(),h6.GetMinimum()])
	h1.SetMaximum(max1*1.15)
	h1.SetMinimum(min1*0.85)
def norm(histogram):
	n = 1/histogram.Integral()
	histogram.Scale(n)
def drawall(hist01,hist1,hist10,hist50,hist100,hist300):
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
	hist50.SetLineColor(5)
	hist100.SetLineColor(6)
	hist300.SetLineColor(7)

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
		hist50.SetMarkerColorAlpha(5,.6)
		hist100.SetMarkerColorAlpha(6,.6)
		hist300.SetMarkerColorAlpha(7,.6)
		
		hist01.SetMarkerStyle(8)
		hist1.SetMarkerStyle(8)
		hist10.SetMarkerStyle(8)
		hist50.SetMarkerStyle(8)
		hist100.SetMarkerStyle(8)
		hist300.SetMarkerStyle(8)
		
		hist01.Draw('B')
		hist1.Draw('Same')
		hist10.Draw('Same')
		hist50.Draw('Same')
		hist100.Draw('Same')
		hist300.Draw('Same')
		
	else:
		norm(hist01)
		norm(hist1)
		norm(hist10)
		norm(hist50)
		norm(hist100)
		norm(hist300)
		setrange(hist01,hist1,hist10,hist50,hist100,hist300)
		#hist01.SetMaximum(maxy)
		#hist01.SetMinimum(miny)
		hist01.Draw('HIST')
		hist1.Draw('HIST SAME')
		hist10.Draw('HIST SAME')
		hist50.Draw('HIST SAME')
		hist100.Draw('HIST SAME')
		hist300.Draw('HIST SAME')

	leg = ROOT.TLegend(.75,.75,.95,.95)
	leg.AddEntry(hist01,"0.1 cm","f")
	leg.AddEntry(hist1,"1 cm","f")
	leg.AddEntry(hist10,"10 cm","f")
	leg.AddEntry(hist50,"50 cm","f")
	leg.AddEntry(hist100,"100 cm","f")
	leg.AddEntry(hist300,"300 cm","f")
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
	hist_pt = ROOT.TH1F("histpt","gen mu pt", 40,0,160)
	hist_eta = ROOT.TH1F("histeta","gen mu eta", 40,-6,6)
	hist_phi = ROOT.TH1F("histphi","gen mu phi", 40,-6,6)
	hist_vxy = ROOT.TH1F("histvertexvxy","gen mu dxy", 50,0,10)
	hist_vz = ROOT.TH1F("histvertexvz","gen mu dz", 50,-10,10)
	hist_trigeff_denom = ROOT.TH1F("histtrigeffdenom","trigeff denominator", 50,0,120)
	hist_trigeff_num = ROOT.TH1F("histtrigeffnum","trigefficiency", 50,0,120)
	hist_recoeff_denom = ROOT.TH1F("histrecoeffdenom","recoeff denominator", 50,0,120)
	hist_recoeff_num = ROOT.TH1F("histrecoeffnum","recoefficiency", 50,0,120)
	hist_pt.Sumw2()
	hist_eta.Sumw2()
	hist_phi.Sumw2()
	hist_vxy.Sumw2()
	hist_vz.Sumw2()
	hist_trigeff_denom.Sumw2()
	hist_trigeff_num.Sumw2()
	hist_recoeff_denom.Sumw2()
	hist_recoeff_num.Sumw2()
	
	#Run over events
	for iev,event in enumerate(events):
		denominator_trig = False # at least 3 gen muons with pT >6 and |eta|<2.4 or at least 1 gen muon with pT>16 and |eta|<2.4
		numerator_trig = False # Demoninator and trigger fired
		denominator_reco = False # 4 gen muons with |eta| <2.4
		numerator_reco = False # 4 muons matched with gen muons (maxdeltaR = 0.5, maxdeltaPt/Pt =1.0)

	    	event.getByLabel(triggerBitLabel,triggerBits)
		event.getByLabel(triggerObjectLabel,triggerObjects)
		event.getByLabel(triggerPrescaleLabel,triggerPrescales)
		if (iev %100 ==0):
			print "Event %d: run %6d, lumi %4d, event %12d" % (iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
	    	
		denom_count_trig = 0
		denom_count_reco =0
		event.getByLabel(tracklable,tracks);
		event.getByLabel(genlable,gen);
		# pick out list of generated muons
		gentracks = [x for x in gen.product() if abs(x.pdgId())==13]

		#fill histograms for generated muon information. Check denom for trigger and reco efficiency
		for gtrack in gentracks:
			print "gtrack: ", gtrack.pt(), gtrack.eta()
			hist_pt.Fill(gtrack.pt())
			hist_eta.Fill(gtrack.eta())
			hist_phi.Fill(gtrack.phi())
			hist_vxy.Fill(float(gtrack.vx()**2 + gtrack.vy()**2)**(0.5))
			hist_vz.Fill(gtrack.vz())

			if abs(gtrack.eta())<2.4:
				denom_count_reco +=1
				if gtrack.pt() >16.0:# and abs(gtrack.eta())<2.4:
					denominator_trig = True
				if gtrack.pt() >6.0:# and abs(gtrack.eta())<2.4:
					denom_count_trig +=1
			
		if not (denominator_trig and (denom_count_trig > 3)):
			denominator_trig =False
		if denom_count_reco >=4:
			denominator_reco = True
		
		# trigger efficiency
	#	print "\n === TRIGGER PATHS ==="
	    	names = event.object().triggerNames(triggerBits.product())
	    	for i in xrange(triggerBits.product().size()):
			if names.triggerName(i) == "HLT_TrkMu16_DoubleTrkMu6NoFiltersNoVtx_v10":
	        		print "Trigger ", names.triggerName(i), ": ", ("PASS" if triggerBits.product().accept(i) else "fail (or not run)")
				if triggerBits.product().accept(i) and denominator_trig:
					numerator_trig = True
		
		print "trigger denominator: ", denominator_trig
		print "trigger numerator: ",numerator_trig
		
		#Reco Efficiency
		num_count_reco=0	
		for track in tracks.product():
			print "track: ", track.pt()
			#match reco mu to gen muons (maxdeltaR = .5 maxdeltapt/pt = 1.0)
			for cur,gtrack in enumerate(gentracks):
				if (abs( ((gtrack.eta()**2+gtrack.phi()**2)**(0.5)) - ((track.eta()**2 + track.phi()**2)**(0.5))) <= 0.5) and ((abs(gtrack.pt()-track.pt())/gtrack.pt()) <= 1.0):
					num_count_reco +=1
					print " matched pt: %s vs %s" %(track.pt(),gtrack.pt())
					del gentracks[cur]
					break

		if denominator_reco and num_count_reco >= 4:
			numerator_reco = True

		print "reco denominator: ", denominator_reco
		print "reco numerator: ",numerator_reco
		#Fill efficiency plots
		for track in tracks.product():
			#fill trigger eff plots
			if denominator_trig:
				hist_trigeff_denom.Fill(track.pt())
			if numerator_trig:
				hist_trigeff_num.Fill(track.pt())
			#fill reco eff plots
			if denominator_reco:
				hist_recoeff_denom.Fill(track.pt())
			if numerator_reco:
				hist_recoeff_num.Fill(track.pt())

	hist_trigeff = hist_trigeff_num.Clone("trigefficiency")
	hist_trigeff.Sumw2()
	hist_trigeff.Divide(hist_trigeff_denom)
	hist_recoeff = hist_recoeff_num.Clone("recoefficiency")
	hist_recoeff.Sumw2()
	hist_recoeff.Divide(hist_recoeff_denom)
	ROOT.gStyle.SetOptStat(0)
	return (hist_pt,hist_eta,hist_phi,hist_vxy,hist_vz,hist_trigeff,hist_recoeff)

(hist_pt1,hist_eta1,hist_phi1,hist_vxy1,hist_vz1,hist_trigeff1,hist_recoeff1) = makehist(events1)
(hist_pt2,hist_eta2,hist_phi2,hist_vxy2,hist_vz2,hist_trigeff2,hist_recoeff2) = makehist(events2)
(hist_pt3,hist_eta3,hist_phi3,hist_vxy3,hist_vz3,hist_trigeff3,hist_recoeff3) = makehist(events3)
(hist_pt4,hist_eta4,hist_phi4,hist_vxy4,hist_vz4,hist_trigeff4,hist_recoeff4) = makehist(events4)
(hist_pt5,hist_eta5,hist_phi5,hist_vxy5,hist_vz5,hist_trigeff5,hist_recoeff5) = makehist(events5)
(hist_pt6,hist_eta6,hist_phi6,hist_vxy6,hist_vz6,hist_trigeff6,hist_recoeff6) = makehist(events6)


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
drawall(hist_pt1,hist_pt2,hist_pt3,hist_pt4,hist_pt5,hist_pt6)
drawall(hist_eta1,hist_eta2,hist_eta3,hist_eta4,hist_eta5,hist_eta6)
drawall(hist_phi1,hist_phi2,hist_phi3,hist_phi4,hist_phi5,hist_phi6)
drawall(hist_vxy1,hist_vxy2,hist_vxy3,hist_vxy4,hist_vxy5,hist_vxy6)
drawall(hist_vz1,hist_vz2,hist_vz3,hist_vz4,hist_vz5,hist_vz6)
drawall(hist_trigeff1,hist_trigeff2,hist_trigeff3,hist_trigeff4,hist_trigeff5,hist_trigeff6)
drawall(hist_recoeff1,hist_recoeff2,hist_recoeff3,hist_recoeff4,hist_recoeff5,hist_recoeff6)
