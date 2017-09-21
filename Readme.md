# Packer-mfa

This is a little script to help build with packer in AWS with MFA turned on.

## Install

Run the following to add the file to your path at `/usr/local/bin`:

Python

```
$ cp packer-mfa.py /usr/local/bin/packer-mfa
```

Shell

```
$ cp packer-mfa.sh /usr/local/bin/packer-mfa
```

## Usage

### Python

Use in place of `packer`.

```
usage: packer-mfa [-h] [-p PROFILE] [-mfa MFA] [-r ROLE]

optional arguments:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        Use a profile defined in ~/.aws/credentials
  -mfa MFA, --mfa MFA   AWS mfa arn
  -r ROLE, --role ROLE  AWS role arn
```

###  Shell

Use `packer-mfa` in place of `packer`.
Export the following in your current shell (replace with your own arns):

```
export AWS_MFA_ROLE_ARN="arn::..."
export AWS_MFA_ARN="arn:..."
```

----------------------------------------------------------------------------------------------------

## Versions

### Python

The newest verison of this script is built with python and requires `boto3` to be installed.

### Shell

There is also a simpler, but still functional earlier version in straight shell code.

This is useful if you dont want to, or cant install the python dependencies.
