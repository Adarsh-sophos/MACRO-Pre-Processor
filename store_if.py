import time

def store_if(i, all, struct): 
    
    t = i+1
    while(all[t] == ""):
        t=t+1    
    p = all[t].split()
    #print(struct)
    while( p[0] != "$end"):
        
        if(p[0] == "$if"):
            struct[-1].get(all[t-1].split()[0]).append({'$if':[t]})
            t = store_if(t, all, struct[-1].get(all[t-1].split()[0]) )
            while(all[t] == ""):
                t=t+1            
            p = all[t].split()
        
        if(p[0] == "$elif" or p[0] == "$else"):
            struct.append({p[0]:[t]})
        
        if(p[0] == "$end"):
            break
        
        t += 1
        while(all[t] == ""):
            t=t+1        
        p = all[t].split()
    
    struct.append({p[0]:[t]})
    return t+1