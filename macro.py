import time
import settings as st
from store_if import store_if
from replace_if import replace_if
from multi_line_macro import multi_line_macro

def single_line_macro(t, line):
    st.macro_name_table[p[1]] = p[2]
    st.macro_def_table[p[1]] = [line, line]

#starting program
if __name__ == '__main__':
        
    start_time = time.clock()
    
    #input file
    fo = open("prog1.txt","r")
    
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
        #elif( p[0] == "$macd" and p[1] == "..."):
            #x=lines.index(t)
            #multi_line_macro(lines,t,x)
        
        #conditional macro
        #elif( p[0] == "$if"):
        #    conditional_macro(t, pq)
        
        #increase line number
        pq=pq+1

    pq=1

    #replcing macros in input file
    for t in lines:
        
        #create tokens
        p = t.split()
        
        #if a empty line is encountered
        if( t == "" ):
            pq=pq+1
            continue        
        
        if(p[0] == "$if"):
            struct = []
            struct.append({'$if':[pq-1]})
            store_if(pq-1, lines, struct)
            print(struct)
            replace_if(pq-1, lines, prnt, struct)
            break
        pq += 1
        
    multi_line_macro(lines,lines[2],2)
    multi_line_macro(lines,lines[8],8)
    multi_line_macro(lines,lines[16],16)
    multi_line_macro(lines,lines[20],20)
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
