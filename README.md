# SYSTEM PROGRAMMING LAB
<br/>

## MACRO-Pre-Processor

DOCUMENTATION For SOPHOS **A Multi-Purpose Macro Pre-processor**

> Developed By :-

> Adarsh Kumar Jain (2015UCP1547)

> Arpit Kumawat(2015UCP1524)

> (Under guidance of Professor Arka Prokash Mazumdar)


## What are Macros ?
-	A macro (which stands for "macroinstruction") is  used to make certain tasks less repetitive by representing a complicated sequence of commands or statements into a shorthand notation.
-	Thus they allow a developer to re-use code and are for notational convenience.

Note that a macro is not the same as a function : functions require special instructions and computational overhead to safely pass arguments and return values.


## What is a Macro Pre-processor ?

-	Preprocessor is just a tool that allows us to use macros in a program and instructs the compiler to do required pre-processing before the actual compilation.
-	It replaces each macro invocation (call)  with the corresponding sequence of statements (expansion) .

 
## Why SOPHOS ?

- SOPHOS is a general purpose macro pre-processor in the sense that is not tied to or integrated with a particular language or piece of software.
- It is developed in python language and it is suitable for both low level language (like NASM) and high level languages (like Python and C).


### Features of SOPHOS :-

 *	Single line and multi line macro definitions
 *	Has its own single line and multi line comments for the convenience of programmer
 *	Allows nested macro definitions and calls
 *	Has conditional macro definitions ( if else clauses )
 *	Allows macro overloading 
 *	Is suitable for both high and low level languages

<br/>
# Syntax for Using macros in SOPHOS


## Macro definitions 


### Single Line Macro Definition : 
Syntax :

`$macd  <macro-name>  <expansion-statements>`

Or

`$macd  <macro-name> ( <parameters> )  <expansion-stmts>`

### Multi Line Macro Definition : 
Syntax :	  
```         
            $macd	. . .       
            <macro-name>   ( <parameters> )            
            <expansion-statements>            
            $$
```
***macro-name***  :  valid identifier name as in most of programming language

***parameters***  :  valid identifier name as in most of programming language, may take default values (like tax=10 )

***expansion-stmts***  :  any statements that user needs to replace using this macro

**Note : parameters are optional in both the cases**

## Including  Comments 

### Single Line Comments  :  	
* using the symbols **--**
* *Syntax* :		 `--  this is a single line comment`

### Multi Line Comments  :		
* using the symbols **<# ....  #>**
* *Syntax* :		
 ```
                    <#   this is
                         multi line
                         comment		#>
```

## Conditional  Macros

Syntax :		
```
            	$if   < expression / macro >
                  	$if   < expression / macro >
                        	$if   < expression / macro >
                            		< expansion-statements >
                            		< expansion-statements >
                       		 $elif
                            		< expansion-statements >
                            		< expansion-statements >
                         	 $end                 
                  	$else
                      		< expansion-statements >
                      		< expansion-statements >
                  	$end
               	
				$elif    < expression / macro >
					< expansion-statements >
                
	    		$else    < expression / macro >
					< expansion-statements >
                
	    		$end
```

- ***expression*** :	expression to test
- ***macro***  :		to set statements by checking if a macro exists or not
 
<br/>
# Some sample macro examples depicting specific features
<br/>
## Single line macro :

### Example  for Python
```
$macd   A 10
$macd  B(a) print(“The value of parameter is “ + a)

print(“The two defined macros will be called here “)
B(20)
print(“Macro A has value “+A)
```

### Example  for  C
```
#include<stdio.h>

$macd   MAX(x=0,y) x>y?x:y;
$macd  hello printf(“lets greet our user !! Hello user . “); 

void main()
{
	hello
	int Maximum=MAX(10,20)
}
```

### Example  for  NASM
```
$macd    stmfora  db "a=%d", 10, 0 

SECTION .data
a: dd 6
stm: stmfora

SECTION .text
extern printf
global main

main:
	push ebp
	mov ebp,esp
	push dword [a]
	push stm
	call printf
	add esp,8
	mov esp, ebp
	pop ebp
	ret
```
<br/>
## Multi Line Macro  :

