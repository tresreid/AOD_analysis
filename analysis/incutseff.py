# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv
from matplotlib.backends.backend_pdf import PdfPages

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
run_all = True



##################################################################################################################
################SETUP FILES FOR ALL COMPARISON
##################################################################################################################
# open files 
if run_all:
	#mass_split = "5p25_dMchi-0p5_"
	mass_splitlist = ["5p25_dMchi-0p5_","60_dMchi-20_"]#["5p25_dMchi-0p5_","6p0_dMchi-2p0_","52p5_dMchi-5_","60_dMchi-20_"]
	rootprefixtres="root://cmseos.fnal.gov//store/user/mreid/iDM/lifetime_"
	rootprefixandre="root://cmseos.fnal.gov//store/user/as2872/iDM/AOD_Samples/lifetime_"
	event_dic = {}
	with open('filelist/andre.txt') as f:
		rootfilesandre = f.readlines()
	with open('filelist/tres.txt') as f:
		rootfilestres = f.readlines()
	for mass_split in mass_splitlist:
		if "5p25_dMchi-0p5" in mass_split:
			rootfilesx = rootfilesandre
			rootprefix = rootprefixandre
			v2 = True
		else:	
			rootfilesx = rootfilestres
			rootprefix = rootprefixtres
			v2 = False
	#rootfilesx = rootfilesx + rootfilesx+ rootfilesx + rootfilesx + rootfilesx
		rootfiles = [x.strip() for x in rootfilesx if ("_AOD" in x) and (mass_split in x)]
		#print rootfiles
		rootfiles1 = [rootprefix+"1mm_v2/%s"%(x.strip()) if v2 else rootprefix+"1mm/%s"%(x.strip()) for x in rootfiles if ("_ctau-1p0_" in x or "_ctau-1_" in x) ]
		rootfiles2 = [rootprefix+"10mm_v2/%s"%(x.strip()) if v2 else rootprefix+"10mm/%s"%(x.strip()) for x in rootfiles if ("_ctau-10p0_" in x or "_ctau-10_" in x) ]
		rootfiles3 = [rootprefix+"100mm_v2/%s"%(x.strip()) if v2 else rootprefix+"100mm/%s"%(x.strip()) for x in rootfiles if ("_ctau-100p0_" in x or "_ctau-100_" in x) ]
		rootfiles4 = [rootprefix+"1000mm_v2/%s"%(x.strip()) if v2 else rootprefix+"1000mm/%s"%(x.strip()) for x in rootfiles if ("_ctau-1000p0_" in x or "_ctau-1000_" in x) ]
		#print rootfiles	
		print rootfiles1	
		print rootfiles2
		print rootfiles3
		print rootfiles4
		events1 = Events(rootfiles1[:1])
		events2 = Events(rootfiles2[:1])
		events3 = Events(rootfiles3[:1])
		events4 = Events(rootfiles4[:1])
		#event_dic[mass_split] = [events3]
		event_dic[mass_split] = [events1,events2,events3,events4]
	savedir = "output/allplots/"
###################################################################################################################################################
def setrange(h1,h2,h3,h4,h5=None):
	max1 = max([h1.GetMaximum(),h2.GetMaximum(),h3.GetMaximum(),h4.GetMaximum()]) if h5 is None else max([h1.GetMaximum(),h2.GetMaximum(),h3.GetMaximum(),h4.GetMaximum(),h5.GetMaximum()])
	min1 = min([h1.GetMinimum(),h2.GetMinimum(),h3.GetMinimum(),h4.GetMinimum()]) if h5 is None else min([h1.GetMinimum(),h2.GetMinimum(),h3.GetMinimum(),h4.GetMinimum(),h5.GetMinimum()])
	h1.SetMaximum(max1*1.15)
	if min1 ==0:
		h1.SetMinimum(0.8)
	else:
		h1.SetMinimum(min1*0.85)
def norm(histogram):
	if histogram.Integral() != 0:
		n = 1/histogram.Integral()
		histogram.Scale(n)
	else:
		pass
def drawall(hist1,hist2,hist3,hist4,hist5,key,leglist,pp,sel,leg,normalized):
	pp.cd(sel+1)
	if hist2 is None:
		hist2 = ROOT.TH1F()
	if hist3 is None:
		hist3 = ROOT.TH1F()
	if hist4 is None:
		hist4 = ROOT.TH1F()
	if hist5 is None:
		hist5 = ROOT.TH1F()
	#format titles
	name = hist1.GetName()
	xtitle = "MET [GeV]" if "ptmet" in name else ('pt [GeV]' if ('pt' in name) else ('eta' if ('eta' in name) else ('phi' if ('phi' in name) else 'unknown')))
	xtitle = xtitle if ('vertex' not in name) else ('dxy [cm]' if 'vxy' in name else ('dz [cm]' if 'vz' in name else 'v unknown'))
	xtitle = xtitle if ('eff' not in name) else ('MET [GeV]' if 'met' in name else ('Mu pt [GeV]' if 'mu' in name else 'eff unknown'))
	xtitle = xtitle if ('dR' not in name and 'dphi' not in name) else ('dR' if 'dR' in name else ('dPhi' if 'dphi' in name else 'angular separation unknown'))
	xtitle = xtitle if ('num' not in name) else ('# of jets ' if 'numjet' in name else ('# of mu' if 'nummu' in name else '# of unknown'))
	
	hist1.GetXaxis().SetTitle(xtitle)
	hist1.GetXaxis().SetTitleOffset(1.4)

	if "ptmet" in name and sel >= 2:
		hist1.GetXaxis().SetRangeUser(120,200)	
	if "ptjet" in name and sel >= 3:
		hist1.GetXaxis().SetRangeUser(120,200)
	if "ptmu" in hist1.GetName() and "ptmusub" in hist2.GetName() and hist3.GetEntries() == 0:
		cut_sel = ["no cuts","n_jet >=1, j1pt > 30 GeV","MET > 120 GeV", "j1pt >120, at most 2 jets w/ pt >30 GeV","at least 2 mu w/ vxy< 740 cm, |vz|<960cm & |eta|<2.4"]
		hist1.SetTitle("%s leading vs subleading Mu pt: %s"%(key,cut_sel[sel]))
	angle_redo = False
	if ("dR" in name or "dphi" in name) and key == "anglelog":
		angle_redo = True
		hist1.GetXaxis().SetRangeUser(0,3)

	#set histogram format
	hist1.SetLineColor(2)
	hist2.SetLineColor(3)
	hist3.SetLineColor(4)
	hist4.SetLineColor(6)
	#if (hist5 is not None):
	hist5.SetLineColor(5)
	hist1.SetMarkerColorAlpha(2,.6)
	hist2.SetMarkerColorAlpha(3,.6)
	hist3.SetMarkerColorAlpha(4,.6)
	hist4.SetMarkerColorAlpha(6,.6)
	#if hist5 is not None:
	hist5.SetMarkerColorAlpha(5,.6)	
	hist1.SetMarkerStyle(8)
	hist2.SetMarkerStyle(8)
	hist3.SetMarkerStyle(8)
	hist4.SetMarkerStyle(8)
	#if hist5 is not None:
	hist5.SetMarkerStyle(8)

	if 'eff' in name:
		pp.SetLogy(0)
		#print "eff: ",name 		
		hist1.SetMaximum(1.0)
		hist1.SetMinimum(0.0)
		hist1.GetYaxis().SetTitle("Efficiency")
		hist1.Draw('E1')
		hist2.Draw('E1 Same')
		hist3.Draw('E1 Same')
		hist4.Draw('E1 Same')
	#	if hist5 is not None:
		hist5.Draw('E1 Same')
	if 'eff' not in name:
		#print "not eff: ", name 
		hist1.GetYaxis().SetTitle("Counts")	
		if normalized:
			norm(hist1)
			norm(hist2)
			norm(hist3)
			norm(hist4)
