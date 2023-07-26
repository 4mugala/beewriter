# beeNote
Is a simple document formant

# Structure
```
? Title (description)
@ Author
# Priority
=
Content
```

## Title (description)
The title (or short description) of the document ``[multiline: allowed, blank: allowed]``

## Author
The author of the document ``[multiline: disallowed, blank: allowed]``

## Priority
This is only used in a give scope and can be whatever you want (or last modified date). ``[multiline: disallowed, blank: allowed]``

## Content
This is where the content of your body goes in. ``[multiline: allowed, blank: allowed]``

## Tags
``?`` + ``\t`` = ``?\t``: title-tag

``@\t``: author-tag

``#\t``: priority-tag

``=\n``: content-tag

## Rules
``multiline``: mean a property (field) can contain multiple lines

``blank``: means a property can be left empty (as an example below)

An example with a multiline title and content and blank title and priority
```
? Hello,
  world.
@
#
=
Some people say life good
On ther hand people say life is hard
```
