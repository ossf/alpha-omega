FROM mcr.microsoft.com/mirror/docker/library/ubuntu:22.04

# Copyright (C) Microsoft Corporation, All rights reserved.

LABEL schema-version="1.0"
LABEL name="toolshed"
LABEL maintainer="Open Source Security Foundation - Omega"
LABEL vendor="OpenSSF"
LABEL build-date="2022-12-07T00:00:00.00Z"
LABEL version="0.8.4"

# Overridable Arguments
ARG DOTNET_VERSION="6.0"
ARG APPLICATION_INSPECTOR_VERSION="1.6.25"
ARG OSSGADGET_VERSION="0.1.365"
ARG GO_VERSION="1.19.3"
ARG BRAKEMAN_VERSION="v5.4.0"
ARG SCC_VERSION="3.0.0"
ARG NODE_VERSION="18.x"
ARG DEVSKIM_VERSION="0.8.4-alpha"
ARG RADARE2_VERSION="5.7.8"
ARG CODEQL_VERSION="v2.11.4"

# Initialize some things
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Los_Angeles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
SHELL ["/bin/bash", "-c"]

# Set work directory
WORKDIR /usr/src/app

# Choose the fastest mirror
#RUN sed -i '1s/^/deb mirror:\/\/mirrors.ubuntu.com\/mirrors.txt focal main restricted universe multiverse\n/' /etc/apt/sources.list && \
#    sed -i '1s/^/deb mirror:\/\/mirrors.ubuntu.com\/mirrors.txt focal-updates main restricted universe multiverse\n/' /etc/apt/sources.list && \
#    sed -i '1s/^/deb mirror:\/\/mirrors.ubuntu.com\/mirrors.txt focal-backports main restricted universe multiverse\n/' /etc/apt/sources.list && \
#    sed -i '1s/^/deb mirror:\/\/mirrors.ubuntu.com\/mirrors.txt focal-security main restricted universe multiverse\n/' /etc/apt/sources.list && \
#    echo /etc/apt/sources.list

# Add source repositories
RUN sed -i 's/^# deb-src/deb-src/' /etc/apt/sources.list

# Remove date checks for aptitude
RUN echo 'Acquire::Check-Valid-Until false;' >> /etc/apt/apt.conf.d/10-nocheckvalid && \
    echo 'Acquire::Check-Date false;' >> /etc/apt/apt.conf.d/10-nocheckvalid

# Core utilities
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
            build-essential \
            fakeroot \
            devscripts \
            curl \
            git \
            make \
            wget \
            mc \
            unzip \
            nano \
            vim \
            dos2unix \
            sed \
            gcc \
            libpq-dev \
            make \
            apt-transport-https \
            python3 \
            python3-pip \
            python3-setuptools \
            python3-dev \
            python3-wheel \
            python-is-python3 \
            jq \
            gnupg \
            g++ \
            make \
            gcc \
            apt-utils \
            file \
            gettext \
            sqlite3 \
            software-properties-common \
            splint \
            cppcheck \
            checksec \
            clamav \
            shellcheck \
            yara \
            strace \
            libboost-regex-dev \
            libboost-program-options-dev \
            libboost-system-dev \
            libboost-filesystem-dev \
            libssl-dev \
            cmake \
            binwalk \
            python3-matplotlib \
            csvtool \
            libhyperscan-dev \
            less \
            pkg-config \
            sudo \
            openssh-client \
            openjdk-17-jdk

##################################
####### Install Core Tools #######
##################################

# Install .NET Core and PowerShell
# License: https://github.com/dotnet/core/blob/main/LICENSE.TXT
# License: https://github.com/PowerShell/PowerShell/blob/master/LICENSE.txt
# Workaround with /etc/apt/preferences based on https://github.com/dotnet/core/issues/7699
RUN cd /tmp && \
    wget -q https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb && \
    touch /etc/apt/preferences && \
    echo "Package: *" >> /etc/apt/preferences && \
    echo "Pin: origin \"packages.microsoft.com\"" >> /etc/apt/preferences && \
    echo "Pin-Priority: 1001" >> /etc/apt/preferences && \
    add-apt-repository universe && \
    apt update && \
    apt-get install -y dotnet-sdk-${DOTNET_VERSION} && \
    apt-get install -y powershell

# Install Go
# License: https://github.com/golang/go/blob/master/LICENSE
RUN cd /opt && \
    wget https://golang.org/dl/go$GO_VERSION.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go$GO_VERSION.linux-amd64.tar.gz && \
    rm go$GO_VERSION.linux-amd64.tar.gz