#		if hist5 is not None:
			norm(hist5)
		setrange(hist1,hist2,hist3,hist4) if hist5 is None else setrange(hist1,hist2,hist3,hist4,hist5)
		p1 = pp.cd(sel+1)
		p1.SetLogy(1) if not angle_redo else p1.SetLogy(0)
		hist1.Draw('HIST')
		hist2.Draw('HIST Same')
		hist3.Draw('HIST Same')
		hist4.Draw('HIST Same')
	#	if hist5 is not None:
		hist5.Draw('HIST Same')

	
	for hist,li in zip([hist1,hist2,hist3,hist4],leglist):
		if hist.GetEntries() != 0:
			leg.AddEntry(hist,li,"f")
	leg.Draw("same")
	pp.Update()
def drawtwo(hist1,hist2,key,leglist,pp,sel, leg):
	pp.cd(sel+1)
	
	#format titles
	name = hist1.GetName()
	xtitle = "MET [GeV]" if "ptmet" in name else ('pt [GeV]' if ('pt' in name) else ('eta' if ('eta' in name) else ('phi' if ('phi' in name) else 'unknown')))
	xtitle = xtitle if ('vertex' not in name) else ('dxy [cm]' if 'vxy' in name else ('dz [cm]' if 'vz' in name else 'v unknown'))
	xtitle = xtitle if ('eff' not in name) else ('MET [GeV]' if 'met' in name else ('Mu pt [GeV]' if 'mu' in name else 'eff unknown'))
	xtitle = xtitle if ('dR' not in name and 'dphi' not in name) else ('dR' if 'dR' in name else ('dPhi' if 'dphi' in name else 'angular separation unknown'))
	xtitle = xtitle if ('num' not in name) else ('# of jets ' if 'numjet' in name else ('# of mu' if 'nummu' in name else '# of unknown'))
	
	hist1.GetXaxis().SetTitle(xtitle)
	hist1.GetXaxis().SetTitleOffset(1.4)

	if "ptmet" in name and sel >= 2:
		hist1.GetXaxis().SetRangeUser(120,200)	
	if "ptjet" in name and sel >= 3:
		hist1.GetXaxis().SetRangeUser(120,200)	
	#set histogram format
	hist1.SetLineColor(2)
	hist2.SetLineColor(3)
	hist1.SetMarkerColorAlpha(2,.6)
	hist2.SetMarkerColorAlpha(3,.6)
	hist1.SetMarkerStyle(8)
	hist2.SetMarkerStyle(8)

	if 'eff' in name:
#		pp.SetLogy(0)
		#print "eff: ",name 		
		hist1.SetMaximum(1.0)
		hist1.SetMinimum(0.0)
		hist1.GetYaxis().SetTitle("Efficiency")
		hist1.Draw('E1')
		hist2.Draw('E1 Same')
	if 'eff' not in name:
		#print "not eff: ", name 
		hist1.GetYaxis().SetTitle("Counts")	
		norm(hist1)
		norm(hist2)
		maxi = max([hist1.GetMaximum(),hist2.GetMaximum()])
		mini = max([hist1.GetMinimum(),hist2.GetMinimum()])
		hist1.SetMaximum(maxi*1.1)
		hist1.SetMinimum(mini*0.9)
#		setrange(hist1,hist2,hist3,hist4) if hist5 is None else setrange(hist1,hist2,hist3,hist4,hist5)
		p1 = pp.cd(sel+1)
#		p1.SetLogy(1)
		hist1.Draw('HIST')
		hist2.Draw('HIST Same')

	
	for hist,li in zip([hist1,hist2],leglist):
		leg.AddEntry(hist,li,"f")
	leg.Draw("same")
	pp.Update()


def draw(histogram):
	c = ROOT.TCanvas("c","c",800,800)
	c.cd
	name = savedir+"%s.png"%(histogram.GetName())
	namepdf = savedir+"%s.pdf"%(histogram.GetName())
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

def draw2d(histogram,title,pp,sel):
	pp.cd(sel+1)
	xtitle = 'eta' 
	ytitle = 'MET [GeV]'
	title = title + " "+histogram.GetTitle()
	histogram.SetTitle(title)
	histogram.GetXaxis().SetTitle(xtitle)
	histogram.GetYaxis().SetTitle(ytitle)
	histogram.Draw("COLZ")

