#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 14:52:14 2020

@author: jannis
"""

from math import exp 
import numpy as np 
import matplotlib.pyplot as plt 
import gif
import seaborn




class Advection_EQ:
    
    U = [[]]
    dim_x = 0
    dt = 0
    dx = 0
    v = 1
    
    def __init__(self,f,dim_x,dt):
        self.f = f 
        self.dx = 1/(dim_x -1)
        self.dt = dt
        self.dim_x = dim_x
        self.alpha = self.v * self.dt / self.dx
        
        for j in range(dim_x):
            self.U[0].append(f(j * self.dx))
        
        
    
    def get(self,n,x):
        return self.U[n][x]
     
    def boundarries(self,u):
        u[0] = u[-1]
        u.append(u[1])
        return u 
        

    
    def run(self,t_steps,U):
        
        reset  = self.U[0].copy()
        self.U = []
        self.U.append(reset)
        
        for n in range(t_steps):
            new_time = [None]
            
            for j in range(self.dim_x-1):
                if(j == 0):
                    continue
                
                u_new = U(1+n,j)

                new_time.append(u_new)                
            
            new_time = self.boundarries(new_time)
            
            self.U.append(new_time)
            
        return self.U
         
    
    def FTCS(self,n,j):
        U = self.get 
        n -= 1
        u_new = U(n,j) - self.alpha / 2 * ( U(n,j+1) - U(n,j-1))
        return u_new 
    
    def LF(self,n,j):
        U = self.get 
        n -= 1
        u_new = 0.5 * ( U(n,j+1) + U(n,j-1)) - self.alpha /2 * ( U(n,j+1) - U(n,j-1))
        return u_new
    
    def Leepfrog(self,n,j):
        U = self.get 
        n -= 1
        
        if(n-1 < 0):
            return U(n,j)
        
        
        u_new = U(n-1,j) - self.alpha * (U(n,j+1) - U(n,j-1))
        return u_new
    
    def LW(self,n,j):
        U = self.get 
        n -= 1
        u_new = U(n,j) - self.alpha / 2 * (U(n,j+1) - U(n,j-1)) + self.alpha **2 / 2 *(U(n,j+1) - 2* U(n,j) + U(n,j-1) )
        return u_new
      
    
        
        

class Wave_EQ:
    
    d = [[]]
    r = [[]]
    U = [[]]
    dim_x = 0
    dt = 0
    dx = 0
    v = 1
    
    # init vars for t = 0 
    def __init__(self,f,dim_x,dt):
        self.dx = 1/(dim_x -1)
        self.dt = dt
        self.dim_x = dim_x
        self.alpha = self.v * self.dt / self.dx
        
        for j in range(dim_x):
            self.U[0].append(f(j * self.dx))
            self.d[0].append(0)
            
        for j in range(dim_x):
            if(j == 0 or j == dim_x-1):
                self.r[0].append(0)
            else:
                temp = (self.U[0][j+1] - self.U[0][j-1])/( 2* self.dx)
                self.r[0].append(temp)
        
    
    def get_U(self,n,x):
        return self.U[n][x]
    
    def get_d(self,n,x):
        return self.d[n][x]
    
    def get_r(self,n,x):
        return self.r[n][x]
    
    # use periodic boundarries 
    def boundarries(self,u):
        u[0] = u[-1]
        u.append(u[1])
        return u 
        

    # main driver 
    def run(self,t_steps,sceam):
        
        reset  = self.U[0].copy()
        self.U = []
        self.U.append(reset)
        
        #loop over all times and locations 
        for n in range(t_steps):
            U_new = [None]
            r_new = [None]
            d_new = [None]
            
            #get r an delta for time step n
            for j in range(self.dim_x-1):
                if(j == 0):
                    continue
                
                if(sceam("r",(n+1,j)) == None):
                    break
                
                r_new.append(sceam("r",(n+1,j)))
                d_new.append(sceam("d",(n+1,j)))
            
            #applie boundarry condition 
            if(len(r_new) > 2):
                r_new = self.boundarries(r_new)
                d_new = self.boundarries(d_new)
            
            #append new data 
            self.r.append(r_new)
            self.d.append(d_new)
            
            # get U for time step n 
            for j in range(self.dim_x-1):
                if(j == 0):
                    continue 
                
                U_new.append(sceam("U",(1+n,j)))

                  
            
            U_new = self.boundarries(U_new)
            
            self.U.append(U_new)
            
        return self.U
         
# callables for different sceams     
    def FTCS(self,x,loc):
        a,b = loc
        U = self.get_U
        d = self.get_d
        r = self.get_r
        
        def U_new(self,n,j):
            
            n -= 1
            new = U(n,j) + self.dt * d(n,j)
            return new 
        
        def r_new(self,n,j):
            
            n -= 1
            new = r(n,j) + self.alpha / 2 *( d(n,j+1) - d(n,j-1))
            return new 
        
        def d_new(self,n,j):
                
            n -= 1
            new = d(n,j) + self.alpha / 2 *  (r(n,j+1) - r(n,j-1))
            return new 
            
        if(x == "r"):
            return r_new(self,a,b)
        elif(x == "d"):
            return d_new(self,a,b)
        else:
            return U_new(self,a,b)
         
            
        
    def LF(self,x,loc):
        a,b = loc
        U = self.get_U
        d = self.get_d
        r = self.get_r
        
        def U_new(self,n,j):
            
            n -= 1
            new = 1 * (U(n,j) + self.dt / 2 * ( d(n+1,j) + d(n,j)))
            return new 
        
        def r_new(self,n,j):
            
            n -= 1
            new = 0.5 * ( r(n,j+1) + r(n,j-1) ) + self.alpha / 2 *(d(n,j+1) - d(n,j-1) )
            return new 
        
        def d_new(self,n,j):
                
            n -= 1
            new = 0.5 * ( d(n,j+1) + d(n,j-1) ) + self.alpha / 2 * ( r(n,j+1) - r(n,j-1) )
            return new 
        
        if(x == "r"):
            return r_new(self,a,b)
        elif(x == "d"):
            return d_new(self,a,b)
        else:
            return U_new(self,a,b)




    def Leepfrog(self,x,loc):
        a,b = loc
        U = self.get_U
        
        
        def U_new(self,n,j):
            a = self.alpha 
            n -= 1
            
            if(n-1 < 0):
                return U(n,j)
            
            new = a**2 * U(n,j+1) + 2 * U(n,j) * (1 - a**2) + a**2 * U(n,j-1) - U(n-1,j)
            return new 
        

        def r_new(self,n,j):
            
            
            return None 
        
        def d_new(self,n,j):        
          
            return None 
        
        if(x == "r"):
            return r_new(self,a,b)
        elif(x == "d"):
            return d_new(self,a,b)
        else:
            return U_new(self,a,b) 
       
        
    
    def LW(self,x,loc):
        a,b = loc
        U = self.get_U
        d = self.get_d
        r = self.get_r
        
        def U_new(self,n,j):
            
            n -= 1
            new = U(n,j) + self.dt / 2 * ( d(n+1,j) + d(n,j))
            return new 
        
        def r_new(self,n,j):
            
            n -= 1
            new = r(n,j) + self.alpha * ( 0.5 * ( d(n,j+1) - d(n,j-1) ) + self.alpha / 2 * ( r(n,j+1) - 2* r(n,j) + r(n,j-1)))
            return new 
        
        def d_new(self,n,j):
                
            n -= 1
            new = d(n,j) + self.alpha * ( 0.5 * ( r(n,j+1) - r(n,j-1) ) + self.alpha / 2 * ( d(n,j+1) - 2* d(n,j) + d(n,j-1)))
            return new 

        if(x == "r"):
            return r_new(self,a,b)
        elif(x == "d"):
            return d_new(self,a,b)
        else:
            return U_new(self,a,b)







# plotting 
@gif.frame
def plot(data,i=None):
    if(i != None):
        plt.plot(i,label="analytic") 
    plt.plot(data,label="numeric")
    
    #plt.ylim((0, 1))
       
# def staring function            
x_0 = 0.5
s   = 0.1
        
f = lambda x: exp(-(x-x_0)**2/s**2)  
f_t = lambda x,t: (exp(-(x-t-x_0)**2/s**2)  + exp(-(x+t-x_0)**2/s**2)) /2


 

dim_x = 200


dx = 1/(dim_x -1)
dt = dx 
a = Advection_EQ(f,dim_x,dt)

# run integration 
# to change sceam edit second parameter
steps = 150
data  = a.run(steps,a.FTCS)

'''
#create gif 
frames = []

data_t = []

for t in range(steps + 1):
    new = []
    for x in range(dim_x):

        new.append(f_t(x*dx,t*dt))
    data_t.append(new)
    


for i,d in enumerate(data):
    frame = plot(d)
    #frame = plot(d,data_t[i])
    frames.append(frame)

#gif.save needs existing file     
gif.save(frames, "/home/jannis/vnump/gifs/LW_unstable.gif", duration=10)
'''