# Usage
```bash
$ ./setenv.py -h
usage: setenv.py [-h] [-c] [-t TEMPLATE] [-o OUTPUT_DIR]

Generate an .env file from a template

options:
  -h, --help            show this help message and exit
  -c, --clear           Not loading .env file
  -t TEMPLATE, --template TEMPLATE
                        Template file path
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Output directory path

Preset: Values read from an existing .env file

Template Rule:
  1. Not in key = value format (mostly comments)
    template
  2. key =
    preset or user input
  3. key = ? command
    preset or command output or user input
  4. key = ! command
    preset or command output
  5. key = * [default]
    preset or default or user input or empty
  6. key = value
    value
```

# Example
## Template
```bash
$ cat env
# DB settings
DB_HOST = ? ip -4 -o a | grep -Ev ' (lo|virbr|br-|docker)' | sed 's;/.*;;; s/.* //'
DB_PORT =
DB_USER = test
DB_PSWD =

# server settings
SERVER_NAME =
SERVER_IP = ! ip -4 -o a | grep -Ev ' (lo|virbr|br-|docker)' | sed 's;/.*;;; s/.* //'
BACKEND_PORT =
WEBHOOK_SLACK = *
```

## Run
```bash
$ ./setenv.py
# DB settings
DB_HOST [192.168.0.3]
DB_PORT []
DB_PORT [] 12345
DB_PSWD [] password

# server settings
SERVER_NAME [] hello world
BACKEND_PORT [] 12346
WEBHOOK_SLACK [](Enter - Skip)
```

## Result
```bash
$ cat .env
# DB settings
DB_HOST=192.168.192.137
DB_PORT=12345
DB_USER=test
DB_PSWD=password

# server settings
SERVER_NAME='hello world'
SERVER_IP=192.168.0.3
BACKEND_PORT=12346
WEBHOOK_SLACK=
```