def makehist(events,mass,life):
	# SET UP HISTOGRAMS*5
	hist_pt_met ={}
	hist_eta_met ={}
	hist_etapt_met ={}
	hist_phi_met ={}
	hist_pt_jet ={}
	hist_eta_jet ={}
	hist_phi_jet ={}
	hist_pt_mu ={}
	hist_eta_mu ={}
	hist_phi_mu ={}
	hist_vxy_mu ={}
	hist_vz_mu ={}
	hist_vz_mu_all ={}
	hist_vxy_mu_all ={}
	hist_pt_musub ={}
	hist_eta_musub ={}
	hist_phi_musub ={}
	hist_vxy_musub ={}
	hist_vz_musub ={}
	hist_dR_mu ={}
	hist_dphi_metmu ={}
	hist_dphi_mumu ={}
	hist_dphi_metjet ={}
	hist_num_mu ={}
	hist_num_jet ={}

	hist_pt_met_rec ={}
	hist_eta_met_rec ={}
	hist_etapt_met_rec ={}
	hist_phi_met_rec ={}
	hist_pt_jet_rec ={}
	hist_eta_jet_rec ={}
	hist_phi_jet_rec ={}
	hist_pt_mu_rec ={}
	hist_eta_mu_rec ={}
	hist_phi_mu_rec ={}
	hist_vxy_mu_rec ={}
	hist_vz_mu_rec ={}
	hist_vz_mu_all_rec ={}
	hist_vxy_mu_all_rec ={}
	hist_pt_musub_rec ={}
	hist_eta_musub_rec ={}
	hist_phi_musub_rec ={}
	hist_vxy_musub_rec ={}
	hist_vz_musub_rec ={}
	hist_dR_mu_rec ={}
	hist_dphi_metmu_rec ={}
	hist_dphi_mumu_rec ={}
	hist_dphi_metjet_rec ={}
	hist_num_mu_rec ={}
	hist_num_jet_rec ={}
	cut_sel = ["no cuts","n_jet >=1, j1pt > 30 GeV","MET > 120 GeV", "j1pt >120, at most 2 jets w/ pt >30 GeV","at least 2 mu w/ vxy< 740 cm, |vz|<960cm & |eta|<2.4"]
	for sel in range(5):
		hist_pt_met[sel]          = ROOT.TH1F("histptmet%s"%sel,"gen leading MET: %s"%cut_sel[sel], 100,0,800)
		hist_eta_met[sel]         = ROOT.TH1F("histetamet%s"%sel,"gen leading Met eta: %s"%cut_sel[sel], 40,-6,6)
		hist_etapt_met[sel]       = ROOT.TH2F("histetaptmet%s"%sel,"gen leading Met eta vs pt: %s"%cut_sel[sel], 40,-6,6,100,0,800)
		hist_phi_met[sel]         = ROOT.TH1F("histphimet%s"%sel,"gen leading Met phi: %s"%cut_sel[sel], 40,-6,6)
		hist_pt_jet[sel]          = ROOT.TH1F("histptjet%s"%sel,"gen leading Jet pt: %s"%cut_sel[sel], 100,0,800)
		hist_eta_jet[sel]         = ROOT.TH1F("histetajet%s"%sel,"gen leading Jet eta: %s"%cut_sel[sel], 40,-6,6)
		hist_phi_jet[sel]         = ROOT.TH1F("histphijet%s"%sel,"gen leading Jet phi: %s"%cut_sel[sel], 40,-6,6)
		hist_pt_mu[sel]           = ROOT.TH1F("histptmu%s"%sel,"gen leading Mu pt: %s"%cut_sel[sel], 100,0,50)
		hist_eta_mu[sel]          = ROOT.TH1F("histetamu%s"%sel,"gen leading Mu eta: %s"%cut_sel[sel], 40,-6,6)
		hist_phi_mu[sel]          = ROOT.TH1F("histphimu%s"%sel,"gen leading Mu phi: %s"%cut_sel[sel], 40,-6,6)
		hist_vxy_mu[sel]          = ROOT.TH1F("histvertexvxymu%s"%sel,"gen leading Mu vxy: %s"%cut_sel[sel], 100,0,600)
		hist_vz_mu[sel]           = ROOT.TH1F("histvertexvzmu%s"%sel,"gen leading Mu vz: %s"%cut_sel[sel], 50,-600,600)
		hist_vxy_mu_all[sel]      = ROOT.TH1F("histvertexvxymuall%s"%sel,"gen all Mu vxy: %s"%cut_sel[sel], 50,0,600)
		hist_vz_mu_all[sel]       = ROOT.TH1F("histvertexvzmuall%s"%sel,"gen all Mu vz: %s"%cut_sel[sel], 50,-600,600)
		hist_pt_musub[sel]        = ROOT.TH1F("histptmusub%s"%sel,"gen subleading Mu pt: %s"%cut_sel[sel], 100,0,30)
		hist_eta_musub[sel]       = ROOT.TH1F("histetamusub%s"%sel,"gen subleading Mu eta: %s"%cut_sel[sel], 40,-6,6)
		hist_phi_musub[sel]       = ROOT.TH1F("histphimusub%s"%sel,"gen subleading Mu phi: %s"%cut_sel[sel], 40,-6,6)
		hist_vxy_musub[sel]       = ROOT.TH1F("histvertexvxymusub%s"%sel,"gen subleading Mu vxy: %s"%cut_sel[sel], 100,0,600)
		hist_vz_musub[sel]        = ROOT.TH1F("histvertexvzmusub%s"%sel,"gen subleading Mu vz: %s"%cut_sel[sel], 50,-600,600)
		hist_num_jet[sel]         = ROOT.TH1F("histnumjet%s"%sel,"gen number of jets: %s"%cut_sel[sel], 10,0,10)
		hist_num_mu[sel]          = ROOT.TH1F("histnummu%s"%sel,"gen number of mu: %s"%cut_sel[sel], 10,0,10)
		hist_dR_mu[sel]           = ROOT.TH1F("histdRmu%s"%sel,"dR: gen leading mu and subleading mu: %s"%cut_sel[sel], 50,0,6)
		hist_dphi_metmu[sel]      = ROOT.TH1F("histdphimetmu%s"%sel," dPhi: gen MET and leading mu: %s"%cut_sel[sel], 50,0,5)
		hist_dphi_mumu[sel]       = ROOT.TH1F("histdphimumu%s"%sel," dPhi: gen leading mu and subleading mu: %s"%cut_sel[sel], 50,0,5)
		hist_dphi_metjet[sel]     = ROOT.TH1F("histdphimetjet%s"%sel," dPhi: gen MET and leading jet: %s"%cut_sel[sel], 50,0,5)
		
		hist_pt_met_rec[sel]      = ROOT.TH1F("histptmetrec%s"%sel,"reco leading MET: %s"%cut_sel[sel], 100,0,800)
		hist_eta_met_rec[sel]     = ROOT.TH1F("histetametrec%s"%sel,"reco leading Met eta: %s"%cut_sel[sel], 40,-6,6)
		hist_etapt_met_rec[sel]   = ROOT.TH2F("histetaptmetrec%s"%sel,"reco leading Met eta vs pt: %s"%cut_sel[sel], 40,-6,6,100,0,800)
		hist_phi_met_rec[sel]     = ROOT.TH1F("histphimetrec%s"%sel,"reco leading Met phi: %s"%cut_sel[sel], 40,-6,6)
		hist_pt_jet_rec[sel]      = ROOT.TH1F("histptjetrec%s"%sel,"reco leading Jet pt: %s"%cut_sel[sel], 100,0,800)
		hist_eta_jet_rec[sel]     = ROOT.TH1F("histetajetrec%s"%sel,"reco leading Jet eta: %s"%cut_sel[sel], 40,-6,6)
		hist_phi_jet_rec[sel]     = ROOT.TH1F("histphijetrec%s"%sel,"reco leading Jet phi: %s"%cut_sel[sel], 40,-6,6)
		hist_pt_mu_rec[sel]       = ROOT.TH1F("histptmurec%s"%sel,"reco leading Mu pt: %s"%cut_sel[sel], 100,0,50)
		hist_eta_mu_rec[sel]      = ROOT.TH1F("histetamurec%s"%sel,"reco leading Mu eta: %s"%cut_sel[sel], 40,-6,6)
		hist_phi_mu_rec[sel]      = ROOT.TH1F("histphimurec%s"%sel,"reco leading Mu phi: %s"%cut_sel[sel], 40,-6,6)
		hist_vxy_mu_rec[sel]      = ROOT.TH1F("histvertexvxymurec%s"%sel,"reco leading Mu vxy: %s"%cut_sel[sel], 100,0,600)
		hist_vz_mu_rec[sel]       = ROOT.TH1F("histvertexvzmurec%s"%sel,"reco leading Mu vz: %s"%cut_sel[sel], 50,-600,600)
		hist_vxy_mu_all_rec[sel]      = ROOT.TH1F("histvertexvxymuallrec%s"%sel,"reco all Mu vxy: %s"%cut_sel[sel], 50,0,600)
		hist_vz_mu_all_rec[sel]       = ROOT.TH1F("histvertexvzmuallrec%s"%sel,"reco all Mu vz: %s"%cut_sel[sel], 50,-600,600)
		hist_pt_musub_rec[sel]    = ROOT.TH1F("histptmusubrec%s"%sel,"reco subleading Mu pt: %s"%cut_sel[sel], 100,0,30)
		hist_eta_musub_rec[sel]   = ROOT.TH1F("histetamusubrec%s"%sel,"reco subleading Mu eta: %s"%cut_sel[sel], 40,-6,6)
		hist_phi_musub_rec[sel]   = ROOT.TH1F("histphimusubrec%s"%sel,"reco subleading Mu phi: %s"%cut_sel[sel], 40,-6,6)
		hist_vxy_musub_rec[sel]   = ROOT.TH1F("histvertexvxymusubrec%s"%sel,"reco subleading Mu vxy: %s"%cut_sel[sel], 100,0,600)
		hist_vz_musub_rec[sel]    = ROOT.TH1F("histvertexvzmusubrec%s"%sel,"reco subleading Mu vz: %s"%cut_sel[sel], 50,-600,600)
		hist_num_jet_rec[sel]     = ROOT.TH1F("histnumjetreco%s"%sel,"reco number of jets: %s"%cut_sel[sel], 10,0,10)
		hist_num_mu_rec[sel]      = ROOT.TH1F("histnummureco%s"%sel,"reco number of mu: %s"%cut_sel[sel], 10,0,10)
		hist_dR_mu_rec[sel]       = ROOT.TH1F("histdRmureco%s"%sel,"dR: reco leading mu and subleading mu: %s"%cut_sel[sel], 50,0,6)
		hist_dphi_metmu_rec[sel] = ROOT.TH1F("histdphimetmureco%s"%sel," dPhi: reco MET and leading mu: %s"%cut_sel[sel], 50,0,5)
		hist_dphi_mumu_rec[sel]    = ROOT.TH1F("histdphimumureco%s"%sel," dPhi: reco leading mu and subleading mu: %s"%cut_sel[sel], 50,0,5)
		hist_dphi_metjet_rec[sel] = ROOT.TH1F("histdphimetjetreco%s"%sel," dPhi: reco MET and leading jet: %s"%cut_sel[sel], 50,0,5)

	hist_trigeff_denom1mu  = ROOT.TH1F("histtrigeffdenom1mu","trigeff denominator", 50,0,80)
	hist_trigeff_num1mu    = ROOT.TH1F("histtrigeffnum1mu","trigefficiency HLT_PFMET120_PFMHT120", 50,0,80)
	hist_trigeff_denom2mu  = ROOT.TH1F("histtrigeffdenom2mu","trigeff denominator", 50,0,80)
	hist_trigeff_num2mu    = ROOT.TH1F("histtrigeffnum2mu","trigefficiency HLT_DoubleMu3_DCA_PFMET50_PFMHT60", 50,0,80)
	hist_trigeff_denom3mu  = ROOT.TH1F("histtrigeffdenom3mu","trigeff denominator", 50,0,80)
	hist_trigeff_num3mu    = ROOT.TH1F("histtrigeffnum3mu","trigefficiency HLT_DoubleMu3_DZ_PFMET50_PFMHT60", 50,0,80)
	hist_trigeff_denom1met = ROOT.TH1F("histtrigeffdenom1met","trigeff denominator", 50,120,200)
	hist_trigeff_num1met   = ROOT.TH1F("histtrigeffnum1met","trigefficiency HLT_PFMET120_PFMHT120", 50,120,200)
	hist_trigeff_denom2met = ROOT.TH1F("histtrigeffdenom2met","trigeff denominator", 50,50,200)
	hist_trigeff_num2met   = ROOT.TH1F("histtrigeffnum2met","trigefficiency HLT_DoubleMu3_DCA_PFMET50_PFMHT60", 50,50,200)
	hist_trigeff_denom3met = ROOT.TH1F("histtrigeffdenom3met","trigeff denominator", 50,50,200)
	hist_trigeff_num3met   = ROOT.TH1F("histtrigeffnum3met","trigefficiency HLT_DoubleMu3_DZ_PFMET50_PFMHT60", 50,50,200)
	hist_recoeff_denom_mu  = ROOT.TH1F("histrecoeffdenommumet","recoeff mu denominator", 50,0,50)
	hist_recoeff_num_mu    = ROOT.TH1F("histrecoeffnummumet","recoefficiency mu", 50,0,50)
	hist_recoeff_denom_met = ROOT.TH1F("histrecoeffdenommet","recoeff met denominator", 50,0,200)
	hist_recoeff_num_met   = ROOT.TH1F("histrecoeffnummet","recoefficiency met", 50,0,200)	
	
	hist_trigeff_denom1mu.Sumw2()
	hist_trigeff_num1mu.Sumw2()
	hist_trigeff_denom2mu.Sumw2()
	hist_trigeff_num2mu.Sumw2()
	hist_trigeff_denom3mu.Sumw2()
	hist_trigeff_num3mu.Sumw2()
	hist_trigeff_denom1met.Sumw2()
	hist_trigeff_num1met.Sumw2()
	hist_trigeff_denom2met.Sumw2()
	hist_trigeff_num2met.Sumw2()
	hist_trigeff_denom3met.Sumw2()
	hist_trigeff_num3met.Sumw2()
	hist_recoeff_denom_mu.Sumw2()
	hist_recoeff_num_mu.Sumw2()
	hist_recoeff_denom_met.Sumw2()
	hist_recoeff_num_met.Sumw2()
	
	#Run over events
	nevents = [0,0,0,0,0,0]
	nevents_rec = [0,0,0,0,0,0]
	for iev,event in enumerate(events):
		if (iev %100 ==0):
			print "Mass-Life:%s-%s, Event %d: run %6d, lumi %4d, event %12d" % (mass,life,iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())

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
		leadingJET_pt =0.
		leadingJET_eta=0.
		leadingJET_phi=0.
		leadingMET_pt =0.
		leadingMu_pt =0.
		leadingMu_eta =0.
		leadingMu_phi =0.
		leadingMu_eta=0.
		leadingMu_phi=0.
		leadingMu_vxy =0.
		leadingMu_vz =0.
		leadingSubMu_pt =0.
		leadingSubMu_eta=0.
		leadingSubMu_phi=0.
		leadingSubMu_vxy =0.
		leadingSubMu_vz =0.
		leadingGenJet_pt =0.
		leadingGenJet_eta=0.
		leadingGenJet_phi=0.
		leadingGenMet_pt =0.
		leadingGenMet_eta =0.
		leadingGenMet_phi =0.
		leadingGenMu_pt =0.0
		leadingGenMu_eta=0.
		leadingGenMu_phi=0.
		leadingGenMu_vxy =0.
		leadingGenMu_vz =0.
		leadingGenSubMu_pt =0.0
		leadingGenSubMu_eta=0.
		leadingGenSubMu_phi=0.
		leadingGenSubMu_vxy =0.
		leadingGenSubMu_vz =0.
		genmucount =0
		genjetcount =0
		genselection3_counter = 0
		genselection4_counter = 0

	
		reco_leadingJET_pt =0.
		reco_leadingJET_eta=0.
		reco_leadingJET_phi=0.
		reco_leadingMET_pt =0.
		reco_leadingMu_pt =0.
		reco_leadingMu_eta =0.
		reco_leadingMu_phi =0.
		reco_leadingMu_eta=0.
		reco_leadingMu_phi=0.
		reco_leadingMu_vxy =0.
		reco_leadingMu_vz =0.
		reco_leadingSubMu_pt =0.
		reco_leadingSubMu_eta=0.
		reco_leadingSubMu_phi=0.
		reco_leadingSubMu_vxy =0.
		reco_leadingSubMu_vz =0.
		reco_leadingGenJet_pt =0.
		reco_leadingGenJet_eta=0.
		reco_leadingGenJet_phi=0.
		reco_leadingGenMet_pt =0.
		reco_leadingGenMet_eta =0.
		reco_leadingGenMet_phi =0.
		reco_leadingGenMu_pt =0.0
		reco_leadingGenMu_eta=0.
		reco_leadingGenMu_phi=0.
		reco_leadingGenMu_vxy =0.
		reco_leadingGenMu_vz =0.
		reco_leadingGenSubMu_pt =0.0
		reco_leadingGenSubMu_eta=0.
		reco_leadingGenSubMu_phi=0.
		reco_leadingGenSubMu_vxy =0.
		reco_leadingGenSubMu_vz =0.
		reco_genmucount =0
		reco_genjetcount =0
		reco_genselection3_counter = 0
		reco_genselection4_counter = 0


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
		mutracks = [x for x in tracks.product()]
		mettracks = [x for x in met.product()]
		jettracks = [x for x in jet.product()]
		ht = 0.0

		#fill histograms for generated muon, jet and met information. Check denom for trigger and reco efficiency for met and mu
		for gmutrack in genmutracks:
			#hist_vxy_mu_all.Fill((float(gmutrack.vx()**2)+float(gmutrack.vy()**2)**2)**(0.5))
			#hist_vz_mu_all.Fill(gmutrack.vz())
			if gmutrack.pt() > 30.0:
				genselection3_counter +=1
			genmucount += 1
			if gmutrack.pt() > leadingGenMu_pt:
				leadingGenSubMu_pt = leadingGenMu_pt
				leadingGenSubMu_eta =leadingGenMu_eta
				leadingGenSubMu_phi =leadingGenMu_phi
				leadingGenSubMu_vxy =leadingGenMu_vxy
				leadingGenSubMu_vz = leadingGenMu_vz
				leadingGenMu_pt = gmutrack.pt()
				leadingGenMu_eta = gmutrack.eta()
				leadingGenMu_phi = gmutrack.phi()	
				leadingGenMu_vxy = (float(gmutrack.vx()**2) + float(gmutrack.vy()**2))**(0.5)
				leadingGenMu_vz = gmutrack.vz()
			elif (gmutrack.pt() <= leadingGenMu_pt) and (gmutrack.pt() > leadingGenSubMu_pt):
				leadingGenSubMu_pt = gmutrack.pt()
				leadingGenSubMu_eta = gmutrack.eta()
				leadingGenSubMu_phi = gmutrack.phi()	
				leadingGenSubMu_vxy = (float(gmutrack.vx()**2) + float(gmutrack.vy()**2))**(0.5)
				leadingGenSubMu_vz = gmutrack.vz()
			if abs(gmutrack.eta())<2.4:
				if (((float(gmutrack.vx()**2) + float(gmutrack.vy()**2))**(0.5))<740) and abs(gmutrack.vz()<960):
					genselection4_counter +=1
				if gmutrack.pt() >3.0:
					denom_count_reco_mu +=1
		for gjtrack in genjettracks:
			genjetcount +=1
			if gjtrack.pt() > leadingGenJet_pt:
				leadingGenJet_pt  =gjtrack.pt()	
				leadingGenJet_eta =gjtrack.eta()
				leadingGenJet_phi =gjtrack.phi()
	#		print "gtrack: ", gtrack.pt(), gtrack.eta()
		for gmtrack in genmettracks:
			if gmtrack.pt() > leadingGenMet_pt:
				leadingGenMet_pt = gmtrack.pt()
				leadingGenMet_eta = gmtrack.eta()
				leadingGenMet_phi = gmtrack.phi()
			if gmtrack.pt()>20.0:
				denom_count_reco_met +=1	


	#run over jet information to add up ht information
		for jtrack in jettracks:
			reco_genjetcount +=1
			#print jtrack.pt()
			if jtrack.pt() > reco_leadingGenJet_pt:
				reco_leadingGenJet_pt  =jtrack.pt()	
				reco_leadingGenJet_eta =jtrack.eta()
				reco_leadingGenJet_phi =jtrack.phi()
			if jtrack.pt() > 20.0 and (abs(jtrack.eta()) < 5.2):
				ht += jtrack.pt()
		if ht >60 :
			trig2_ht = True
		#run over met information 
		for mtrack in mettracks:
			if mtrack.pt() > reco_leadingGenMet_pt:
				reco_leadingGenMet_pt = mtrack.pt()
				reco_leadingGenMet_eta = mtrack.eta()
				reco_leadingGenMet_phi = mtrack.phi()
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
			
		for track in mutracks:
			#if track.pt() > 20.0:
			reco_genmucount += 1
			if track.pt() > reco_leadingGenMu_pt:
				reco_leadingGenSubMu_pt = reco_leadingGenMu_pt
				reco_leadingGenSubMu_eta =reco_leadingGenMu_eta
				reco_leadingGenSubMu_phi =reco_leadingGenMu_phi
				reco_leadingGenSubMu_vxy =reco_leadingGenMu_vxy
				reco_leadingGenSubMu_vz = reco_leadingGenMu_vz
				reco_leadingGenMu_pt = track.pt()
				reco_leadingGenMu_eta = track.eta()
				reco_leadingGenMu_phi = track.phi()	
				reco_leadingGenMu_vxy = (float(track.vx()**2) + float(track.vy()**2))**(0.5)
				reco_leadingGenMu_vz = track.vz()
			elif (track.pt() <= reco_leadingGenMu_pt) and (track.pt() > reco_leadingGenSubMu_pt):
				reco_leadingGenSubMu_pt = track.pt()
				reco_leadingGenSubMu_eta = track.eta()
				reco_leadingGenSubMu_phi = track.phi()	
				reco_leadingGenSubMu_vxy = (float(track.vx()**2) + float(track.vy()**2))**(0.5)
				reco_leadingGenSubMu_vz = track.vz()
			if abs(track.eta())<2.4:	
				if (((float(track.vx()**2) + float(track.vy()**2))**(0.5))<740) and abs(track.vz()<960):
					reco_genselection4_counter +=1
				if track.pt()>3.0:
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
#################################################################################################################################3
## Fill plots
##################################################################################################################################	
#1. n_jet >=1, j1pT>30GeV   
#2. MET>120GeV 
#3. j1pT>120GeV, at most two jets with pT>30GeV 
#4. at least two muons with pT >2GeV, eta<2.5 (this step for gen-level only)
		#for sel in range(5):
		cutpass = [False]*5
		cutpassrec = [False]*5
			#if sel == 0:
		cutpass[0] = True 
		cutpassrec[0] = True 
		#	elif sel == 1:
		cutpass[1] = (genjetcount >= 1 and leadingGenJet_pt > 30)
		cutpassrec[1] = (reco_genjetcount >= 1 and reco_leadingGenJet_pt > 30)
		#	elif sel == 2:
		cutpass[2]= (leadingGenMet_pt > 120)
		cutpassrec[2]= (reco_leadingGenMet_pt > 120)
		#	elif sel == 3:
		cutpass[3] = (genselection3_counter <=2 and leadingGenJet_pt >120)
		cutpassrec[3] = (reco_genselection3_counter <=2 and reco_leadingGenJet_pt >120)
		#	elif sel == 4:
		cutpass[4] = (genselection4_counter >=2)
		cutpassrec[4] = (reco_genselection4_counter >=2)
		#	else:
		#	cutpass = False	
		#	cutpassrec = False	
		for sel in range(5):
			if not cutpass[sel]:
				break
			else:	
				nevents[sel] += 1
				for gmutrack in genmutracks:
					hist_vxy_mu_all[sel].Fill((float(gmutrack.vx()**2)+float(gmutrack.vy()**2)**2)**(0.5))
					hist_vz_mu_all[sel].Fill(gmutrack.vz())
				if not leadingGenMu_pt == 0.0:
					hist_pt_mu[sel].Fill(leadingGenMu_pt)
					hist_eta_mu[sel].Fill(leadingGenMu_eta)
					hist_phi_mu[sel].Fill(leadingGenMu_phi)
					hist_vxy_mu[sel].Fill(leadingGenMu_vxy)
					hist_vz_mu[sel].Fill(leadingGenMu_vz)	
					hist_dphi_mumu[sel].Fill(abs(leadingGenSubMu_phi-leadingGenMu_phi))
					hist_dR_mu[sel].Fill((float(leadingGenMet_eta-leadingGenMu_eta)**2 +float(leadingGenMet_phi-leadingGenMu_phi)**2)**(0.5))
					if not leadingGenSubMu_pt ==0.0:
						hist_pt_musub[sel].Fill(leadingGenSubMu_pt)
						hist_eta_musub[sel].Fill(leadingGenSubMu_eta)
						hist_phi_musub[sel].Fill(leadingGenSubMu_phi)
						hist_vxy_musub[sel].Fill(leadingGenSubMu_vxy)
						hist_vz_musub[sel].Fill(leadingGenSubMu_vz)
				hist_pt_jet[sel].Fill(leadingGenJet_pt)
				hist_eta_jet[sel].Fill(leadingGenJet_eta)
				hist_phi_jet[sel].Fill(leadingGenJet_phi)
				hist_pt_met[sel].Fill(leadingGenMet_pt)
				hist_eta_met[sel].Fill(leadingGenMet_eta)
				hist_etapt_met[sel].Fill(leadingGenMet_eta,leadingGenMet_pt)
				hist_phi_met[sel].Fill(leadingGenMet_phi)
				hist_dphi_metmu[sel].Fill(abs(leadingGenMet_phi-leadingGenMu_phi))
				hist_dphi_metjet[sel].Fill(abs(leadingGenMet_phi - leadingGenJet_phi))
				hist_num_jet[sel].Fill(genjetcount)
				hist_num_mu[sel].Fill(genmucount)
