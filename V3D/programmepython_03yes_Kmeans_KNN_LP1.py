
# coding: utf-8

# In[235]:


get_ipython().magic('matplotlib inline')
import os
#import sys
#sys.path.append(os.path.join(os.path.dirname(os.path.realpath("03_Yes")), '/Users/Vivo-Na/Desktop/Analyses10copie/'))
import math
import glob
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
plt.rcParams["svg.fonttype"]="none"


# In[227]:


#03yes reduced classes (8) and text files (343)
#folder_path=os.chdir("/Users/Vivo-Na/Downloads/03_Yes_reduced")

#folder_path=os.chdir("/Users/laurentpottier/Documents/LP/Recherches/Projet_Fondation/Langages&Maths/Anaconda/FromNa1/V9-28juin/class/03_Yes_reduced")
#folder_path="/Users/laurentpottier/Documents/LP/Recherches/Projet_Fondation/Langages&Maths/Anaconda/FromNa1/V9-28juin/class/03_Yes_reduced"
folder_path="/Users/laurentpottier/Documents/LP/Recherches/Projet_Fondation/Langages&Maths/Anaconda/LPanalyse/V10LP/PopPlinn/class/PopPlinnTxt"

#folder_path="/Users/Vivo-Na/Downloads/03_Yes/"

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

class_path=os.chdir("/Users/laurentpottier/Documents/LP/Recherches/Projet_Fondation/Langages&Maths/Anaconda/LPanalyse/V10LP/PopPlinn/class/PopPlinnTxt/")

#filetext="03yes_class_reduced.txt"
#with open(filetext) as f:
#        classes = f.read().splitlines()
#print(classes)  


# # # Class

# In[ ]:





# # # Central frequency and frequency bandwidth

# In[216]:


def f_to_midi (f) :
    return 69+12*math.log(f/440,2)

print ("note de freq 261Hz :" , f_to_midi (261))

def midi_to_f (n) :
    return 440*2**((n-69)/12)

print ("frequence de note 60 :" , midi_to_f (60), "Hz")


# In[228]:



f_ls = [21.5,32.3,43.1,53.8,64.6,86.1,107.7,140.0,172.3,215.3,269.2,344.5,441.4,549.1,699.8,872.1,1109.0,1388.9,1755.0,2217.9,2788.5,3520.7,4435.8,5587.9,7041.4,8871.7,11175.7,14071.9]

L = [] # liste des tailles des lignes
for k in range(27):
    L.append(4+2*k)

f_c = [] # frequences centrales des bandes
for i in range(len(f_ls)-1):
    f_c.append(math.sqrt(f_ls[i+1]*f_ls[i]))
    
f_c_midi = [] # valeur centrale des bandes en note MIDI
for freq in f_c:
    f_c_midi.append(f_to_midi(freq))

f_c_moy = 0 
for freq in f_c:
    f_c_moy += freq
    f_c_moy /= 27
    
f_c_gmoy = 0
for freq in f_c:
    f_c_gmoy += math.log(freq, 2)
    f_c_gmoyR =  2**(f_c_gmoy/27)

f_cA = np.asarray(f_c)
f_cA = f_cA[:, np.newaxis]
    
#print (f_c_midi)
print (f_c_moy, f_c_gmoy)


# In[218]:


#print(len(f_ls))
W=[]
for i in range(len(f_ls)-1):
    W.append(f_ls[i+1]-f_ls[i])
#print(W)


# # # Time duration of text files

# In[219]:


import re

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

print(timetxt("AlanStivell_PopPlinn_1971m.wav_sr44100_deb00_45_00_t02_50_pas02_50.txt"))
#timetxt("AlanStivell_PopPlinn_1971m.wav_sr44100_deb00_45_00_t02_50_pas02_50.txt")


# In[220]:


print(timetxt("AlanStivell_PopPlinn_1971m.wav_sr44100_deb00_45_00_t02_50_pas02_50.txt"))
print(timetxt("AlanStivell_PopPlinn_1971m.wav_sr44100_deb01_22_50_t02_50_pas02_50.txt"))


# In[229]:


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
    


# In[230]:


file1 = "AlanStivell_PopPlinn_1971m.wav_sr44100_deb01_02_50_t02_50_pas02_50.txt"
S = read(file1)
#print (S)


# # # Spectral Features

# In[225]:


# moyennes des amplitudes par ligne (des fréquences basses vers hautes)
def moy_des_amps (S):
    Sk_mean=[]
    for k in range(27):
        sum_s=0
        for j in range(4+2*k):
            sum_s+=S[k][j]
        Sk_mean.append(sum_s/(4+2*k))
    return Sk_mean  

print("amps:",moy_des_amps(S))


# In[213]:


#centroid
def centroid(S):
    Sk_mean = moy_des_amps(S)
    sum_sc=0
    sum_sfk=0
    for k in range(27):
        sum_sfk+=Sk_mean[k]*f_c[k]
        sum_sc+=Sk_mean[k]            
    if sum_sc == 0 :
        centroid=0
    else:
        centroid=sum_sfk/sum_sc
    #print('centroid' , centroid)
    return centroid

