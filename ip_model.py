from gurobipy import *
from readFile import SMTIFileReader
         
class SMTIWeakStability():
    def __init__(self, filename):
        s = SMTIFileReader()
        s.read(filename)
        self.men = s.men
        self.women = s.women
        self.matching = dict()
        self.blocking_pair = False
        
        # Create a new Gurobi Model
        self.J = Model("SMTI")
        
    def assignmentConstraints(self):
        # Create variables        
        # =============================================== CONSTRAINT 1 ===============================================#
        # for each acceptable (man, woman) pair we create the binary variable xij and impose constraint 1   #
        #=============================================================================================================#
        for man in self.men:                        
            SumsMenVariables = LinExpr()
            m_list = self.men[man]["list"]
            self.men[man]["variables"] = {}
            for tie in m_list:
                for woman in tie:                         
                    # addVar(lb, ub, obj, vtype, name, column)
                    xij = self.J.addVar(lb=0.0, ub=1.0, obj=0.0, vtype=GRB.BINARY, name=man + " is assigned " + woman)   
                    self.men[man]["variables"][woman] = xij
                    #self.studentdict[student][1][project] = xij            
                    SumsMenVariables += xij 
            # .. add constraint that a man can only be assigned one woman
            # addConstr(lhs, sense, rhs, name)
            self.J.addConstr(SumsMenVariables <= 1, "Constraint for "+ man)
        #======================================================================
        for woman in self.women:                        
            SumsWomenVariables = LinExpr()
            w_list = self.women[woman]["list"]            
            for tie in w_list:
                for man in tie:                     
                    SumsWomenVariables += self.men[man]["variables"][woman] 
            # .. add constraint that a woman must not be assigned to more than one man
            # addConstr(lhs, sense, rhs, name)
            self.J.addConstr(SumsWomenVariables <= 1, "Constraint for "+ woman)
        
    # =============================================================================================================#
    # we define thetaij :::::: if thetaij = 1, m_i is either unmatched in M or prefers w_j to M(m_i)
    #=============================================================================================================#
    def theta(self, man, woman):
        thetaij = LinExpr()
        sumWij = LinExpr()
        # fist we get the rank of woman on man's list
        woman_rank = self.men[man]['list_rank'][woman]
        for tie in self.men[man]['list'][:woman_rank]:
            for wp in tie:
                sumWij += self.men[man]['variables'][wp]
        thetaij.addConstant(1.0)
        thetaij.add(sumWij, -1)
        return thetaij
    
    # =============================================================================================================#
    # we define alphaij ::: if alphaij = 1, w_j is either unmatched in M or prefers m_i to M(w_j)
    #=============================================================================================================#
    def alpha(self, man, woman):
        alphaij = LinExpr()
        sumMij = LinExpr()
        # fist we get the rank of man on woman's list
        man_rank = self.women[woman]['list_rank'][man]
        for tie in self.women[woman]['list'][:man_rank]:
            for mq in tie:
                sumMij += self.men[mq]['variables'][woman]
        alphaij.addConstant(1.0)
        alphaij.add(sumMij, -1)
        return alphaij

    # =============================================== CONSTRAINT 2 ===============================================#
    # we enforce constraints to avoid blocking pair for each acceptable (man, woman) pair
    #=============================================================================================================#
    def avoidblockingpair(self):                
        # for all acceptable (man, woman) pairs
        for man in self.men:
            for tie in self.men[man]['list']:
                for woman in tie:    
                    thetaij = self.theta(man, woman)
                    alphaij = self.alpha(man, woman)                    
                    ## ---- blocking pair constraint -----
                    self.J.addConstr(thetaij + alphaij <= 1, "constraint - avoid blocking pair")
                
    
    # =============================================== CONSTRAINT 3 ==============================================#
    # we maximize the objective function
    #=============================================================================================================#
    def objfunction(self):        
        # finally we add the objective function to maximise the number of matched student-project pairs
        Totalxijbinaryvariables = LinExpr()
        for man in self.men:
            for tie in self.men[man]['list']:    
                for woman in tie:
                    Totalxijbinaryvariables += self.men[man]['variables'][woman]
        #Totalxijbinaryvariables = quicksum(self.studentdict[student][1][project] for student in self.studentdict for project in self.studentdict[student][1])
        #setObjective(expression, sense=None)
        self.J.setObjective(Totalxijbinaryvariables, GRB.MAXIMIZE) 

    def run_ip_model(self):
        self.assignmentConstraints()
        self.avoidblockingpair()
        self.objfunction()
        self.J.optimize()
        for man in self.men:
            match_found = False
            for tie in self.men[man]['list']:    
                for woman in tie:
                    a = self.J.getVarByName(man + " is assigned " + woman)                    
                    if a.x == 1.0:
                        match_found = True
                        self.matching[man] = woman
                        self.women[woman]['matching'] = man
                        #print(f"{man} --> {woman}")
                        break
                if match_found:
                    break

    def check_blocking_pairs(self):
        # we will run ip model before this and self.matching would be populated
        for man in self.men:
            if man in self.matching:
                assigned_woman = self.matching[man]
                rank_assigned_woman = self.men[man]['list_rank'][assigned_woman]
                # we need to check all women that this man prefers to his current assignment
                preferred_women = self.men[man]['list'][:rank_assigned_woman-1]
            else:
                preferred_women = self.men[man]['list']
            # for each prefeered_woman, check if she forms a blocking pair with man
            for tie in preferred_women:
                for woman in tie:
                    assigned_man = self.women[woman]['matching']
                    rank_assigned_man = self.women[woman]['list_rank'][assigned_man]
                    rank_man = self.women[woman]['list_rank'][man]
                    if rank_man < rank_assigned_man:
                        self.blocking_pair = True
                        return True
        return False
        
        
S = SMTIWeakStability("ex1.txt")
#S = SMTIWeakStability("ex2.txt")
#S = SMTIWeakStability("ex3.txt")
S.run_ip_model()
blocking_pairs = S.check_blocking_pairs()
print(f"matching has blocking pairs: {blocking_pairs}")
for k, v in S.matching.items():
    print(f"{k} ---> {v}")    
    