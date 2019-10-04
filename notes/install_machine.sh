## install machine scripts

set -euv

# golang                                                                                                                                                                                             
GOLANG_VERSION=1.11
GOLANG_DOWNLOAD_URL=https://golang.org/dl/go$GOLANG_VERSION.linux-amd64.tar.gz
GOLANG_DOWNLOAD_SHA256=b3fcf280ff86558e0559e185b601c9eade0fd24c900b4c63cd14d1d38613e499

curl -fsSL "$GOLANG_DOWNLOAD_URL" -o golang.tar.gz && \
      echo "$GOLANG_DOWNLOAD_SHA256  golang.tar.gz" | sha256sum -c -

tar -C /usr/local -xzf golang.tar.gz && rm golang.tar.gz

PATH=/usr/local/go/bin:$PATH

# put following lines into .bashrc
# ```
#   export PATH=/usr/local/go/bin:$PATH
#   export GOBIN=/usr/local/go
# ```
# do not set GOPATH which may break the thrift afterwards.                                                                                                                                           
export GOBIN=/usr/local/go/bin && curl https://raw.githubusercontent.com/golang/dep/v0.5.0/install.sh | sh


# thrift
THRIFT_VERSION=0.9.3

curl -sSL http://archive.apache.org/dist/thrift/$THRIFT_VERSION/thrift-$THRIFT_VERSION.tar.gz -o thrift.tar.gz \
      && mkdir -p /usr/src/thrift \
      && tar zxf thrift.tar.gz -C /usr/src/thrift --strip-components=1 \
      && rm thrift.tar.gz \
      && cd /usr/src/thrift \
      && ./configure \
      && make -j `grep processor /proc/cpuinfo | wc -l` \
      && make install \
      && cd / \
      && rm -rf /usr/src/thrift