print("centroid:",round(centroid(S)),"Hz")


# In[214]:


#variance et sd
def variance(S):
    Sk_mean=[]
    for k in range(27):
        sum_s=0
        for j in range(4+2*k):
            sum_s+=S[k][j]
        Sk_mean.append(sum_s/(4+2*k))
    sum_var=0
    sum_skm=0
    for k in range(27):
        sum_var+=Sk_mean[k]*((f_c[k]-centroid(S))**2)
        sum_skm+=Sk_mean[k]
    variance=sum_var/sum_skm
    #print("variance", variance)
    return variance

# sd: 
def sd(filetext):
    sd=math.sqrt(variance(filetext))
    return sd

print("sd:",round(sd(S)),"Hz")


# In[124]:


# sd: biased standard deviation (N)
def sdLow(S):
    Sk_mean = moy_des_amps(S)
    sum_sd=0
    sum_skm=0
    for k in range(27):
        diff=f_c[k]-centroid(S)
        if diff <0:
            sum_sd+=Sk_mean[k]*(diff**2)
            sum_skm+=Sk_mean[k]
    sdLow=math.sqrt(sum_sd/sum_skm)
    return sdLow

# sd: biased standard deviation (N)
def sdHigh(S):
    Sk_mean = moy_des_amps(S)
    sum_sd=0
    sum_skm=0
    for k in range(27):
        diff=f_c[k]-centroid(S)
        if diff >0:
            sum_sd+=Sk_mean[k]*(diff**2)
            sum_skm+=Sk_mean[k]
    sdHigh=math.sqrt(sum_sd/sum_skm)
    return sdHigh
    
def c_min_sdlow(S): 
    return round(centroid(S) - sdLow(S),1)

def c_plus_sdHi(S): 
    return round(centroid(S) + sdHigh(S),1)


print("centroid:", round(centroid(S),1),"Hz")
print("centre-ecartlow:", c_min_sdlow(S),"Hz")
print("centre+ecartHigh:", c_plus_sdHi(S),"Hz")


# In[232]:


#MIDI centroid
def midi_centroid(S):
    Sk_mean = moy_des_amps(S)
    sum_sc=0
    sum_sfk=0
    for k in range(27):
        sum_sfk+=Sk_mean[k]*f_to_midi(f_c[k])
        sum_sc+=Sk_mean[k]            
    if sum_sc == 0 :
        midi_centroid=0
    else:
        midi_centroid=sum_sfk/sum_sc
    #print('centroid' , centroid)
    return midi_centroid


print("Midicentroid:", round(midi_centroid(S),1),"MIDI")


# In[233]:


#ecartHigh
def midi_ecartHigh(S): 
    Sk_mean = moy_des_amps(S) 
    sum_var=0 
    sum_skm=0 
    for k in range(27): 
        df = f_to_midi(f_c[k])-midi_centroid(S) 
        if df>0:
            sum_var+=Sk_mean[k]*(df**2)
            sum_skm+=Sk_mean[k]
    varianceHigh=sum_var/sum_skm
    #print(\"variance\", variance)
    return math.sqrt(varianceHigh)

#ecartLow 
def midi_ecartLow(S): 
    Sk_mean = moy_des_amps(S) 
    sum_var=0 
    sum_skm=0 
    for k in range(27): 
        df = f_to_midi(f_c[k])-midi_centroid(S) 
        if df<0:
            sum_var+=Sk_mean[k]*(df**2)
            sum_skm+=Sk_mean[k]
    varianceLow=sum_var/sum_skm
    #print(\"variance\", variance)
    return math.sqrt(varianceLow)

def mc_min_eclow(S): 
    return round(midi_centroid(S) - midi_ecartLow(S),1)

def mc_plus_ecHi(filetext): 
    return round(midi_centroid(S) + midi_ecartHigh(S),1)

mcd = round(midi_centroid(S),1)
mcd_eL = round(mc_min_eclow(S),1)
mcd_eH = round(mc_plus_ecHi(S),1)
print("midi_centroid:", mcd,"MIDI /", round(midi_to_f(mcd)),"Hz")
print("centr-ecartLow:", mcd_eL,"MIDI /", round(midi_to_f(mcd_eL),1),"Hz") 
print("centr+ecartHigh:", mcd_eH,"MIDI /", round(midi_to_f(mcd_eH),1),"Hz")


# In[236]:


#midi spectral slope
def midi_spectral_slope_reg(S):
    f_csA_midi = np.asarray(f_c_midi)
    f_csA_midi = f_csA_midi[:, np.newaxis]
    Sk_meanA = np.asarray(moy_des_amps(S))
    Sk_meanA = Sk_meanA[:, np.newaxis]
    modeleReg = LinearRegression()
    modeleReg.fit(f_csA_midi, Sk_meanA)
    #plt.scatter(f_csA, Sk_meanA)
    return modeleReg

