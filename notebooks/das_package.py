import glob
import os
import wget
import datetime
from datetime import datetime
import h5py
from nptdms import TdmsFile
import dask.array as da
import numpy as np
import matplotlib.pyplot as plt




plt.rc('font', size=20)          # controls default text sizes
# plt.rc('axes', titlesize=10)     # fontsize of the axes title
# plt.rc('axes', labelsize=10)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=20)    # fontsize of the tick labels
plt.rc('ytick', labelsize=20)    # fontsize of the tick labels
# plt.rc('figure', titlesize=10)  # fontsize of the figure title





def find_time_url(url, interrogator):

    if interrogator == "Optasense":
        data_format = "Z.h5"
        factor = 0
    elif interrogator == "Silixa":
        data_format = ".tdms"
        factor = 4

    # Find the index of ".h5"
    index = url.find(data_format)
    # Get the 6 characters before the index
    if index >= 6:
        result = url[index-6-factor:index-factor]
    else:
        result = url[:index]  # If there are less than 6 characters before ".h5"

    return result




def dl_file(folder, url):
    """Download the file at the given url
    Parameters
    ----------
    folder : string
        the folder of the file
    url : string
        url location of the file
    Returns
    -------
    filepath : string
        local path destination of the file
    """
    filename = url.split('/')[-1]
    filepath = os.path.join(folder, filename)
    if os.path.exists(filepath) == True:
        print(f'{filename} already stored locally')
    else:
        # Create the data subfolder if it doesn't exist
        os.makedirs(folder, exist_ok=True)
        wget.download(url, out=folder, bar=wget.bar_adaptive)
        print(f'Downloaded {filename}')
    return filepath, filename




def dl_das_files(folder, url, first_file_time, file_timing_length, n):

    """Download the DAS files
    Parameters
    ----------
    folder : string
        the folder of the file
    url : string
        url location of the file
    first_file_time: int
        minites and seconds of the first file
    file_timing_length: int
        length of each file in second
    n: int
        number of files

    Returns
    -------
    files_names : list
        list of the files names
    """

    m = int(first_file_time)
    
    for i in range(n):
        if m%100 >= 60:
            m += 40
        if m%10000 >= 6000:
            m += 4000
        if m-240000 >= 0:
            m = m-240000
            index = url.find(first_file_time)
            day = int(url[index-2])
            new_day = day + 1
            url = url[:index-2] + f'{new_day}' + url[index-1:]


        if m<10:
            new_first_file_time = f"00000{int(m)}"
        elif m<100:
            new_first_file_time = f"0000{int(m)}"
        elif m<1000 and m>=100:
            new_first_file_time = f"000{int(m)}"
        elif m<10000 and m>=1000:
            new_first_file_time = f"00{int(m)}"
        elif m<100000 and m>=10000:
            new_first_file_time = f"0{int(m)}"
        else:
            new_first_file_time = f"{int(m)}"

        new_url = url.replace(first_file_time, new_first_file_time)

        dl_file(folder, new_url)
        m += file_timing_length

    files_names = glob.glob(f"{folder}/*")

    return files_names




