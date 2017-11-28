
# coding: utf-8

# In[9]:

import os
import sys; sys.path.append("~/HHbbgg_ETH_devel/bregression/python") # to load packages
import training_utils as utils
import numpy as np
reload(utils)
import preprocessing_utils as preprocessing
reload(preprocessing)
import plotting_utils as plotting
reload(plotting)
import optimization_utils as optimization
reload(optimization)
import postprocessing_utils as postprocessing
reload(postprocessing)
from sklearn.externals import joblib
import pandas as pd
import root_pandas as rpd
import matplotlib.pyplot as plt
import training_utils as utils
import ROOT
from ROOT import gROOT



ntuples = 'heppy_05_10_2017'
# "%" sign allows to interpret the rest as a system command
get_ipython().magic(u'env data=$utils.IO.ldata$ntuples')
files = get_ipython().getoutput(u'ls $data | sort -t_ -k 3 -n')

#ttbar= [s for s in files if "ttbar_RegressionPerJet_heppy_energyRings3_forTesting.root" in s] #energy rings large and proper sample with Jet_e
#ttbar= ["../../bregression//output_root/treeScaleResolution20p70_full_quantile_regression_alpha.root" ] 
ttbar= ["../../bregression//output_root/treeScaleResolution20p70_op2_full_quantile_regression_alpha.root" ] 
treeName = 'reducedTree'

utils.IO.add_target(ntuples,ttbar,1)
utils.IO.add_features(ntuples,ttbar,1)

for i in range(len(utils.IO.targetName)):        
    print "using target file n."+str(i)+": "+utils.IO.targetName[i]
for i in range(len(utils.IO.featuresName)):        
    print "using features file n."+str(i)+": "+utils.IO.featuresName[i]



branch_names = 'Jet_pt_reg,Jet_pt,Jet_eta,Jet_mcFlavour,Jet_mcPt,noexpand:Jet_mcPt/Jet_pt,rho,Jet_mt,Jet_leadTrackPt,Jet_leptonPtRel,Jet_leptonDeltaR,Jet_neHEF,Jet_neEmEF,Jet_vtxPt,Jet_vtxMass,Jet_vtx3dL,Jet_vtxNtrk,Jet_vtx3deL,Jet_energyRing_dR0_em_Jet_e,Jet_energyRing_dR1_em_Jet_e,Jet_energyRing_dR2_em_Jet_e,Jet_energyRing_dR3_em_Jet_e,Jet_energyRing_dR4_em_Jet_e,Jet_energyRing_dR0_neut_Jet_e,Jet_energyRing_dR1_neut_Jet_e,Jet_energyRing_dR2_neut_Jet_e,Jet_energyRing_dR3_neut_Jet_e,Jet_energyRing_dR4_neut_Jet_e,Jet_energyRing_dR0_ch_Jet_e,Jet_energyRing_dR1_ch_Jet_e,Jet_energyRing_dR2_ch_Jet_e,Jet_energyRing_dR3_ch_Jet_e,Jet_energyRing_dR4_ch_Jet_e,Jet_energyRing_dR0_mu_Jet_e,Jet_energyRing_dR1_mu_Jet_e,Jet_energyRing_dR2_mu_Jet_e,Jet_energyRing_dR3_mu_Jet_e,Jet_energyRing_dR4_mu_Jet_e,Jet_numDaughters_pt03,nPVs,Jet_leptonPt,b_scale,b_res_20p70'.split(",") #
features = 'Jet_pt,Jet_eta,rho,Jet_mt,Jet_leadTrackPt,Jet_leptonPtRel,Jet_leptonDeltaR,Jet_neHEF,Jet_neEmEF,Jet_vtxPt,Jet_vtxMass,Jet_vtx3dL,Jet_vtxNtrk,Jet_vtx3deL,Jet_energyRing_dR0_em_Jet_e,Jet_energyRing_dR1_em_Jet_e,Jet_energyRing_dR2_em_Jet_e,Jet_energyRing_dR3_em_Jet_e,Jet_energyRing_dR4_em_Jet_e,Jet_energyRing_dR0_neut_Jet_e,Jet_energyRing_dR1_neut_Jet_e,Jet_energyRing_dR2_neut_Jet_e,Jet_energyRing_dR3_neut_Jet_e,Jet_energyRing_dR4_neut_Jet_e,Jet_energyRing_dR0_ch_Jet_e,Jet_energyRing_dR1_ch_Jet_e,Jet_energyRing_dR2_ch_Jet_e,Jet_energyRing_dR3_ch_Jet_e,Jet_energyRing_dR4_ch_Jet_e,Jet_energyRing_dR0_mu_Jet_e,Jet_energyRing_dR1_mu_Jet_e,Jet_energyRing_dR2_mu_Jet_e,Jet_energyRing_dR3_mu_Jet_e,Jet_energyRing_dR4_mu_Jet_e,Jet_numDaughters_pt03'.split(",") #
features_cat = 'Jet_pt,Jet_eta,nPVs,Jet_mt,Jet_leadTrackPt,Jet_leptonPtRel,Jet_leptonPt,Jet_leptonDeltaR,Jet_neHEF,Jet_neEmEF,Jet_vtxPt,Jet_vtxMass,Jet_vtx3dL,Jet_vtxNtrk,Jet_vtx3deL'.split(",") #same as Caterina