###########################3 Fill reco plots#####################
		for sel in range(5):
			if not cutpassrec[sel]:
				break
			else:
				nevents_rec[sel] += 1
				for track in mutracks:
					hist_vxy_mu_all_rec[sel].Fill((float(track.vx()**2)+float(track.vy()**2)**2)**(0.5))
					hist_vz_mu_all_rec[sel].Fill(track.vz())
				if not reco_leadingGenMu_pt == 0.0:
					hist_pt_mu_rec[sel].Fill(reco_leadingGenMu_pt)
					hist_eta_mu_rec[sel].Fill(reco_leadingGenMu_eta)
					hist_phi_mu_rec[sel].Fill(reco_leadingGenMu_phi)
					hist_vxy_mu_rec[sel].Fill(reco_leadingGenMu_vxy)
					hist_vz_mu_rec[sel].Fill(reco_leadingGenMu_vz)
					hist_dphi_mumu_rec[sel].Fill(abs(reco_leadingGenSubMu_phi-reco_leadingGenMu_phi))
					hist_dR_mu_rec[sel].Fill((float(reco_leadingGenMet_eta-reco_leadingGenMu_eta)**2 +float(reco_leadingGenMet_phi-reco_leadingGenMu_phi)**2)**(0.5))
					if not reco_leadingGenSubMu_pt ==0.0:
						hist_pt_musub_rec[sel].Fill(reco_leadingGenSubMu_pt)
						hist_eta_musub_rec[sel].Fill(reco_leadingGenSubMu_eta)
						hist_phi_musub_rec[sel].Fill(reco_leadingGenSubMu_phi)
						hist_vxy_musub_rec[sel].Fill(reco_leadingGenSubMu_vxy)
						hist_vz_musub_rec[sel].Fill(reco_leadingGenSubMu_vz)
				hist_pt_jet_rec[sel].Fill(reco_leadingGenJet_pt)
				hist_eta_jet_rec[sel].Fill(reco_leadingGenJet_eta)
				hist_phi_jet_rec[sel].Fill(reco_leadingGenJet_phi)
				hist_pt_met_rec[sel].Fill(reco_leadingGenMet_pt)
				hist_eta_met_rec[sel].Fill(reco_leadingGenMet_eta)
				hist_etapt_met_rec[sel].Fill(reco_leadingGenMet_eta,reco_leadingGenMet_pt)
				hist_phi_met_rec[sel].Fill(reco_leadingGenMet_phi)
				hist_dphi_metmu_rec[sel].Fill(abs(reco_leadingGenMet_phi-reco_leadingGenMu_phi))
				hist_dphi_metjet_rec[sel].Fill(abs(reco_leadingGenMet_phi - reco_leadingGenJet_phi))
				hist_num_jet_rec[sel].Fill(reco_genjetcount)
				hist_num_mu_rec[sel].Fill(reco_genmucount)

