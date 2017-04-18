import pandas as pd
import random
import numpy as np

class init_chromo:
	def __init__(self, chromosome_length, Npop):
		self.chromosome_length = chromosome_length
		self.Npop = Npop

	def rand_generate_chromosome(self):
		length = self.chromosome_length
		Npop = self.Npop
		_chromo = list()

		for i in range(0,Npop,+1):
			_chromosome = list()

			for i in range(0,length,+1):
				bit = float('%.2f'%  random.uniform(0.0,1.0))	#bit = float('%.2f'%  random.uniform(0.0,1.0))
				_chromosome.append(bit)

			_chromo.append(_chromosome)

		return _chromo