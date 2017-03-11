import time
import settings as st
from store_if import store_if
from replace_if import replace_if
from multi_line_macro import multi_line_macro
from multi_line_macro import single_line_macro
from multi_line_macro import parameter
from replace_multi import replace_multi_line_macro
from replace_multi import create_parameter_table

    

#starting program
if __name__ == '__main__':
        
    start_time = time.clock()
    
    #input file
    fo = open("prog2.txt","r")
    
    lines = fo.readlines()
    fo.close()
    prnt = list(lines)
    i=0
    
    #remove any whitespaces before processing
    for q in lines:
        lines[i] = q.strip()
        i=i+1
    
    
    #lexical analysis (Creating tokens)
    for q in lines:
        j=0
        r=q
        
        for i in range(1,len(q)):
            if( not q[i].isalnum() and q[i] != " " and q[i] != "_" and q[i] != "$" and (q[i] != "." or q[i-1].isidentifier())):
                
                #if( not q[i-1].isalnum() and q[i-1] != " " ):
                #    continue
                
                if( i == len(q)-1 ):
                    if( q[i-1] == " " ):
                        continue
                    else:
                        r = r[:i+j]+" "+r[i+j:]
                        j=j+1                    
                
                elif( q[i-1] == " " and q[i+1] == " " ):
                    continue
                
                elif( q[i-1] == " " and q[i+1] != " " ):
                    r = r[:i+j+1]+" "+r[i+j+1:]
                    j=j+1
                
                elif( q[i-1] != " " and q[i+1] == " " ):
                    r = r[:i+j]+" "+r[i+j:]
                    j=j+1
                
                else:
                    r = r[:i+j] + " " + r[i+j] + " " + r[i+j+1:]
                    j=j+2
        lines[lines.index(q)] = r
    
    #print(prnt)   
    
    
    
    '''************************ stores all macro defination ************************'''
    
    #tracks number of lines
    pq = 1
    
    #flag to check when multi-line comments are started
    flag = False
    
    #iterate over every line in files
    for t in lines:
        
        #create tokens
        p = t.split()
        
        #if a empty line is encountered
        if( t == "" ):
            pq=pq+1
            continue
        
        #check the ending of comment
        if( flag ):
            prnt[pq-1] = ""
            if( len(p)>1 and p[-2] == '#' and p[-1] == '>' ):
                flag = False
                pq+=1
            else:       
                pq+=1
            continue
        
        #check for single line comment
        elif( p[0] == '-' and p[1] == '-' ):
            prnt[pq-1] = ""
            pq=pq+1
            continue
        
        #check for starting of multi-line comment
        elif( p[0] == '<' and p[1] == '#' ):
            prnt[pq-1] = ""
            pq=pq+1
            flag = True
            continue
        
        #check for single line MACRO
        elif( p[0] == "$macd" and p[1] != "..."):
            single_line_macro(t, lines.index(t))
        
        #check for multi-line macro defination
        elif( p[0] == "$macd" and p[1] == "..."):
            multi_line_macro(lines,t,pq-1)
        
        #increase line number
        pq=pq+1


    
    '''************************ Replace all macros used ************************'''
    
    #tracks line index
    pq=0
    
    #flag to check when multi line macro defination starts and ends
    multi_flag = False
    
    #replcing macros in input file
    while(pq < len(lines)):
        
        #create tokens
        p = lines[pq].split()
        
        #if a empty line is encountered
        if( lines[pq] == "" ):
            pq=pq+1
            continue
        
        #check the ending of multi-line defination
        if( multi_flag ):
            #prnt[pq] = ""
            if( p[0] == "$$"):
                multi_flag = False
                pq+=1
            else:
                pq+=1
            continue        
        
        #skip single line defination
        elif(len(p) > 1 and p[0] == "$macd" and p[1] != "..."):
            #prnt[pq] = ""
            pass
        
        #skip multi-line defination
        elif(len(p) > 1 and p[0] == "$macd" and p[1] == "..."):
            #prnt[pq] = ""
            pq=pq+1
            multi_flag = True
            continue
        
        #replace an $if statement
        elif(p[0] == "$if"):
            struct = []
            struct.append({'$if':[pq]})
            store_if(pq, lines, struct)
            print(struct)
            replace_if(pq, lines, prnt, struct)
            break
        
        #replace single and multi-line macro
        else:
            
            #for every key check line
            for key in st.macro_name_table:
                
                #if any key is found in that line
                if(key in p):
                    
                    #find the index of key
                    k_i = p.index(key)
                    
                    #check if it's multi-line macro name used
                    if(len(p)-1>k_i and p[k_i+1] == "("):
                        
                        s_i = prnt[pq].index("(")
                        e_i = prnt[pq].index(")", s_i)
                        
                        #get the actual parameter table for macro-call statement
                        actual_par = create_parameter_table(key, prnt[pq][s_i+1:e_i])
                        
                        #replace macro with its defination
                        pq = replace_multi_line_macro(actual_par, pq, prnt, key, lines) + pq + 1
                        continue
                    
                    #else macro is single line
                    else:
                        s_i = st.macro_def_table.get(key)[0]
                        prnt[pq] = prnt[pq].replace(key, prnt[s_i][prnt[s_i].index(key)+1:-1])
        
        #increase line number
        pq += 1
        
    
    
    '''************************ Replace all macro definations given ************************'''
    
    #tracks line index
    pq=0
    
    #flag to check when multi line macro defination starts and ends
    multi_flag = False
    
    #replcing macros in input file
    while(pq < len(lines)):
        
        #create tokens
        p = lines[pq].split()
        
        #if a empty line is encountered
        if( lines[pq] == "" ):
            pq=pq+1
            continue
        
        #check the ending of comment
        if( multi_flag ):
            prnt[pq] = ""
            if( p[0] == "$$"):
                multi_flag = False
                pq+=1
            else:
                pq+=1
            continue        
        
        #replace single line macro with ""
        elif(len(p) > 1 and p[0] == "$macd" and p[1] != "..."):
            prnt[pq] = ""
            pass
        
        #replace multi-line macro with ""
        elif(len(p) > 1 and p[0] == "$macd" and p[1] == "..."):
            prnt[pq] = ""
            pq=pq+1
            multi_flag = True
            continue
        
        pq += 1    
        


    
    '''************************ Finally write output in file ************************'''
    
    print("macro name table : ")
    print(st.macro_name_table)
    print("macro def table : ")
    print(st.macro_def_table)
    print("parameter name table : " )
    print(st.parameter_name_table)
    #output file
    fp = open("output.txt","w")
    
    for s in prnt:
        fp.write(s)
    fp.close() 
    
    end_time = time.clock()
    #input_time = sum(time_list)
    run_time = end_time - start_time
    fp.close()
