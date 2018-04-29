#!/bin/bash
rename()
{
startDir=.

for arg in "$@" ; do
find $startDir \( -name "* *" -o -name "* *" \) -print |
while read old ; do
new=$(echo "$old" | tr -s '\011' ' ' | tr -s ' ' '.')
mv "$old" "$new"
done
done
}
rename d f # Renames your directories with spaces first, then files
