import time

#def single_line_macro():
    

#def multi_line_macro():
    


#starting program
if __name__ == '__main__':
    
    start_time = time.clock()
    
    #input file
    fo = open("prog.c","r")
    
    #output file
    fp = open("output.txt","w")
    
    lines = fo.readlines()
    prnt = lines
    i=0
    
    #stores macros name
    macro_name_table = {}
    
    #this table is used while processing the defination of a macro
    parameter_name_table = {}
    
    #keyword parameter default table
    default_table = {}
    
    #stores defination of a macro
    macro_def_table = {}
    
    #contains formal parameter values ( i.e. conatains actual parameter )
    actual_parameter_table = {}
    
    
    #remove any whitespaces before processing
    for q in lines:
        lines[i] = q.strip()
        i=i+1
    
    
    #lexical analysis (Creating tokens)
    for q in lines:
        j=0
        r=q
        
        for i in range(1,len(q)):
            if( not q[i].isalnum() and q[i] != " " and q[i] != "_" and (q[i] != "." or q[i-1].isidentifier())):
                
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
    
    #print(lines)
    
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
            if( len(p)>1 and p[-2] == '#' and p[-1] == '>' ):
                flag = False
                pq+=1
            else:       
                pq+=1
            continue
        
        #check for single line comment
        elif( p[0] == '-' and p[1] == '-' ):
            pq=pq+1
            continue
        
        #check for starting of multi-line comment
        elif( p[0] == '<' and p[1] == '#' ):
            pq=pq+1
            flag = True
            continue
        
        #check for single line MACRO
        elif( p[0] == "$macd" and p[1] != "..."):
            single_line_macro(t, pq)
        
        #check for multi-line macro defination
        elif( p[0] == "$macd" and p[1] == "..."):
            multi_line_macro(t, pq)
        
        #conditional macro
        elif( p[0] == "$if"):
            conditional_macro(t, pq)
        
        #increase line number
        pq=pq+1
    
    end_time = time.clock()
    #input_time = sum(time_list)
    run_time = end_time - start_time
    fp.close()