# Install Node.js
# License: https://github.com/nodejs/node/blob/master/LICENSE
RUN curl -sL https://deb.nodesource.com/setup_$NODE_VERSION | bash -
RUN apt-get update && \
    apt-get install -y nodejs

# Install NodeJsScan
# License: https://github.com/ajinabraham/nodejsscan/blob/master/LICENSE
RUN pip3 install --disable-pip-version-check nodejsscan

# Install CppCheck
# License: https://github.com/danmar/cppcheck/blob/main/COPYING
RUN apt-get install -y cppcheck

# Install Radare2
# License: https://rada.re/r/license.html
RUN groupadd -r nonroot && \
    useradd -m -d /home/nonroot -g nonroot -s /usr/sbin/nologin -c "Nonroot User" nonroot && \
    mkdir -p /home/nonroot/workdir && \
    chown -R nonroot:nonroot /home/nonroot && \
    usermod -a -G sudo nonroot && echo 'nonroot:nonroot' | chpasswd && \
            echo "nonroot ALL=(ALL) NOPASSWD: ALL" >/etc/sudoers.d/nonroot && \
    mkdir /opt/radare2 && \
    chown nonroot:nonroot /opt/radare2
USER nonroot
RUN cd /opt && \
    git clone https://github.com/radareorg/radare2 /opt/radare2 && \
    cd /opt/radare2 && \
    git checkout $RADARE2_VERSION && \
    sh ./sys/install.sh && \
    r2pm init && \
    r2pm update
USER root
RUN chown -R root:root /opt/radare2

# Install CodeQL
# License: https://github.com/github/codeql-cli-binaries/blob/main/LICENSE.md
# Additional License per agreement with GitHub for less-restricted OpenSSF internal usage only.
# Install and pre-compile CodeQL queries
RUN cd /opt && \
    wget https://github.com/github/codeql-cli-binaries/releases/download/$CODEQL_VERSION/codeql-linux64.zip && \
    unzip codeql-linux64.zip && \
    rm codeql-linux64.zip && \
    git clone https://github.com/github/codeql codeql-queries && \
    cd codeql-queries && \
    git checkout "codeql-cli/$CODEQL_VERSION" && \
    cd .. && \
    PATH="/opt/codeql:$PATH" && \
    codeql query compile --threads=0 /opt/codeql-queries/javascript/ql/src/codeql-suites/javascript-security-and-quality.qls && \
    codeql query compile --threads=0 /opt/codeql-queries/java/ql/src/codeql-suites/java-security-and-quality.qls && \
    codeql query compile --threads=0 /opt/codeql-queries/csharp/ql/src/codeql-suites/csharp-security-and-quality.qls && \
    codeql query compile --threads=0 /opt/codeql-queries/python/ql/src/codeql-suites/python-security-and-quality.qls && \
    codeql query compile --threads=0 /opt/codeql-queries/cpp/ql/src/codeql-suites/cpp-security-and-quality.qls && \
    codeql query compile --threads=0 --additional-packs=/opt/codeql-queries/misc /opt/codeql-queries/go/ql/src/codeql-suites/go-security-and-quality.qls && \
    codeql query compile --threads=0 --additional-packs=/opt/codeql-queries/misc /opt/codeql-queries/ruby/ql/src/codeql-suites/ruby-security-and-quality.qls

# Install Lizard (code complexity analyzer)
# License: https://github.com/terryyin/lizard/blob/master/LICENSE.txt
RUN pip3 install --disable-pip-version-check lizard

# Install ShhGit
# License: MIT
RUN cd /opt && \
    git clone --depth 1 https://github.com/eth0izzle/shhgit && \
    PATH="/usr/local/go/bin:$PATH" && \
    cd shhgit && \
    go build -v -i

# Install SecretScanner
# License: MIT
RUN PATH="/usr/local/go/bin:$PATH" && \
    go install github.com/deepfence/SecretScanner@771073a459c4dcd4c38b537b7a5ddfb290d0a064

# Install SCC (line of code calculator)
# License: MIT
RUN cd /opt && \
    wget https://github.com/boyter/scc/releases/download/v$SCC_VERSION/scc-$SCC_VERSION-i386-unknown-linux.zip && \
    unzip scc-$SCC_VERSION-i386-unknown-linux.zip && \
    mv scc /usr/local/bin && \
    rm scc-$SCC_VERSION-i386-unknown-linux.zip

# Install Brakeman
# License: https://github.com/presidentbeef/brakeman/blob/main/LICENSE.md
RUN apt-get install -y ruby
RUN cd /opt && \
    git clone https://github.com/presidentbeef/brakeman.git && \
    cd brakeman && \
    git checkout $BRAKEMAN_VERSION && \
    gem build brakeman.gemspec && \
    gem install brakeman-*.gem

