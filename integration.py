#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 19:46:34 2020

@author: jannis
"""
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from math import pi,cos,sin


class Integration:
    
    
    def trapez(self,f,interval,N=None):
        x_s ,x_e = interval
        
        i=1
        
        I = [f(x_s)+f(x_e)]
        X = [x_s ,x_e]
        while(True):
         
            X_new = []
            for j in range(1,len(X)):
                d = (X[j] - X[j-1])/2
                
                X_new.append(X[j]-d)
                
            X.extend(X_new)
            X.sort()
            
            integral= 0 
            
            for x in X_new:
                integral+=f(x)
                
            m =   (X[1]-X[0])
            
            if(m<0):
                m *= -1
            integral *= m
            
            
            integral += 0.5 * I[i-1]
            
            I.append(integral)
            
            
            
            i+=1
            
            if(N != None):
                if(i ==  N):
                    print("points:",len(X))
                    return I[-1]
            
            else:return "No N specified"
                  
    def simpsons(self,f,interval,N):
        
        x_s ,x_e = interval
        h = (x_e -x_s)/(N-1)
        
        I = 0
        itera = []
        for i in range(N):
            
            if(i == 0 or i==N-1):
                I += 1/3 * f(x_s + i*h)
            elif(i%2==1):
                I += 4/3 * f(x_s + i*h)
            else:
                I += 2/3 * f(x_s + i*h)
            
            itera.append(I)
                
            
        
        I *= h
        
        return I
    
    def open_intervall(self,interval,N):
        x_s ,x_e = interval
        step = (x_e -x_s)/(N-1)
        x_e -= step
        x_s += step
        
        return (x_s ,x_e)
        
    def of1(self,f,interval,N):
        x_s ,x_e = interval
        h = (x_e -x_s)/(N-1)
        
        I = 0
        for i in range(N):
            if(i == 0 or i==N-1):
                I += 3/2 * f(x_s + i*h)
           
            else:
                I +=  f(x_s + i*h)
        
        I *= h
        return I 
        
    def of2(self,f,interval,N):
        x_s ,x_e = interval
        h = (x_e -x_s)/(N-1)
        
        I = 0
        for i in range(N):
            if(i == 0 or i==N-1):
                I += 27/12 * f(x_s + i*h)
            elif(i == N-2 or i == 1):
                I += 0 
            elif(i == N-3 or i == 2):
                I += 13/12 * f(x_s + i*h)
            
            elif(i%2==1):
                I += 4/3 * f(x_s + i*h)
            else:
                I += 2/3* f(x_s + i*h)
        
        I *= h  
        return I 

def N_rec(N):
    if(N == 2):
        return 3
    else:
        return N_rec(N-1) + N_rec(N-1) -1    

c = Integration()
N = 2000

interval = c.open_intervall((0,1) , N)

y = lambda x : (x-x**2)**-0.5

R1 = []
R2 = []
N_val = []
for n in range(100,N,2):
    
    R1.append(abs(c.of1(y, interval , n ) ))
    R2.append(abs(c.of2(y, interval , n ) ))
    N_val.append(n)

df = pd.DataFrame({"i) ":R1,"ii) ":R2},index=N_val)


'''
m = 2
n = 4
N= 6
f = lambda x : (sin(x))**(2*m-1) * (cos(x))**(2*n-1)

t = []
s = []
n_p = []

for a in range(2,N):
    


    interval = (0,pi/2)
    trap = c.trapez(f,interval,a)
    t.append(abs(trap-0.025))
    b = N_rec(a)
    n_p.append(b)
    sim = c.simpsons(f,interval,b)
    s.append(abs(sim-0.025))


#df = pd.DataFrame({"Trapez":t},index=n_p)
df = pd.DataFrame({"R Simpsons":s,"R Trapez":t},index=n_p)
df.plot()
'''