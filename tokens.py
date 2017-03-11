def create_tokens(q):
    
    j = 0
    r = q
    
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
    return r