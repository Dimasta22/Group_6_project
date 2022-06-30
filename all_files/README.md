

Working with the notebook:
There are options: 'create', 'add', 'change', 'sort', 'find', 'file',
                   'clear', 'remove', 'show', 'exit', 'close', 'good bye'.

All parameters are entered with a space, example: create some request
#############################################################################################
Commands: 'show', 'clear', 'exit', 'close', 'good bye' do not have some options.

The 'create' command creates a new note. Accepts parameters: title and note.
Example: create Football I like Brazil team

Command: 'add' adding title or tag
Example: add tag Argentina

Command: 'change' title or tag
Example: change title Football Sport

Command: 'remove' is removing all note
Example: remove Football

Command: 'sort' is sorting all tags in note
Example: sort Football

Command: 'find' is finding all match in note
Example: find Foot

Command: 'file' write and read addressbook in file. Take a value 'read' or 'write'
Command: 'clear' delete all notes.
Command: 'show' show all notes.
Commands: 'exit', 'close', 'good bye' are completing a project

############################################################################
Working with the address book:
There are options: 'hello', 'create', 'add phone', 'add email', 'add address', 'add birthday',
                   'show all', 'change phone', 'change email', 'change address', 'phone',
                   'delete phone', 'delete email', 'delete address', 'birthday', 'show',
                   'file', 'clear', 'find', 'remove', 'exit', 'close', 'good bye'.

All parameters are entered with a space, example: create some request
#############################################################################################
'email' option must contain '@' symbol and end with .domain
'phone' option must contain 12 or 10 numbers
'address' option must contain: type of street(st, ave, etc.) '.' name of street '/'
                               number of house '/' and optional param number of flat
'birthday' has the form 22.01.2000
############################################################################################
Commands: 'hello', 'show all', 'clear', 'exit', 'close', 'good bye' do not have some options.

The 'create' command creates a new user. Accepts parameters: Name, phone, email, birthday, address.
All parameters, except for the name, can be in a different sequence. Also, there can be many phones,
                                                                           emails and addresses.
Example: create Misha 0675558888 misha@gmail.com 0997846552 misha@mail.ua st.Slavy/14/96 14.02.2000

Commands: 'add phone', 'add email', 'add address', 'add birthday' take a value 'name' and params.
Example: add email Misha misha_1@gmail.com

Commands: 'change phone', 'change email', 'change address' take a value which need to change and
                                                           new value.
Example: change phone Misha 0675558888 0675559999

Commands: 'delete phone', 'delete email', 'delete address' take a value which need to delete
Example: delete address st.Slavy/14/96

Commands: 'exit', 'close', 'good bye' are completing a project
Commands: 'show all', 'show' show addressbook. 'show' take a value numer of contact.
Command 'find' searches for any match. Take a value params
Command 'file' write and read addressbook in file. Take a value 'read' or 'write'
Command 'remove' remove contact from addressbook. Take a value name of contact
Command 'phone' showing contact number. Take a value name of contact
Command 'clear' delete all contact from addressbook.
Command 'birthday' shows how many days are left until the birthday. Take a value name of contact
############################################################################################
