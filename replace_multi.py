import settings as st

def replace_multi_line_macro(actual_par, i, prnt, key, lines):
    
    tab_len = space_len = 0
    
    #find the index of key
    ix = prnt[i].index(key)
    
    #calculate how much indentation to give
    for c in prnt[i][:ix]:
        if( c == '\t'):
            tab_len += 1
        else:
            space_len += 1
    
    #form the indentation string
    idtn_str = '\t'*tab_len + ' '*space_len
    idtn_str_1 = prnt[i][:ix]
    k=1
    
    #remove the current macro line from output
    prnt.pop(i)
    lines.pop(i)
    
    #get the line range of macro
    def_r = st.macro_def_table.get(key)
    
    #iterate over macro-defination line
    for j in range(def_r[0]+2, def_r[1]):
        
        #store the current line
        temp = prnt[j]
        
        #check for keys in that line to be replaced
        for key in actual_par:
            if(key in lines[j].split()):
                temp = temp.replace(key, actual_par[key])
        
        if(k==1):
            prnt.insert(i, idtn_str_1+temp)
        else:
            prnt.insert(i, idtn_str+temp)
        lines.insert(i,"")
        i=i+1
        k=k+1
    
    #return the number of new lines added
    return def_r[1]-def_r[0]-3
    

def create_parameter_table(key, s):
    
    #split to get each arguments passed
    p = s.split(",")
    
    #check for number of positional arguments
    n_of_pos_par = st.macro_name_table.get(key)[1][0]
    
    if(s==""):
        len_p = 0
    else:
        len_p = len(p)
    
    if( n_of_pos_par > len_p ):
        print("Invalid no of arguments for macro "+key)
    
    opt_arg = len(p)-1
    if(s==""):
        opt_arg = -1
    
    apt = {}
    
    #store the keyword arguments passed in macro call
    for t in p:
        if("=" in t):
            temp = t.split('=')
            apt[temp[0].strip()] = temp[1].strip()
            opt_arg -= 1
    
    #get the parameter table for macro
    par_list = st.parameter_name_table.get(key) 
    
    #for every key in returned parameter table
    for i in range(len(par_list)):
        
        #get the key and value
        var_key = list(par_list[i].keys())[0]
        var_value = list(par_list[i].values())[0]
        
        #if the key is already in called statement, then continue
        if(var_key in apt):
            continue
        
        #if key's value in defination if None, then store the called argument
        if( var_value == None ):
            apt[var_key] = p[i].strip()
        
        #else check for their default or passed value
        else:
            if( i > opt_arg ):
                apt[var_key] = var_value
            else:
                apt[var_key] = p[i].strip()
    
    #return the formed parameter table
    return apt