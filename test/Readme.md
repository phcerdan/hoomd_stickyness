Local installation.
http://hoomd-blue.readthedocs.io/en/stable/compiling.html

Hoomd has been installed to /usr/local/hoomd using python2.7
Two options:
export PYTHONPATH=/usr/local
But not pretty good changing python environments, versions, etc.

or

create symlink to already installed python modules.
ln -s /usr/local/hoomd /usr/lib/python2.7/dist-packages/


See test on how to use it.
execute it with:
python lj.py

note that hoomd lj.py (2015 usage is not used)