#####################################################################################################
	# trigger efficiency
	#	print "\n === TRIGGER PATHS ==="
#######################################################################################################
	    	names = event.object().triggerNames(triggerBits.product())
	    	for i in xrange(triggerBits.product().size()):
			if "HLT_PFMET120_PFMHT120_IDTight_v" in names.triggerName(i):
				if triggerBits.product().accept(i) and denominator_trig1:
					numerator_trig1 = True
			if "HLT_DoubleMu3_DCA_PFMET50_PFMHT60_v" in names.triggerName(i):
				if triggerBits.product().accept(i) and denominator_trig2:
					numerator_trig2 = True
			if "HLT_DoubleMu3_DZ_PFMET50_PFMHT60_v" in names.triggerName(i):
				if triggerBits.product().accept(i) and denominator_trig3:
					numerator_trig3 = True
		if denominator_trig1:
			hist_trigeff_denom1met.Fill(leadingGenMet_pt)
			hist_trigeff_denom1mu.Fill(leadingGenMu_pt)
		if numerator_trig1:
			hist_trigeff_num1met.Fill(leadingGenMet_pt)
			hist_trigeff_num1mu.Fill(leadingGenMu_pt)
		if denominator_trig3:
			hist_trigeff_denom3met.Fill(leadingGenMet_pt)
			hist_trigeff_denom3mu.Fill(leadingGenMu_pt)
		if numerator_trig3:
			hist_trigeff_num3met.Fill(leadingGenMet_pt)
			hist_trigeff_num3mu.Fill(leadingGenMu_pt)
		if denominator_trig2:
			hist_trigeff_denom2met.Fill(leadingGenMet_pt)
			hist_trigeff_denom2mu.Fill(leadingGenMu_pt)
		if numerator_trig2:
			hist_trigeff_num2met.Fill(leadingGenMet_pt)
			hist_trigeff_num2mu.Fill(leadingGenMu_pt)
		if denominator_reco_met:
			hist_recoeff_denom_met.Fill(leadingGenMet_pt)
	#		hist_recoeff_denom_met.Fill(leadingGenMu_pt)
		if numerator_reco_met:
			hist_recoeff_num_met.Fill(leadingGenMet_pt)
	#		hist_recoeff_num_met.Fill(leadingGenMu_pt)

		#fill reco eff plots
		if denominator_reco_mu:
			hist_recoeff_denom_mu.Fill(leadingGenMu_pt)
		if numerator_reco_mu:
			hist_recoeff_num_mu.Fill(leadingGenMu_pt)

	hist_trigeff1mu = hist_trigeff_num1mu.Clone("trigefficiency1mu")
	hist_trigeff1mu.Sumw2()
	hist_trigeff1mu.Divide(hist_trigeff_denom1mu)
	hist_trigeff2mu = hist_trigeff_num2mu.Clone("trigefficiency2mu")
	hist_trigeff2mu.Sumw2()
	hist_trigeff2mu.Divide(hist_trigeff_denom2mu)
	hist_trigeff3mu = hist_trigeff_num3mu.Clone("trigefficiency3mu")
	hist_trigeff3mu.Sumw2()
	hist_trigeff3mu.Divide(hist_trigeff_denom3mu)
	hist_trigeff1met = hist_trigeff_num1met.Clone("trigefficiency1met")
	hist_trigeff1met.Sumw2()
	hist_trigeff1met.Divide(hist_trigeff_denom1met)
	hist_trigeff2met = hist_trigeff_num2met.Clone("trigefficiency2met")
	hist_trigeff2met.Sumw2()
	hist_trigeff2met.Divide(hist_trigeff_denom2met)
	hist_trigeff3met = hist_trigeff_num3met.Clone("trigefficiency3met")
	hist_trigeff3met.Sumw2()
	hist_trigeff3met.Divide(hist_trigeff_denom3met)
	hist_recoeff_mu = hist_recoeff_num_mu.Clone("recoefficiencymu")
	hist_recoeff_mu.Sumw2()
	hist_recoeff_mu.Divide(hist_recoeff_denom_mu)
	hist_recoeff_met = hist_recoeff_num_met.Clone("recoefficiencymet")
	hist_recoeff_met.Sumw2()
	hist_recoeff_met.Divide(hist_recoeff_denom_met)
	ROOT.gStyle.SetOptStat(0)
	
	allreturns = {}

	metgen = [hist_pt_met,hist_eta_met,hist_phi_met]
	jetgen = [hist_pt_jet,hist_eta_jet,hist_phi_jet]
	mugen  = [hist_pt_mu,hist_eta_mu,hist_phi_mu,hist_vxy_mu,hist_vz_mu,hist_vxy_mu_all,hist_vz_mu_all]
	mugens = [hist_pt_musub,hist_eta_musub,hist_phi_musub,hist_vxy_musub,hist_vz_musub]
	angular_sep = 	[hist_dR_mu,hist_dphi_metmu,hist_dphi_mumu,hist_dphi_metjet]
	nums = [hist_num_mu,hist_num_jet]
	
	metgenrec = [hist_pt_met_rec,hist_eta_met_rec,hist_phi_met_rec]
	jetgenrec = [hist_pt_jet_rec,hist_eta_jet_rec,hist_phi_jet_rec]
	mugenrec  = [hist_pt_mu_rec,hist_eta_mu_rec,hist_phi_mu_rec,hist_vxy_mu_rec,hist_vz_mu_rec,hist_vxy_mu_all_rec,hist_vz_mu_all_rec]
	mugensrec = [hist_pt_musub_rec,hist_eta_musub_rec,hist_phi_musub_rec,hist_vxy_musub_rec,hist_vz_musub_rec]
	angular_seprec = [hist_dR_mu_rec,hist_dphi_metmu_rec,hist_dphi_mumu_rec,hist_dphi_metjet_rec]
	numsrec = [hist_num_mu_rec,hist_num_jet_rec]
	

	trigsmu =[hist_trigeff1mu,hist_trigeff2mu,hist_trigeff3mu]
	trigsmet=[hist_trigeff1met,hist_trigeff2met,hist_trigeff3met]
	recos  = [hist_recoeff_mu,hist_recoeff_met]

	allreturnsgen = metgen+jetgen+mugen+mugens+angular_sep+nums
	allreturnsrec = metgenrec+jetgenrec+mugenrec+mugensrec+angular_seprec+numsrec	
	allreturns["hist"] = allreturnsgen+allreturnsrec
	allreturns["eff"] = trigsmu+trigsmet+recos
	allreturns["hist2d"] = [hist_etapt_met,hist_etapt_met_rec]
	allreturns["nevents"] = [nevents,nevents_rec]
	allreturns["muons"] = (hist_pt_mu,hist_pt_musub)
	return allreturns
