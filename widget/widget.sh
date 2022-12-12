#!/bin/bash

## It's a simple script, which creates Jtt widget using termux-widget.
## So…you must install it :-)
## v0.1.0
## v0.1.1 Add checking of existing .shortcuts dir

if ! [[ -d "$HOME/.shortcuts" ]]; then
	echo "Creating .shortcuts"
	mkdir -p $HOME/.shortcuts/icons
	chmod -R u=rwx $HOME/.shortcuts/*
fi

read -p "Enter widget name: " WN

echo -e "#!/bin/bash\n\nPERL5LIB=\"$HOME/perl5/lib/perl5\${PERL5LIB:+:\${PERL5LIB}}\"\n\nexport PERL5LIB\n\nperl $(dirname $(dirname `realpath $0`))/jtt" > $HOME/.shortcuts/$WN


cp `dirname $0`/jtt.png $HOME/.shortcuts/icons/$WN.png