# Install Graudit
# License: GPL-3.0
RUN cd /opt && \
    git clone --depth 1 https://github.com/wireghoul/graudit

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

# DevSkim
# License: MIT
RUN cd /opt && \
    wget -q https://github.com/microsoft/DevSkim/releases/download/v$DEVSKIM_VERSION/DevSkim_linux_$DEVSKIM_VERSION.zip -O DevSkim.zip && \
    unzip DevSkim.zip && \
    rm DevSkim.zip && \
    mv DevSkim_linux_$DEVSKIM_VERSION DevSkim && \
    cd DevSkim && \
    chmod a+x ./devskim

# Manalyze
# License: GPL-3.0
RUN cd /opt && \
    git clone --depth 1 https://github.com/JusticeRage/Manalyze.git manalyze && \
    cd manalyze && \
    cmake . && \
    make && \
    make install

# Update ClamAV Signatures
RUN freshclam

# Install Scanner Dependencies
RUN pip3 --disable-pip-version-check install \
        azure-storage-queue \
        requests \
        PyGithub \
        requests-cache \
        packageurl-python \
        bandit \
        semgrep \
        detect-secrets \
        python-Levenshtein \
        jschema_to_python \
        sarif_om

# R2C Semgrep (with many rules)
# License: LGPLv2.1 - https://github.com/returntocorp/semgrep/blob/develop/LICENSE
RUN mkdir /opt/semgrep-rules && \
    cd /opt/semgrep-rules && \
    wget -O auto.yml https://semgrep.dev/c/p/auto && \
    wget -O brakeman.yml https://semgrep.dev/c/p/brakeman && \
    wget -O ci.yml https://semgrep.dev/c/p/ci && \
    wget -O clientside-js.yml https://semgrep.dev/c/p/clientside-js && \
    wget -O command-injection.yml https://semgrep.dev/c/p/command-injection && \
    wget -O default.yml https://semgrep.dev/c/p/default && \
    wget -O django.yml https://semgrep.dev/c/p/django && \
    wget -O docker-compose.yml https://semgrep.dev/c/p/docker-compose && \
    wget -O docker.yml https://semgrep.dev/c/p/docker && \
    wget -O dockerfile.yml https://semgrep.dev/c/p/dockerfile && \
    wget -O electron-desktop-app.yml https://semgrep.dev/c/p/electron-desktop-app && \
    wget -O eslint-plugin-security.yml https://semgrep.dev/c/p/eslint-plugin-security && \
    wget -O expressjs.yml https://semgrep.dev/c/p/expressjs && \
    wget -O flask.yml https://semgrep.dev/c/p/flask && \
    wget -O github-actions.yml https://semgrep.dev/c/p/github-actions && \
    wget -O gitlab-bandit.yml https://semgrep.dev/c/p/gitlab-bandit && \
    wget -O gitlab-eslint.yml https://semgrep.dev/c/p/gitlab-eslint && \
    wget -O golang.yml https://semgrep.dev/c/p/golang && \
    wget -O insecure-transport.yml https://semgrep.dev/c/p/insecure-transport && \
    wget -O java.yml https://semgrep.dev/c/p/java && \
    wget -O javascript.yml https://semgrep.dev/c/p/javascript && \
    wget -O jwt.yml https://semgrep.dev/c/p/jwt && \
    wget -O kubernetes.yml https://semgrep.dev/c/p/kubernetes && \
    wget -O mobsfscan.yml https://semgrep.dev/c/p/mobsfscan && \
    wget -O nginx.yml https://semgrep.dev/c/p/nginx && \
    wget -O nodejs.yml https://semgrep.dev/c/p/nodejs && \
    wget -O nodejsscan.yml https://semgrep.dev/c/p/nodejsscan && \
    wget -O ocaml.yml https://semgrep.dev/c/p/ocaml && \
    wget -O owasp-top-ten.yml https://semgrep.dev/c/p/owasp-top-ten && \
    wget -O phpcs-security-audit.yml https://semgrep.dev/c/p/phpcs-security-audit && \
    wget -O python.yml https://semgrep.dev/c/p/python && \
    wget -O r2c-best-practices.yml https://semgrep.dev/c/p/r2c-best-practices && \
    wget -O r2c-bug-scan.yml https://semgrep.dev/c/p/r2c-bug-scan && \
    wget -O r2c-ci.yml https://semgrep.dev/c/p/r2c-ci && \
    wget -O r2c-security-audit.yml https://semgrep.dev/c/p/r2c-security-audit && \
    wget -O r2c.yml https://semgrep.dev/c/p/r2c && \
    wget -O react.yml https://semgrep.dev/c/p/react && \
    wget -O ruby.yml https://semgrep.dev/c/p/ruby && \
    wget -O secrets.yml https://semgrep.dev/c/p/secrets && \
    wget -O semgrep-misconfigurations.yml https://semgrep.dev/c/p/semgrep-misconfigurations && \
    wget -O semgrep-rule-lints.yml https://semgrep.dev/c/p/semgrep-rule-lints && \
    wget -O sql-injection.yml https://semgrep.dev/c/p/sql-injection && \
    wget -O supply-chain.yml https://semgrep.dev/c/p/supply-chain && \
    wget -O terraform.yml https://semgrep.dev/c/p/terraform && \
    wget -O test.yml https://semgrep.dev/c/p/test && \
    wget -O trailofbits.yml https://semgrep.dev/c/p/trailofbits && \
    wget -O typescript.yml https://semgrep.dev/c/p/typescript && \
    wget -O xss.yml https://semgrep.dev/c/p/xss && \
    wget -O gitlab-gosec.yml https://semgrep.dev/c/r/gitlab.gosec && \
    wget -O hazanasec.weak_crypto.yml https://semgrep.dev/c/p/hazanasec.weak_crypto && \
    wget -O hazanasec.non-prepared-sql-statements.yml https://semgrep.dev/c/p/hazanasec.non-prepared-sql-statements && \
    wget -O hazanasec.nodejs_nosql_injection.yml https://semgrep.dev/c/p/hazanasec.nodejs_nosql_injection && \
    wget -O hazanasec.jwt-security-audit.yml https://semgrep.dev/c/p/hazanasec.jwt-security-audit && \
    wget -O hazanasec.generic_possible_xss.yml https://semgrep.dev/c/p/hazanasec.generic_possible_xss && \
    wget -O hazanasec.possible_path_traversal.yml https://semgrep.dev/c/p/hazanasec.possible_path_traversal && \
    wget -O findsecbugs.yml https://semgrep.dev/c/p/findsecbugs && \
    wget -O webappsecurityz.3zrr-rules.yml https://semgrep.dev/c/p/webappsecurityz.3zrr-rules && \
    wget -O traw.c.yml https://semgrep.dev/c/p/traw.c && \
    wget -O tkisason.javascript-kitchensink.yml https://semgrep.dev/c/p/tkisason.javascript-kitchensink && \
    semgrep -f /opt/semgrep-rules --validate --metrics=off

