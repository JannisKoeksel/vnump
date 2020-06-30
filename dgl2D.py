#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 17:20:12 2020

@author: jannis
"""
from math import exp 
import numpy as np 
import matplotlib.pyplot as plt 
import gif
import seaborn
from mpl_toolkits.mplot3d import Axes3D

class Data:
    
    U = []
    r = []
    l = []
    s = []
    
    dim = 0
   
    dr = 0
    dt = 0
    
    v = 1
    
    def __init__(self,f,dim,dr):
        self.dim = dim 
        self.dr = dr
        self.dt = dr / ( 4 * self.v)
        self.alpha = self.v * self.dt / self.dr
        
        self.add_U(self.loop_val(f))
        
        
        
    def loop(self,call,t = None):
         
        mat = []
        
        for x in range(self.dim):
            row = []
            for y in range(self.dim):
                if(t != None):
                    val = call(self,t,x,y)
                else:
                    val = call(self,x,y)
                row.append(val)
            mat.append(row)
        
        return mat
    
    
    def loop_val(self,call,t = None):
         
        mat = []
        
        for x in range(self.dim):
            row = []
            for y in range(self.dim):
                x_c = x * self.dr
                y_c = y * self.dr
                
                if(t != None):
                    t *= self.dt
                    val = call(t,x_c,y_c)
                else:
                    val = call(x_c,y_c)
                row.append(val)
            mat.append(row)
        
        return mat
    
    def add_U(self,mat):
        mat = self.periodic(mat)
        
        self.U.append(mat)
        
    def add_r(self,mat):
        mat = self.periodic(mat)
        
        self.r.append(mat)
        
    def add_l(self,mat):
        mat = self.periodic(mat)
        
        self.l.append(mat)
        
    def add_s(self,mat):
        mat = self.periodic(mat)
        
        self.s.append(mat)
        
    def periodic(self,mat):
        for x in mat:
            x.insert(0,x[-1])
            x.append(x[1])
        mat.insert(0,mat[-1])
        mat.append(mat[1])
        return mat

    def get_U(self,n,i,j):
        return self.U[n][i][j]
    
    def get_r(self,n,i,j):
        return self.r[n][i][j]
    
    def get_l(self,n,i,j):
        return self.l[n][i][j]
    
    def get_s(self,n,i,j):
        return self.s[n][i][j]
    
    
    
    
class Driver:
    
    def __init__(self,f,dim,dr):
        self.data = Data(f,dim,dr)
        self.dim = dim 
        self.dr = dr
        self.f = f
        
     
        
    
    def reset(self):
        self.data = Data(self.f,self.dim,self.dr)
     
    def Leepfrog(self,steps):
        
        def U_new(self,n,i,j):
            U = self.get_U
            n -= 1
            if(n-1 < 0):
                return U(n,i,j)
            new = self.alpha**2 *( U(n,i+1,j) + U(n,i-1,j) + U(n,i,j+1) + U(n,i,j-1) ) + 2 * U(n,i,j)* (1-self.alpha**2) - U(n-1,i,j)
            return new 
        
        for t in range(steps):
            mat  = self.data.loop(U_new,t)
            self.data.add_U(mat)
    
    
        return self.data.U

x_0 = y_0 = 0.5
s = 0.1

f = lambda x,y:  y*x #exp(- ((x-x_0)**2 + (y-y_0)**2)  /  s**2)  

dim = 5 
steps = 100

dr = 1/(dim-1)
driver = Driver(f,dim,dr)

fig = plt.figure()
ax = fig.gca(projection='3d')


data = driver.Leepfrog(steps)



X = [x for x in range(dim+2)]
Y = X
X, Y = np.meshgrid(X, Y)


