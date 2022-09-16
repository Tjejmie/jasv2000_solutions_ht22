#!/usr/bin/env python

""" DT179G - LAB ASSIGNMENT 2
You find the description for the assignment in Moodle, where each detail regarding requirements
are stated. Below you find the inherent code, some of which fully defined. You add implementation
for those functions which are needed:

 - authenticate_user(..)
 - format_username(..)
 - decrypt_password(..)
"""

import argparse
import sys

__version__ = '1.1'
__desc__ = "A simple script used to authenticate spies!"


def authenticate_user(credentials: str) -> bool:
    """Procedure for validating user credentials"""
    agents = {  # Expected credentials. MAY NOT BE MODIFIED!!
        'Dan_Aykroyd': 'i0N00h00~0[$',          # cipher: bEauTy
        'John_Belushi': 'J0j0S%0V0w0L0',        # cipher: CaLzOnE
        'Chevy_Chase': 'i0J0u0j0u0J0Zys0r0{',   # cipher: bAnanASplit
    }
    user_tmp = pass_tmp = str()


    ''' PSEUDO CODE
    PARSE string value of 'credentials' into its components: username and password.
    SEND username for FORMATTING by utilizing devoted function. Store return value in 'user_tmp'.
    SEND password for decryption by utilizing devoted function. Store return value in 'pass_tmp'.
    VALIDATE that both values corresponds to expected credentials existing within dictionary.
    RETURN outcome of validation as BOOLEAN VALUE.
    '''

    pass_tmp = credentials.rsplit(" ")[-1]
    user_tmp = credentials.split(" ")[0:2]

    user_tmp = format_username(user_tmp)
    pass_tmp = decrypt_password(pass_tmp)

    for key, val in agents.items():
        if key == user_tmp:
            if val == pass_tmp:
                return True



def format_username(username: list) -> str:
    """Procedure to format user provided username"""

    ''' PSEUDO CODE
    FORMAT first letter of given name to be UPPERCASE.
    FORMAT first letter of surname to be UPPERCASE.
    REPLACE empty space between given name and surname with UNDERSCORE '_'
    RETURN formatted username as string value.
    '''
    for i in range(len(username)):
        username[i] = username[i].title()

    username = '_'.join(map(str, username))

    return username

def decrypt_password(password: str) -> str:
    """Procedure used to decrypt user provided password"""
    rot7, rot9 = 7, 9       # Rotation values. MAY NOT BE MODIFIED!!
    vowels = 'AEIOUaeiou'   # MAY NOT BE MODIFIED!!
    decrypted = str()

    ''' PSEUDO CODE
    REPEAT {
        DETERMINE if char IS VOWEL.
        DETERMINE ROTATION KEY to use.
        DETERMINE decryption value
        ADD decrypted value to decrypted string
    }
    
    RETURN decrypted string value
    '''

    for i, char in enumerate(password):
        if char in vowels:
            if i % 2 != 0:
                tmp = ord(char) + rot9
                new_val = chr((tmp - 126) + 32) if tmp > 127 else chr(tmp)
                decrypted += f"0{new_val}0"
            elif i % 2 == 0:
                tmp = ord(char) + rot7
                new_val = chr((tmp - 126) + 32) if tmp > 127 else chr(tmp)
                decrypted += f"0{new_val}0"
        else:
            if i % 2 != 0:
                tmp = ord(char) + rot9
                new_val = chr((tmp - 126) + 32) if tmp > 127 else chr(tmp)
                decrypted += new_val
            elif i % 2 == 0:
                tmp = ord(char) + rot7
                new_val = chr((tmp - 126) + 32) if tmp > 127 else chr(tmp)
                decrypted += new_val

    return decrypted


def main():
    """The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    epilog = "DT0179G Assignment 2 v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('credentials', metavar='credentials', type=str,
                        help="Username and password as string value")

    args = parser.parse_args()

    if not authenticate_user(args.credentials):
        print("Authentication failed. Program exits...")
        sys.exit()

    print("Authentication successful. User may now access the system!")


if __name__ == "__main__":
    main()
