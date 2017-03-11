import time
import settings as st

#function to create entry in parameter list      
def create_entry(line,entry):
    
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
            return(entry)
        
        # getting parameter value
        v=line[k+2:len(line)]
        #print("value : "+v)
        
        #adding entry
        item={}
        item[p]=v
        entry.append(item)
        
    # if the parameter has value no value just add the parameter
    else:
        p=line[0:len(line)]
        if(not(p.isidentifier())):
            print("Invalid parameter name : "+p)
            return(entry)
        #print("parameter : "+p)
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
        entry=create_entry(lent,entry)
        
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
                entry=create_entry(lent,entry)
                break  
            lent=line[k:l-1]
            entry=create_entry(lent,entry)
            k=l+2
            
           
    #print("Entries are:")
    #print(entry)
    if(s in st.parameter_name_table):
        if(len(st.parameter_name_table[s])==len(entry)):
            print("Macro already defined : "+s)
            return '*'
        else:
            st.parameter_name_table[s]=[st.parameter_name_table[s],entry]
    else:
        st.parameter_name_table[s]=entry
    return(s)

# function to check for multi line macro definition
def multi_line_macro(lines,t,pq):
    k=pq
    pq=pq+1
    # creating parameter definition table
    mname=parameter(lines[pq])
    # check for any macro definition error
    if(mname is '*'):
        #print("Error in macro definition")
        return '*'
    pq=pq+1
    #if no error add macro in list
    while(lines[pq]!="$$"):
        pq=pq+1
    st.macro_name_table[mname]=None
    st.macro_def_table[mname]=[k,pq]
    return(pq)