def midi_sp_slope (S):
    return midi_spectral_slope_reg(S).coef_[0][0]

def plot_slope(S):
    modeleReg = midi_spectral_slope_reg(S)
    f_csA_midi = np.asarray(f_c_midi)
    f_csA_midi = f_csA_midi[:, np.newaxis]
    Sk_meanA = np.asarray(moy_des_amps(S))
    Sk_meanA = Sk_meanA[:, np.newaxis]
    plt.scatter(f_csA_midi, Sk_meanA)
    
    x_min = 10
    x_max = 130

    X_NEW = np.linspace(x_min, x_max, 100)
    X_NEW = X_NEW[:,np.newaxis]

    Y_NEW = modeleReg.predict(X_NEW)

    plt.plot(X_NEW, Y_NEW, color='coral', linewidth=3)
    plt.grid()
    plt.xlim(x_min, x_max)
    plt.ylim(-0.2, 0.2)

    plt.title("regression linéaire test", fontsize=10)
    plt.xlabel('f_cs_midi')
    plt.xlabel('a_ls_midi')

    plt.savefig("simple_linear_regression_test_midi.png", bbox_inches='tight')
    plt.show()

plot_slope (S)
print ("slope : " + str(midi_sp_slope(S)))



# In[239]:


#spectral slope
def spectral_slope_reg(S):
    f_csA = np.asarray(f_c)
    f_csA = f_csA[:, np.newaxis]
    Sk_meanA = np.asarray(moy_des_amps(S))
    Sk_meanA = Sk_meanA[:, np.newaxis]
    modeleReg = LinearRegression()
    modeleReg.fit(f_csA, Sk_meanA)
    #plt.scatter(f_csA, Sk_meanA)
    return modeleReg

def sp_slope (S):
    return spectral_slope_reg(S).coef_[0][0]

def plot_slope(filetext):
    modeleReg = spectral_slope_reg(S)
    f_csA = np.asarray(f_c)
    f_csA = f_csA[:, np.newaxis]
    Sk_meanA = np.asarray(moy_des_amps(S))
    Sk_meanA = Sk_meanA[:, np.newaxis]
    plt.scatter(f_csA, Sk_meanA)
    
    x_min = 20
    x_max = 14000

    X_NEW = np.linspace(x_min, x_max, 100)
    X_NEW = X_NEW[:,np.newaxis]

    Y_NEW = modeleReg.predict(X_NEW)

    plt.plot(X_NEW, Y_NEW, color='coral', linewidth=3)
    #plt.scale.LogScale
    plt.grid()
    plt.xlim(x_min, x_max)
    plt.txaxis=dict(type='log', autorange=True)
    plt.ylim(-0.2, 0.2)

    plt.title("regression linéaire test", fontsize=10)
    plt.xlabel('f_cs')
    plt.xlabel('a_ls')
    plt.xscale("log")

    plt.savefig("simple_linear_regression_test.png", bbox_inches='tight')
    plt.show()

plot_slope (S)
print ("slope : " + str(sp_slope(S)))



# In[125]:


def skewness(S):
    Sk_mean = moy_des_amps(S)
    sum_sk=0
    sum_skm=0
    for k in range(27):
        sum_sk+=Sk_mean[k]*((f_c[k]-centroid(S))**3)
        sum_skm+=Sk_mean[k]
    skewness=(sum_sk/sum_skm)/(sd(S)**3)
    return skewness

print(skewness(S))


# In[126]:



def kurtosis(S):
    Sk_mean = moy_des_amps(S)
    sum_kt=0
    sum_skm=0
    for k in range(27):
        sum_kt+=Sk_mean[k]*((f_c[k]-centroid(S))**4)
        sum_skm+=Sk_mean[k]
    kurtosis=(sum_kt/sum_skm)/(sd(S)**4)
    return kurtosis

print(kurtosis(S))


# In[127]:


#spectral rolloff at 85%
def sp_rolloff(S):
    Sk_mean = moy_des_amps(S)
    sum_skm=0
    sum_rf=0
    for k in range(27):
        sum_skm+=Sk_mean[k]
    for k in range(27):
        sum_rf+=Sk_mean[k]
        if sum_rf>=0.85*sum_skm:
            rf=f_c[k]
            break
    return rf

#print(sum_skm)
#print("rf0.85",rf)


print(sp_rolloff(S))


# In[248]:


#spectral slope
def spectral_slope_old(S):
    Sk_mean = moy_des_amps(S)
    for k in range(27):
        sum_s=0
        for j in range(4+2*k):
            sum_s+=S[k][j]
        Sk_mean.append(sum_s/(4+2*k)) 
    sum_skm=0
    sum_fk2=0
    sum_fk=0
    sum_fsk=0
    K=27
    for k in range(27):
        sum_skm+=Sk_mean[k]
        sum_fk+=f_c[k]
        sum_fk2+=f_c[k]**2
        sum_fsk+=f_c[k]*Sk_mean[k]
    ssl=(1/sum_skm)*(K*sum_fsk-sum_fk*sum_skm)/(K*sum_fk2-sum_fk**2)
    return ssl


