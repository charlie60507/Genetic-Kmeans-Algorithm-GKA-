import pandas as pd
import random
import math
import operator
import numpy as np
import lib.GA_selection as Selection
import lib.GA_crossover as Crossover
import lib.GA_mutation as Mutation

pd.options.mode.chained_assignment = None 
random.seed(1)

class Genetic_Algo:
	def __init__(self, Npop, Ps, Pm, Pc, budget, data, Generation_count):
		self.Npop = Npop
		self.Ps = Ps
		self.Pm = Pm
		self.Pc = Pc
		self.budget = budget
		self.data = data
		self.Generation_count = Generation_count

	def sort_chromosome(self,chromo_unsorted):
		length = len(chromo_unsorted[0]) - 1
		return sorted(chromo_unsorted, reverse=True,key=lambda elem: elem[length]) 

	def rand_generate_chromosome(self, _data, chromosome_length):
		
		_chromo = list()
		Npop = self.Npop


		for i in range(0,Npop,+1):
			_chromosome = list()

			for i in range(0,chromosome_length,+1):
				bit = float('%.2f'%  random.uniform(0.0,1.0))	#bit = float('%.2f'%  random.uniform(0.0,1.0))
				_chromosome.append(bit)

			_chromo.append(_chromosome)

		return _chromo

	def GA_Process(self,_chromo_with_fit,_count_fit_time):
		chromo_with_fit = _chromo_with_fit
		count_fit_time = _count_fit_time
		budget = self.budget
		Ps = self.Ps
		Pm = self.Pm
		Pc = self.Pc
		Npop = self.Npop

		print "------------Generation:",self.Generation_count,"-----------------"
		chromo = self.sort_chromosome(chromo_with_fit)

		# ------------------------simple ranking selection------------------------
		GA_select = Selection.Selection_Process(Npop,Ps,self.sort_chromosome)
		chromo = GA_select.selection(chromo)

		#  ------------------------------Crossover---------------------------------
		GA_crossover = Crossover.Crossover_Process(Npop,Pc,self.sort_chromosome,self.data,count_fit_time)
		chromo,count_fit_time = GA_crossover.crossover(chromo)


		#  ------------------------------Mutation---------------------------------
		GA_mutation = Mutation.Mutation_Process(Npop,Pm,self.sort_chromosome,self.data,count_fit_time)
		chromo,count_fit_time = GA_mutation.mutation(chromo)

		self.Generation_count += 1
		return chromo,count_fit_time,self.Generation_count
