The **Job time tracker** is a simple program that allows you to keep track of the time worked and the salary received for it.  

First of all, it is worth saying that this program was planned as a mobile application launched through [Termux]( https://github.com/termux ).  

In addition, for ease of use, you can use [Termux-widget](https://github.com/termux/termux-widget).  
With Jtt provides the simple script *widget.sh* that will create a widget and prepare the runtime environment.  

The program stores its data in \*.jtt files in *data* dir.

The hidden '.config' file stores program configuration:  
- Path to current \*.jtt file. To change it use -f/--file [path-to-file].  
- Current lang code. Use -l/--lang LANG_CODE to change it.

For more details see help.  

**About**  

This is the second version of the program.  Unlike the first version, which was written as a bash script using awk and sed, this version is written in pure Perl.

The main reasons for the appearance of this program, apart from practical personal use, is the practice in Perl and the first experience of interacting with git.

If someone ever finds this program and uses it, bug reports can be sent to beloveugenii@gmail.com.  

**Whats new**  

**v.1.0.10**  
The Calendar::Simple module is now located in the directory with the program, which eliminates the need to install it; 
Widget creation script rewritten in Perl;  

**v1.0.9**  
Big changes in output subroutines: the UI now looks clearly and adapts for different width of terminal window;  
Main part of output subroutine was included in one subroutine, which return array of subroutine refs;  
Some little changes in translations;  
New way in command line options handlers;  

**v1.0.8**  
The data from .config file now availeble via $config hashref;  
The data structure used in the program has been changed: now all data from the file \*.jtt is available via a hashref $user_data;  
All translations now placed in one file 'translation'. It parses for strings which available via hashref $translation;  
The calculation of the information displayed is given in a separate function. It can be accessed via a hashref $info;  
Many functions were divided into smaller;  
Add *-h* command line key to show help;  
Add long names of command line keys;  
Another small changes;  

**v1.0.7**  
Verision of *widget.sh* up to 0.1.0. So it must be tested;  
Add -w key to *Jtt* to start *widget.sh*: ./jtt -w;  

**v1.0.6**  
Add *widget.sh* script to creating termux-widget;  

**v1.0.5**  
Change autocompletion module to Term::Completion;  
Calendar::Simple module now let in program dir;  
Add handlers for creating 'data' dir and '.config' file if they not exist;  

**v1.0.4**   
Add autocomplete in open another file menu and set parameter menu;  

**v1.0.3**  
Now can use \*.jtt file stored everywere;  
Correct handling of command-line options;  

