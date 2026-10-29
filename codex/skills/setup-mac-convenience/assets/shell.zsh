source "$HOME/.config/mac-convenience/homebrew.zsh"

if (( ! $+functions[omz] )); then
  export ZSH="${ZSH:-$HOME/.oh-my-zsh}"
  ZSH_THEME=robbyrussell
  plugins=(git)
  source "$ZSH/oh-my-zsh.sh" || return
fi

if (( ! $+functions[_zsh_autosuggest_start] )); then
  source "$(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh" || return
fi

if (( ! $+functions[fasd_cd] )); then
  eval "$(fasd --init posix-alias zsh-hook zsh-ccomp zsh-ccomp-install zsh-wcomp zsh-wcomp-install)"
fi

alias ls=eza
alias a='fasd -a'
alias s='fasd -si'
alias d='fasd -d'
alias f='fasd -f'
alias sd='fasd -sid'
alias sf='fasd -sif'

if (( ! $+widgets[fzf-history-widget] )); then
  source <(fzf --zsh)
fi

unalias z zz j 2>/dev/null || true
eval "$(zoxide init zsh)"
alias zz=zi
alias j=zi