#if not run_all:
#	(allreturns1,hist2d1) = makehist(events1)
#	(allreturns2,hist2d2) = makehist(events2)
#	(allreturns3,hist2d3) = makehist(events3)
#	(allreturns4,hist2d4) = makehist(events4)
	
#	if run_lifetimes:
#		for h1,h2,h3,h4 in zip(allreturns1,allreturns2,allreturns3,allreturns4):
#			drawall(h1,h2,h3,h4,None)
#	else:
#		for h1,h2,h3,h4 in zip(allreturns1,allreturns2,allreturns3,allreturns4):
#			drawall(h1,h2,h3,h4,None)

def pad(plots_dic,sel):
	for key in plots_dic:
		if len(plots_dic[key]) < 5:
			if sel:
				plots_dic[key] += [[[None]*5]*len(plots_dic[key][0])]*(5-len(plots_dic[key]))
			else:	
				plots_dic[key] += [[None]*len(plots_dic[key][0])]*(5-len(plots_dic[key]))
if run_all:
        print "running all"
        mass_splitlist1 = ["5p25_dMchi-0p5_","60_dMchi-20_"]#["5p25_dMchi-0p5_","6p0_dMchi-2p0_","52p5_dMchi-5_","60_dMchi-20_"]
        mass_splitlist2 = ["5 Gev (10%)","50 GeV (40%)"]#,"5 GeV (40%)","50 GeV (10%)","50 GeV (40%)"]
        lifelist = ["ctau 1mm","ctau 10mm","ctau 100mm","ctau 1000mm"]
        plots_dicmass = {}
        plots2d_dicmass = {}
        plotseff_dicmass = {}
        plots_diclife = {}
        plots2d_diclife = {}
        plotseff_diclife = {}
        plotsmuons_diclife = {}
        plotsmuons_dicmass = {}
	counts_diclife ={}
	counts_dicmass ={}
        for lkey in lifelist:
                plots_diclife[lkey]=[]
                plots2d_diclife[lkey] = []
                plotseff_diclife[lkey] = []
                plotsmuons_diclife[lkey] = []
                counts_diclife[lkey] = []
        for mass_split,key in zip(mass_splitlist1,mass_splitlist2):
                plots_dicmass[key] = []
                plots2d_dicmass[key] = []
                plotseff_dicmass[key] = []
                plotsmuons_dicmass[key] = []
                counts_dicmass[key] = []
                for num,life in enumerate(lifelist):
                        all_ret = makehist(event_dic[mass_split][num],key,life)
                        plots_dicmass[key].append(all_ret["hist"])
                        plots2d_dicmass[key].append(all_ret["hist2d"])
                        plotseff_dicmass[key].append(all_ret["eff"])
                        plotsmuons_dicmass[key].append(all_ret["muons"])
                        counts_dicmass[key].append(all_ret["nevents"])
                        plots_diclife[life].append(all_ret["hist"])
                        plots2d_diclife[life].append(all_ret["hist2d"])
                        plotseff_diclife[life].append(all_ret["eff"])
                        plotsmuons_diclife[life].append(all_ret["muons"])
                        counts_diclife[life].append(all_ret["nevents"])
	pad(plots_dicmass,True)
	pad(plotseff_dicmass,False)
	pad(plots_diclife,True)
	pad(plotseff_diclife,False)
