# Deep learning AWS environment

## EC2 machine
Choose `p2.xlarge`

```
$ uname -m && cat /etc/*release
x86_64
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=16.04
DISTRIB_CODENAME=xenial
DISTRIB_DESCRIPTION="Ubuntu 16.04.3 LTS"
NAME="Ubuntu"
VERSION="16.04.3 LTS (Xenial Xerus)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 16.04.3 LTS"
VERSION_ID="16.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
VERSION_CODENAME=xenial
UBUNTU_CODENAME=xenial
```

## System packages
```
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
      bzip2 \
      g++ \
      git \
      graphviz \
      libgl1-mesa-glx \
      libhdf5-dev \
      openmpi-bin \
      wget \
      emacs
```

## docker & nvidia-docker for GPU

### Docker

Choose the CE version which is free.

Docker install instruction: https://docs.docker.com/install/linux/docker-ce/ubuntu/

```
sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

sudo apt-get install docker-ce=17.12.0~ce-0~ubuntu
```

### Nvidia docker
GPU driver

http://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#package-manager-installation

```
$ lspci -nnk | grep VGA -A8
00:02.0 VGA compatible controller [0300]: Cirrus Logic GD 5446 [1013:00b8]
	Subsystem: XenSource, Inc. GD 5446 [5853:0001]
	Kernel modules: cirrusfb
00:03.0 Ethernet controller [0200]: Device [1d0f:ec20]
	Kernel driver in use: ena
	Kernel modules: ena
00:1e.0 3D controller [0302]: NVIDIA Corporation GK210GL [Tesla K80] [10de:102d] (rev a1)
	Subsystem: NVIDIA Corporation GK210GL [Tesla K80] [10de:106c]
	Kernel driver in use: nvidia
```


Choose the CUDA version by platform type: https://developer.nvidia.com/cuda-downloads

In this case, it is
```
wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.1.85-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1604_9.1.85-1_amd64.deb
sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
sudo apt-get update
sudo apt-get install cuda
```

Nvidia Docker install instruction: https://github.com/NVIDIA/nvidia-docker


Uninstall v1 in case it was previously installed
```
sudo docker volume ls -q -f driver=nvidia-docker | xargs -r -I{} -n1 docker ps -q -a -f volume={} | xargs -r docker rm -f
sudo apt-get purge -y nvidia-docker
```

Install v2
```
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
  sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/ubuntu16.04/amd64/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update

sudo apt-get install -y nvidia-docker2
sudo pkill -SIGHUP dockerd
```

Verify nvidia docker v2 is working
```
sudo docker run --runtime=nvidia --rm nvidia/cuda nvidia-smi
```
You will see something like
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 390.30                 Driver Version: 390.30                    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Tesla K80           Off  | 00000000:00:1E.0 Off |                    0 |
| N/A   59C    P0    73W / 149W |      0MiB / 11441MiB |     81%      Default |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```

Run the command line below, then you don't need `sudo` for docker
```
sudo usermod -aG docker $USER
```

## Anaconda
https://www.anaconda.com/download/#linux
```
$ wget https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh
$ bash Anaconda3-5.1.0-Linux-x86_64.sh -b
$ echo -e "\nexport PATH=`pwd`/anaconda3/bin:\$PATH" >> ~/.bashrc
```

## Keras
```
cd ~
mkdir code
cd code/
git clone https://github.com/keras-team/keras.git
cd keras/docker/
~/code/keras/docker$ make test
```
then you will see something like:
```
Successfully tagged keras:latest
GPU=0 nvidia-docker run -it -v /home/ubuntu/code/keras:/src/workspace -v "/home/ubuntu/Data":/data --env KERAS_BACKEND=tensorflow keras py.test tests/
============================= test session starts ==============================
platform linux -- Python 3.6.3, pytest-3.4.2, py-1.5.2, pluggy-0.6.0 -- /opt/conda/bin/python
cachedir: .pytest_cache
rootdir: /src, inifile: pytest.ini
plugins: xdist-1.22.2, pep8-1.0.6, forked-0.2, cov-2.5.1
[gw0] linux Python 3.6.3 cwd: /src
[gw1] linux Python 3.6.3 cwd: /src
[gw0] Python 3.6.3 |Anaconda, Inc.| (default, Oct 13 2017, 12:02:49)  -- [GCC 7.2.0]
[gw1] Python 3.6.3 |Anaconda, Inc.| (default, Oct 13 2017, 12:02:49)  -- [GCC 7.2.0]
```

Check GPU info inside docker
```
$ nvidia-docker run -it -v ~/code/keras:/src/workspace -v "/home/$USER/Data":/data --env KERAS_BACKEND=tensorflow keras bash -c "python -c \"import tensorflow as tf; tf.Session(config=tf.ConfigProto(log_device_placement=True))\""
```
you can see something like
```
2018-03-15 03:26:52.821258: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1212] Found device 0 with properties: 
name: Tesla K80 major: 3 minor: 7 memoryClockRate(GHz): 0.8235
pciBusID: 0000:00:1e.0
```

## GPU usage monitoring

* nvidia-smi
```
watch -n 1 nvidia-smi
```

* glances
https://github.com/nicolargo/glances
```
pip install glances[action,browser,cloud,cpuinfo,chart,docker,export,folders,gpu,ip,raid,snmp,web,wifi]

glances
```
