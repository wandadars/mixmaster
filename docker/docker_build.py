#!/usr/bin/env python

def write_common_dockerfile(f,copy_loc):
    f.write('FROM ubuntu:17.04 \n')
    f.write('MAINTAINER Cantera\n\n')

    f.write('RUN apt-get update  &&    \ \n')
    f.write('    apt-get upgrade -y && \ \n')
    f.write('    apt-get install -y    \ \n')
    f.write('    sudo                  \ \n')
    f.write('    vim                   \ \n')
    f.write('    vim-data              \ \n')
    f.write('    git                   \ \n')
    
    #General Cantera package requirements
    f.write('    g++                   \ \n')
    f.write('    python                \ \n')
    f.write('    scons                 \ \n')
    f.write('    libboost-dev++        \ \n')

    #Python2 module requirements
    f.write('    cython                \ \n')
    f.write('    python-dev            \ \n')
    f.write('    python-numpy          \ \n')
    f.write('    python-numpy-dev      \ \n')
    f.write('    python-setuptools     \ \n')
    f.write('    libboost-dev++        \ \n')


    f.write('    python3               \ \n')
    f.write('    python3-dev           \ \n')
    f.write('    python3-setuptools    \ \n')
    f.write('    python3-numpy         \ \n')
    f.write('    blas-devel            \ \n')
    f.write('    blas-devel-static     \ \n')
    f.write('    lapack-devel          \ \n')
    f.write('    iproute2              \ \n')
    f.write('    curl                  \ \n')
    f.write('    tar                   \ \n')
    f.write('    which                 \n\n')


    f.write('USER root \n')
    f.write('RUN echo "root:canterauser" | chpasswd      && \ \n')
    f.write('    groupadd -g 1000 canterauser            && \ \n')
    f.write('    useradd -u 1000 -d /home/canterauser -m -s /bin/bash canterauser  && \ \n')
    f.write('    passwd -d canterauser \n\n')


    f.write('RUN mkdir -p -m0755           \ \n')
    f.write('    /opt/Cantera              \ \n')
    f.write('    /opt/MixMaster            \ \n')
    f.write('    /home/canterauser/workdir \n\n')

    #Clone repositories
    f.write('RUN git clone https://github.com/Cantera/cantera.git /opt/cantera       \ \n')
    f.write('RUN git clone https://github.com/Cantera/mixmaster.git  /opt/mixmaster  \ \n')


    f.write('USER canterauser \n')
    f.write('COPY ' + './docker/image_env_setup.sh' + ' ' + '/opt/Cantera \n\n')


def write_dockerfile(f):
    f.write('ENV PATH="$PATH":"/opt/Cantera/bin:/usr/lib64/mpi/gcc/openmpi/bin" \n')
    f.write('ENV LD_LIBRARY_PATH="/usr/lib64:/opt/Cantera/lib:" \n')
    f.write('ENV PS1="[\u@docker: \w]\$ " \n')
    f.write('ENV TERM="xterm-256color" \n')
    f.write('ENV GREP_OPTIONS="--color=auto" \n')
    f.write('ENV EDITOR=/usr/bin/vim \n\n')

    f.write('USER root \n')
    f.write('RUN chmod +x  /opt/Cantera/image_env_setup.sh \n\n')

    f.write('USER canterauser \n')
    f.write('RUN cp /etc/skel/.bashrc ~/.bashrc \n')
    f.write('RUN echo ". /opt/Cantera/image_env_setup.sh" >> ~/.bashrc \n\n')

    f.write('RUN SOURCE_DIR=/opt/Cantera  &&                                \ \n')
    f.write('    BUILD_DIR=/opt/Cantera_build  &&                           \ \n')
    f.write('    mkdir $BUILD_DIR &&                                        \ \n')
    f.write('    scons build python_package=full prefix=$(BUILD_DIR)_build  \ \n')
    f.write('    sudo scons install                                         \ \n')

    f.write('USER canterauser:canterauser \n')



#Main
f = open('Dockerfile','w')
write_common_dockerfile(f,copy_loc)
write_dockerfile(f)
f.close()
