
# coding: utf-8

# In[2]:

def euclid_dist(t1,t2):
    return np.sqrt(sum((t1-t2)**2))


# In[3]:

def DTWDistance(s1, s2):
    DTW={}
    
    for i in range(len(s1)):
        DTW[(i, -1)] = float('inf')
    for i in range(len(s2)):
        DTW[(-1, i)] = float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(s1)):
        for j in range(len(s2)):
            dist= (s1[i]-s2[j])**2
            DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)])
		
    return np.sqrt(DTW[len(s1)-1, len(s2)-1])


# In[4]:

def DTWDistance(s1, s2,w):
    DTW={}
    
    w = max(w, abs(len(s1)-len(s2)))
    
    for i in range(-1,len(s1)):
        for j in range(-1,len(s2)):
            DTW[(i, j)] = float('inf')
    DTW[(-1, -1)] = 0
  
    for i in range(len(s1)):
        for j in range(max(0, i-w), min(len(s2), i+w)):
            dist= (s1[i]-s2[j])**2
            DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)])
		
    return np.sqrt(DTW[len(s1)-1, len(s2)-1])


# In[5]:

def LB_Keogh(s1,s2,r):
    LB_sum=0
    for ind,i in enumerate(s1):
        
        lower_bound=min(s2[(ind-r if ind-r>=0 else 0):(ind+r)])
        upper_bound=max(s2[(ind-r if ind-r>=0 else 0):(ind+r)])
        
        if i>upper_bound:
            LB_sum=LB_sum+(i-upper_bound)**2
        elif i<lower_bound:
            LB_sum=LB_sum+(i-lower_bound)**2
    
    return np.sqrt(LB_sum)


# In[6]:

from sklearn.metrics import classification_report

def knn(train,test,w):
    preds=[]
    for ind,i in enumerate(test):
        min_dist=float('inf')
        closest_seq=[]
        #print ind
        for j in train:
            if LB_Keogh(i[:-1],j[:-1],5)<min_dist:
                dist=DTWDistance(i[:-1],j[:-1],w)
                if dist<min_dist:
                    min_dist=dist
                    closest_seq=j
        preds.append(closest_seq[-1])
    return classification_report(test[:,-1],preds)


# In[7]:

import random

def k_means_clust(data,names, num_clust,num_iter,w):  
    counter=0
    centroids=random.sample(list(data),num_clust)
    
    for n in range(num_iter):
        counter+=1
        assignments={}
        mapClust={}
        #assign data points to clusters
        for ind,i in enumerate(data):
            min_dist=float('inf')
            closest_clust=None
            for c_ind,j in enumerate(centroids):
                if LB_Keogh(i,j,5)<min_dist:
                    cur_dist=DTWDistance(i,j,w)
                    if cur_dist<min_dist:
                        min_dist=cur_dist
                        closest_clust=c_ind
            if closest_clust in assignments:
                assignments[closest_clust].append(ind)
            else:
                assignments[closest_clust]=[]
    
        #recalculate centroids of clusters
        for key in assignments:
            nameString=''
            clust_sum=0
            for k in assignments[key]:
                clust_sum=clust_sum+data[k]
                name=names[k].replace('_',' ')
                if name not in nameString:
                    nameString+=name+' // '
            centroids[key]=[m/len(assignments[key]) for m in clust_sum]
            mapClust[nameString]=centroids[key]
        
    return mapClust


# In[ ]:

import numpy as np
def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')


# Sélection des données, avec des lignes de longueur égale

# In[ ]:

#train = np.genfromtxt('datasets/train.csv', delimiter='\t')
from matplotlib.pyplot import *
from textwrap import wrap
test = np.genfromtxt('datasets/output.csv', delimiter='\t')
with open('datasets/names.txt', 'r') as namesFile:
    stringNames=namesFile.read()
namesArray=stringNames.split(' ')
#arrays = [np.array(map(int, line.split('\t'))) for line in open('datasets/test.csv')]
data=test
import matplotlib.pylab as plt
import numpy as np

mapOfTimeSeries=k_means_clust(data, namesArray,10,200,100)
values=list(mapOfTimeSeries.values())
keys=list(mapOfTimeSeries.keys())
for idx,i in enumerate(mapOfTimeSeries.values()):

    keys = [ '\n'.join(wrap(l, 50)) for l in keys ]
    key = keys[idx]
    
    p=plt.plot(movingaverage(i, 22),label=key)
    legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=1,
       ncol=2, mode="expand", borderaxespad=0.)

show()


# In[ ]:



