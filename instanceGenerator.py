#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 13:14:15 2023

@author: sofiat
"""

import random

class StableMarriageInstance:
    
    def __init__(self, size):
        self.no_men = size
        self.no_women = size
        # self.list_low_bound = list_low_bound
        # self.list_up_bound = list_up_bound
        
        self.men_list = [f"{i}" for i in range(1,self.no_men+1)]
        self.women_list = [f"{i}" for i in range(1,self.no_women+1)]        
        self.men = {}
        self.women = {}
        
        
    # stable marriage with complete list and no ties (SM) - we just need the size
    def sm_no_ties(self):
        for man in self.men_list:
            man_pref_list = self.women_list[:]
            random.shuffle(man_pref_list)
            self.men[man] = man_pref_list
        
        for woman in self.women_list:
            woman_pref_list = self.men_list[:]
            random.shuffle(woman_pref_list)
            self.women[woman] = woman_pref_list
        print("Stable Marriage with Complete List (No Ties)")
        for k, v, in self.men.items():
            print(f"{k} ---> {v}")
        print()
        for k, v, in self.women.items():
            print(f"{k} ---> {v}")
        print()       
    
    # stable marriage with incomplete list and no ties (SMI) - we need upper and lower bound on the preference list length
    def smi_no_ties(self, list_lower_bound, list_upper_bound):                
        # an error check here could verify that the list_upper_bound does not exceed self.no_men (TO-DO)      
        for man in self.men_list:
            man_pref_list = self.women_list[:]
            random.shuffle(man_pref_list)
            list_length = random.randint(list_lower_bound, list_upper_bound)
            self.men[man] = man_pref_list[:list_length]        
        # now construct the women's list
        self.women = {w: [] for w in self.women_list}
        for man in self.men:
            for woman in self.men[man]:
                self.women[woman].append(man)
        # now we shuffle the women's list
        for woman in self.women:
            current_list = self.women[woman][:]
            random.shuffle(current_list)
            self.women[woman] = current_list
        print("Stable Marriage with Incomplete List (No Ties)")
        for k, v, in self.men.items():
            print(f"{k} ---> {v}")
        print()
        for k, v, in self.women.items():
            print(f"{k} ---> {v}")
        print()
        
    # stable marriage with complete list and ties (SMT) - in addition to size, we need the tie density on both sides
    def sm_ties(self, men_tie_density, women_tie_density):
        self.sm_no_ties()
        # to decide if a woman will be tied with her successor..
        # if men_tie_density = 0, no tie in the preference list
        # if men_tie_density = 1, the preference list is a single tie
        for man in self.men:
            no_tie_list = self.men[man][:]
            tied_list = [[no_tie_list[0]]]
            for woman in no_tie_list[1:]:
                if random.uniform(0,1) <= men_tie_density:
                    tied_list[-1].append(woman)
                else:
                    tied_list.append([woman])
            self.men[man] = tied_list
        # -------------------------------------
        for woman in self.women:
            no_tie_list = self.women[woman][:]
            tied_list = [[no_tie_list[0]]]
            for man in no_tie_list[1:]:
                if random.uniform(0,1) <= women_tie_density:
                    tied_list[-1].append(man)
                else:
                    tied_list.append([man])
            self.women[woman] = tied_list
        print("Stable Marriage with Complete List and Ties")
        for k, v, in self.men.items():
            print(f"{k} ---> {v}")
        print()
        for k, v, in self.women.items():
            print(f"{k} ---> {v}")
        print()
        
    # stable marriage with incomplete list and ties (SMTI)
    def smi_ties(self, list_lower_bound, list_upper_bound, men_tie_density, women_tie_density):
        self.smi_no_ties(list_lower_bound, list_upper_bound)
        # to decide if a woman will be tied with her successor..
        # if men_tie_density = 0, no tie in the preference list
        # if men_tie_density = 1, the preference list is a single tie
        for man in self.men:
            no_tie_list = self.men[man][:]
            tied_list = [[no_tie_list[0]]]
            for woman in no_tie_list[1:]:
                if random.uniform(0,1) <= men_tie_density:
                    tied_list[-1].append(woman)
                else:
                    tied_list.append([woman])
            self.men[man] = tied_list
        # -------------------------------------
        for woman in self.women:
            no_tie_list = self.women[woman][:]
            tied_list = [[no_tie_list[0]]]
            for man in no_tie_list[1:]:
                if random.uniform(0,1) <= women_tie_density:
                    tied_list[-1].append(man)
                else:
                    tied_list.append([man])
            self.women[woman] = tied_list
        print("Stable Marriage with Incomplete List and Ties")
        for k, v, in self.men.items():
            print(f"{k} ---> {v}")
        print()
        for k, v, in self.women.items():
            print(f"{k} ---> {v}")
        print()    
        
    def write_to_file(self, filename):
        with open(filename, 'w') as I:
            I.write(f"{self.no_men} {self.no_men}\n")
            if type(self.men['1'][0]) == str: # means we are not writing the tie case
                for i in range(1, self.no_men+1):                
                    I.write(f"{i}: {' '.join(self.men[str(i)])}\n")
                for j in range(1, self.no_men+1):                
                    I.write(f"{j}: {' '.join(self.women[str(j)])}\n")
            else:
                for i in range(1, self.no_men+1):  
                    man_list = self.men[str(i)]
                    to_write = []
                    for tie in man_list:
                        if len(tie) == 1:
                            to_write.append(tie[0])
                        else:
                            to_write.append(f"({' '.join(tie)})")
                    I.write(f"{i}: {' '.join(to_write)}\n")
                for j in range(1, self.no_men+1):  
                    woman_list = self.women[str(j)]
                    to_write = []
                    for tie in woman_list:
                        if len(tie) == 1:
                            to_write.append(tie[0])
                        else:
                            to_write.append(f"({' '.join(tie)})")
                    I.write(f"{j}: {' '.join(to_write)}\n")
        I.close()
    
    
        

s = StableMarriageInstance(11)
#s.sm_no_ties()
#s.smi_no_ties(1, 5)
#s.sm_ties(0.1, 0.2)
s.smi_ties(5, 11, 0.2, 0.3)
s.write_to_file("in3.txt")
