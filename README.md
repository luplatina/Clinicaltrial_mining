# Clinicaltrial_mining
Scaping the date, drug and contact information from clinicaltrial.gov website.

## Overview
This project has three steps, 
* 1)Scraping data from https://clinicaltrials.gov and store the data as csv; 
* 2)Allow user to extract target disease and use class to store the data; 
* 3)Visualization.  
A web app [trialminer](http://trialminer.site) can perform the same functions with a convient user interface. 

## How to use the module package
Download the module package. then go to the directory in a terminal. Open a python command shell. test code is shown as follow:
```
from trialmining import loadtrialDF
from trialmining import trial_struct
trial_C, trial_R = loadtrialDF.TrialDF_general('leukemia') #imput target disease, 'leukemia' is an example
loadtrialDF.Trial_visual(trial_C,trial_R) #visualize the trial info, output looks like demostration 1.
loadtrialDF.printcontact(trial_R,5) #output recruiting trial info, output looks like demostration 2. 

```
The output should look like files shown in the demostration later.  

I use class to store the clinical trial information. The general features present in all clinical trials can be summarized as 

-- trial class attributes: 
* nct_id, 
* trial_status, 
* start_date,
* title

Trials with different status like completed and recruiting have different features we are intereted in. For completed trials, their treatment method information, like drug and biological treatment, can be interesting to check. For recruiting trials, their contact information can be very important for patient need helps from new treatment. Therefore two subclasses have been defined, completed trial class and clinical trial class. They hierachical design give completed trials class extra attribute treatment method, and give recruiting trials class extra attrtibute contact information. 

--completed trial class attributes:
* treatment method (drug or biological)

--recruiting trial class attributes:
* contact info


## Demostration 1: Leukemia trials information
A step by step series to extract the info of certain disease is to use a terminal, run as follow : 

The start time distribution for completed and recruiting trials are presented. And the ratio of drug and biological treatment was shown in the bar chart.
![figure_1](https://cloud.githubusercontent.com/assets/19654472/24596048/193aa4ac-180a-11e7-8d22-80bf9ef6b9f3.png)

## Demostration 2: Recruiting Leukemia trials contact information 

NCT00167219 
 Kim Nelson, RN   Masonic Cancer Center, University of Minnesota 
 612-273-2925   knelso62@fairview.org

NCT00186147 
 Physician Referrals   Stanford University 
 (650) 723-0822   nan

NCT00341016 
 Maureen Hatch, M.D.   National Cancer Institute (NCI) 
 (301) 594-7658   hatchm@mail.nih.gov

NCT00345345 
 Olga J Rios, R.N.   National Heart, Lung, and Blood Institute (NHLBI) 
 (301) 496-4462   olga.rios@nih.gov

NCT00357565 
 Christen Ebens, MD   Masonic Cancer Center, University of Minnesota 
 612-624-0123   ebens012@umn.edu