print(spectral_slope_old(S))


# In[250]:


#spectral flatness 
def sp_flatness(S):
    Sk_mean = moy_des_amps(S)
    sum_skm=0
    mult_skm=1
    K=26
    for k in range(26):
        sum_skm+=Sk_mean[k]
        mult_skm*=max(Sk_mean[k], 0.00001)
        pow_skm=mult_skm**(1/K)
    if sum_skm == 0 :
        sf=0
    else:
        sf=pow_skm/((1/K)*sum_skm)
    return sf

def spectral_flatness_old(S):
    Sk_mean = moy_des_amps(S)
    sum_skm=0
    mult_skm=1
    K=26
    for k in range(26):
        sum_skm+=Sk_mean[k]
        mult_skm*=Sk_mean[k]
        pow_skm=mult_skm**(1/K)
    sf=pow_skm/((1/K)*sum_skm)
    return sf

print(sp_flatness (S))


# In[251]:


# moyennes des amplitudes par ligne (des fréquences basses vers hautes)
def produit_des_amps (S):
    Sk_mult=1
    for k in range(27):
        mult_s=1
        for j in range(4+2*k):
            mult_s*=max(S[k][j]**(0.5/(k+2)), 0.00000001)
        Sk_mult*=mult_s
    return Sk_mult  

# moyennes des amplitudes par ligne (des fréquences basses vers hautes)
def flatness_list (S):
    Sk_flat=[]
    for k in range(27):
        mult_s=1
        for j in range(4+2*k):
            mult_s*=max(S[k][j]**(0.5/(k+2)), 0.00000001)
        Sk_flat.append(mult_s)
    return Sk_flat  

#spectral flatness moyenne
def sp_flatness_moy(S):
    Sk_flat = flatness_list(S)
    Sm=0
    for k in range(27):
         Sm+=Sk_flat[k]
    #print(Sm)
    return Sm/27

#formule equivalente
def sp_flatness_moy2(S):
    Sk_flat = flatness_list(S)
    Sk_flatA = np.asarray(Sk_flat)
    return Sk_flatA.mean()

def sp_flatness_max(S):
    Sk_flat = flatness_list(S)
    Sm=0
    for k in range(27):
        if Sm<Sk_flat[k]:
            Sm=Sk_flat[k]
            value = k
    return [value, f_c[value], Sm]
         
    #print(Sm)
    return Sm/27

def sp_flatness_min(S):
    Sk_flat = flatness_list(S)
    Sm=1
    for k in range(27):
        if Sm>Sk_flat[k]:
            Sm=Sk_flat[k]
            value = k
    return [value, f_c[value], Sm]

def sp_flatness_maxamp(S):
    return sp_flatness_max(S)[2]
def sp_flatness_maxfreq(S):
    return sp_flatness_max(S)[1]
def sp_flatness_minamp(S):
    return sp_flatness_min(S)[2]
def sp_flatness_minfreq(S):
    return sp_flatness_min(S)[1]

print("sp_flatness_maxamp:", sp_flatness_maxamp(S))
print("sp_flatness_maxfreq:", sp_flatness_maxfreq(S))
print("sp_flatness_minamp:", sp_flatness_minamp(S))
print("sp_flatness_minfreq:", sp_flatness_minfreq(S))


# In[242]:


def sp_crest(S):
    Sk_mean = moy_des_amps(S)
    sum_skm=0
    K=27
    max_skm=[]
    for k in range(27):
        sum_skm+=Sk_mean[k]
        for j in range(4+2*k):
            max_skm.append(np.max(S[k][j]))
    max_sk=max(max_skm)
    screst=max_sk/((1/K)*sum_skm)
    return screst

print(spectral_crest (S))


# In[243]:



# rms with original value of frequency bin k=27
def rms(S):
    Sk_mean = moy_des_amps(S)
    sum_skr=[]
    for k in range(27):
        sum_sk=0
        for j in range(L[k]):
            sum_sk+= (1/L[k])*(S[k][j]**2)
        sum_skr.append(sum_sk)
    #print(sum_skr)
    sum_rms=0
    for k in range(27):
        sum_rms+=sum_skr[k]
    rms=math.sqrt(sum_rms)
    return rms  

print(rms(S))


# In[ ]:


# maxfreq25 (amp max de la bande 25) approx 8000Hz
def maxfreq25(S):
    maxfreq25=max(S[25])
    return maxfreq25


# In[164]:


S2 = [[8, 0, 3],[4, 5, 6],[7, 8, 9]]
S3 = [8, 0, 3, 4, 5, 6, 7, 8, 9]

#print(re.search('3', str(S2)))
#print (S3.index(7))


# In[244]:


