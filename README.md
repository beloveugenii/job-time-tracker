The **Job time tracker** is a simple program that allows you to keep track of the time worked and the salary received for it.  

First of all, it is worth saying that this program was planned as a mobile application launched through [Termux]( https://github.com/termux ).  

In addition, for ease of use, you can use [Termux-widget](https://github.com/termux/termux-widget).  
With Jtt provides the simple script *widget.sh* that will create a widget and prepare the runtime environment.  

**About**  

This is the second version of the program.  Unlike the first version, which was written as a bash script using awk and sed, this version is written in pure Perl.

The main reasons for the appearance of this program, apart from practical personal use, is the practice in Perl and the first experience of interacting with git.

If someone ever finds this program and uses it, bug reports can be sent to beloveugenii@gmail.com.  

**Update**

I present to your attention the third version of the program, completely rewritten in Python.

The functionality remains the same as in previous versions.
However, a new command syntax is now used, and the data is stored in the SQLite database.

At the moment, the program is not finished, but it can already be used. 

A Python parser is provided for migration from the Perl version (bash could be dispensed with).
