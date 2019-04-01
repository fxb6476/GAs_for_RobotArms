#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 18:55:16 2019

@author: flef
"""

from GA import *

# Desired end effector location.
x = .5
y = .3
z = .3
fit = 0

# Initialize your population. I made mine 500.
test_pop = GA(500)

i = 0
while (fit < 50) and (i < 200):
    
    # Start by calculating the current fitness of the population.
    test_pop.calc_fitness(x,y,z)
    
    # Now that you know the most fit members of society.
    # You can go ahead and reproduce.
    test_pop.reproduce()
    
    # You now have a new population consisting of the old population,
    # and the new babies you just made.
    # Thus calculate the fitness of the new members of the society.
    test_pop.calc_fitness(x,y,z)
    
    # Now that you have new members, and old members, and the fitness of them,
    # you can start selecting only the most fit members.
    test_pop.selection()
    
    # Now that you have created a new stronger population it is time to add
    # a little diversity to the system through mutation.
    test_pop.mutate(.08)
    
    # Lastly I calculate the fitness one more time so that I can relay back
    # the most fit member to see if I can stop or not.
    test_pop.calc_fitness(x,y,z)
    
    # Adding the most fit members fitness to my termination variable.
    fit = test_pop.get_most_fit(x,y,z)[0]
    i = i+1
    print([i, fit])

# Saving the best population, and there fitness's to variables.
pop = test_pop.population
fits = test_pop.fitness

# Printing out the final results of our GA.
# The format is as follows:
#
#
#
# [fitness, theta1, theta2, theta3, px, py, pz]
#
print(test_pop.get_most_fit(x,y,z))