#!/usr/bin/env python3

import os
import argparse
import boto3
import getpass

# Arguments
parser = argparse.ArgumentParser()

# Profile
parser.add_argument(
  "-p", "--profile",
  help="Use a profile defined in ~/.aws/credentials"
)

# No profile
parser.add_argument(
  "-mfa", "--mfa",
  help="AWS mfa arn"
)

parser.add_argument(
  "-r", "--role",
  help="AWS role arn"
)

# TODO: not sure if we can tell boto about a diff creds file
# parser.add_argument(
#   "-c", "--credentials_file",
#   default="~/.aws/credentials",
#   help="Path to your credentials file. Defaults to: ~/.aws/credentials"
# )

args, unknownargs = parser.parse_known_args()

AWS_ACCESS_KEY_ID=None
AWS_SECRET_ACCESS_KEY=None
AWS_SESSION_TOKEN=None


#--[ Assume Role ]------------------------------------------------------------------------------------------------------

credentials = None

if args.profile: # Use the profile from ~/.aws/credentials
  session = boto3.Session(
    profile_name=args.profile,
  )

  credentials = session.get_credentials()

  AWS_ACCESS_KEY_ID=credentials.access_key
  AWS_SECRET_ACCESS_KEY=credentials.secret_key
  AWS_SESSION_TOKEN=credentials.token

else: # no profile
  if args.role and args.mfa: # Use the role with MFA
    # ask for mfa token
    token = getpass.getpass("Enter your MFA token: ")

    sts_client = boto3.client('sts')

    session = sts_client.assume_role(
      RoleArn=args.role,
      RoleSessionName='packer',
      SerialNumber=args.mfa,
      TokenCode=token
    )

    AWS_ACCESS_KEY_ID=session['Credentials']['AccessKeyId']
    AWS_SECRET_ACCESS_KEY=session['Credentials']['SecretAccessKey']
    AWS_SESSION_TOKEN=session['Credentials']['SessionToken']

  else: # no mfa
    if args.role: # Just use the role

      sts_client = boto3.client('sts')

      session = sts_client.assume_role(
        RoleArn=args.role,
        RoleSessionName='packer',
      )

      AWS_ACCESS_KEY_ID=session['Credentials']['AccessKeyId']
      AWS_SECRET_ACCESS_KEY=session['Credentials']['SecretAccessKey']
      AWS_SESSION_TOKEN=session['Credentials']['SessionToken']

    else: # No profile, no role, no mfa -- Fail
      exit('Exiting: you need to set a profile with: --profile, or provide --role and/or --mfa')

#--[ Run packer ]-------------------------------------------------------------------------------------------------------

if AWS_ACCESS_KEY_ID is None or AWS_SECRET_ACCESS_KEY is None or AWS_SESSION_TOKEN is None:
        exit('Exiting: Something went wrong;.')

# Add the keys to the env
os.environ['AWS_ACCESS_KEY_ID']=AWS_ACCESS_KEY_ID
os.environ['AWS_SECRET_ACCESS_KEY']=AWS_SECRET_ACCESS_KEY
os.environ['AWS_SESSION_TOKEN']=AWS_SESSION_TOKEN

# Prepare the command for packer
packer_cmd = ' '.join(unknownargs)
cmd = 'packer %s' % packer_cmd

# Run
print('Running: packer %s' % packer_cmd)
os.system(cmd) # returns the exit status
