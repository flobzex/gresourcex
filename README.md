# gresourcex
A GResource file extractor made in python.

## What is GResource?
GResource is a precompiled bundle file that stores the source files
of a GTK theme. You can learn more about it by running `man gresource`.

## How does it work?
There is a program, `gresource`, that provides some operations to
these files. The more important of them are: `list` and `extract`.

It works by calling the command `gresource list <target_file>` to
get a list of the resources within the GResource file, and then,
calling `gresource extract <res_name>` for every resource within
the GResource file, capturing its output and writing it to a file.

