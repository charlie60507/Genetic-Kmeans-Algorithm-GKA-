import pandas as pd
import random
import math
import json
import operator
import numpy as np
import ConfigParser
pd.options.mode.chained_assignment = None 
random.seed(1)

class Evaluate:
	def __init__(self,chromo,data):
		self.chromo = chromo
		self.data = data
		self.dim = data.shape[1]
		self.penalty = 1000000

		config_file = "config.txt"
		config = ConfigParser.ConfigParser()
		config.read(config_file)
		self.kmax = int(config.get("vars", "kmax"))

	def cal_dis(self,chromosome):
		kmax = self.kmax
		dim = self.dim
		data = self.data
		dis_set = list()
		temp = []
		dis = 0
		all_index = list()
		all_dis = list()

		for z in range(0,data.shape[0],+1):
			for i in range(0,kmax,+1):
				if chromosome[i] >= 0.5:		# tag=1 -> used
					for j in range(0,dim,+1):	#j is # of dim 	
						square = pow(chromosome[kmax + dim*i+j] - data.loc[z][j],2)
						temp.append(square)		# save (center-point)^2 in temp

					for t in range(0,dim,+1):
						dis += temp[t]

					dis = math.sqrt(dis)
					dis_set.append(dis)
					dis = 0
					temp = []

				elif chromosome[i] < 0.5:	# tag=0 -> not used
					dis_set.append(self.penalty)	

			all_dis,all_index = self.find_min(dis_set,chromosome,all_index,all_dis)
			dis_set = []	#clear dis_set	# calculate distance

		return all_dis,all_index

	def find_min(self,dis_set,chromosome,all_index,all_dis):
		temp_1 = list()
		dis_1 = 0

		if not dis_set ==[]:
			n = dis_set.index(min(dis_set))	# n is index 
			min_dis = dis_set[n]
			all_index.append(n+1)

		all_dis.append(min_dis)

		# handle no center is used -> assign to center1
		for k in range(0,len(all_dis),+1):	
			if all_dis[k] == 1000000:
				for z in range(0,self.data.shape[0],+1):	# norm_data.shape[0]
					for j in range(0,self.dim,+1):	#j is # of dim 
						i = 0
						square = pow(chromosome[self.kmax+self.dim*i+j] - self.data.loc[z][j],2)
						temp_1.append(square)
					for t in range(0,self.dim,+1):
						dis_1 += temp_1[t]
					dis_1 = math.sqrt(dis_1)
				all_dis[k] = dis_1
				temp_1 =[]

		return all_dis,all_index

	def cal_inter(self,all_dis,all_index,count_inter,inter_sum):
		kmax = self.kmax
		data = self.data
		all_sum = 0

		for i in range(0,data.shape[0],+1):		#norm_data.shape[0]
			for k in range(0,kmax,+1):		# k: # of cluster(Kmax) 
				center_no = k+1

				if all_index[i] == center_no:
				   count_inter[center_no]+=1
				   inter_sum[center_no] += all_dis[i]

		for i in range(0,kmax,+1):
			if count_inter[i+1]==0:	# 0 can't be Denominator
				count_inter[i+1]=1	# set Denominator = 1

		for i in range(0,kmax,+1):
			all_sum += inter_sum[i+1]/count_inter[i+1]

		inter_score = all_sum/(kmax)

		return inter_score

	def cal_intra(self,chromosome):
		kmax = self.kmax
		dim = self.dim
		center_temp = list()
		center_list = list() 
		count = 0

		for i in range(0,kmax,+1):	# catch center point in chromo to center_list
			if chromosome[i] > 0.5:
				count+=1
				for j in range(0,dim,+1):	#j is # of dim 	
					center_temp.append(chromosome[kmax+dim*i+j])
				center_list.append(center_temp)		#
				center_temp=[]
		i = 0
		
		if count == 0:		
			intra_score = 0
		elif count == 1:	
			intra_score = 0
		elif count >= 2:
			for j in range(i+1,count,+1):
				for i in range(0,count-1,+1):
					v1 = center_list[i]
					v2 = center_list[j]
					vec = list(map(lambda x: x[0]-x[1], zip(v1,v2))) # Combination : count get 2
					vec_square = list(map(lambda x: pow(x,2), vec)) # square of vec
					sum_intra = sum(vec_square)
			intra_score = math.sqrt(sum_intra) / count

		return intra_score

	def cal_fitness(self,intra_score,inter_score,chromosome_with_fit,count_fit_time):
		if inter_score != 0:
			fitness = float(intra_score) / float(inter_score)
		else:
			fitness = 0

		chromosome_with_fit.append(fitness)
		count_fit_time += 1
		return fitness,chromosome_with_fit,count_fit_time

	def cal_child_fit(self,child,count_fit_time):	# child, kmax, count_fit_time
		kmax = self.kmax

		count_inter = (np.zeros(kmax+1)).tolist()
		inter_sum = (np.zeros(kmax+1)).tolist()
		all_dis,all_index = self.cal_dis(child)
		inter_score = self.cal_inter(all_dis,all_index,count_inter,inter_sum)
		intra_score = self.cal_intra(child)

		# cal fitness
		if inter_score != 0:
			fitness = float(intra_score) / float(inter_score)
		else:
			fitness = 0

		child.append(fitness)
		count_fit_time += 1

		return child,count_fit_time

	def print_Ibest(self,Ibest,count_fit_time):
		kmax = self.kmax

		count_inter = (np.zeros(kmax+1)).tolist()
		inter_sum = (np.zeros(kmax+1)).tolist()
		all_dis,all_index = self.cal_dis(Ibest)
		inter_score = self.cal_inter(all_dis,all_index,count_inter,inter_sum)
		intra_score = self.cal_intra(Ibest)

		if inter_score != 0:
			fitness = float(intra_score) / float(inter_score)
		else:
			fitness = 0

		print "Cal fit time:",count_fit_time
		print "Ibest Fitness:",fitness
		print "Cluster Index:",all_index
		print ""

	def cal_chromo_fit(self):
		kmax = self.kmax
		chromo = self.chromo
		generation = len(chromo)
		data = self.data
		chromo_with_fit = self.chromo
		count_fit_time = 0

		for i in range(0,generation,+1):
			count_inter = (np.zeros(kmax+1)).tolist()
			inter_sum = (np.zeros(kmax+1)).tolist()

			all_dis,all_index = self.cal_dis(chromo[i])
			inter_score = self.cal_inter(all_dis,all_index,count_inter,inter_sum)
			intra_score = self.cal_intra(chromo[i])
			fitness,chromosome_with_fit,count_fit_time = self.cal_fitness(intra_score,inter_score,chromo_with_fit[i],count_fit_time)
			chromo_with_fit[i] = chromosome_with_fit

		return chromo_with_fit,count_fit_time

	def output_result(self,Ibest,_data):
		print "Saving the result..."
		kmax = self.kmax
		count_inter = (np.zeros(kmax+1)).tolist()
		inter_sum = (np.zeros(kmax+1)).tolist()
		all_dis,all_index = self.cal_dis(Ibest)

		# decode cluster center
		rule_index = list()

		for i in range(self.kmax):
			if Ibest[i] >= 0.5:
				rule_index.append(1)
			else:
				rule_index.append(0)

		rDict = dict()
		tmp = Ibest[self.kmax:]
		for i in range(self.kmax):
			if rule_index[i] == 1:
				begin_index = i*self.dim
				rDict[i+1] = tmp[begin_index : begin_index + self.dim]

		with open('result/cluster_center.json', 'w') as outfile:
			json.dump(rDict, outfile,sort_keys = True, indent = 4, separators=(',', ': '))

		# rename df header
		col_name = list()
		for i in range(_data.shape[1]):
			col_name.append("f{0}".format(i))
		_data.columns = col_name

		# insert cluster result
		_data['Cluster Index'] = pd.Series(all_index,index = _data.index)
		_data.to_csv('result/result.csv',index = None)
		print "Done."