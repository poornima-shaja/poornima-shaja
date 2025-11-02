str="";    
for Row in range(0,7):    
    for Col in range(0,7):     
        if (Col == 1 or ((Row == 0 or Row == 3 or Row == 6) and (Col < 5 and Col > 1)) or (Col == 5 and (Row != 0 and Row != 3 and Row != 6))) :  
            str=str+"*"    
        else:      
            str=str+" "    
    str=str+"\n"    
print(str)

result_str="";    
for row in range(0,7):    
    for column in range(0,7):     
        if (column == 3 or (row == 0 and column > 0 and column <6)):  
            result_str=result_str+"*"    
        else:      
            result_str=result_str+" "    
    result_str=result_str+"\n"    
print(result_str)

str="";    
for Row in range(0,7):    
    for Col in range(0,7):     
        if (((Row == 0 or Row == 3 or Row == 6) and Col > 1 and Col < 5) or (Col == 1 and (Row == 1 or Row == 2 or Row == 6)) or (Col == 5 and (Row == 0 or Row == 4 or Row == 5))):  
            str=str+"*"    
        else:      
            str=str+" "    
    str=str+"\n"    
print(str)

