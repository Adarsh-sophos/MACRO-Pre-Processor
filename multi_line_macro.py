import time
import settings as st


#function to create entry in parameter list      
def create_entry(line,entry,pos_para,key_para):
    
    print(line)
    k=0
    # check if the parameter has value
    if('=' in line):
        # getting parameter name
        while(line[k]!='='):
            k+=1
            
        p=line[0:k-1]
        #print("parameter : "+p)
        
        # checking parameter name is valid
        if(not(p.isidentifier())):
            print("Invalid parameter name : "+p)
            return(entry,pos_para,key-para)
        
        # getting parameter value
        v=line[k+2:len(line)]
        #print("value : "+v)
        
        #adding entry
        item={}
        item[p]=v
        entry.append(item)
        key_para+=1
        
    # if the parameter has no value just add the parameter
    else:
        p=line[0:len(line)]
        if(not(p.isidentifier())):
            print("Invalid parameter name : "+p)
            return(entry,pos_para,key_para)
        #print("parameter : "+p)
        item={}
        item[p]=None
        entry.append(item)
        pos_para+=1
        
    return(entry,pos_para,key_para)



#function to check for parameters in each macro
def parameter(line):
    
    entry=[]
    j=0
    pos_para=0
    key_para=0
    #checking for ending bracket
    if(line[-1]!=')'):
        print("Ending bracket missing in : "+line)
        return '*'
    
    # getting macro name
    while(line[j]!=' '):
        j=j+1
    s=line[0:j]
    #print("macro : "+s)
    
    #checking macro name is valid
    if(not(s.isidentifier())):
        print("Invalid macro name : "+s)
        return '*'
    j=j+1
    
    #checking starting bracket
    if(line[j]!='('):
        print("Opening bracket missing in : "+line)
        return '*'
    j=j+2
    
    # if no parameter then add none entry
    if(line[j]==')' and j==len(line)-1):
        if(s in st.parameter_name_table):
            if(st.parameter_name_table[s]== None):
                print("Macro already defined")
                return '*'
        st.parameter_name_table[s]=None
        
    # if single parameters add it
    elif(',' not in line):
        k=j
        while(line[k]!=')'):
            k+=1
        lent=line[j:k-1]
        ret=create_entry(lent,entry,pos_para,key_para)
        entry=ret[0]
        pos_para=ret[1]
        key_para=ret[2]
        
    #multiple parameters present
    else:
        #print("need to check for multiple parameters")
        k=j
        
        # get each parameter, value and create entry
        while(k<len(line)):
            l=k
            
            while(line[l]!=',' and line[l]!=')' ):
                l=l+1
            if(line[l]==')'):
                lent=line[k:l-1]
                ret=create_entry(lent,entry,pos_para,key_para)
                entry=ret[0]
                pos_para=ret[1]
                key_para=ret[2]
                break  
            lent=line[k:l-1]
            ret=create_entry(lent,entry,pos_para,key_para)
            entry=ret[0]
            pos_para=ret[1]
            key_para=ret[2]
            
            k=l+2
    
    #print("Entries are:")
    #print(entry)
    if(s in st.parameter_name_table):
        if(len(st.parameter_name_table[s])==len(entry)):
            print("Macro already defined : "+s)
            return '*'
        else:
            st.parameter_name_table[s].append(entry)
    else:
        st.parameter_name_table[s]=[entry]
    return(s,[pos_para,key_para])



# function to check and create single line macro
def single_line_macro(t,pq, prnt):
    p=t.split()
    
    # creating parameter definition table
    
    # macro without parameter
    if(p[2]!='('):
        mname=p[1]
        if(mname in st.macro_name_table):
            printf("Macro already defined : "+mname)
        else:
            st.macro_name_table[mname] = [[1],[0,0]]
            st.macro_def_table[mname] = [[pq]]
            st.parameter_name_table[mname] = prnt[pq][prnt[pq].index(p[2]):-1]
            
    # macro with parameter        
    else:
        s_i = t.index(p[1])
        e_i = t.index(")", s_i+1)
        tnew=t[s_i:e_i+1]
        
        # creating parameter definition table
        #print(tnew)
        mname=parameter(tnew)
        
        # check for any macro definition error
        if(mname[0] is '*'):
            
            #print("Error in macro definition")
            return '*'
        
        #if no error add macro in list
        if(mname[0] in st.macro_name_table):
            st.macro_name_table[mname[0]][0][0]=st.macro_name_table[mname[0]][0][0]+1
            st.macro_name_table[mname[0]].append(mname[1])
            st.macro_def_table[mname[0]].append([pq])
        else:
            st.macro_name_table[mname[0]]=[[1],mname[1]]
            st.macro_def_table[mname[0]]=[[pq]]
    return(pq)



# function to check and create multi line macro definition
def multi_line_macro(lines,t,pq):
    
    k=pq
    pq=pq+1
    
    # creating parameter definition table
    mname=parameter(lines[pq])
    
    # check for any macro definition error
    if(mname[0] is '*'):
        
        #print("Error in macro definition")
        return '*'
    pq=pq+1
    abc=0
    #if no error add macro in list
    while(abc>=0):
    	if(lines[pq]==""):
    		pass
    	elif(lines[pq].split()[0]=="$macd"):
    		abc+=1
    	elif(lines[pq].split()[0]=="$$"):
    		abc-=1
    	pq+=1
    pq-=1  
    if(mname[0] in st.macro_name_table):
        st.macro_name_table[mname[0]][0][0]=st.macro_name_table[mname[0]][0][0]+1
        st.macro_name_table[mname[0]].append(mname[1])
        st.macro_def_table[mname[0]].append([k,pq])
    else:
        st.macro_name_table[mname[0]]=[[1],mname[1]]
        st.macro_def_table[mname[0]]=[[k,pq]]
    return(pq)

