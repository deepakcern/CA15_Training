#!/usr/bin/env python
from ROOT import TFile,TGraph,gStyle, TTree, TH1F,TH2F,TH2D, TH1D, TH1, TCanvas, TChain,TGraphAsymmErrors, TMath, TH2D, TLorentzVector, AddressOf, gROOT, TNamed
import ROOT as ROOT
import os
import sys, optparse
from array import array
import math
import numpy as numpy_
#import matplotlib.pyplot as plt

ROOT.gROOT.LoadMacro("Loader.h+")
outfilename= "pt_reweight.root"
#outfilename= "OUTPUT_QCD500-700_train.root"
ntuple = TChain("outTree")
ntuple.Add(sys.argv[1])

NEntries = ntuple.GetEntries()

if len(sys.argv)>2:
    #if sys.argv[2]=="test":
    NEntries=int(sys.argv[2])
    print "WARNING: Running in TEST MODE"

print 'NEntries = '+str(NEntries)


xbin     =[170,185,200,220,240,260,280,300,330,360,390,420,450,500,550,600,650,700,750,800,900,1000,1200,1400,1600,1800,2000,2500,3000]
nbins    =len(xbin)-1


h_ptNorm    = TH1F("h_ptNorm","h_ptNorm", nbins, xbin)

h_pt_weight =TH1F('h_pt_weight','h_pt_weight',  nbins,xbin)

for ievent in range(NEntries):
    if ievent%100==0: print "Processed %d of %d events..." %(ievent,NEntries)

    ntuple.GetEntry(ievent)
    n_ptPruned    = ntuple.__getattr__('ptPruned')
    h_ptNorm.Fill(n_ptPruned)


h_ptNorm.Scale(1/h_ptNorm.Integral())

for i in range(1,nbins):
    a=h_ptNorm.GetBinContent(i)
    h_pt_weight.SetBinContent(i,1/a)

f = TFile(outfilename,'RECREATE')
f.cd()
h_pt_weight.Write()