#amps max et min
def max_amp(S):
    maxs = []
    for k in range(27):
        maxs.append(max(S[k]))
    return max(maxs)

def max_amoy(S):
    return max(moy_des_amps(S))

def min_amp(S):
    mins = []
    for k in range(27):
        mins.append(min(S[k]))
    return min(mins)
                    
print('max_amp :',round(max_amp(S),3))
print('max_amoy :',round(max_amoy(S),3))
print('min_amp :',round(min_amp(S),5))


# In[245]:


def max_freq(S):
    maxs = []
    maxi = 0
    indx = 0
    for k in range(27):
        maxs.append(max(S[k]))
    maxi = max(maxs)
    indx = maxs.index(maxi)
    #print ("indx :", indx, "amp :", maxs[indx])
    return f_c[indx]

def max_moy_freq(S):
    maxs = moy_des_amps(S)
    maxi = max(maxs)
    indx = maxs.index(maxi)
    #print ("indx :", indx, "amp :", maxs[indx])
    return f_c[indx]


print('max_freq :',round(max_freq(S),5))
print('max_moy_freq :',round(max_moy_freq(S),5))


# In[246]:


def mode_freq_old(S):
    Sk_mean = moy_des_amps(S)
    Sk_sum = np.sum(Sk_mean)
    Sk_cum = 0
    indx = 0
    for k in range(27):
        if Sk_cum < 0.5:
            #print (Sk_mean[k])
            indx+=1
            Sk_cum+=(Sk_mean[k]/Sk_sum)
    #print (indx)
    return f_ls[indx-1]
            
#Sk_mean = moy_des_amps(S)
#print(Sk_mean[0])
print('mode_freq :',round(mode_freq(S),5), "Hz")


# In[252]:


def mode_freq(S):
    Sk_mean = moy_des_amps(S)
    Sk_sum = np.sum(Sk_mean)
    Sk_cum = 0
    indx1 = 0
    indx2 = 0
    indx3 = 0
    for k in range(27):
        if Sk_cum < 0.75:
            indx3+=1
            Sk_cum+=(Sk_mean[k]/Sk_sum)
        if Sk_cum < 0.5:
            indx2+=1
        if Sk_cum < 0.25:
            indx1+=1
    #print (indx)
    return [f_ls[indx1-1], f_ls[indx2-1], f_ls[indx3-1]]

print('mode_freq :',mode_freq(S))


def mode_freq1(S):    
    return mode_freq(S)[0]
    
def mode_freq2(S):    
    return mode_freq(S)[1]
    
def mode_freq3(S):    
    return mode_freq(S)[2]
        


# # # Temporal features

# In[22]:



def temporal_centroid(filetext):
    with open(filetext) as f:
        mylist = f.read().splitlines()
        S=[]
        for x in range(8):
            mylist.pop(0)
        for element in reversed(mylist):
            element2=[float(i) for i in element.split()]
            S.append(element2)  
    sum_e=[]
    for k in range(27):
        e=0
        for j in range(L[k]):
            e+=(1/L[k])*(S[k][j]**2)
        sum_e.append(e)
    tc=[]
    sum_et=[]
    for k in range(27):
        et=0
        j=0
        for t in np.arange(0,3,3/L[k]):
            et+=(t/L[k])*(S[k][j]**2)
            j+=1
        sum_et.append(et)
        if sum_e[k]==0:
            tc.append(1.5/3)
        else:
            tc.append(sum_et[k]/(3*sum_e[k]))
    return tc     

print(temporal_centroid(file1))


# In[23]:



def derivate(filetext):
# spectral difference of matrix S
    with open(filetext) as f:
        mylist = f.read().splitlines()
        for x in range(8):
            mylist.pop(0)
        S=[]
        for element in reversed(mylist):
            element2=[float(i) for i in element.split()]
            S.append(element2) 
    B=[]
    for k in range(27):
        B.append(np.zeros(L[k]-1))
        for j in range(L[k]-1):
            B[k][j]=S[k][j+1]-S[k][j]

    #sum of abs of matrix B
    sum_bin=[]
    for k in range(27):
        sum_tmp=0
        for j in range(L[k]-1):
            sum_tmp += abs(B[k][j])
        sum_bin.append(sum_tmp)
    #print(sum_bin)
    #print(len(sum_bin)) 
    return sum_bin


print(derivate(file1))


# In[24]:



#averaged abs sum of matrix B
def derivate2(filetext):
# spectral difference of matrix S
    with open(filetext) as f:
        mylist = f.read().splitlines()
        for x in range(8):
            mylist.pop(0)
        S=[]
        for element in reversed(mylist):
            element2=[float(i) for i in element.split()]
            S.append(element2)
    B=[]
    for k in range(27):
        B.append(np.zeros(L[k]-1))
        for j in range(L[k]-1):
            B[k][j]=S[k][j+1]-S[k][j]

    #averaged abs sum of matrix B
    avg_sum_bin=[]
    for k in range(27):
        sum_tmp=0
        for j in range(L[k]-1):
            sum_tmp += (1/(L[k]-1))*abs(B[k][j])
        avg_sum_bin.append(sum_tmp)
    #print(avg_sum_bin[0])
    #print(len(avg_sum_bin))
    return avg_sum_bin

