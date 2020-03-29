# Make Python 3.7 as the default version

If you want to use python 3.7 as default version you can create an alias.

vim ~/.bashrc

and then add the following alias.

which python3.7
/usr/local/bin/python3.7

alias python='/usr/local/bin/python3.7'

Then source the .bashrc file.

source ~/.bashrc