def saveplots(plots_dic,plotseff_dic,plots2d_dic,counts_dic,plotsmuons_dic,olist,normalized):
	for key in plots_dic:
		ofile = "output_test2/%s_cutsel.pdf"%(key.replace(" ","_"))
		pp = ROOT.TCanvas("pp","pp",800,800)
		t1 = ROOT.TText(0.5,0.5,key)
	  	t1.SetTextAlign(22);
		t1.SetTextSize(0.05);
		t1.Draw();
		nevents_text = {}
		nevents_textrec = {}
		for i,li in enumerate(olist):
			ypos = 0.4-i*.05
			nevents_text[i] = ROOT.TText(0.5,ypos,"\n Gen %s: %s(c1:%s(%.2f%%[%.2f%%]),c2:%s(%.2f%%[%.2f%%]),c3:%s(%.2f%%[%.2f%%]),c4:%s(%.2f%%[%.2f%%]))"%(li,counts_dic[key][i][0][0],
			counts_dic[key][i][0][1],100*counts_dic[key][i][0][1]/float(counts_dic[key][i][0][0]),0 if counts_dic[key][i][0][0] == 0 else 100*counts_dic[key][i][0][1]/float(counts_dic[key][i][0][0]),
			counts_dic[key][i][0][2],100*counts_dic[key][i][0][2]/float(counts_dic[key][i][0][0]),0 if counts_dic[key][i][0][1] == 0 else 100*counts_dic[key][i][0][2]/float(counts_dic[key][i][0][1]),
			counts_dic[key][i][0][3],100*counts_dic[key][i][0][3]/float(counts_dic[key][i][0][0]),0 if counts_dic[key][i][0][2] == 0 else 100*counts_dic[key][i][0][3]/float(counts_dic[key][i][0][2]),
			counts_dic[key][i][0][4],100*counts_dic[key][i][0][4]/float(counts_dic[key][i][0][0]),0 if counts_dic[key][i][0][3] == 0 else 100*counts_dic[key][i][0][4]/float(counts_dic[key][i][0][3])
			))
			nevents_textrec[i] = ROOT.TText(0.5,ypos-.025,"\n Reco %s: %s(c1:%s(%.2f%%[%.2f%%]),c2:%s(%.2f%%[%.2f%%]),c3:%s(%.2f%%[%.2f%%]),c4:%s(%.2f%%[%.2f%%]))"%(li,counts_dic[key][i][1][0],
			counts_dic[key][i][1][1],100*counts_dic[key][i][1][1]/float(counts_dic[key][i][1][0]),0 if counts_dic[key][i][1][0] == 0 else 100*counts_dic[key][i][1][1]/float(counts_dic[key][i][1][0]),
			counts_dic[key][i][1][2],100*counts_dic[key][i][1][2]/float(counts_dic[key][i][1][0]),0 if counts_dic[key][i][1][1] == 0 else 100*counts_dic[key][i][1][2]/float(counts_dic[key][i][1][1]),
			counts_dic[key][i][1][3],100*counts_dic[key][i][1][3]/float(counts_dic[key][i][1][0]),0 if counts_dic[key][i][1][2] == 0 else 100*counts_dic[key][i][1][3]/float(counts_dic[key][i][1][2]),
			counts_dic[key][i][1][4],100*counts_dic[key][i][1][4]/float(counts_dic[key][i][1][0]),0 if counts_dic[key][i][1][3] == 0 else 100*counts_dic[key][i][1][4]/float(counts_dic[key][i][1][3])
			))
			nevents_text[i].SetTextAlign(22)
			nevents_text[i].SetTextSize(0.013)
			nevents_text[i].Draw() 
			nevents_textrec[i].SetTextAlign(22)
			nevents_textrec[i].SetTextSize(0.013)
			nevents_textrec[i].Draw() 
	 
		pp.Print(ofile+"(")
		pp.Clear()
		pp.Divide(2,3)
		for h1,h2,h3,h4,h5 in zip(plots_dic[key][0],plots_dic[key][1],plots_dic[key][2],plots_dic[key][3],plots_dic[key][4]):
			leg = {}
			for sel in range(5):
				leg[sel] = ROOT.TLegend(.70,.70,.85,.85)
				drawall(h1[sel],h2[sel],h3[sel],h4[sel],h5[sel],key,olist,pp,sel,leg[sel],normalized)
			pp.Print(ofile)
			del leg
			if "dR" in h1[sel].GetName() or "dphi" in h1[sel].GetName():
				leg={}
				for sel in range(5):
					leg[sel] = ROOT.TLegend(.70,.70,.85,.85)
					drawall(h1[sel],h2[sel],h3[sel],h4[sel],h5[sel],"anglelog",olist,pp,sel,leg[sel],normalized)
				pp.Print(ofile)
				del leg
		for i,h in enumerate(plots2d_dic[key]):
			for hi in h:
				for sel in range(5):
					draw2d(hi[sel],olist[i],pp,sel)
				pp.Print(ofile)
		for i,(mu,submu) in enumerate(plotsmuons_dic[key]):
			leg = {}
			for sel in range(5):
				leg[sel] = ROOT.TLegend(.70,.70,.85,.85)
				drawall(mu[sel],submu[sel],None,None,None,olist[i],["Leading","Subleading"],pp,sel,leg[sel],False)
			pp.Print(ofile)
			del leg		
		pp.Clear()	
		pp.cd(0)	
		t2 = ROOT.TText(0.5,0.5,"efficiencies")
	  	t2.SetTextAlign(22);
		t2.SetTextSize(0.05);
		t2.Draw();
		pp.Print(ofile)
		for h1,h2,h3,h4,h5 in zip(plotseff_dic[key][0],plotseff_dic[key][1],plotseff_dic[key][2],plotseff_dic[key][3],plotseff_dic[key][4]):
			leg = ROOT.TLegend(.70,.70,.85,.85)
			drawall(h1,h2,h3,h4,h5,key,olist,pp,-1,leg,normalized)
			pp.Print(ofile)
			del leg
		pp.Print(ofile+")")
		del pp


saveplots(plots_dicmass,plotseff_dicmass,plots2d_dicmass,counts_dicmass,plotsmuons_dicmass,lifelist,False)
saveplots(plots_diclife,plotseff_diclife,plots2d_diclife,counts_diclife,plotsmuons_diclife,mass_splitlist2,True)
