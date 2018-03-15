# See detailed explanation in deep-learning-aws-env.md
#
# Worked with `p2.xlarge` EC2 machine
#
# Usage:
#   sh step1-deep-learning-aws-env.sh
#
# This script should be run only once, running requires removing some installed packages beforehands, e.g.
# ```
#   sudo apt-get remove -y --ignore-missing docker-ce
#   rm -rf ~/anaconda3 ~/code
# ```


set -euv

echo "\nexport PATH=`pwd`/anaconda3/bin:\$PATH\n" >> ~/.bashrc

## system package
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
    bzip2 \
    g++ \
    git \
    graphviz \
    libgl1-mesa-glx \
    libhdf5-dev \
    openmpi-bin \
    wget

## docker
sudo apt-get install -y \
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

sudo apt-get install -y docker-ce=17.12.0~ce-0~ubuntu

## nvidia-docker
wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.1.85-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1604_9.1.85-1_amd64.deb
sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
sudo apt-get update
sudo apt-get install -y cuda
rm -rf cuda-repo-ubuntu1604_9.1.85-1_amd64.deb

sudo docker volume ls -q -f driver=nvidia-docker | xargs -r -I{} -n1 docker ps -q -a -f volume={} | xargs -r docker rm -f
sudo dpkg --purge nvidia-docker

curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
  sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/ubuntu16.04/amd64/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update

sudo apt-get install -y nvidia-docker2
sudo pkill -SIGHUP dockerd

### verify nvidia-docker
sudo docker run --runtime=nvidia --rm nvidia/cuda nvidia-smi

### no need `sudo` for `docker` from now on. This requires log-out and log-in again.
sudo usermod -aG docker $USER

## Anaconda
wget https://repo.continuum.io/archive/Anaconda3-5.1.0-Linux-x86_64.sh
bash Anaconda3-5.1.0-Linux-x86_64.sh -b
echo "\nexport PATH=`pwd`/anaconda3/bin:\$PATH" >> ~/.bashrc
rm -rf Anaconda3-5.1.0-Linux-x86_64.sh

## keras
cd ~
mkdir -p code
cd code/
git clone https://github.com/keras-team/keras.git
cd ~/code/keras/docker
sudo make build

### verify keras
sudo nvidia-docker run -it -v ~/code/keras:/src/workspace -v "/home/$USER/Data":/data --env KERAS_BACKEND=tensorflow keras bash -c "python -c \"import tensorflow as tf; tf.Session(config=tf.ConfigProto(log_device_placement=True))\""


## s3 & tools
sudo apt-get install -y \
      awscli \
      emacs \
      s3cmd
pip install glances[action,browser,cloud,cpuinfo,chart,docker,export,folders,gpu,ip,raid,snmp,web,wifi]