# Yara Rules
# License: GPL-2.0 - https://github.com/Yara-Rules/rules/blob/master/LICENSE
RUN cd /opt && \
    git clone --depth 1 https://github.com/Yara-Rules/rules yara-rules

# Trust But Verify
# License: MIT - https://github.com/verifynpm/tbv/blob/master/LICENSE
RUN npm i -g tbv

# ILSpy
# License: MIT - https://github.com/icsharpcode/ILSpy/blob/master/doc/license.txt
RUN cd /opt && \
    dotnet tool install --global ilspycmd

# Snyk Code
# License: Apache - https://github.com/snyk/cli/blob/master/LICENSE
# API License Terms of Service: https://snyk.io/policies/terms-of-service/
# Requires an API Key (not distributed) in order to use this tool.
RUN npm i -g snyk

########################
####### Finalize #######
########################

# Add --build-arg CACHEBUST=$(date -Format o) to avoid caching
ARG CACHEBUST=1

# Set up the path
RUN echo "export PATH=/root/go/bin:/opt/codeql:/opt/brakeman:/opt/OSSGadget:/opt/ApplicationInspector:/opt/DevSkim:/usr/local/go/bin:/opt/shhgit:/opt:/opt/graudit:/opt/manalyze/bin:/opt/toolshed:$PATH" >> /root/.bashrc
ENV PATH="/root/go/bin:/opt/codeql:/opt/brakeman:/opt/OSSGadget:/opt/ApplicationInspector:/opt/DevSkim:/usr/local/go/bin:/opt/shhgit:/opt:/opt/graudit:/opt/manalyze/bin:/opt/toolshed:${PATH}"

ENV DOTNET_CLI_TELEMETRY_OPTOUT=1

ADD worker/tools/runtools.sh /opt/toolshed/
ADD worker/tools/toolshed_sarif.py /opt/toolshed/
ADD worker/tools/parse_purl.py /opt/toolshed/
ADD worker/tools/edit_distance.py /opt/toolshed/
ADD worker/tools/postprocess.py /opt/toolshed/
ADD worker/tools/etc/* /opt/toolshed/etc/

RUN dos2unix /opt/toolshed/runtools.sh && \
    chmod +x /opt/toolshed/runtools.sh

ENTRYPOINT ["/opt/toolshed/runtools.sh"]
