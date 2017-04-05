import os
import glob
import pandas as pd
import numpy as np
import time
import re
#from trial_struct import completedtrial, recruitingtrial, clinicaltrial 
from trialmining.trial_struct import completedtrial, recruitingtrial, clinicaltrial 
import matplotlib.pyplot as plt

def TrialDF_general(keyword):
    #load all trials has the keyword, keyword = 'leukemia'
    #obtain the index, subDF;
    ##load scrape_all.csv.
    diseasename=keyword
    fn0 = './data/clinicaltrial_general.csv'
    dfID0 = pd.DataFrame.from_csv(fn0, encoding = "ISO-8859-1");
    #print('The demensionality of the Datafram:', dfID0.shape)
    nct_id0=dfID0['nct_id'].values;
    trial_status0=dfID0['trial_status'].values;
    clinical_result0=dfID0['clinical_result'].values;
    phase0=dfID0['phase'].values;
    start_date0=dfID0['start_date'].values;
    intervention_type0=dfID0['intervention_type'].values;
    intervention_name0=dfID0['intervention_name'].values;
    nct_title0=dfID0['nct_title'].values;
    #dfID0.head(n=10)
    
    testtitle=dfID0.nct_title.values
    index_title=[]
    #title only can give preliminary search;
    # more accurate search should include trial discription 
    for i in range(len(testtitle)):
        match=re.search(diseasename,testtitle[i],re.IGNORECASE)
        index_title.append(bool(match))
    index_title = np.array(index_title)
    index_statusa = (trial_status0 == 'Completed')
    index_statusb = (trial_status0 == 'Recruiting')
    index_result = (clinical_result0 == 1)
    index_drug = (intervention_type0 == 'Drug')
    index_bio = (intervention_type0 == 'Biological')
    index_figa1 = index_title&index_statusa #disease+completed
    index_figa2 = index_title&index_statusb #disease+recruiting
    index_figc1 = index_title&index_statusa&index_drug #disease+completed+drug
    index_figc2 = index_title&index_statusa&index_bio #disease+completed+bio
    drugname=np.array(intervention_name0)[index_figc1]
    bioname=np.array(intervention_name0)[index_figc2]
    
    print('Completed and recruiting trials for '+diseasename+ ':',\
     len(dfID0.nct_title[index_figa1].values),\
     len(dfID0.nct_title[index_figa2].values))
    print('drug and biological ratio in trail: ', len(drugname),len(bioname))
    print('drug and biological ratio without duplicate items: ',\
     len(np.unique(drugname)),len(np.unique(bioname)))
    #could I use index creat a class list?
    #class list1: completed index_figa1
    #class list2: recruiting index_figa2
    nct_id1 = nct_id0[index_figa1]
    trial_status1 = trial_status0[index_figa1]
    start_date1 = start_date0[index_figa1]
    treat_type1 = intervention_type0[index_figa1]
    treat_info1 = intervention_name0[index_figa1]
    
    nct_id2 = nct_id0[index_figa2]
    trial_status2 = trial_status0[index_figa2]
    start_date2 = start_date0[index_figa2]
    
    trial_C = []
    for i in range(len(nct_id1)):
        trial_C.append(completedtrial(nct_id1[i], trial_status1[i],\
        start_date1[i], treat_type1[i], treat_info1[i])) 
        
    trial_R0 = []
    for i in range(len(nct_id2)):
        trial_R0.append(clinicaltrial(nct_id2[i], trial_status2[i],\
        start_date2[i]))
        
    trial_R = TrialDF_contact( index_figa2, trial_R0 )
    #print(trial_R[0].contact_name)
    #trial_R[0].print_contact()
    #print(trial_R[0].start_year)
    return trial_C, trial_R #drugname, bioname
    
     
     
        
def TrialDF_contact( index_recruit, trial_R0 ):
    fn2 = './data/clinicaltrial_contact.csv'
    dfID2 = pd.DataFrame.from_csv(fn2, encoding = "ISO-8859-1");
    dfID2_sub=dfID2.iloc[index_recruit]
    nct_id2 = dfID2_sub['nct_id'].values;
    contact_name2 = dfID2_sub['contact_name'].values;
    contact_org2 = dfID2_sub['contact_org'].values;
    contact_phone2 = dfID2_sub['contact_phone'].values;
    contact_email2 = dfID2_sub['contact_email'].values;

    trial_R = []
    for i in range(len(nct_id2)):
        if pd.isnull(contact_name2[i])==False:
            trial_R.append(recruitingtrial(nct_id2[i], trial_R0[i].trial_status,\
            trial_R0[i].start_date, contact_name2[i], contact_org2[i],\
            contact_phone2[i], contact_email2[i]))
    return trial_R
    
def Trial_visual(trial_C, trial_R):
    drugname = []
    bioname = []
    startyear_C = []
    startyear_R = []

    for i in range(len(trial_C)):
        if trial_C[i].treat_type=='Drug':
            drugname.append(trial_C[i].treat_info)
        if trial_C[i].treat_type=='Biological':
            bioname.append(trial_C[i].treat_info)
        if trial_C[i].start_year != None:
            startyear_C.append(trial_C[i].start_year)
    for i in range(len(trial_R)):
        if trial_R[i].start_year != None:
            startyear_R.append(trial_R[i].start_year)
        
    plt.figure(1,figsize=(8, 4))

    ax1b=plt.subplot(1,2,1)
    xyear=np.arange(1990,2020)
    ax1b.hist(startyear_C,xyear,alpha = 0.7, label='completed')
    ax1b.hist(startyear_R,xyear,alpha = 0.7, label='recruiting')
    ax1b.set_xlabel('years')
    ax1b.set_ylabel('number of trials')
    ax1b.legend(loc='upper left')

    ax1c=plt.subplot(1,2,2)
    ax1c.bar([1,2],[len(drugname),len(bioname)],label='total')
    ax1c.bar([1,2],[len(np.unique(drugname)),len(np.unique(bioname))],label='distinct')
    plt.xticks([1, 2], ['Drug', 'Biological'])
    ax1c.set_ylabel('number of treatments')
    ax1c.legend(loc='upper right')
    plt.tight_layout()
    plt.suptitle('clinical trial info')
    plt.subplots_adjust(top=0.90)

    plt.show()
    
def printcontact(trial_R, N=5):
    #only recuiting trials have contact info
    for i in trial_R[:N]:
        i.print_contact()    

    
    

#####################################################
#keyword = 'leukemia'  
#trial_C, trial_R = TrialDF_general(keyword)
#for i in trial_R[:10]:
#    i.print_contact()    
#Trial_visual(trial_C, trial_R)
#####################################################
# python ./loadtrialDF.py
# suggestion from ethan,
#pep8 for clean code;
#unittest2
#build dictionary or use sqlite may save some running time;
#build module package not a single py file;

#from trialmining import loadtrialDF
#from trialmining import trial_struct
#trial_C, trial_R = loadtrialDF.TrialDF_general('leukemia')
#loadtrialDF.Trial_visual(trial_C,trial_R)
#loadtrialDF.printcontact(trial_R,5)


#
#test2=trial_struct.recruitingtrial('nct1001','completed',1990,'a','b','c','d')
#

