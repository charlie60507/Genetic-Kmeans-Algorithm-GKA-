import pandas as pd
import random
import math
import operator
import numpy as np
import lib.evaluate_fitness as eval_fitness

pd.options.mode.chained_assignment = None 
# random.seed(1)

class Mutation_Process:
	def __init__(self,Npop,Pm,sort_chromosome,data,count_fit_time):
		self.Npop = Npop
		self.Pm = Pm
		self.sort_chromosome = sort_chromosome
		self.data = data
		self.count_fit_time = count_fit_time

	def do_mutation(self,chromo_before_m,chromo_after_m,flag_mutation,fitness_list,i,_count_fit_time):
		Pm = self.Pm

		chromo_before_m = chromo_before_m[:-1]
		dice = list()
		chromosome = list()
		bit_flag = list()
		length = len(chromo_before_m)

		for j in range(0,length,+1):
			#print `j`+": "+ `chromo_after_c[j]`
			dice.append(float('%.2f'%  random.uniform(0.0,1.0)))	#dice.append(float('%.2f'%  random.uniform(0.0,1.0)))
			if dice[j] > Pm:
				chromosome.append(chromo_before_m[j])
				bit_flag.append(0)

			if dice[j] <= Pm:
				chromosome.append(float('%.2f'%  random.uniform(0.0,1.0)))	#c.append(float('%.2f'%  random.uniform(0.0,1.0)))
				bit_flag.append(1)

		check = sum(bit_flag)

		if check == 0:
			flag_mutation[i] = 0
			chromosome.append(fitness_list[i])
		else: 
			flag_mutation[i] = 1

			#---user define----
			evaluate = eval_fitness.Evaluate(chromo_before_m,self.data)
			chromosome,_count_fit_time = evaluate.cal_child_fit(chromosome,_count_fit_time)
			#------------------

		chromo_after_m.append(chromosome) 
		return chromo_after_m,_count_fit_time

	def mutation(self,chromo):
		fitness_list = list()
		chromo_after_mutation = list()
		flag_mutation = (np.zeros(self.Npop)).tolist()
		count_fit_time = self.count_fit_time

		for i in range(0,self.Npop,+1):		
			temp = chromo[i]
			fitness_list.append(temp[-1])

		for i in range(0,self.Npop,+1):
			if i == 0:	# Ibest doesn't need mutation
				chromo_after_mutation.append(chromo[0])
				flag_mutation[0] = 0
			else:
				chromo_after_mutation,count_fit_time = self.do_mutation(chromo[i],	chromo_after_mutation,flag_mutation,fitness_list,i,count_fit_time)

		chromo_after_mutation = self.sort_chromosome(chromo_after_mutation)
		return chromo_after_mutation,count_fit_time