print(derivate2(file1))


# In[25]:



#normalized averaged abs sum of matrix B
def derivate_rel(filetext):
# spectral difference of matrix S
    with open(filetext) as f:
        mylist = f.read().splitlines()
        for x in range(8):
            mylist.pop(0)
        S=[]
        for element in reversed(mylist):
            element2=[float(i) for i in element.split()]
            S.append(element2)
        Sk_mean=[]
        for k in range(27):
            sum_s=0
            for j in range(4+2*k):
                sum_s+=S[k][j]
            Sk_mean.append(sum_s/(4+2*k))
    B=[]
    for k in range(27):
        B.append(np.zeros(L[k]-1))
        for j in range(L[k]-1):
            B[k][j]=S[k][j+1]-S[k][j]

    #sum of abs of matrix B
    sum_bin=[]
    for k in range(27):
        sum_tmp=0
        for j in range(L[k]-1):
            sum_tmp += abs(B[k][j])/Sk_mean[k]
        sum_bin.append(sum_tmp/L[k])
    #print(sum_bin)
    #print(len(sum_bin)) 
    return sum_bin

print(derivate_rel(file1))


# In[26]:



#zero crossing rate without excluding zero values
def zerozcr(filetext):
    with open(filetext) as f:
        mylist = f.read().splitlines()
        for x in range(8):
            mylist.pop(0)
        S=[]
        for element in reversed(mylist):
            element2=[float(i) for i in element.split()]
            S.append(element2) 
    B=[]
    for k in range(27):
        B.append(np.zeros(L[k]-1))
        for j in range(L[k]-1):
            B[k][j]=S[k][j+1]-S[k][j]
    count=0
    for k in range(27):
        for j in range(1,L[k]-1):
            if B[k][j]*B[k][j-1]<0:
                count+=1
    return count

print(zerozcr(file1))


# In[27]:



#zero crossing rate with excluding zero values, more accurate 
#with considering two postive and negative values with a zero in between
#use nonzerozcr for following calculation
def nonzerozcr(filetext):
    with open(filetext) as f:
        mylist = f.read().splitlines()
        S=[]
        for x in range(8):
            mylist.pop(0)
        for element in reversed(mylist):
            element2=[float(i) for i in element.split()]
            S.append(element2) 
    B=[]
    for k in range(27):
        B.append(np.zeros(L[k]-1))
        for j in range(L[k]-1):
            B[k][j]=S[k][j+1]-S[k][j]
    count=0
    B_nonzero=[]
    for k in range(27):
        B_nonzero.append(B[k][B[k]!=0])
    for k in range(27):
        for j in range(len(B_nonzero[k])-1):
            if B_nonzero[k][j]*B_nonzero[k][j+1]<0:
                count+=1
    return count

print(nonzerozcr(file1))


# In[28]:



#zero crossing rate with excluding zero values, more accurate 
#with considering two postive and negative values with a zero in between
#use nonzerozcr vector without summing up across frequency bins
def nonzerozcr_list(filetext):
    with open(filetext) as f:
        mylist = f.read().splitlines()
        for x in range(8):
            mylist.pop(0)
        S=[]
        for element in reversed(mylist):
            element2=[float(i) for i in element.split()]
            S.append(element2) 
    B=[]
    for k in range(27):
        B.append(np.zeros(L[k]-1))
        for j in range(L[k]-1):
            B[k][j]=S[k][j+1]-S[k][j]
    
    zcr=[]
    B_nonzero=[]
    for k in range(27):
        B_nonzero.append(B[k][B[k]!=0])
    for k in range(27):
        count=0
        for j in range(len(B_nonzero[k])-1):
            if B_nonzero[k][j]*B_nonzero[k][j+1]<0:
                count+=1
        zcr.append(count)
    return zcr

print(nonzerozcr_list(file1))


# # # Filelist
# 

# In[29]:


#folder_path=os.chdir("/Users/laurentpottier/Documents/LP/Recherches/Projet_Fondation/Langages&Maths/Anaconda/FromNa1/V9-28juin/class/03_Yes_reduced")
#folder_path="/Users/laurentpottier/Documents/LP/Recherches/Projet_Fondation/Langages&Maths/Anaconda/FromNa1/V9-28juin/class/03_Yes_reduced"
folder_path="/Users/laurentpottier/Documents/LP/Recherches/Projet_Fondation/Langages&Maths/Anaconda/LPanalyse/V10LP/PopPlinn/class/PopPlinnTxt"


# folder_path=os.chdir("/Users/Vivo-Na/Downloads/03_Yes_reduced")
filelist = []
for path, dirs, files in os.walk(folder_path):
    for filename in files:
        if 'txt' in filename :
                filelist.append(filename)
