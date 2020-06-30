#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 13:13:57 2020

@author: jannis
"""
import numpy as np
import seaborn as seb 
from random import randint
from math import pi, exp
import pandas as pd

class Rnd:
    def rnd(self,s,e):
        delta = e-s 
        r = randint(0,1e10)
        
        r = r/1e10 * delta + s 
        return r 
    
    def dist(self,s,e,f,alpha):
        y = self.rnd(s,e)
        p_y = f(y)
        
        x = self.rnd(0,alpha)
        
        if(x < p_y ):
            return y
        
        
    def dist_cum(self,s,e,f,N):
        ret = []
        
        delta = int(e-s)
        maximum = 0
        
        for n in range(delta):
            if(maximum < f(n+1)):
                maximum = f(n+1)
                
                
        print(maximum)  
        
        while(len(ret) < N):
            r = self.dist(s,e,f,maximum)
            if(r != None):
                ret.append(r)
            
        return ret 


class MonteCarlo:
    
    def integrate_1D(self,f,s,e,points):
        I = 0
        f_2 = 0 
        f_1_2 = 0 
        
        rnd = Rnd()
        for n in range(points):
            f_n = f(rnd.rnd(s, e))
            
            I += f_n
            
            f_2 += f_n ** 2 
            
        I /= points 
        f_1_2 = I**2
        
        S = (f_2/points - f_1_2)**0.5
        
        return(I,S)
    
    
            
            
        
        
        
    

'''  
T = 6e3
p = lambda x : 8 * pi * x**2 * 1/(exp(x/6e3)-1) 
e = 5e4

rnd = Rnd()

dist = rnd.dist_cum(0, e, p, 1e4)

seb.distplot(dist)

'''

points = [10,20,50,100,200,500,1000,2000,5000]
f_1 = lambda x : 1/(1+x**2) 
f_2 = lambda x : 1/(1+x**2) * 3/(4-2*x)
mc = MonteCarlo()
I1 = []
I2 = []
S1 = []
S2 = []
p4 = []
for p in points:

    i,s = mc.integrate_1D(f_1, 0, 1, p )
    I1.append(abs(i))
    S1.append(s)
    i,s = mc.integrate_1D(f_2, 0, 1, p )
    
    I2.append(abs(i))
    S2.append(s)
    p4.append(pi/4)


df = pd.DataFrame(data = {"I1":I1,"I2":I2,"Pi/4":p4}, index=points)
dfr = pd.DataFrame(data = {"S1":S1,"S2":S2}, index=points)
df.plot(logy=True)
dfr.plot(loglog=True)

