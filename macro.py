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


    #function to create entry in parameter list      
    def create_entry(line,entry):
        k=0
        # check if the parameter has value
        if('=' in line):
            # getting parameter name
            while(line[k]!='='):
                k+=1
            p=line[0:k-1]
            print("parameter : "+p)
            # checking parameter name is valid
            if(not(p.isidentifier())):
                print("Invalid parameter name : "+p)
                return(entry)
            # getting parameter value
            v=line[k+2:len(line)]
            print("value : "+v)
            #adding entry
            item={}
            item[p]=v
            entry.append(item)
        else:# if the parameter has value no value just add the parameter
            p=line[0:len(line)]
            if(not(p.isidentifier())):
                print("Invalid parameter name : "+p)
                return(entry)
            print("parameter : "+p)
            item={}
            item[p]=None
            entry.append(item)
            
        return(entry)

    #function to check for parameters in each macro
    def parameter(line):
        entry=[]
        j=0
        #checking for ending bracket
        if(line[-1]!=')'):
            print("Ending bracket missing in : "+line)
            return
        # getting macro name
        while(line[j]!=' '):
            j=j+1
        s=line[0:j]
        print("macro : "+s)
        #checking macro name is valid
        if(not(s.isidentifier())):
            print("Invalid macro name : "+s)
            return
        j=j+1
        #checking starting bracket
        if(line[j]!='('):
            print("Opening bracket missing in : "+line)
            return
        j=j+2
        # if no parameter then add none entry
        if(line[j]==')' and j==len(line)-1):
            parameter_name_table[s]=None
        elif(',' not in line):# if single parameters add it
            k=j
            while(line[k]!=')'):
                k+=1
            lent=line[j:k-1]
            entry=create_entry(lent,entry)
        else:#multiple parameters present
            print("need to check for multiple parameters")
            k=j
            # get each parameter, value and create entry
            while(k<len(line)):
                l=k
                
                while(line[l]!=',' and line[l]!=')' ):
                    l=l+1
                if(line[l]==')'):
                    lent=line[k:l-1]
                    entry=create_entry(lent,entry)
                    break  
                lent=line[k:l-1]
                entry=create_entry(lent,entry)
                k=l+2
                
               
        print("Entries are:")
        print(entry)
        parameter_name_table[s]=entry
        return
    
    
    end_time = time.clock()
    #input_time = sum(time_list)
    run_time = end_time - start_time
    fp.close()
