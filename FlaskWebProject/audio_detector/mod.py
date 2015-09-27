import numpy
import scipy
from FlaskWebProject.audio_detector import mfcc
import matplotlib.mlab as mlab
import scipy.io.wavfile as wav



# Calculate and Plot Hz spectrogram
# rate: signal sample rate
# noverlap: overlap between each two frames
# Returns the hz spectrum and an axesImage
def hz_spec(signal, rate=44100, nfft=64, overlap=0):
    
    (spec, freqs, bins) = mlab.specgram(signal, NFFT=nfft, Fs=rate, noverlap=0)
    spec = numpy.where(spec==0, numpy.finfo(float).eps, spec)
    
    return spec



#Convert hz spectrum to mel spectrum 
def mel_spec(hz_spec, rate=44100, nbin=40, nfft=64):

    high_mel = mfcc.hz_to_mel(rate/2.0)
    
    #Calculate mel bins
    mel_list = numpy.linspace(0, high_mel, nbin+1)[1:]
    
    #convert values of the mel bins to hz
    hz_list = mfcc.mel_to_hz(mel_list)    

    #Width of each hz bin of the hz spectrum
    hz_unit = (rate/2.0)/(nfft/2.0+1)
     
    mel_spec = []
    mel_spec.append(hz_spec[0].tolist())
    
    for i in range(1, len(hz_list)): 
        
        # Get hz bins belong to the same mel bin
        start = int(numpy.floor(hz_list[i-1]/float(hz_unit)))
        end = int(numpy.floor(hz_list[i]/float(hz_unit)))+1
        
        mel_bin = []
        hz_bins = hz_spec[start:end,:].T

        #calculate the values in the mel bin
        for x in range(0, len(hz_bins)):
            mel_bin.append(numpy.mean(hz_bins[x])) 
    
        mel_spec.append(mel_bin)
    
    return mel_spec





# Apply FFT over spectrum bins
# spec: hz or mel spectrum
# nsample: number of bins in the spectrum
def linear_mod(spec, nsample):
    
    mod = numpy.absolute(numpy.fft.fft(spec.T, int(numpy.floor(nsample)), axis=0))
    mod = mod[:nsample/float(2)+1,:]
    mod = numpy.where(mod==0, numpy.finfo(float).eps, mod)
    
    return mod



#Calculate mean, standard deviation and max 
def msm(data):
    me = numpy.mean(data, axis=0)
    std = numpy.std(data, axis=0)
    mx = numpy.max(data, axis=0)
    
    return (me, std, mx)



# Build log bins
# mod_n: number of modulation coefficients
# nbin: number of log bins to build
def log_bins(mod_n, nbin=48, min_freq=1/float(60), max_freq=344.0):
    
    #frequecies of the linear bins
    freqs_arr = numpy.linspace(0, max_freq, mod_n)[1:]
    
    #make nbin equal spaces in the log frequency space 
    low_freq = numpy.log10(min_freq)
    high_freq = numpy.log10(max_freq)

    bin_freqs = numpy.power(10.0, numpy.linspace(low_freq, high_freq, nbin-1))

    interp_bins = numpy.int32(numpy.around(numpy.interp(bin_freqs,
                                                        freqs_arr,
                                                        numpy.linspace(1, mod_n-1, mod_n-1))))

    return interp_bins



#Map linear bins to log bins
def bin_mapping(interp_bins, nbin=48):
    
    bin_map = []
    bin_map.append([0])
    bin_map.append([interp_bins[0]])

    for i in range(1, nbin-1):
        lasti = interp_bins[i-1]
        thisi = interp_bins[i]

        if thisi == lasti:
            bin_map.append([thisi])
        else:
            bin_map.append(numpy.linspace(lasti+1, thisi, thisi-lasti).tolist())
            
    return bin_map



#Put linear bins into corresponding log bins
#Take the average if a log bin contains multiple linear bins
def log_mod(mod, mod_n=10336, min_freq=1/float(60), max_freq=344, nbin=48):
    
    interp_bins = log_bins(mod_n, nbin)
    bin_map = bin_mapping(interp_bins, nbin)
    
    logmod = []
    
    for i in range(0, nbin):
    
        start = int(bin_map[i][0])  #first element in the log bin, a index of linear bin
        end = int(bin_map[i][-1]+1)
        
        logbin = numpy.mean(mod[start:end,:], axis=0).tolist()
        
        logmod.append(logbin)
        
    return numpy.array(logmod)







