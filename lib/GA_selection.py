import pandas as pd
import random
import math
import operator
import numpy as np
pd.options.mode.chained_assignment = None 
random.seed(1)

class Selection_Process:
	def __init__(self,Npop,Ps,sort_chromosome):
		self.Npop = Npop
		self.Ps = Ps
		self.sort_chromosome = sort_chromosome

	def selection(self,chromo_with_fit_sorted):
		Npop = self.Npop
		Ps = self.Ps

		for i in range(0,int(Ps*Npop),+1):		# replace the worst Ps*Npop individual with the best Ps*Npop individual
			chromo_with_fit_sorted[Npop-1-i] = chromo_with_fit_sorted[i]

		chromo_with_fit_sorted = self.sort_chromosome(chromo_with_fit_sorted)	# sort chromosomes after ranking selection
		return chromo_with_fit_sorted