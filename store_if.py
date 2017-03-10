def store_if(i, all, struct): 
    
    #point to the next line of $if
    t = i+1
    
    #skip any empty lines
    while(all[t] == ""):
        t=t+1

    #create tokens
    p = all[t].split()
    
    #iterate over every line until $end is found
    while( p[0] != "$end"):
        
        #if a nested $if found, then do the same process
        if(p[0] == "$if"):
            
            #append the current $if or $elif before calling
            struct[-1].get(all[t-1].split()[0]).append({'$if':[t]})
            
            #store the return index
            t = store_if(t, all, struct[-1].get(all[t-1].split()[0]) )
            
            #skip any empty lines
            while(all[t] == ""):
                t=t+1    
            
            #create tokens
            p = all[t].split()
        
        #if any $else or $elif is found, then append them
        if(p[0] == "$elif" or p[0] == "$else"):
            struct.append({p[0]:[t]})
        
        #as $end is found, break the loop
        if(p[0] == "$end"):
            break
        
        #increase line index
        t += 1
        
        #skip any empty lines
        while(all[t] == ""):
            t=t+1
            
        p = all[t].split()
    
    #finally append the $end statement
    struct.append({p[0]:[t]})
    
    #return the next index of $end statement
    return t+1