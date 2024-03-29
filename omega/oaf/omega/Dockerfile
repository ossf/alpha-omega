# TODO: Fix latest to a specific number
FROM ubuntu:latest

LABEL name="oaf"
LABEL maintainer="Open Source Security Foundation - Omega"
LABEL vendor="OpenSSF"
LABEL version="0.1.0"

# Overridable Arguments
ARG DOTNET_VERSION="6.0"
ARG APPLICATION_INSPECTOR_VERSION="1.9.1"
ARG OSSGADGET_VERSION="0.1.401"
ARG GO_VERSION="1.20.4"
ARG BRAKEMAN_VERSION="v6.0.0"
ARG SCC_VERSION="3.0.0"
ARG NODE_VERSION="19.x"
ARG DEVSKIM_VERSION="1.0.6"
ARG RADARE2_VERSION="5.8.6"
ARG CODEQL_VERSION="v2.13.1"
ARG UBUNTU_VERSION="22.04"

# Initialize some things
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Los_Angeles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
SHELL ["/bin/bash", "-c"]

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    	    build-essential \
	    fakeroot \
	    curl \
	    wget \
	    python3 \
            python3-pip \
            python3-setuptools \
            python3-dev \
            python3-wheel \
            python-is-python3 \
	    python3-venv \
	    file \
	    unzip \
	    gcc \
	    sed \
	    sudo \
	    libssl-dev \
	    less \
	    dotnet-sdk-${DOTNET_VERSION}

# Install .NET Core and PowerShell
# License: https://github.com/dotnet/core/blob/main/LICENSE.TXT
# License: https://github.com/PowerShell/PowerShell/blob/master/LICENSE.txt
# Workaround with /etc/apt/preferences based on https://github.com/dotnet/core/issues/7699
# RUN cd /tmp
# RUN wget -q -a -O https://packages.microsoft.com/config/ubuntu/${UBUNTU_VERSION}/packages-microsoft-prod.deb && \
#     dpkg -i packages-microsoft-prod.deb && \
#     rm packages-microsoft-prod.deb && \
#     touch /etc/apt/preferences && \
#     echo "Package: *" >> /etc/apt/preferences && \
#     echo "Pin: origin \"packages.microsoft.com\"" >> /etc/apt/preferences && \
#     echo "Pin-Priority: 1001" >> /etc/apt/preferences && \
#     add-apt-repository universe && \
#     apt update && \
#     apt-get install -y dotnet-sdk-${DOTNET_VERSION}

# Install Go
# License: https://github.com/golang/go/blob/master/LICENSE
RUN cd /opt && \
    wget https://golang.org/dl/go$GO_VERSION.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go$GO_VERSION.linux-amd64.tar.gz && \
    rm go$GO_VERSION.linux-amd64.tar.gz

# Install OSS Gadget
# License: MIT
RUN cd /opt && \
    wget -q https://github.com/microsoft/OSSGadget/releases/download/v${OSSGADGET_VERSION}/OSSGadget_linux_${OSSGADGET_VERSION}.tar.gz -O OSSGadget.tar.gz && \
    tar zxvf OSSGadget.tar.gz && \
    rm OSSGadget.tar.gz && \
    mv OSSGadget_linux_${OSSGADGET_VERSION} OSSGadget && \
    sed -i 's@${currentdir}@/tmp@' OSSGadget/nlog.config

# ApplicationInspector
# License: MIT
RUN cd /opt && \
    wget -q https://github.com/microsoft/ApplicationInspector/releases/download/v${APPLICATION_INSPECTOR_VERSION}/ApplicationInspector_linux_${APPLICATION_INSPECTOR_VERSION}.zip -O ApplicationInspector.zip && \
    unzip ApplicationInspector.zip && \
    rm ApplicationInspector.zip && \
    mv ApplicationInspector_linux_${APPLICATION_INSPECTOR_VERSION} ApplicationInspector && \
    cd ApplicationInspector && \
    chmod a+x ./ApplicationInspector.CLI

RUN mkdir -p /opt/oaf

# Set up the path
RUN echo "export PATH=/root/go/bin:/opt/OSSGadget:/opt/ApplicationInspector:/usr/local/go/bin:/opt/oaf:$PATH" >> /root/.bashrc
ENV PATH="/root/go/bin:/opt/OSSGadget:/opt/ApplicationInspector:/usr/local/go/bin:/opt/oaf:${PATH}"

ADD __init__.py /opt/oaf/
ADD oaf.py /opt/oaf/
COPY assertion/ /opt/oaf/assertion/
ADD requirements.txt /opt/oaf

RUN pip install -r /opt/oaf/requirements.txt

WORKDIR /opt/oaf/

ENTRYPOINT ["python","/opt/oaf/oaf.py"]