def optasense(filenames):
    """Loading the Optasense files from the local storage and concatenating them together using Dask array

    Parameters
    ----------
    filenames : list
        such as filenames = ['file1', 'file2', ...]. The elements of the list should be str

    Returns
    -------
    rawData : dask array
        [0:nnx, 0:nns]
    
    dt: float
        time step (micro sec)
    
    fs: float
        sampling rate (Hz)

    dx: float
        channel spacing

    nx: int
        number of channels

    ns: int
        number of samples in each channel

    L: float
        gauge length in m

    sf: float
        scale factor

    rawDataTime[0]: datetime
        the starting time of the data
    """

    #Loading the files in dask array
    dask_arrays = []
    for fn in filenames:
        fp = h5py.File(fn,'r')
        d = fp['Acquisition']['Raw[0]']['RawData']
        array = da.from_array(d, chunks=(1000, 1000))
        dask_arrays.append(array)

    # concatenate arrays along first axis
    rawData = da.concatenate(dask_arrays, axis=1)

    print(f"The concatenated data shape: {rawData.shape}")

    fpath = filenames[0]
    fp = h5py.File(fpath,'r')
    rawDataTime = fp['Acquisition']['Raw[0]']['RawDataTime']
    print('The first value in \"RawDataTime\" is',rawDataTime[0],\
        'which is the timestamp of the first sample in microseconds.')
    print('This equates to the date and time',datetime.utcfromtimestamp(rawDataTime[0]*1e-6))

    dt = (rawDataTime[1] - rawDataTime[0])/1000
    print('the time step is equal to = ', dt*1000, 'microsecond')

    # sampling rate in Hz
    fs = fp['Acquisition']['Raw[0]'].attrs['OutputDataRate']
    print('\nsampling rate in Hz = ', fs)
    # channel spacing in m
    dx = fp['Acquisition'].attrs['SpatialSamplingInterval'] 
    print('channel spacing in m = ', dx)
    # number of channels
    nx = fp['Acquisition']['Raw[0]'].attrs['NumberOfLoci'] 
    print('number of channels = ', nx)
    # number of samples
    ns = fp['Acquisition']['Raw[0]']['RawDataTime'].attrs['Count'] * len(filenames)
    print('number of samples in each channel = ', ns)
    # gauge length in m
    L = fp['Acquisition'].attrs['GaugeLength'] 
    print('gauge length in m = ', L)

    # refractive index
    n = fp['Acquisition']['Custom'].attrs['Fibre Refractive Index'] 
    sf = (2*np.pi)/2**16 * (1550.12 * 1e-9)/(0.78 * 4 * np.pi * n * L)

    starting_time = rawDataTime[0]

    return rawData, dt, fs, dx, nx, ns, L, sf, starting_time




def silixa(filenames):
    """Loading the Optasense files from the local storage and concatenating them together using Dask array

    Parameters
    ----------
    filenames : list
        such as filenames = ['file1', 'file2', ...]. The elements of the list should be str

    Returns
    -------
    rawData : dask array
        [0:nnx, 0:nns]
    
    dt: float
        time step (micro sec)
    
    fs: float
        sampling rate (Hz)

    dx: float
        channel spacing

    nx: int
        number of channels

    ns: int
        number of samples in each channel

    L: float
        gauge length in m

    sf: float
        scale factor

    rawDataTime[0]: datetime
        the starting time of the data
    """

    #Loading the files in dask array
    dask_arrays = []
    for fn in filenames:
        fp = TdmsFile.read(fn)
        group = fp['Measurement']
        d = np.asarray( [group[channel].data for channel in group] )
        array = da.from_array(d, chunks=(1000, 1000))
        dask_arrays.append(array)

    # concatenate arrays along first axis
    rawData = da.concatenate(dask_arrays, axis=1)

    print(f"The concatenated data shape: {rawData.shape}")

    fpath = filenames[0]
    fp = TdmsFile.read(fpath)
    group = fp['Measurement']
    acousticData = np.asarray( [group[channel].data for channel in group] )
    props = fp.properties
    print(props)
    startTime_utc = props['GPSTimeStamp']
    startTime_utc = startTime_utc.astype(float)
    startTime_timestamp = int(startTime_utc)
    startTime_utc = datetime.utcfromtimestamp(startTime_timestamp*1e-6)

    print('The first value in \"RawDataTime\" is',startTime_timestamp,\
        'which is the timestamp of the first sample in microseconds.')
    print('This equates to the date and time',startTime_utc)

    # sampling rate in Hz
    fs = props['SamplingFrequency[Hz]']
    print('\nsampling rate in Hz = ', fs)
    # Time step
    dt = (1/fs)*1000
    print('the time step is equal to = ', dt*1000, 'microsecond')
    # channel spacing in m
    dx = props['SpatialResolution[m]']
    print('channel spacing in m = ', dx)
    # number of channels
    nx = acousticData.shape[0] 
    print('number of channels = ', nx)
    # number of samples
    ns = acousticData.shape[1] * len(filenames)
    print('number of samples in each channel = ', ns)
    # gauge length in m
    L = props['GaugeLength']
    print('gauge length in m = ', L)

    # refractive index
    sf = (116 * fs * 10**-9) / (L * 2**13)

    starting_time = startTime_timestamp

    return rawData, dt, fs, dx, nx, ns, L, sf, starting_time




