
# coding: utf-8

# author : odysseusPolymetis


from lxml import etree
import os.path
import fnmatch
from numpy import cumsum
from operator import itemgetter
import numpy as np
import itertools
from matplotlib.pyplot import *
from textwrap import wrap
import numpy as np
from sklearn.metrics import classification_report
import random
import re
import csv
import matplotlib.pylab as plt
import numpy as np
import argparse


print('This software generates a figure of profile clusters on a selected corpus \nusage: --dir path/to/your/source/dir --figname name_for_your_fig')
parser = argparse.ArgumentParser()
parser.add_argument('--dir', help= '/your/directory/to/tagged/files/')
parser.add_argument('--figname', help= 'name_for_your_fig')
args = parser.parse_args()
if len(sys.argv) == 1:
    sys.exit()

argsdir= os.path.join(args.dir, '')
argsfig= os.path.join(args.figname, '')
directory_dataset='dataset/'
if not os.path.exists(directory):
    os.makedirs(directory)

files_list=fnmatch.filter(os.listdir(path_to_folder), '*.xml')

files_list=fnmatch.filter(os.listdir(path_to_folder), '*.xml')

def euclid_dist(t1,t2):
    return np.sqrt(sum((t1-t2)**2))

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

def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

chaps=list()
names=list()
data_per_name=list()

for file in files_list:
    print(file)
    global_nb_words = 0
    tmpFile=file.replace("/",":")
    full_path=path_to_folder+tmpFile
    if os.path.isfile(full_path):
        tree=etree.parse(full_path)
        nb_words_per_chap=list()
        if tree.findall(".//div[@type='chapter']"):
            nb_chaps = len(tree.findall(".//div[@type='chapter']"))
            for idx, chap in enumerate(tree.findall(".//div[@type='chapter']")):
                nb_words = len(chap.findall(".//word"))
                global_nb_words+= nb_words
                nb_words_per_chap.append(nb_words)
        
            list_perc_per_chap=list()
            cum_l = np.cumsum(nb_words_per_chap)
            for idx,num in enumerate(cum_l):
                if idx>0:
                    cur_num = (num/global_nb_words)*100
                    prev_num = (cum_l[idx-1]/global_nb_words)*100
                    list_perc_per_chap.append(cur_num - prev_num)
                else:
                    list_perc_per_chap.append((num/global_nb_words)*100)
              
            num_div = 101/len(list_perc_per_chap)
            
            perc_chap_100=dict()
            val=0
            num_div_prev=num_div
            
            index=0
            for i in range(0,101):      
                if i > num_div_prev:
                    num_div_prev+=num_div
                    index+=1
                perc_chap_100[i]=(list_perc_per_chap[index]/num_div)
            
            names.append(re.sub(u'\n','',tree.find(".//title").text).replace("     ","").replace(" ","_"))
            
            data_per_name.append(perc_chap_100.values())          
            
        else :
            print("!!! No chapter found in file : "+file)         

with open('datasets/names.txt', 'w') as f:
    f.write((' '.join(names*4)))
    f.close()
writer=csv.writer(open('datasets/data.csv','w'),delimiter='\t')
for i in range (0,4):
    for percs in data_per_name:
        writer.writerow(percs)

num_clusters=5
num_iters=50
w=20

print("You have asked for 5 clusters and 50 iterations. Please wait.")
plt.rcParams["figure.figsize"] = [16,9]
test = np.genfromtxt('datasets/data.csv', delimiter='\t')
with open('datasets/names.txt', 'r') as namesFile:
    stringNames=namesFile.read()
namesArray=stringNames.split(' ')

mapOfTimeSeries=k_means_clust(test,namesArray,num_clusters,num_iters,w)
values=list(mapOfTimeSeries.values())
keys=list(mapOfTimeSeries.keys())
fig=plt.figure()
for idx,i in enumerate(mapOfTimeSeries.values()):

    keys = [ '\n'.join(wrap(l, 50)) for l in keys ]
    key = keys[idx]
    p=plt.plot(movingaverage(i, 1),label=key)
    legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=1,
       ncol=2, mode="expand", borderaxespad=0.)


fig.savefig(argsfig+'.png')
plt.close(fig)