#print (filelist)
print(len(filelist))



# In[46]:



times=[]
for i in range(len(filelist)):
    times.append(timetxt(filelist[i]))
print(times)


# # export des donnees

# # # problème avec le tri des fichiers par date, donc on crée une classe pour cela
# 

# In[47]:



class Features:
    def __init__(self, filename, time, filearray, centroid, centre_ecartLow, centre_ecartHigh,sflatness,rms,maxfreq25):
        self.filename = filename
        self.time = time
        self.filearray = filearray
        self.centroid = centroid
        self.centre_ecartLow=centre_ecartLow
        self.centre_ecartHigh=centre_ecartHigh
        self.sflatness=sflatness
        self.rms=rms 
        self.maxfreq25=maxfreq25
 


# In[48]:




feature_objects = []
for file in filelist:
    feature_objects.append(Features(file, timetxt(file), read(file), 
                                    centroid(file),centre_ecartLow(file),centre_ecartHigh(file),
                                    spectral_flatness(file),rms(file),
                                    maxfreq25(file)))
#print("file:",file)
#print("time:",timetxt2(file))
#print("filearray",read(file))
#print("centroid:",centroid(file))
#print("sdLow:",sdLow(file))
#print("sdHigh:",sdHigh(file))
#print("skewness:",skewness(file))
#print("kurtosis:",kurtosis(file))
#print("rms:",rms(file))
#print(centroid_objects)
#print("temporal_centroid",temporal_centroid(file))
#print("derivate",derivate(file))
#print("zcr",nonzerozcr(file))
#print("maxfreq25",maxfreq25(file))



# In[49]:



from operator import itemgetter, attrgetter

times = []
filearrays=[]
centroids = []
centre_ecartLows=[]
centre_ecartHighs=[]
sflatnesses=[]
rmses=[]
maxfreq25s=[]

for obj in sorted(feature_objects, key=attrgetter('time')):
    times.append(obj.time)
    filearrays.append(obj.filearray)
    centroids.append(obj.centroid)
    centre_ecartLows.append(obj.centre_ecartLow)
    centre_ecartHighs.append(obj.centre_ecartHigh)
    sflatnesses.append(obj.sflatness)
    rmses.append(obj.rms)
    maxfreq25s.append(obj.maxfreq25)
    
    


# # # ziplist self similarity matrix

# In[50]:



#for loop for feature extraction
from itertools import *
zip_list=[]
for i in zip(centroids,centre_ecartLows,centre_ecartHighs,sflatnesses,rmses,maxfreq25s):
    zip_list.append(i)
#print("zip_list:",zip_list)


# In[51]:


from sklearn import preprocessing
std_scale = preprocessing.StandardScaler().fit(zip_list)
df_std = std_scale.transform(zip_list)
#print("df_std:",df_std)



# In[52]:



def initialize_clusters(points, k):
    """Initializes clusters as k randomly selected points from points."""
    return points[np.random.randint(points.shape[0], size=k)]



# In[53]:



def get_distances(centroid, points):
    """Returns the distance the centroid is from each data point in points."""
    return np.linalg.norm(points - centroid, axis=1)


# In[54]:



k = 4
maxiter = 50
# Initialize our centroids by picking random data points
centroids = initialize_clusters(df_std, k)
# Initialize the vectors in which we will store the
# assigned classes of each data point and the
# calculated distances from each centroid
classes = np.zeros(df_std.shape[0], dtype=np.float64)
distances = np.zeros([df_std.shape[0], k], dtype=np.float64)

# Loop for the maximum number of iterations
for i in range(maxiter):
    
    # Assign all points to the nearest centroid
    for i, c in enumerate(centroids):
        distances[:, i] = get_distances(c, df_std)
    #print("distances",distances) 
    #print(distances[:,1])
    # Determine class membership of each point
    # by picking the closest centroid
    classes = np.argmin(distances, axis=1)
    #print("classes:",classes)
    # Update centroid location using the newly
    # assigned data point classes
    for c in range(k):
        centroids[c] = np.mean(df_std[classes == c], 0)
    #print("centroids",centroids)



# In[55]:



import pandas as pd
import numpy

df = pd.DataFrame(df_std)

df.columns=['centroid','centre_ecartLow','centre_ecartHigh',
            'sflatness','rms','maxfreq25']
df["classes"]=classes
#print(df)
grouped=df.groupby(["classes"],sort=True)
#print(grouped)
sums=grouped.sum()
#print(sums)


# In[56]:



import plotly
import plotly.graph_objs as go
plotly.offline.init_notebook_mode()
data = [go.Heatmap(z=sums.values.tolist(), 
                   y=['Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3'],
                   x=['centroid',
                      'centre_ecartLow',
                      'centre_ecartHigh',
                      'sflatness','rms','maxfreq25'],
                   colorscale='Viridis')]
plotly.offline.iplot(data, filename='pandas-heatmap')



# In[57]:



