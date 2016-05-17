Title: Deep Learning Setup
Date: 2016-05-15
Category: Deep Learning
Tags: python, cuda, theano, caffe
Author: TDB
Summary: Instructions to setup common deep learning tools on Ubuntu 14.04
hese instructions are for Linux (Ubuntu) based but should be adaptable to other distros without too much work


# First make sure Ubuntu is up to date

	sudo apt-get update  
	sudo apt-get upgrade  
	sudo apt-get install build-essential  
	sudo apt-get autoremove

# Install gfortran (to compile OpenBlas)

    sudo apt-get install gfortran  

# Configure OpenBlas for fast linear algebra operations

    cd git  
    git clone https://github.com/xianyi/OpenBLAS  
    cd OpenBLAS  
    make FC=gfortran  
    sudo make PREFIX=/usr/local install


# The tricky bit: getting your GPU up and running

### First verify your GPU is nVidia compatible

	lspci | grep -i nvidia

You should see something like

	03:00.0 3D controller: NVIDIA Corporation GM108M [GeForce 830M] (rev ff)

In my case, a GeForce 830M which is CUDA compatible: perfect !

Next we should make sure the drivers are up to date:

	sudo add-apt-repository ppa:graphics-drivers/ppa
	sudo apt-get update
	sudo apt-get install nvidia-352

This is the official repository which should be safe to add to your PPA list. There are newer drivers but this one is the recommended one. Restart your system afterwards.

Next step: configuring CUDA

### Install cuda

Go to 

    https://developer.nvidia.com/cuda-downloads

Select distribution and follow the instructions in the guide to set up CUDA. The guide is long because it deals with multiple Unix distributions. The core instructions are actually pretty limited.

Points you should pay attention to:

- For some Unix distributions it is crucial to disable the nouveau drivers which may conflict with the nVidia ones.
- Make sure to add CUDA to your `.bashrc` or `.zshrc`

The instructions for the last point are in the guide but let's paste them here for completeness:

	echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
	echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
	source ~/.bashrc

The guide also gives you the opportunity to test your CUDA installation by compiling some examples. Compile them with:

	/usr/local/cuda/bin/cuda-install-samples-7.5.sh ~/cuda-samples
	cd ~/cuda-samples/NVIDIA*Samples
	make -j $(($(nproc) + 1))

The $(($(nproc) + 1)) statement uses all the available cores on your machines to compile faster.

Next step is to install CuDNN.


### Install CUDNN

Go to 

    https://developer.nvidia.com/cudnn

Register, download and extract files
Currently (Apr 2016), theano is not up to date with the latest cuda (cudnn v5) so for now, use cudnn v4.

