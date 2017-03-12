# SYSTEMS PROGRAMMING LAB


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
                    
			      $elif		< expression / macro >
				          < expansion-statements-2>
                
			      $else		< expression / macro >
				          < expansion-statements-3>
                
			      $end
```

- ***expression*** :	expression to test
- ***macro***  :		to set statements by checking if a macro exists or not
 
Some sample macro examples depicting specific features

