
# coding: utf-8

# In[24]:


import os
import math
import glob
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
plt.rcParams["svg.fonttype"]="none"


# In[25]:


folder_path="/Users/laurentpottier/Documents/LP/Recherches/Projet_Fondation/Langages&Maths/Anaconda/LPanalyse/PopPlinn/class/PopPlinnTxtSel"
filelist = []
for path, dirs, files in os.walk(folder_path):
    for filename in files:
        if 'txt' in filename :
                filelist.append(filename)
#print (filelist)
print(len(filelist))


#get classes in string
#class_path=os.chdir("/Users/Vivo-Na/Desktop/class/")
#class_path=os.chdir("/Users/laurentpottier/Documents/LP/Recherches/Projet_Fondation/Langages&Maths/Anaconda/FromNa1/V9-28juin/class/")

class_path=os.chdir("/Users/laurentpottier/Documents/LP/Recherches/Projet_Fondation/Langages&Maths/Anaconda/LPanalyse/PopPlinn/class/PopPlinnTxtSel/")

#filetext="03yes_class_reduced.txt"
#with open(filetext) as f:
#        classes = f.read().splitlines()
#print(classes)  


#filetext="03popplinn_class_reduced.txt"
#with open(filetext) as f:
#        classes = f.read().splitlines()
#print(classes)  


# In[26]:


def f_to_midi (f) :
    return 69+12*math.log(f/440,2)

print ("note de freq 261Hz :" , f_to_midi (261))

def midi_to_f (n) :
    return 440*2**((n-69)/12)

print ("frequence de note 60 :" , midi_to_f (60), "Hz")


# In[27]:



f_ls = [21.5,32.3,43.1,53.8,64.6,86.1,107.7,140.0,172.3,215.3,269.2,344.5,441.4,549.1,699.8,872.1,1109.0,1388.9,1755.0,2217.9,2788.5,3520.7,4435.8,5587.9,7041.4,8871.7,11175.7,14071.9]

L = [] # liste des tailles des lignes
for k in range(27):
    L.append(4+2*k)

f_c = [] # frequences centrales des bandes
for i in range(len(f_ls)-1):
    f_c.append(math.sqrt(f_ls[i+1]*f_ls[i]))
    
f_c_midi = []
for i in range(len(f_c)):
    f_c_midi.append(f_to_midi(f_c[i]))

f_c_moy = 0 
for i in range(len(f_c)):
    f_c_moy += f_c[i]
    f_c_moy /= 27
    
f_c_gmoy = 0
for i in range(len(f_c)):
    f_c_gmoy += math.log(f_c[i], 2)
    f_c_gmoyR =  2**(f_c_gmoy/27)

#formule equivalente
#f_c_gmoy2 = 0
#for i in range(len(f_c)):
#    f_c_gmoy2 += f_to_midi(f_c[i])
#    f_c_gmoyR2 =  midi_to_f(f_c_gmoy2/27)

    
print("len(f_ls) :", len(f_ls), "bornes")
W=[]
for i in range(len(f_ls)-1):
    W.append(round(f_ls[i+1]-f_ls[i], 2))
print("w :" , W)    
    
print ("f_c :", f_c)
print ("f_c_moy :", round(f_c_moy,1), "Hz") # (en Hz) moyenne des frequences des centres des bandes 
print ("f_c_gmoyR :", round(f_c_gmoyR,1), "Hz") # (en Hz) moyenne des centres calculée par les notes MIDI
#print ("f_c_gmoyR :", f_c_gmoyR2) # (en Hz) moyenne des centres calculée par les notes MIDI

f_cA = np.asarray(f_c)
f_cA = f_cA[:, np.newaxis]
#print (round(3.149 , 2))


# In[28]:


# read filetxt and generate array S
def read(filetext):
    with open(filetext) as f:
        mylist = f.read().splitlines()
        for x in range(8):
            mylist.pop(0)
        S=[]
        for element in reversed(mylist):
            element2=[float(i) for i in element.split()]
            S.append(element2)
        return S
    


# In[29]:


file1 = "PopPlinn_sr44100_deb00_00_00_t02_00_pas02_00.txt"
S1 = read(file1)
file2 = "PopPlinn_sr44100_deb01_00_00_t02_00_pas02_00.txt"
S2 = read(file2)


# In[30]:


# plus file name unite comme secondes 
def timetxt (filetext):
    str_L = filetext.rsplit(sep='_')
    test = 0
    result = 0
    for str in str_L:
        if test == 3:
            cent = int(str)
            result+=(cent/100)
            test = 0
        if test == 2:
            sec = int(str)
            test = 3
            result+=sec
        if re.search('deb', str):
            test = 1
            min = int(str[4-5])
            result+=(min*60)
            test = 2
    return result

print(timetxt(file2))


# In[31]:


def ampmax(S, k):
    ampmx = 0
    for j in range(4+2*k):
        ampmx = max(ampmx, S[k][j])
    return ampmx

def ampmin(S, k):
    ampmn = 1
    for j in range(4+2*k):
        ampmn = min(ampmn, S[k][j])
    return ampmn

def deltaamp(S, k):
    return ampmax(S, k) - ampmin(S, k)

def moy_ecart_amps(S):
    ecarts = []
    for k in range(26):
        ecarts.append(deltaamp(S, k))
    ecartsA = np.asarray(ecarts)
    return ecartsA.mean()
        

#for k in range(27):
#    print("k =",1+k ,"amp min=", round(ampmin(S1, k),2),"amp max=", round(ampmax(S1, k),2), "ecart" ,round(deltaamp(S1, k), 2))
for k in range(27):
    print("k =",1+k ,"amp min=", round(ampmin(S2, k),2),"amp max=", round(ampmax(S2, k),2), "ecart" ,round(deltaamp(S2, k), 2))
    
print("moyenne des écarts d'amplitudes :",round(moy_ecart_amps (S1),3))
print("moyenne des écarts d'amplitudes :",round(moy_ecart_amps (S2),3))


# In[64]:


def array_eucl_dist(Arr1, Arr2):
    res = np.subtract(Arr1, Arr2)
    res = np.multiply(res, res)
    res = np.sum(res)
    return res**0.5

def selfsimil (S, k):
    dist = 0
    distmin = 1
    distmax = 0
    for j in range(3+2*k):
        d = (array_eucl_dist(S[k], np.roll(S[k],j+1))/(1+k))
        dist += d
        distmin = min(distmin, d)
        distmax = max(distmax, d)
        print(d)
    return [dist, distmin, distmax]

np.round_(selfsimil (S2, 15), 4)


#voir les zero cross de la dérivée de d = nbre de cycles
# ecarts, pics

