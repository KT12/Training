## Comments and tips on installing Tensorflow with GPU support

The purpose of this document is to ease the building of Tensorflow from source for others and to have a document to fall back on in case I need to rebuild it again.  Both the TF and NVIDIA CUDA/cuDNN installs hit some bumps in the road.  I also deviated from the standard instructions in order to make things work.

### System specifications
* OS: Ubuntu 16.04 LTS
* CPU: Intel® Core™ i7-4600M CPU @ 2.90GHz × 4
* GPU: GeForce GT 730M/PCIe/SSE2
* RAM: 16 GB
* Python package manager: conda 4.3.16 

TF instrux [here](https://www.tensorflow.org/install/install_sources/).  To enable GPU support, one must install TF from source (instead of using the binary package).  

### Getting Started
* Clone TF to a local repo - pretty standard
* [Install](https://bazel.build/versions/master/docs/install-ubuntu.html) `bazel`
* `numpy`, `pip`, and `wheel` are already included with `conda`.  Only installed `dev` using: `pip install dev` instead of `sudo apt-get`
* I opted not to use a virtualenv.

### Installing CUDA 8.0.6
* Check that your NVIDIA card [supports CUDA](https://developer.nvidia.com/cuda-gpus)
* [Install CUDA for Ubuntu](http://docs.nvidia.com/cuda/cuda-installation-guide-linux/#axzz4VZnqTJ2A)
* [Check all the necessary software prerequisites](http://docs.nvidia.com/cuda/cuda-installation-guide-linux/#pre-installation-actions)
* [After downloading](https://developer.nvidia.com/cuda-downloads) the appropriate package, it opened in Ubuntu Software.  Ran `sudo apt-get update` and `sudo apt-get install cuda`.  Pretty painless.
* The post-install CUDA actions were not very smooth.  the [NVIDIA instructions](http://docs.nvidia.com/cuda/cuda-installation-guide-linux/#post-installation-actions) direct you to add a faulty `PATH` and `LD_LIBRARY_PATH`.
    Instead of:  
    `export PATH=/usr/local/cuda-8.0.61/bin${PATH:+:${PATH}}`  
    `export LD_LIBRARY_PATH=/usr/local/cuda-8.0.61/lib64\ ${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}`  
    Set the variables to:  
    `export PATH=/usr/local/cuda-8.0/bin${PATH:+:${PATH}}`  
    `export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64\ ${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}`  
    by using `sudo gedit ~/.bashrc`.  
* To verify the install by [writing samples](http://docs.nvidia.com/cuda/cuda-installation-guide-linux/#install-samples), the instructions once again are mistaken:
    Instead of:  
    `cuda-install-samples-8.0.61.sh <dir>` (I used `~` as `<dir>`)  
    This got the job done:  
    `bash cuda-install-samples-8.0.sh`  
    It turns out, much like the faulty `PATH` variables leading to non-existent folders, `cuda-install-samples-8.0.61.sh` did not exist on my machine.
* Trying to run `deviceQuery` was also problematic.  The instructions on the NVIDIA website did not work as the folder name was not updated.
    Instead:  
    `cd NVIDIA_CUDA-8.0._Samples/1_Utilities`
    `sudo make`
    Only then did `./deviceQuery` run correctly.  Similar tests can be run on the other included samples.

### Installing cuDNN 6.0
* One has to sign up to the NVIDIA developer program before being allowed to download cuDNN.
* Generally painless, as I used the `.deb` files.

### Configure the install
* These steps are a little annoying, but should configure Tensorflow to your machine's specifications.
* Press `Enter` without any text to choose the default option.
* The only non-default options I chose were:
    `Do you wish to build TensorFlow with CUDA support? [y/N]`
    **`Y`**  
    `Please specify a list of comma-separated Cuda compute capabilities you want to build with.`  
    **`3.0`**

### Use bazel to build
* This next step took about 20 minutes.  
    Build the package: `bazel build --config=opt --config=cuda //tensorflow/tools/pip_package:build_pip_package`  
    While the instructions cautioned that RAM usage would be high, I found that it was all 4 of my processor cores which were taxed instead.

### Use pip to install the package
* `sudo pip install /tmp/tensorflow_pkg/XXXXXXXXXXX` (replace XXXXXXXXXX with the specific package)
* Problems similar to [this](https://github.com/tensorflow/tensorflow/issues/5017#event-829612640)cropped up.  The solution was to run `conda install libgcc` which upgraded libgcc and allowed TF to be installed. 