import seaborn as sns
sns.set(style="ticks")
sns_plot=sns.pairplot(df, hue="classes")
sns_plot.savefig('df3_spec12.png')




# In[60]:


from mpl_toolkits.mplot3d import Axes3D
group_colors = ['skyblue', 'coral', 'lightgreen', 'red']
colors = [group_colors[j] for j in classes]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df_std[:,0],df_std[:,1],df_std[:,2],df_std[:,3],color=colors, alpha=0.5)
ax.scatter(centroids[:,0], centroids[:,1],centroids[:,2],centroids[:,3],color=['blue', 'darkred', 'green', 'black'], marker='o', lw=2)
ax.set_xlabel('$x_0$')
ax.set_ylabel('$x_1$');
ax.set_ylabel('$x_2$');


# In[62]:



group_colors = ['skyblue', 'coral', 'lightgreen', 'red']
colors = [group_colors[j] for j in classes]

fig, ax = plt.subplots(figsize=(6,6))
ax.scatter(df_std[:,0],df_std[:,1],color=colors, alpha=0.5)
ax.scatter(centroids[:,0], centroids[:,1],color=['blue', 'darkred', 'green'], marker='o', lw=2)
ax.set_xlabel('$x_0$')
ax.set_ylabel('$x_1$');


# # # KNN classification

# In[63]:



def distk(x,y):
    sumdist=0
    for i,j in zip(x,y):
        sumdist+=(i-j)**2
    distk=np.sqrt(sumdist)
    return distk


# In[64]:


def most_common(lst):
    return max(set(lst), key=lst.count)


# In[65]:


# x,test data,X,training data,y training data classes,k,number of classes
def KNN(x,X,y,k):
    x_c=[] 
    for j in range(len(x)):
        order=[]# list of (distance, index) 
        for i in range(len(X)):
            dist=distk(x[j],X[i])
            order.append((dist,i))
        order.sort()
        klass=[]
        for element in order[:k]:
            index = element[1]
            klass.append(y[index])
        x_class=most_common(klass)
        x_c.append(x_class)
    return x_c


# In[66]:


X_train, X_cv, y_train, y_cv = train_test_split(df_std, classes, test_size=0.3, random_state=42)


# In[67]:


print(KNN(X_cv,X_train,y_train,3))


# In[68]:



def getAccuracy(y_test, y_predict):
    correct_sum = 0
    for i in range(len(y_test)):
        if y_test[i] == y_predict[i]:
            correct_sum += 1
    accuracy=correct_sum/float(len(y_test)) * 100.0
    return accuracy


# In[69]:


y_predict=KNN(X_cv,X_train,y_train,6)
getAccuracy(y_cv, y_predict)


# In[70]:



def getBestk(X_train, X_cv, y_train, y_cv):   # cv:cross-validation
    acc=[]
    for k in range(1,10):
        print("progress=",k*100/10,"%")
        y_predict=KNN(X_cv,X_train,y_train,k)
        accuracy=getAccuracy(y_cv,y_predict)
        acc.append((k,accuracy))
    return acc


# In[71]:


getBestk(X_train, X_cv, y_train, y_cv)


# In[72]:




def KNN(x,X,y,k):
    x_c=[] 
    for j in range(len(x)):
        order=[]# list of (distance, index) 
        for i in range(len(X)):
            edist=edDynamic(x[j],X[i])
            order.append((edist,i))
        order.sort()
        klass=[]
        for element in order[:k]:
            index = element[1]
            klass.append(y[index])
        x_class=most_common(klass)
        x_c.append(x_class)
    return x_c

def getAccuracy(y_test, y_predict):
    correct_sum = 0
    for i in range(len(y_test)):
        if y_test[i] == y_predict[i]:
            correct_sum += 1
    accuracy=correct_sum/float(len(y_test)) * 100.0
    return accuracy


#X_train, X_cv, y_train, y_cv = train_test_split(X, y, test_size=0.33, random_state=42)

def getBestk(X_train, X_cv, y_train, y_cv):   # cv:cross-validation
    acc=[]
    for k in range(1,11):
        print("progress=",k*100/10,"%")
        y_predict=KNN(X_cv,X_train,y_train,k)
        accuracy=getAccuracy(y_cv,y_predict)
        acc.append((k,accuracy))
    return acc

def getBestk(X_train, X_cv, y_train, y_cv):   # cv:cross-validation
    acc=[]
    for k in range(1,10):
        print("progress=",k*100/10,"%")
        y_predict=KNN(X_cv,X_train,y_train,k)
        accuracy=getAccuracy(y_cv,y_predict)
        acc.append((k,accuracy))
    return acc


# In[ ]:



#k = np.arange(1,11,1)
#acc = [94,88,76,76,76,76,73,73,73,64]
#plt.plot(k, acc)
#plt.xlabel('number of k')
#plt.ylabel('accuracy(%)')
#plt.title('Find the optimal k')
#plt.grid(True)
#plt.savefig("test.png")
#plt.show()

