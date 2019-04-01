#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 19:37:59 2019

@author: flef
"""
import random as rand
import numpy as np
import math as mt

class GA:
    
    def __init__(self, pop_size):
        
        self.pop_size = pop_size
        self.population = np.zeros((pop_size,30)) #n rows 30 columns
        self.fitness = np.zeros((pop_size))     #n rows 1 column
        
        for i in range(pop_size):
            #Randomly setting initial values of population
            num1 = rand.randint(0,1023) #Numbers are 0b0011 1111 1111
            num2 = rand.randint(0,1023)
            num3 = rand.randint(0,1023)
            
            row = '{0:010b}'.format(num1) + '{0:010b}'.format(num2) + '{0:010b}'.format(num3)
            self.population[i] = list(row)
            
        self.population = self.population.astype(int)
            
    def calc_fitness(self, x, y, z):
        
        for i in range(self.pop_size):
            num1 = int(''.join( self.population[i, 0:10].astype(str) ),2) * (360/1023)
            num2 = int(''.join( self.population[i, 10:20].astype(str) ),2) * (360/1023)
            num3 = int(''.join( self.population[i, 20:30].astype(str) ),2) * (360/1023)
            
            # Fitness based on Euclidean distance from desired point...
            px = mt.cos(mt.radians(num1)) * (mt.cos(mt.radians(num2)) + mt.cos( mt.radians(num2) + mt.radians(num3) ))
            py = mt.sin(mt.radians(num1)) * (mt.cos(mt.radians(num2)) + mt.cos( mt.radians(num2) + mt.radians(num3) ))
            pz = 1 + mt.sin(mt.radians(num2)) + mt.sin(mt.radians(num2) + mt.radians(num3))
                        
            fit = 1.0 / mt.sqrt( (px-x)**2 + (py-y)**2 + (pz-z)**2 )
            
            self.fitness[i] = fit
        
        #Make fitness array add up to 1
        sum_f = float(np.sum(self.fitness))

        for i in range(self.pop_size):
            self.fitness[i] = self.fitness[i]/sum_f
    
    def reproduce(self):
        
        new_pop = np.zeros(( int(self.pop_size) ,30))
        
        for i in range( int(self.pop_size/2) ):
            choice = np.random.choice(list(range(self.pop_size)), 2, p=np.transpose(self.fitness).tolist())
            babys = self.two_point_cross(choice);
            new_pop[i] = babys[0]
            new_pop[i+1] = babys[1]
        
        self.population = np.append(self.population, new_pop, axis = 0)
        self.population = self.population.astype(int)
        self.pop_size = self.population[:,1].size
        self.fitness = np.zeros((self.pop_size))     #n rows 1 column

        
    def two_point_cross(self, parents):
        par1 = self.population[parents[0]].tolist()
        par2 = self.population[parents[1]].tolist()
        
        child1 = par1[0:5] + par2[5:10] + par1[10:15] + par2[15:20] + par1[20:25] + par2[25:30]
        child2 = par2[0:5] + par1[5:10] + par2[10:15] + par1[15:20] + par2[20:25] + par1[25:30]
        
        return [child1, child2]
    
    def selection(self):
        
        new_pop = np.zeros(( int(self.pop_size/2), 30))
        
        winners = self.fitness.argsort()[-int(self.pop_size/2):][::-1]
        
        for i in range( int(self.pop_size/2) ):
            new_pop[i] = self.population[winners[i]]
        
        self.population = np.zeros(( int(self.pop_size/2), 30))
        self.population = new_pop
        self.population = self.population.astype(int)
        self.fitness = np.zeros(( int(self.pop_size/2)))
        self.pop_size = self.population[:,1].size
    
    def mutate(self, mu_val):
        
        for i in range(self.pop_size):
            flip = np.random.choice([0, 1], 30, p=[1-mu_val, mu_val])
            self.population[i] = np.logical_xor(self.population[i], flip).astype(int)
        
    def get_most_fit(self,x,y,z):
        
        winner = self.fitness.argsort()[-1:][::-1][0]
        
        num1 = int(''.join( self.population[winner, 0:10].astype(str) ),2) * (360/1023)
        num2 = int(''.join( self.population[winner, 10:20].astype(str) ),2) * (360/1023)
        num3 = int(''.join( self.population[winner, 20:30].astype(str) ),2) * (360/1023)
        
        # Fitness based on Euclidean distance from desired point...
        px = mt.cos(mt.radians(num1)) * (mt.cos(mt.radians(num2)) + mt.cos( mt.radians(num2) + mt.radians(num3) ))
        py = mt.sin(mt.radians(num1)) * (mt.cos(mt.radians(num2)) + mt.cos( mt.radians(num2) + mt.radians(num3) ))
        pz = 1 + mt.sin(mt.radians(num2)) + mt.sin(mt.radians(num2) + mt.radians(num3))
        
        fit = 1.0 / mt.sqrt( (px-x)**2 + (py-y)**2 + (pz-z)**2 )
        
        return [fit, num1, num2, num3, px, py, pz]
    