base_cuts='(Jet_pt > 20) & (Jet_eta<2.5 & Jet_eta>-2.5) & (Jet_mcFlavour==5 | Jet_mcFlavour==-5) & (Jet_mcPt>0) & (Jet_mcPt<6000) & (Jet_pt_reg>0)'


branch_names = [c.strip() for c in branch_names]
features = [c.strip() for c in features]
features_cat = [c.strip() for c in features_cat]


#pt_regions = '(Jet_mcPt>0),(Jet_mcPt<100),(Jet_mcPt>=100 & Jet_mcPt<300),(Jet_mcPt>=300 & Jet_mcPt<700),(Jet_mcPt>700)'.split(",")
pt_regions = '(Jet_mcPt>0),(Jet_mcPt<100),(Jet_mcPt>=100 & Jet_mcPt<300),(Jet_mcPt>=300 & Jet_mcPt<400),(Jet_mcPt>=400 & Jet_mcPt<600),(Jet_mcPt>=600)'.split(",")
eta_regions_names = '|Jet_eta|<0.5,|Jet_eta|>=0.5 & |Jet_eta|<1.0,|Jet_eta|>=1.0 & |Jet_eta|<1.5,|Jet_eta|>=1.5 & |Jet_eta|<2.0,|Jet_eta|>=2.0'.split(",")
eta_regions = '(Jet_eta<0.5 & Jet_eta>-0.5),((Jet_eta>=0.5 & Jet_eta<1.0) |(Jet_eta<=-0.5 & Jet_eta>-1.0)),(( Jet_eta>=1.0 & Jet_eta<1.5)|(Jet_eta<=-1.0 & Jet_eta>-1.5)),( (Jet_eta>=1.5 & Jet_eta<2.0)|(Jet_eta<=-1.5 & Jet_eta>=-2.0 )),(Jet_eta>=2.0 | Jet_eta<=-2.0)'.split(",")

region_names = pt_regions+eta_regions_names

