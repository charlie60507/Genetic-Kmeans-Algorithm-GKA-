import lib.genetic_algorithm as genetic_algorithm
import lib.evaluate_fitness as eval_fitness
import lib.initial_population as init_pop

from sklearn import preprocessing
import ConfigParser
import numpy as np
import pandas as pd
import random
# random.seed(0)

def read_vars(config_file):
	config = ConfigParser.ConfigParser()
	config.read(config_file)
	budget = int(config.get("vars", "budget"))
	kmax = int(config.get("vars", "kmax"))
	Npop = int(config.get("vars", "Npop"))
	Ps = float(config.get("vars", "Ps"))
	Pm = float(config.get("vars", "Pm"))
	Pc = float(config.get("vars", "Pc"))

	return budget,kmax,Ps,Pm,Pc,Npop

def normalize(data):
	norm_data = data
	data = data.astype(float)
	norm_data = norm_data.astype(float)

	for i in range(0,data.shape[1]):
		tmp = data.iloc[:,i]	
		max_element = np.amax(tmp)
		min_element = np.amin(tmp)
		for j in range(0,norm_data.shape[0]):
			norm_data[i][j] = float(data[i][j]-min_element) / (max_element - min_element)

	norm_data.to_csv('result/norm_data.csv',index = None,header = None)
	return norm_data


if __name__ == '__main__':
	config_file = "config.txt"
	data =  pd.read_csv('data/if2_iris.csv',header = None) 
	dim = data.shape[1]
	
	# kmeans parameters & GA parameters
	Generation_count = 0
	budget,kmax,Ps,Pm,Pc,Npop = read_vars(config_file)

	print "-------------GA Info-------------------"
	print 'budget',budget
	print 'kmax',kmax
	print 'Npop',Npop
	print 'Ps',Ps
	print 'Pm',Pm
	print 'Pc',Pc
	print "---------------------------------------"

	chromosome_length = kmax + kmax*dim

	#-------------------------------------------------------#
	# 							main 						#
	#-------------------------------------------------------#

	data = normalize(data)	# normalize
	initial = init_pop.init_chromo(chromosome_length,Npop)
	chromo = initial.rand_generate_chromosome()	# initial generate chromosome
	evaluate = eval_fitness.Evaluate(chromo,data)	# eval fit of chromo

	# ------------------cal fitness------------------# 
	chromo_with_fit,count_fit_time = evaluate.cal_chromo_fit()
	# print chromo_with_fit
	# exit(0)

	# ------------------------GA----------------------#
	while count_fit_time <= budget:
		GA = genetic_algorithm.Genetic_Algo(Npop, Ps, Pm, Pc, budget, data, Generation_count)
		chromo_with_fit,count_fit_time,Generation_count = GA.GA_Process(chromo_with_fit,count_fit_time)
		Ibest = chromo_with_fit[0]
		evaluate.print_Ibest(Ibest,count_fit_time)

	# ------------------output result-------------------#
	evaluate.output_result(Ibest,data)