A `<extractionpath>/cuda` is created
Copy the contents of the /cuda folder to your cuda installation repository
On Ubuntum this should be :

    cd <extractionpath>cuda
    sudo cp lib64/* /usr/local/cuda/lib64/
    sudo cp include/cudnn.h /usr/local/cuda/include/


If everything's working fine, you can move on to the next step: configuring python for scientific computing.

# Configure python

### Download anaconda

The Anaconda distribution has most libraries of interest and can super easily be set up on Linux, Windows and Mac:

Go to 

    https://www.continuum.io/downloads

Download the binaries and run

    bash Anaconda-x.y.z-Linux-x86_64.sh (Linux)  

### Install pip

    conda install pip

### Install the optional pydot

    pip install pydot

You may have to change your version of pyparser if you get an error message.

Now let's move on to deep learning libraries. We'll start with theano.

# Theano installation

### Install bleeding edge theano

    pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git

### Configure theano with a .theanorc file

In your home directory, create a `.theanorc` file in which you'll put the following:

    [global]
    device = gpu  
    floatX = float32

    [blas]
    ldflags = -L/usr/local/lib -lopenblas

    [nvcc]
    fastmath = True

    [cuda]
    root = /usr/lib/nvidia-cuda-toolkit

    [dnn.conv]
    algo_bwd_filter = deterministic
    algo_bwd_data = deterministic


The last flag may slow down the computations but allows deterministic results. To get faster convolutions, you should set it to:

	[dnn.conv]
	algo_fwd = time_once
	algo_bwd_data = time_once

### Check theano sees cudnn

    >>> from theano.sandbox.cuda.dnn import *
    Using gpu device 0: Quadro K620 (CNMeM is disabled, CuDNN 4007)
    >>> print dnn_available()
    True
    >>> print dnn_available.msg
    None
    >>> 

### Theano test script

Run this script to make sure theano can use the GPU/CPU normally


```python
from theano import function, config, shared, sandbox  
import theano.tensor as T  
import numpy  
import time

vlen = 10 * 30 * 768  # 10 x #cores x # threads per core  
iters = 1000

rng = numpy.random.RandomState(22)  
x = shared(numpy.asarray(rng.rand(vlen), config.floatX))  
f = function([], T.exp(x))  
print f.maker.fgraph.toposort()  
t0 = time.time()  
for i in xrange(iters):  
    r = f()
t1 = time.time()  
print 'Looping %d times took' % iters, t1 - t0, 'seconds'  
print 'Result is', r  
if numpy.any([isinstance(x.op, T.Elemwise) for x in f.maker.fgraph.toposort()]):  
    print 'Used the cpu'
else:  
    print 'Used the gpu'

### You can enable CNMeM with 

    [lib]
    cnmem = 0.01

in the `.theanorc` file

The value represents the start size (either in MB or the fraction of total GPU memory) of the memory pool. If more memory is needed, Theano will try to obtain more, but this can cause memory fragmentation.
 
###  Check speed of theano/OpenBlas

	python `python -c "import os, theano; print os.path.dirname(theano.__file__)"`/misc/check_blas.py

This will run some tests ans you can compare the speed of your setup with different reference setups

### Run some tests (optional and very slow...)

    NumPy (~30s): python -c "import numpy; numpy.test()"
    SciPy (~1m): python -c "import scipy; scipy.test()"
    Theano (~30m): python -c "import theano; theano.test()"
 
### In case of an error message dealing with theano cache:
 
	rm -rf $HOME/.theano


Now let's setup Caffe, which is somewhat more involved

# Caffe installation

### General dependencies

	sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev
	sudo apt-get install libopencv-dev libhdf5-serial-dev protobuf-compiler
	sudo apt-get install --no-install-recommends libboost-all-dev
	sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev

If an error is thrown with the boost library do :

	sudo apt-get --purge remove libboost-all-dev libboost-dev libboost-doc
	sudo apt-get install -f
	sudo dpkg --configure -a
	sudo apt-get clean
	sudo apt-get update
	sudo apt-get install libboost1.54-dev

Then relaunch the commands to install general dependencies

### Get caffe

	git clone https://github.com/BVLC/caffe.git

	cp Makefile.config.example Makefile.config
	# Adjust Makefile.config 
	# (See example at the end of this post)

You should especially pay attention to the anaconda part, the opencv part, the use CUDNN part.
If you have openblas installed, replace 

	Blas := atlas to
	BLAS := open

Then:

	make all -j $(($(nproc) + 1))
	make pycaffe -j $(($(nproc) + 1))
	make test -j $(($(nproc) + 1))
	make runtest -j $(($(nproc) + 1))


More often than not, you may run into errors during comilation. Here are a few gotchas I've dealt with:

### Conflict with HDF5

Add anaconda2 to the lib path to link the proper hdf5 library. Also add the `x86_64-linux-gnu` path.
In your `.bashrc`:

	export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/tmain/anaconda2/lib
	export LD_LIBRARY_PATH=/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
	export PYTHONPATH=~/caffe/python:$PYTHONPATH

### Getting pycaffe to work :

In the folder `caffe/python` install all the requirements

	for req in $(cat requirements.txt); do pip install $req; done

Then export python path :
In your `.basrhc` file :

	export PYTHONPATH=<caffe-home>/python:$PYTHONPATH

### My Makefile.config for Caffe

	## Refer to http://caffe.berkeleyvision.org/installation.html
	# Contributions simplifying and improving our build system are welcome!

	# cuDNN acceleration switch (uncomment to build with cuDNN).
	USE_CUDNN := 1

	# CPU-only switch (uncomment to build without GPU support).
	# CPU_ONLY := 1

	# uncomment to disable IO dependencies and corresponding data layers
	# USE_OPENCV := 0
	# USE_LEVELDB := 0
	# USE_LMDB := 0

	# uncomment to allow MDB_NOLOCK when reading LMDB files (only if necessary)
	#	You should not set this flag if you will be reading LMDBs with any
	#	possibility of simultaneous read and write
	# ALLOW_LMDB_NOLOCK := 1

	# Uncomment if you're using OpenCV 3
	OPENCV_VERSION := 3

	# To customize your choice of compiler, uncomment and set the following.
	# N.B. the default for Linux is g++ and the default for OSX is clang++
	# CUSTOM_CXX := g++

	# CUDA directory contains bin/ and lib/ directories that we need.
	CUDA_DIR := /usr/local/cuda
	# On Ubuntu 14.04, if cuda tools are installed via
	# "sudo apt-get install nvidia-cuda-toolkit" then use this instead:
	# CUDA_DIR := /usr

	# CUDA architecture setting: going with all of them.
	# For CUDA < 6.0, comment the *_50 lines for compatibility.
	CUDA_ARCH := -gencode arch=compute_20,code=sm_20 \
				-gencode arch=compute_20,code=sm_21 \
				-gencode arch=compute_30,code=sm_30 \
				-gencode arch=compute_35,code=sm_35 \
				-gencode arch=compute_50,code=sm_50 \
				-gencode arch=compute_50,code=compute_50

	# BLAS choice:
	# atlas for ATLAS (default)
	# mkl for MKL
	# open for OpenBlas
	BLAS := open
	# Custom (MKL/ATLAS/OpenBLAS) include and lib directories.
	# Leave commented to accept the defaults for your choice of BLAS
	# (which should work)!
	# BLAS_INCLUDE := /path/to/your/blas
	# BLAS_LIB := /path/to/your/blas

	# Homebrew puts openblas in a directory that is not on the standard search path
	# BLAS_INCLUDE := $(shell brew --prefix openblas)/include
	# BLAS_LIB := $(shell brew --prefix openblas)/lib

	# This is required only if you will compile the matlab interface.
	# MATLAB directory should contain the mex binary in /bin.
	# MATLAB_DIR := /usr/local
	# MATLAB_DIR := /Applications/MATLAB_R2012b.app

	# NOTE: this is required only if you will compile the python interface.
	# We need to be able to find Python.h and numpy/arrayobject.h.
	# PYTHON_INCLUDE := /usr/include/python2.7 \
	# 		/usr/lib/python2.7/dist-packages/numpy/core/include
	# Anaconda Python distribution is quite popular. Include path:
	# Verify anaconda location, sometimes it's in root.
	ANACONDA_HOME := $(HOME)/anaconda2
	PYTHON_INCLUDE := $(ANACONDA_HOME)/include \
			$(ANACONDA_HOME)/include/python2.7 \
			$(ANACONDA_HOME)/lib/python2.7/site-packages/numpy/core/include \

	# Uncomment to use Python 3 (default is Python 2)
	# PYTHON_LIBRARIES := boost_python3 python3.5m
	# PYTHON_INCLUDE := /usr/include/python3.5m \
	#                 /usr/lib/python3.5/dist-packages/numpy/core/include

	# We need to be able to find libpythonX.X.so or .dylib.
	# PYTHON_LIB := /usr/lib
	PYTHON_LIB :=/home/tmain/anaconda2/lib

	# Uncomment to support layers written in Python (will link against Python libs)
	WITH_PYTHON_LAYER := 1

	# Whatever else you find you need goes here.
	INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include
	LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib

	# If Homebrew is installed at a non standard location 
	# (for example your home directory) 
	# and you use it for general dependencies
	# INCLUDE_DIRS += $(shell brew --prefix)/include
	# LIBRARY_DIRS += $(shell brew --prefix)/lib

	# Uncomment to use `pkg-config` to specify OpenCV library paths.
	# (Usually not necessary -- OpenCV libraries 
	# are normally installed in one of the above $LIBRARY_DIRS.)
	# USE_PKG_CONFIG := 1

	BUILD_DIR := build
	DISTRIBUTE_DIR := distribute

	# Uncomment for debugging. 
	# Does not work on OSX due to https://github.com/BVLC/caffe/issues/171
	# DEBUG := 1

	# The ID of the GPU that 'make runtest' will use to run unit tests.
	TEST_GPUID := 0

	# enable pretty build (comment to see full commands)
	Q ?= @