import pandas as pd
import random
import math
import operator
import numpy as np
import lib.evaluate_fitness as eval_fitness

pd.options.mode.chained_assignment = None 
# random.seed(0)

class Crossover_Process:
	def __init__(self,Npop,Pc,sort_chromosome,data,count_fit_time):
		self.Npop = Npop
		self.Pc = Pc
		self.sort_chromosome = sort_chromosome
		self.data = data
		self.count_fit_time = count_fit_time

	def do_crossover(self,chromo,i,index,_count_fit_time):

		listA = []
		length = len(chromo[0])
		cut = random.randint(1,length-1)
		parent1 = chromo[index[i]]
		parent2 = chromo[index[i+1]]
		tmp1 = parent1[:-1]
		tmp2 = parent2[:-1]
		child1 = tmp1[0:cut] + tmp2[cut:length]
		child2 = tmp1[cut:length] + tmp2[0:cut]

		# ----user_define----
		evaluate = eval_fitness.Evaluate(chromo,self.data)
		child1,_count_fit_time = evaluate.cal_child_fit(child1,_count_fit_time)
		child2,_count_fit_time = evaluate.cal_child_fit(child2,_count_fit_time)
		# -------------------

		listA.append(parent1)
		listA.append(parent2)
		listA.append(child1)
		listA.append(child2)
		listA = sorted(listA, reverse=True,key=lambda elem: elem[len(parent1)-1]) 	
		chromo[index[i]] = listA[0]
		chromo[index[i+1]] = listA[1]

		return chromo, _count_fit_time

	def crossover(self,chromo):
		Npop = self.Npop
		Pc = self.Pc 
		_count_fit_time = self.count_fit_time

		index = random.sample(range(0, Npop-1), int(Pc*Npop))	# random (Pc*Npop) number
		for i in range(0,int(Pc*Npop)/2,+1):	# do how many time
			chromo,_count_fit_time = self.do_crossover(chromo,i,index,_count_fit_time)

		chromo = self.sort_chromosome(chromo)
		
		return chromo,_count_fit_time