### Example  for Python
```
$macd ...
	sum1(a,b,c=5)
	print(“sum is”)
	x=a + b + c
	print(x)
$$

print(“Program to calculate sum of three numbers “ )
sum1(10 , 27 )
```

### Example  for  C
```
#include<stdio.h>

$macd ...
	sum(c, k, a=helo, b=newone)
	printf("The sum is ");
	int x = a+b+c+k;
$$

void main()	
{
	sum(10,20,30)
	printf("%d", x);	
}
```

### Example  for  NASM
```
$macd  ... 
	stmfora( )
	a: dd 6
	stm : db "a=%d", 10, 0 
$$

SECTION .data
stmfora

SECTION .text
extern printf
global main

main:
	push ebp
	mov ebp,esp
	push dword [a]
	push stm
	call printf
	add esp,8
	mov esp, ebp
	pop ebp
ret
```

</br>
## Single  Line  And  Multi  Line  Comments  :

### Example  for Python
```
<#  this example uses 
	A multi line 
	comment	
	#>
	
$macd  A 10

print(“Macro  has value “+A)
```

### Example for C
```
#include<stdio.h>

--Using single line macro to comment some definitions
 --$macd F 60
 
$macd H 80
$macd MIN 10

Void main()
{
	printf(“macro h is %d“,H );
	printf(“macro min is %d“,MIN );
}
```

### Example  for  NASM
```
$macd  ... 
stmt(  )
<#	 a: dd 6  
commented so not replaced   #>
stm : db "a=%d", 10, 0 
$$

SECTION .data
stmt(  )
SECTION .text
extern printf
global main

main:
	push ebp
	mov ebp,esp
	push stm
	call printf
	add esp,8
	mov esp, ebp
	pop ebp
	ret
```

<br/>
## Conditional macro :

### Example  For Python
```
$macd e 50
--$macd d 60

$if d			
print(“d  is defined “)
print(“I am in d“)

$elif e
print(“e  is defined “)
print(“I am in e“)

$else
Print(“Both d and e are not defined “)	
print(“I am not in d and e“)

$end
```

### Example For C 
```
#include<stdio.h>
$macd   g 10
$macd   h 200
$macd   e 30
$macd   d 0
Void main()
{
	$if d
		$if h
			Printf(“h and d are defined");
		$else
			Printf(“d is defined");
		$end
	$elif e
		Printf(“e is defined	);
	$else
		Printf(“d and e are not defined “);
	$end
}
```


### Example For NASM
```
$macd   g test

SECTION .data
$if g
	Greet:  db “Hello !!”,10,0
$else
	Greet:  db  “No greeting”,10,0
$end

SECTION .text
extern printf
global main

main:
	push ebp
	mov ebp,esp
	push stm
	call printf
	add esp,4
	mov esp, ebp
	pop ebp
ret
```

<br/>
## Macro Overloading  :
*This macro preprocessor allows macro overloading that is same name macros can be created if they have different number of parameters. Thus same name macro can have multiple definitions.*

### Example  for macro overloading  ( Example For C )
```
<# 	Here same macro ‘sum’ is defined multiple times with different number of parameters		 #>

$macd ...
	sum(a,,b,,c=1,d=2,e=3)
	printf(“This sum has 5 parameters”);
$$

$macd ...
	sum( )
	printf(“This sum has no parameters”);
$$

$macd ...
	sum(a=helo,b=newone)
	printf(“This sum has 2 parameters”);
$$

$macd ...
	sum(a,b,c)
	printf(“This sum has 3 parameters”);
$$

sum(2,4,7)
sum( ,  )
sum(5, 4, , , )
sum( )
```
<br/>
## Nested Macro Definition And Calls

### Calling a macro inside definition of another (Example for python)

```
$macd  SUM(a,b,c) sum3( b, c) print(a)

$macd ...
sum3( x , y )
total=x+y
print(total)
$$

SUM(5,10,20)
```

### Defining a macro inside another macro ( Example for C )
```
$macd ...
	sum(a,b,c=5)
	printf(“the sum is “);
	
	$macd ...
		sum12(a,b,c,d)	
		printf(“this is a nested macro definition “);
		int x=a + b + c+d;
	$$
	
	int x=a+b+c;
$$

sum12(5,10,2,6)
```
