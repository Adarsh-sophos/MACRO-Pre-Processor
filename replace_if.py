import settings

def replace_if(i, all, actual, struct):
    
    t = i
    no_check = False
    
    if(type(struct[0]) == dict):
        nos = 0
    elif(type(struct[0]) == int):
        nos =1
    
    if_ends = struct[-1].get('$end')[0]
    
    while( t != if_ends ):
        
        p = all[t].split()
        
        if(no_check):
            all[t] = ""
            t = t + 1
            while(all[t] == ""):
                t=t+1
            actual[t] = "\n"
            
            continue
        
        elif( (len(p) > 1 and (p[0]=="$elif" or p[0]=="$if") and p[1] in settings.macro_name_table) or p[0] == "$else" ):
            no_check = True
            actual[t] = "\n"
            all[t] = ""
            
            t = t + 1
            p = all[t].split()
            
            if( p[0] == "$if"):
                t = replace_if(t, all, actual, struct[nos].get(list(struct[nos].keys())[0]))
                while(all[t] == ""):
                    t=t+1                
                p = all[t].split()
            
            while( p[0] != "$elif" and p[0] != "$else" and p[0] != "$end"):
                t = t + 1
                
                while(all[t] == ""):
                    t=t+1
                    
                p = all[t].split()
            
            actual[t] = "\n"
                
        else:
            nos += 1
            actual[t] = "\n"
            all[t] = ""
            t = t + 1
            p = all[t].split()
            
            elif_n = struct[nos].get('$elif')
            if(elif_n != None):
                elif_n = elif_n[0]
                
            else_n = struct[nos].get('$else')
            if(else_n != None):
                else_n = else_n[0]
                
            end_n = struct[nos].get('$end')
            if(end_n != None):
                end_n = end_n[0]            
           
            #print(elif_n)
            
            while( t != elif_n and t != else_n and t != end_n ):
                actual[t] = "\n"
                all[t] = ""
                t = t + 1
                
                while(all[t] == ""):
                    t=t+1
                                
            
        while(all[t] == ""):
            t = t + 1
            continue
        
        #print(all[t])
    
    
    actual[t] = "\n"
    all[t] = ""
    return t+1