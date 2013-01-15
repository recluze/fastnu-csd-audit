class StudentRecord():
    def __init__(self, studentname, project_type, weight, milestone_type):
        self.tconf = 0
        self.ec = 0 
        self.pd = 0 
        self.so = 0
        self.ex = 0 
        self.ir = 0 
        self.pr = 0 
        
        self.project_type = project_type 
        self.name = studentname
        self.weight = weight 
        self.milestone_type = milestone_type
        
    def total(self):
        total = 0 
        total += (self.pd)
        total += (self.so) 
        total += (self.ex) 
        total += (self.ir) 
        total += (self.pr)
        return total 
    
    def weighted_total(self): 
        if self.project_type == 'FYP':
            if self.milestone_type == 'Presentation': 
                return self.total() / 35 * self.weight
            else: 
               return self.total() / 10 * self.weight



class ProjectRecord():
    def __init__(self, projecttitle):
        self.studentrecords = {}
        self.co = '' 
        self.title = projecttitle

    def num_students(self):
        try: 
            n = 0 
            for k, v in self.studentrecords.items():
                n += 1 
        except Exception, e: 
            raise RuntimeError(e)
        return n 
    

class MilestoneResultsCompiler():
    def __init__(self, weight, milestone_cat):
        self.project_results = {}
        self.weight = weight 
        self.milestone_cat = milestone_cat
        
    def add_student_eval(self, eval):
        r = self.project_results
        
        student = eval.student 
        project = eval.milestone.project 
        title = eval.milestone.project.title
        
        if project not in r: 
            r[project] = ProjectRecord(title)
           
        # pr is project record 
        prd = r[project]
        srs = prd.studentrecords
        
        # create new student record if we don't already have it  
        if student not in srs.keys(): 
            srs[student] = StudentRecord(student.name, str(self.milestone_cat.project_type), self.weight, self.milestone_cat.milestone_type)

        # sr is student record
        sr = srs[student]
            
        # incorporate this record into the accumulation of student record
        ec = eval.evaluator_confidence
        if abs(ec - 0) < 0.000001:  ec = 0.000001  # too low confidence. Ignore 
         
        pd = eval.problem_difficulty if eval.problem_difficulty else 0
        so = eval.solution_strength if eval.solution_strength else 0 
        ex = eval.execution if eval.execution else 0
        ir = eval.issue_resolution if eval.issue_resolution else 0
        pr = eval.presentation  if eval.presentation else 0
        co = eval.comments 
         
        sr.pd = ((sr.ec * sr.pd) + (ec * pd)) / (sr.ec + ec)
        sr.so = ((sr.ec * sr.so) + (ec * so)) / (sr.ec + ec) 
        sr.ex = ((sr.ec * sr.ex) + (ec * ex)) / (sr.ec + ec)
        sr.ir = ((sr.ec * sr.ir) + (ec * ir)) / (sr.ec + ec)
        sr.pr = ((sr.ec * sr.pr) + (ec * pr)) / (sr.ec + ec)
        prd.co = prd.co + '\n' + co 
        
        
        # update total evaluator confidence 
        sr.ec += ec
 
    def get_compiled_result(self):
        return self.project_results
        
        
        
        
        
        
        
        
