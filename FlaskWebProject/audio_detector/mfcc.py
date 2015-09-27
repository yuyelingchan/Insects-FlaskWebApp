import math
import numpy
import scipy.fftpack



# Split signal into frames
# Returns the frames in a 2d array
def sig_frame(signal, frame_len=512, noverlap=256):

    sig_len = len(signal)
    frame_len = int(numpy.round(frame_len))
    frame_step = int(numpy.round(frame_len-noverlap))
       
    #calculate number of frames
    if sig_len <= frame_len:
        frame_num = 1
    else:
        frame_num = 1 + int(math.ceil((sig_len-frame_len)/float(frame_step)))
                       
    #add zeros to the end of the signal if the length of the signal is shorter than (frame_num*frame_len)
    total_len = frame_len + (frame_num-1)*frame_step
 
    pad_len = total_len - sig_len
    zeros = numpy.zeros(pad_len)
    
    pad_sig = numpy.concatenate((signal,zeros))
    
    
    #indices of the signal samples
    indices = numpy.tile(numpy.arange(0,frame_len), (frame_num,1)) +\
                         numpy.tile(numpy.arange(0,frame_num*frame_step,frame_step),(frame_len,1)).T
    indices= numpy.array(indices, dtype = numpy.int32)
    
    return pad_sig[indices]



# Apply a window function to the frames
def windowing(frames, win_func=lambda x:numpy.ones((1,x))):
   
    win = numpy.tile(win_func(len(frames[0])),(len(frames),1))
    return frames*win



# Calculate power spectrum
# NFFT: fft window size
def power_spec(frames, NFFT):
    
    fft_arr = numpy.fft.rfft(frames,NFFT)
    pspec = 1.0 / float(NFFT * numpy.square(numpy.absolute(fft_arr)))
    pspec = numpy.where(pspec==0, numpy.finfo(float).eps, pspec)
    return pspec



# Convert frequency to mel
def hz_to_mel(freq):
    return 2259*numpy.log10(1+ freq/700.0)

# Convert mel to frequency
def mel_to_hz(mel):
    return 700*(10**(mel/2259.0) -1)



# Build filter bank
def filter_bank(rate=44100, NFFT=64,filter_num=26, low_freq=0, high_freq=22050):

    #Calculate mel bins
    low_mel = hz_to_mel(low_freq)
    high_mel = hz_to_mel(high_freq)

    mel_arr = numpy.linspace(low_mel,high_mel,filter_num+2)

    # Calculate fft bins
    bin_arr = numpy.floor(((NFFT + 1)* (mel_to_hz(mel_arr)))/float(rate))

    # Calculate values of the filters
    filterbank = numpy.zeros([filter_num,NFFT/2+1])
    for i in range(0,filter_num):
        for j in range(int(bin_arr[i]),int(bin_arr[i+1])):
            filterbank[i,j] = (j- bin_arr[i])/float((bin_arr[i+1]-bin_arr[i]))

        for j in range(int(bin_arr[i+1]),int(bin_arr[i+2])):
            filterbank[i,j] = (bin_arr[i+2] - j)/float((bin_arr[i+2] - bin_arr[i+1]))

    return filterbank



# Calculate mel spectrum
def mel_spec(filterbank, power_spec):

    mspec = numpy.dot(power_spec,filterbank.T)   
    # We may need to calculate log, make sure there is no zero
    mspec = numpy.where(mspec==0, numpy.finfo(float).eps, mspec)
    
    return mspec



# Calculate logged mel spectrum
def log_spec(mel_spec):
    return numpy.log(mel_spec)




# Calculate dct cepstrum coefficient
# ncoe: number of coefficients to keep
def dct_ceps(spec,ncoe = 13):
    return scipy.fftpack.dct(spec.T)[:,:ncoe+1]







