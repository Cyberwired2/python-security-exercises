#String Exercises

 #Exercise 1:Password Strenght Checker
   .Use len() to check length
   .Use any() with generator   expressions:  
    any(c,isupper() for c in password) any(c.islower() for c in password)
    any(.isdigit() for c in password)
    any(notc.isalmn() for c in password)

  #Exercise 2: IP Address Validator

    Use str.split('.') to break into parts
    Check if you have exactly 4 parts
    Convert each part to int and check range 0-255
    Handle exceptions for non-numeric parts

    Exercise 3: URL Parser

    Look for :// to separate protocol
    Find the first / after protocol to separate domain and path
    Use str.split('?') to separate path and query parameters
    Parse query parameters by splitting on & and then =

#Number Exercises
 #Exercise: Network Address Calculator
 