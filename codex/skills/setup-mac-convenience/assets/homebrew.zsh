if (( $+commands[brew] )); then
  if [[ -z ${HOMEBREW_PREFIX:-} ]]; then
    eval "$(brew shellenv)"
  fi
else
  for mac_convenience_brew in /opt/homebrew/bin/brew /usr/local/bin/brew; do
    if [[ -x "$mac_convenience_brew" ]]; then
      eval "$("$mac_convenience_brew" shellenv)"
      break
    fi
  done
  unset mac_convenience_brew
fi

typeset -U path PATH
path=("$HOME/.local/bin" "$HOME/.cargo/bin" $path)
export PATH
