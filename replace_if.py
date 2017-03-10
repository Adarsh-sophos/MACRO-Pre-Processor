import settings

def replace_if(i, all, actual, struct):
    
    #index of line where if statement starts
    t = i
    
    #flag to check if a condition is true
    no_check = False
    
    #checking the nested level
    if(type(struct[0]) == dict):
        nos = 0
    elif(type(struct[0]) == int):
        nos =1
    
    #line index where $if condition's $end found
    if_ends = struct[-1].get('$end')[0]
    
    #iterate over every line until $end is found
    while( t != if_ends ):
        
        #creating tokens
        p = all[t].split()
        
        #if condition is true, remove all the lines
        if(no_check):
            all[t] = ""
            t = t + 1
            
            #skip any empty lines
            while(all[t] == ""):
                t=t+1
                
            actual[t] = "\n"
            
            continue
        
        #if an $if or $elif statement found, then check the condition or if an $else statement then don't check
        elif( (len(p) > 1 and (p[0]=="$elif" or p[0]=="$if") and p[1] in settings.macro_name_table) or p[0] == "$else" ):
            
            #change the flag as condition is true
            no_check = True
            actual[t] = "\n"
            all[t] = ""
            
            t = t + 1
            p = all[t].split()
            
            #if a nested $if is found, then again call the same function with new index(t) of $if statement
            if( p[0] == "$if"):
                t = replace_if(t, all, actual, struct[nos].get(list(struct[nos].keys())[0]))

                #skip any empty lines
                while(all[t] == ""):
                    t=t+1

                p = all[t].split()
            
            #as condition is true, so keep the statements until a $elif or $else or $end is not found
            while( p[0] != "$elif" and p[0] != "$else" and p[0] != "$end"):
                t = t + 1
                
                #skip any empty lines
                while(all[t] == ""):
                    t=t+1
                    
                p = all[t].split()
            
            actual[t] = "\n"
                
        else:
            #if condition is false, then point to the next condition
            nos += 1
            actual[t] = "\n"
            all[t] = ""
            t = t + 1
            p = all[t].split()
            
            #corresponding $elif line index
            elif_n = struct[nos].get('$elif')
            if(elif_n != None):
                elif_n = elif_n[0]
            
            #corresponding $else line index    
            else_n = struct[nos].get('$else')
            if(else_n != None):
                else_n = else_n[0]
                
            #corresponding $end line index
            end_n = struct[nos].get('$end')
            if(end_n != None):
                end_n = end_n[0]            
           
            #print(elif_n)
            
            #if condition is false, then remove every line until a new condition is found
            while( t != elif_n and t != else_n and t != end_n ):
                actual[t] = "\n"
                all[t] = ""
                t = t + 1
                
                #skip any empty lines
                while(all[t] == ""):
                    t=t+1
                                
        #skip any empty lines    
        while(all[t] == ""):
            t = t + 1
            continue
        
        #print(all[t])
    
    
    actual[t] = "\n"
    all[t] = ""
    return t+1