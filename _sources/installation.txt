========================================
Installation
========================================

.. highlight:: console
   :linenothreshold: 1000

----------------------------------------
Pre-requisites
----------------------------------------

____________________
Installing git
____________________

Run the following commands to install Git::

    $ sudo apt-get install -y aptitude
    $ sudo aptitude build-dep git-core
    $ cd ~
    $ wget http://git-core.googlecode.com/files/git-1.7.10.tar.gz
    $ tar xzvf git-1.7.10.tar.gz

    $ cd git-1.7.10
    $ ./configure
    $ make
    $ sudo make install

    $ git --version

    $ cd ../ && rm -rf git-1.7.10*

----------------------------------------
Installing icsv
----------------------------------------

Run the following commands in a terminal::

    $ cd /opt
    $ git clone https://github.com/bponsler/icsv
    $ sudo chown -R $USERNAME:$USERNAME icsv

    $ cd icsv
    $ python setup.py build
    $ python setup.py install


.. highlight:: python
   :linenothreshold: 1000
