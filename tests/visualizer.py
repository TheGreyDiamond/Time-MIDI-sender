#import the pyplot and wavfile modules 

import matplotlib.pyplot as plot

from scipy.io import wavfile

 

# Read the wav file (mono)

samplingFrequency, signalData = wavfile.read('Eyes_of_Glory.wav')

 

# Plot the signal read from wav file

plot.subplot(211)

plot.title('Spectrogram of a wav file')

 

plot.plot(signalData)

plot.xlabel('Sample')

plot.ylabel('Amplitude')
print(plot.xlim())
plot.xlim(10000,80000)
plot.show()
