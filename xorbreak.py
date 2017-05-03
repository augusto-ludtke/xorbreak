#!/usr/bin/python

"""
Usage:
    ./xorbreak.py [-f|-g|-d] [options] FILE

Options:
    -f                              Find the most probable key lenghts
    -g                              Guess the key value
    -d                              Decrypt the ciphertext
    -l LENGTH --length=KEYLENGTH    Key length when trying to guess the key value
    -k KEY --key=KEY                Key used to decrypt the file
    -h --help                       This help message

Example:
    ./xorbreak -f ciphertext.txt
    ./xorbreak -g -l 15 ciphertext.txt
    ./xorbreak -d -k D132A31ED87AB1 ciphertext.txt
"""

from docopt import docopt
import re

def main():
    options = docopt(__doc__)

    ciphertext = load_ciphertext(options['FILE'])
    print "Ciphertext:", len(ciphertext), "bytes" 

    if options['-d']:
        key = []
        key_hex = re.findall('[0-9a-fA-F]{2}', options['--key'])
        for key_byte in key_hex:
            key.append(int(key_byte, 16))
        cleartext = decrypt(ciphertext, key)
        print "Key:", printable_key(key)
        print "Cleartext:", cleartext

    if options['-f']:
        find_key_lengths(ciphertext, 30)        

    if options['-g']:
        guess_key_value(ciphertext, int(options['--length']))

def printable_key(key):
    key_ascii_string = ''
    key_hex_string = ''
    for key_byte in key:
        key_ascii_string += printable_character(key_byte)
        key_hex_string += hex(key_byte)[2:].upper()
    return key_ascii_string + " (" + key_hex_string +")"

def guess_key_value(ciphertext, keylength):
    guessed_key = [0 for x in range(keylength)]

    for column in range(keylength):
        max_score = 0
        for key_byte in range(256):
            score = 0
            for position in range(len(ciphertext)):
                if ((position - column) % keylength == 0):
                    cleartext_byte = ciphertext[position] ^ key_byte
                    score += get_score(cleartext_byte)
            if (score > max_score):
                max_score = score
                guessed_key[column] = key_byte
    print "Probable key:", printable_key(guessed_key)
    cleartext = decrypt(ciphertext, guessed_key)
    print "Cleartext:", cleartext

def get_score(cleartext_byte):
    score = 0

    if ((cleartext_byte >= 32) and (cleartext_byte < 255)):
        score += 1;
    if ((chr(cleartext_byte) >= 'A') and (chr(cleartext_byte) <= 'Z')):
        score += 1;
    if ((chr(cleartext_byte) >= 'a') and (chr(cleartext_byte) <= 'z')):
        score += 2;
    if (chr(cleartext_byte) == '_'): # Roadsec ciphertext hack
        score += 2;
    if (chr(cleartext_byte) == ' '):
        score += 5;
    if (chr(cleartext_byte) == ','):
        score += 2;
    if ((chr(cleartext_byte) == '.') or (chr(cleartext_byte) == '!') or
        (chr(cleartext_byte) == ';') or (chr(cleartext_byte) == '?')):
        score += 1;

    return score

def find_key_lengths(ciphertext, max_key_length):
    total_ic = {}

    for candidate_key_length in range(1, max_key_length + 1):
        # Frequencies of each column
        frequencies = [[0 for x in range(max_key_length)] for y in range(256)]
        for position in range(len(ciphertext)):
            column = position % candidate_key_length;
            frequencies[ciphertext[position]][column] += 1

        # Length of text in each column (N)
        length_n = [0 for x in range (max_key_length)]
        for column in range(candidate_key_length):
            for character in range(256):
                length_n[column] += frequencies[character][column]

        # Calculate ni * (ni -1)
        for column in range(candidate_key_length):
            for character in range(256):
                frequencies[character][column] *= frequencies[character][column] * (frequencies[character][column] - 1)

        # Calculates sum(ni*(ni-1)) for each column
        frequency_sum = [0 for x in range (max_key_length)]
        for column in range(candidate_key_length):
            for character in range(256):
                frequency_sum[column] += frequencies[character][column]

        # Index of coincidence for each column (sum(ni*(ni-1)))/(N*(N-1))
        column_ic = [0 for x in range (max_key_length)]
        for column in range(candidate_key_length):
            if length_n[column] > 1:
                column_ic[column] = frequency_sum[column] / (length_n[column] * (length_n[column] - 1.0))

        # Total index of coincidence for this key length
        ic = 0
        for column in range(candidate_key_length):
            ic += column_ic[column]
        total_ic[candidate_key_length] = ic

    sorted_total_ic = sorted(total_ic.items(), key=lambda x:x[1], reverse=True)
    print "Most probable key lengths"
    print "Length        Index of coincidence"
    for i in range(10):
        print  '{:>4}'.format(sorted_total_ic[i][0]), "       ", '{:>10.3f}'.format(sorted_total_ic[i][1])


def load_ciphertext(ciphertext_file):
    ciphertext = []
    file = open(ciphertext_file)
    ciphertext_hex = re.findall('[0-9a-fA-F]{2}', file.read())
    for ciphertext_byte in ciphertext_hex:
        ciphertext.append(int(ciphertext_byte, 16))
    file.close
    return ciphertext

def decrypt(ciphertext, key):
    cleartext = ''
    for i in range(len(ciphertext)):
        cleartext_byte = ciphertext[i] ^ key[i % len(key)]
        cleartext += printable_character(cleartext_byte)
    return cleartext

def printable_character(character):
    return '.' if ((character < 32) or (character > 127)) else chr(character)

main()