import pandas as pd
import numpy as np
import time

class clinicaltrial:
    
    num_of_trials = 0
    
    def __init__(self, nct_id, trial_status, start_date):
        self.nct_id = nct_id#self is instant
        self.trial_status = trial_status
        self.start_date = start_date
        
        clinicaltrial.num_of_trials += 1
    #regular method, class method, static method    
    @property #define as method, but can use as attribute    
    def start_year(self):
        rawdate = self.start_date
        if pd.isnull(rawdate):
            datetest1 = None
        else:
            datetest1=int(rawdate.split(" ")[-1])
        return datetest1
        
    def __repr__(self):
        return "trial('{}','{}','{}')".format(self.nct_id, self.trial_status, self.start_date) 
    def __str__(self):
        return "trial('{}','{}','{}')".format(self.nct_id, self.trial_status, self.start_date) 
        
        
#subclass of completed and recruiting
class completedtrial(clinicaltrial):
    #completed trial focused on drug/bio info 
    treat_dict = { 'Drug': 1, 'Biological': 2 } 
    def __init__(self, nct_id, trial_status, start_date, treat_type=None, treat_info=None):
        #never pass dictionary or list to be default 
        super().__init__(nct_id, trial_status, start_date)
        self.treat_type = treat_type
        self.treat_info = treat_info
        
    def print_treat(self):
        print(self.nct_id, self.treat_type, self.treat_info)
    def __repr__(self):
        return "trial_C('{}','{}','{}','{}','{}')".format(self.nct_id, self.trial_status, self.start_date,\
         self.treat_type, self.treat_info) 
    def __str__(self):
        return "trial_C('{}','{}','{}','{}','{}')".format(self.nct_id, self.trial_status, self.start_date,\
         self.treat_type, self.treat_info) 

class recruitingtrial(clinicaltrial):
    #recruiting trial focused on contact info
    def __init__(self, nct_id, trial_status, start_date,\
     contact_name=None, contact_org=None,\
     contact_phone=None, contact_email=None ):
        #never pass dictionary or list to be default 
        super().__init__(nct_id, trial_status, start_date)
        self.contact_name = contact_name
        self.contact_org = contact_org
        self.contact_phone = contact_phone
        self.contact_email = contact_email
        
    def print_contact(self):
        print(self.nct_id, '\n', self.contact_name, ' ', self.contact_org,\
        '\n', self.contact_phone, ' ', self.contact_email)
    def __repr__(self):
        return "trial_R('{}','{}','{}','{}','{}','{}','{}')".format(self.nct_id, self.trial_status, self.start_date,\
         self.contact_name, self.contact_org, self.contact_phone, self.contact_email) 
    def __str__(self):
        return "trial_R('{}','{}','{}','{}','{}','{}','{}')".format(self.nct_id, self.trial_status, self.start_date,\
         self.contact_name, self.contact_org, self.contact_phone, self.contact_email)
        