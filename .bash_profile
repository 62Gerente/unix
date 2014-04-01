#-------------------- COLOR --------------------   

#enables color in the terminal bash shell
export CLICOLOR=1
#sets up the color scheme for list export
LSCOLORS=gxfxcxdxbxegedabagacad
#sets up the prompt color (currently a green similar to linux terminal)
export PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;36m\]\w\[\033[00m\]\$'
#enables color for iTerm
export TERM=xterm-color

#-------------------- OTHER --------------------

[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*

[[ -r ~/.bashrc  ]] && . ~/.bashrc

#-------------------- RVM -------------------

[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm"
PATH=$PATH:$HOME/.rvm/bin # Add RVM to PATH for scripting

PATH=$PATH:/usr/local/rvm/bin # Add RVM to PATH for scripting

#-------------------- HOME BIN --------------------

PATH=$PATH:~/bin
alias pg='pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log'


export PGHOST=localhost