#for i_r,region in enumerate(pt_regions+eta_regions):
if (1>0):
    cuts = base_cuts

    data_frame = (rpd.read_root(utils.IO.featuresName[0],treeName, columns = branch_names)).query(cuts)
    X_features = preprocessing.set_features(treeName,branch_names,features,cuts)
    X_features_cat = (preprocessing.set_features(treeName,branch_names,features_cat,cuts))
    X_test_features = preprocessing.get_test_sample(pd.DataFrame(X_features),0.)
    nTot,dictVar = postprocessing.stackFeaturesReg(data_frame,branch_names,5)

    outTags = ['full_sample_w_weights_opt_onwo','20p70_full_quantile_regression']
    X_predictions_compare = []
    for num in range(len(outTags)):
        outTag = outTags[num]
        if ('quantile' not in outTag) :
            loaded_model = joblib.load(os.path.expanduser('~/HHbbgg_ETH_devel/bregression/output_files/regression_heppy_'+outTag+'.pkl'))  
            X_pred_data = loaded_model.predict(X_test_features).astype(np.float64)
        else : X_pred_data = nTot[:,dictVar['b_scale']]
        X_predictions_compare.append(X_pred_data)

    comparison_tags = outTags
    outTagComparison = 'ComparisonScale0p2' 
    style=False 
    style=True
    plotting.plot_hist(X_predictions_compare,outTagComparison,True,['reg','quantile 0-2'])


########################################
################plot regions##############
    
#pt_regions = '(Jet_mcPt<100),(Jet_mcPt>=100 & Jet_mcPt<300),(Jet_mcPt>=300 & Jet_mcPt<700),(Jet_mcPt>700)'.split(",")
#eta_regions_names = '|Jet_eta|<0.5,|Jet_eta|>=0.5 & |Jet_eta|<1.0,|Jet_eta|>=1.0 & |Jet_eta|<1.5,|Jet_eta|>=1.5 & |Jet_eta|<2.0,|Jet_eta|>=2.0'.split(",")
#eta_regions = '(Jet_eta<0.5 & Jet_eta>-0.5),((Jet_eta>=0.5 & Jet_eta<1.0) |(Jet_eta<=-0.5 & Jet_eta>-1.0)),(( Jet_eta>=1.0 & Jet_eta<1.5)|(Jet_eta<=-1.0 & Jet_eta>-1.5)),( (Jet_eta>=1.5 & Jet_eta<2.0)|(Jet_eta<=-1.5 & Jet_eta>=-2.0 )),(Jet_eta>=2.0 | Jet_eta<=-2.0)'.split(",")
#X_pt_region=[] # list of pandas DataFrame
#X_eta_region=[] # list of pandas DataFrame
#X_pt_region_Caterina=[] # list of pandas DataFrame
#X_eta_region_Caterina=[] # list of pandas DataFrame
#target_dist = []
#target_dist_Caterina = []
##target_dist.append('RegressedFactor')
#target_dist.append('noexpand:Jet_mcPt/RegressedFactor/Jet_pt')
#target_dist_Caterina.append('noexpand:Jet_mcPt/Jet_pt_regNew')
#addName = 'RegressedFactor,noexpand:Jet_mcPt/RegressedFactor,noexpand:Jet_mcPt/Jet_pt_regNew,noexpand:Jet_mcPt/RegressedFactor/Jet_pt'.split(",")
#for region in pt_regions:
#    cuts_regions = cuts+'&'+region
#    X_pt_region.append(preprocessing.cut_region(processPath,"reducedTree",branch_names+addName,target_dist,cuts_regions))
#    X_pt_region_Caterina.append(preprocessing.cut_region(processPath,"reducedTree",branch_names+addName,target_dist_Caterina,cuts_regions))
#for region in eta_regions:
#    cuts_regions = cuts+'&'+region
#    X_eta_region.append(preprocessing.cut_region(processPath,"reducedTree",branch_names+addName,target_dist,cuts_regions))
#    X_eta_region_Caterina.append(preprocessing.cut_region(processPath,"reducedTree",branch_names+addName,target_dist_Caterina,cuts_regions))

#plotting.plot_regions(X_pt_region,pt_regions,True,50,"AfterReg_ptregion",False)
#plotting.plot_regions(X_eta_region,eta_regions_names,True,50,"AfterReg_etaregion",False)
#plotting.plot_regions(X_pt_region_Caterina,pt_regions,True,50,outTag,False)
#plotting.plot_regions(X_eta_region_Caterina,eta_regions_names,True,50,"AfterReg_etaregionCaterina",False)



# In[ ]:


