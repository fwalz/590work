
# coding: utf-8

# In[2]:


from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
#matplotlib.rcParams.update({'font.size': 22})
import statistics 
#Fourier Transform
from scipy.fftpack import fft

#figure size


#N=Number of points
N=200
#This is my "base" array, also the "pure signal" I will add the noise to this array
basearray=N*[float(100)]

#This is how I will generate "noise" in my signals
#Max value of error
errormax=15
noise1=np.random.normal(0, errormax, N)

#Pump array
array1=basearray+noise1
mean1=statistics.mean(array1)
stdev1=statistics.stdev(array1)
roundedstdev1=round(stdev1,3)
roundedmean1=str(round(mean1,3))
print(f"The standard deviation of array1 (Pump) is {roundedstdev1} and the mean is {roundedmean1}")

#The second array- probe
noise2=np.random.normal(0, errormax, N)
#print(noise1)
array2=basearray+noise2
mean2=statistics.mean(array2)
stdev2=statistics.stdev(array2)
roundedstdev2=round(stdev2,3)
roundedmean2=str(round(mean2,3))
print(f"The standard deviation of array2 (Probe) is {roundedstdev2} and the mean is {roundedmean2}")

#I want a pulse (point in array) at 1ms, this is my time array
pulsewidth=0.001
t1ms=np.arange(0., N*pulsewidth, pulsewidth)

#Pump plot
plt.figure(figsize=(13,8))
plt.tick_params(labelsize=16)
plt.ylabel('Signal')
plt.xlabel('Time (s)')
plt.title("Pump array " +r'$\mu$='+str(round(stdev1,3))+", " "mean="+str(round(mean1,3)))
plt.plot(t1ms,array1)
plt.show()

#Probe plot
plt.figure(figsize=(13,8))
plt.tick_params(labelsize=16)
plt.ylabel('Signal')
plt.xlabel('Time (s)')
plt.title("Probe array " +r'$\mu$='+str(round(stdev2,3))+", " "mean="+str(round(mean2,3)))
plt.plot(t1ms,array2)
plt.show()

#Adding probe and pump + signal 
total=array1+array2

#I realize that we will just get the basearray if we do total-array1-array2
#How do I solve this problem?


#Here I assumed that the pump and the probe are the basearrays so I can preserve the uncertanties.
signal1=total-basearray
meansignal1=statistics.mean(signal1)
stdevsignal1=statistics.stdev(signal1)
roundedstdevsignal1=round(stdevsignal1,3)
roundedmeansignal1=str(round(meansignal1,3))
print(f"The standard deviation of signal1 (Pump + Probe - Inital Signal) is {roundedstdevsignal1} and the mean is {roundedmeansignal1}")


# In[11]:


#######################################################################################################################

#time axis is from the above code
#initally I used a 1ms pulse for N points
#pulsewidth=0.001
#t1ms=np.arange(0., N*pulsewidth, pulsewidth)

#Frequency in Hz (for general squarewave)
f1=100

#This
#signal.square(2*np.pi*f1*t1ms)
#gives me a square wave that goes from -1 to 1 but I want a wave from 0 to 1
squarewavef= 1/2*(signal.square(2*np.pi*f1*t1ms)+abs(signal.square(2*np.pi*f1*t1ms)))

#Modulating the pump 
# Frequency for pump in squarewave
fpump=100
deltatpump=0
squarewavepump= 1/2*(signal.square(2*np.pi*fpump*t1ms+deltatpump)+abs(signal.square(2*np.pi*fpump*t1ms+deltatpump)))
modpump=squarewavepump*array1
plt.figure(figsize=(13,8))
plt.tick_params(labelsize=16)
plt.ylabel('Signal')
plt.xlabel('Time (s)')
plt.title("Pump Signal * Square Wave with "+r'$\Delta$t='+str(deltatpump)+", f="+str(fpump)+"Hz")
plt.plot(t1ms,modpump)
plt.show()

#Modulating the probe 
# Frequency for pump in probe squarewave
fprobe=50
deltatprobe=0
squarewaveprobe= 1/2*(signal.square(2*np.pi*fprobe*t1ms+deltatprobe)+abs(signal.square(2*np.pi*fprobe*t1ms+deltatprobe)))
modprobe=squarewaveprobe*array2
plt.figure(figsize=(13,8))
plt.tick_params(labelsize=16)
plt.ylabel('Signal')
plt.xlabel('Time (s)')
plt.title("Probe Signal * Square Wave with "+r'$\Delta$t='+str(deltatprobe)+", f="+str(fprobe)+"Hz")
plt.plot(t1ms,modprobe)
plt.show()

#Adding the two modulated pulses 
modsignal=modpump+modprobe
#Here I am mulitplying by the sin(fpump-fprobe+(sum of deltaTs))
modsignal2=modsignal*np.sin((fpump-fprobe)*2*np.pi*t1ms+(deltatpump+deltatprobe))
plt.figure(figsize=(13,8))
plt.tick_params(labelsize=16)
plt.ylabel('Signal')
plt.xlabel('Time (s)')
plt.subtitle("Pump + Probe", fontsize=16)
plt.plot(t1ms,modsignal)
plt.show()