def chunk_load(rawData, channels_chunk, time_chunk, dt, fs, dx, sf, starting_time):
    """This function put the specified chunk of the data in an numpy array

    Parameters
    ----------
    rawData : dask array
        [0:number of channels, 0:number of samples in one channel]

    channels_chunk : list
        [chmin, chmax, chint]

    time_chunk : list
        [tmin, tmax, tint]

    sf : float
        scale factor

    fs : int
        sampling rate (Hz)

    starting_time: datetime timestamp
        the starting time of the data

    Returns
    -------
    trace : numpy array
        [chmin:chmax:chint, tmin:tmax:tint]

    dist: array
        an array for distance axis of the trace

    time: array
        an array for time axis of the trace

    starting_time: datetime utc
        the starting time of the data
    """

    chmin, chmax, chint = channels_chunk
    tmin, tmax, tint = time_chunk

    trace = rawData[chmin:chmax:chint,tmin:tmax:tint]
    nnx = trace.shape[0]
    nns = trace.shape[1]
    # mn = np.tile(np.mean(trace,axis=1),(nns,1)).T
    trace = trace - np.mean(trace, axis=1, keepdims=True)
    trace *= sf
    trace = trace.compute()

    dist = (np.arange(chmin, chmax, chint))*dx
    time = np.arange(0, tmax-tmin, tint)/fs

    starting_time = datetime.utcfromtimestamp((starting_time + tmin*dt*1e3)*1e-6)

    return trace, dist, time, starting_time




def strain2strainrate(data, dt, tint):
    """This function put the specified chunk of the data in an numpy array

    Parameters
    ----------
    rawData : numpy array in strain
        

    dt: float
        time step (micro sec)


    Returns
    -------
    str_rate : numpy array in strain rate

    """

    str_rate = np.gradient(data, axis=1)
    str_rate = str_rate/(dt*tint/1000)

    return str_rate




def plot_tx(trace, time, dist, file_begin_time_utc=0, fig_size=(12, 10), v_min=None, v_max=None):
    """
    Spatio-temporal representation (t-x plot) of the strain data

    Inputs:
    :param trace: a [channel x time sample] nparray containing the strain data in the spatio-temporal domain
    :param time: the corresponding time vector
    :param dist: the corresponding distance along the FO cable vector
    :param file_begin_time_utc: the time stamp of the represented file
    :param fig_size: Tuple of the figure dimensions. Default fig_size=(12, 10)
    :param v_min: sets the min nano strain amplitudes of the colorbar. Default v_min=0
    :param v_max: sets the max nano strain amplitudes of the colorbar, Default v_max=0.2

    Outputs:
    :return: a tx plot

    """

    fig = plt.figure(figsize=fig_size)
    # determine if the envelope should be implemented here rather than just abs
    # Replace abs(trace) per abs(sp.hilbert(trace, axis=1)) ? 
    shw = plt.imshow(abs(trace.T) * 10 ** 9, extent=[dist[0] * 1e-3, dist[-1] * 1e-3, time[0], time[-1]], aspect='auto',
                     origin='lower', cmap='jet', vmin=v_min, vmax=v_max)
    plt.xlabel('Distance (km)')
    plt.ylabel('Time (s)')
    plt.tick_params(axis='both', which='major', pad=15)
    bar = fig.colorbar(shw, aspect=30, pad=0.015)
    bar.set_label('Strain Rate Envelope (x$10^{-9}$)')

    # if isinstance(file_begin_time_utc, datetime):
    #     plt.title(file_begin_time_utc.strftime("%Y-%m-%d %H:%M:%S"), loc='right')
    plt.tight_layout()
    # plt.show()