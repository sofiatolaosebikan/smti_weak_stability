#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 15:28:21 2023

@author: sofiat
"""

class SMTIFileReader():
    def __init__(self):
        self.men = dict()
        self.women = dict()
        

    def read(self, filename):
        with open(filename) as I:
            I = I.readlines()
            instance_size = I[0].strip().split()
            men_size, women_size = instance_size
            # ..reading the men's preference list..
            for line in I[1:int(men_size) + 1]:
                line = line.strip().split(':')
                m = f'm{line[0]}'
                m_list = []                
                ongoing_tie = False
                m_list_rank = {}
                w_rank = 1
                for char in line[1]:
                    if char.isdigit() and not ongoing_tie:
                        m_list.append([f'w{char}'])
                        m_list_rank[f'w{char}'] = w_rank
                        w_rank += 1
                    elif char=='(':
                        tie = []
                        ongoing_tie = True  
                    elif char.isdigit() and ongoing_tie:
                        tie.append(f'w{char}')
                        m_list_rank[f'w{char}'] = w_rank
                    elif char == ')':
                        m_list.append(tie)                                                
                        ongoing_tie = False
                        w_rank += 1
                self.men[m] = {"list": m_list, "list_rank": m_list_rank}
                        
                #print(m, self.men[m])                
            # ..reading the women's preference list..
            for line in I[int(men_size)+1: ]:
                line = line.strip().split(':')
                w = f'w{line[0]}'                
                w_list = []                
                ongoing_tie = False
                w_list_rank = {}
                m_rank = 1
                for char in line[1]:
                    if char.isdigit() and not ongoing_tie:
                        w_list.append([f'm{char}'])
                        w_list_rank[f'm{char}'] = m_rank
                        m_rank += 1
                    elif char=='(':
                        tie = []
                        ongoing_tie = True  
                    elif char.isdigit() and ongoing_tie:
                        tie.append(f'm{char}')
                        w_list_rank[f'm{char}'] = m_rank
                    elif char == ')':
                        w_list.append(tie)                                                
                        ongoing_tie = False
                        m_rank += 1
                self.women[w] = {"list": w_list, "list_rank": w_list_rank}
                #print(w, self.women[w])
            
            
        
s = SMTIFileReader()         
s.read("mcdermid.txt")