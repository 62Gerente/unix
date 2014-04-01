export EDITOR=vim
export PATH=.:$HOME/unix/bin:$HOME/bin:$PATH

function reload () {
    source "$HOME/unix/bash/alias";
    source "$HOME/unix/bash/alias_git";
    source "$HOME/unix/bash/alias_personal";
    source "$HOME/unix/bash/other";
    source "$HOME/unix/bash/git_prompt";
    source "$HOME/unix/bash/commands";
    source "/usr/local/etc/bash_completion.d/git-completion.bash";
}

reload;

### Added by the Heroku Toolbelt
export PATH="/usr/local/heroku/bin:$PATH"
