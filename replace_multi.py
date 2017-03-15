import settings as st
from tokens import create_tokens
import re

def replace_multi_line_macro(actual_par, i, prnt, key, lines, n_index):
    
    tab_len = space_len = 0
    
    #find the index of key
    ix = prnt[i].index(key)
    
    #calculate how much indentation to give
    for c in prnt[i][:ix]:
        if( c == '\t'):
            tab_len += 1
        #else:
            #space_len += 1
    
    #form the indentation string
    idtn_str = '\t'*tab_len + ' '*space_len
    idtn_str_1 = prnt[i][:ix]
    k=1
    
    #remove the current macro line from output
    prnt.pop(i)
    lines.pop(i)
    
    #get the line range of macro
    def_r = st.macro_def_table.get(key)[n_index]
    
    if(len(def_r) == 1):
        j = def_r[0]
        #store the current line
        b_end = prnt[j].index(")")
        temp = prnt[j][b_end+2:]
        
        #check for keys in that line to be replaced
        for key in actual_par:
            if(key in lines[j].split()):
                pattern = '\\b'+key+'\\b'
                try:
                    s_c = temp.index('"')
                    e_c = temp.index('"', s_c+1)
                except:
                    temp = re.sub(pattern,actual_par[key],temp)
                else:
                    first = temp[:s_c]
                    second = temp[s_c:e_c+1]
                    third  = temp[e_c+1:]
                    temp_1 = re.sub(pattern,actual_par[key],first)
                    temp_2 = re.sub(pattern,actual_par[key],third)
                    temp = temp_1 + second + temp_2
                #temp = temp.replace(key, actual_par[key])
    
        prnt.insert(i, idtn_str_1+temp)       
        lines.insert(i,temp)
        lines[i] = create_tokens(lines[i])
               
        return 0
    
    #iterate over macro-defination line
    for j in range(def_r[0]+2, def_r[1]):
        
        #store the current line
        temp = prnt[j].lstrip()
        
        #check for keys in that line to be replaced
        for key in actual_par:
            if(key in lines[j].split()):
                pattern = '\\b'+key+'\\b'
                try:
                    s_c = temp.index('"')
                    e_c = temp.index('"', s_c+1)
                except:
                    temp = re.sub(pattern,actual_par[key],temp)
                else:
                    first = temp[:s_c]
                    second = temp[s_c:e_c+1]
                    third  = temp[e_c+1:]
                    temp_1 = re.sub(pattern,actual_par[key],first)
                    temp_2 = re.sub(pattern,actual_par[key],third)
                    temp = temp_1 + second + temp_2                
                #temp = temp.replace(key, actual_par[key])
        
        if(k==1):
            prnt.insert(i, idtn_str_1+temp)
        else:
            prnt.insert(i, idtn_str+temp)
        
        lines.insert(i,temp)
        lines[i] = create_tokens(lines[i])
        i=i+1
        k=k+1
    
    #return the number of new lines added
    return def_r[1]-def_r[0]-3
    

def create_parameter_table(key, s):
    
    #split to get each arguments passed
    p = s.split(",")
    
    key_arg = pos_arg = 0
    
    if(s==""):
        len_p = 0
    else:
        len_p = len(p)
    
    if(len_p != 0):
        for qs in p:
            if("=" in qs):
                key_arg+=1
            else:
                pos_arg+=1
                
    flag_a = False
    name_tab = st.macro_name_table.get(key)
    def_n = name_tab[0][0]
    if(def_n > 1):
        for iq in range(1,def_n+1):
            if(name_tab[iq][0] == pos_arg):
                name_index = iq
                flag_a = True
        if(not flag_a):
            for iq in range(1,def_n+1):
                if( name_tab[iq][0] + name_tab[iq][1] == pos_arg + key_arg):
                    name_index = iq
                    flag_a = True                
                '''if(name_tab[iq][0] + name_tab[iq][1] >= pos_arg+key_arg):
                    name_index = iq
                    flag_a = True'''
    else:
        name_index = 1
        flag_a = True
    
    if(not flag_a):
        print("Error in parameter passing "+s)
        return {}
    
    #check for number of positional arguments
    n_of_pos_par = st.macro_name_table.get(key)[name_index][0]   
    
    #if( n_of_pos_par > len_p ):
    #    print("Invalid no of arguments for macro "+key)
    
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
    par_list = st.parameter_name_table.get(key)[name_index-1] 
    
    #for every key in returned parameter table
    for i in range(len(par_list)):
        
        #get the key and value
        var_key = list(par_list[i].keys())[0]
        var_value = list(par_list[i].values())[0]
        
        #if the key is already in called statement, then continue
        if(var_key in apt):
            continue
        
        #if key's value in defination is None, then store the called argument
        if( var_value == None ):
            #print(par_list)
            apt[var_key] = p[i].strip()
        
        #else check for their default or passed value
        else:
            if( i > opt_arg ):
                apt[var_key] = var_value
            else:
                apt[var_key] = p[i].strip()
    
    #return the formed parameter table
    return [apt,name_index-1]


def nested_macro(m,n,lines,prnt):
    
    total_n = 0
    i = m
    k=0
    
    while(k<n):
        
        p = lines[i].split()
        
        try:
            c_s = p.index('"')
            c_e = p.index('"', c_s+1)
            p = p[:c_s] + p[c_e+1:]
        except:
            pass
        
        #for every key check line
        for key in st.macro_name_table:
            
            #if any key is found in that line
            if(key in p):
                
                #find the index of key
                k_i = p.index(key)
                
                #check if it's multi-line macro name used
                def_rn = st.macro_def_table.get(key)[0]
                
                if(len(def_rn)==2 or len(p)-1>k_i and p[k_i+1] == "("):
                    
                    try:
                        s_i = prnt[i].index("(")
                        e_i = prnt[i].index(")", s_i)
                    except:
                        actual_par, n_index = create_parameter_table(key, "")
                    else:
                    
                        #get the actual parameter table for macro-call statement
                        actual_par, n_index = create_parameter_table(key, prnt[i][s_i+1:e_i])
                    
                    #replace macro with its defination
                    ab = replace_multi_line_macro(actual_par, i, prnt, key, lines, n_index)
                    total_n += ab
                    cd = nested_macro(i,ab+1,lines,prnt)
                    total_n += cd
                    i = i + cd
                    i = i + ab + 1
                
                #else macro is single line
                else:
                    pattern = '\\b'+key+'\\b'
                    try:
                        s_c = prnt[i].index('"')
                        e_c = prnt[i].index('"', s_c+1)
                    except:
                        prnt[i] = re.sub(pattern,st.parameter_name_table.get(key),prnt[i])
                    else:
                        first = prnt[i][:s_c]
                        second = prnt[i][s_c:e_c+1]
                        third  = prnt[i][e_c+1:]
                        temp_1 = re.sub(pattern,st.parameter_name_table.get(key),first)
                        temp_2 = re.sub(pattern,st.parameter_name_table.get(key),third)
                        prnt[i] = temp_1 + second + temp_2
                    #prnt[i] = prnt[i].replace(key, st.parameter_name_table.get(key))
            k += 1
    
    return total_n
