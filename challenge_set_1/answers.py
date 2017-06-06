#! /usr/bin/python
# Challenge 2+ & conversion of bytes
import struct
# Challenge 3
import string


def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])


def xor(a_byte, b_byte):
    return struct.pack('B', (ord(a_byte) ^ ord(b_byte)))


def character_frequency(input_str):
    """
        Takes an input string and determines the chi^2 value for it's contents.
        The chi^2 value is a kind of 'score' of the character frequency for the
        contents of a string. higher-scores mean the string is more likely
        english.
    """
    expected_character_frequency = {
        'a': 8.167,
        'b': 1.492,
        'c': 2.782,
        'd': 4.253,
        'e': 12.702,
        'f': 2.228,
        'g': 2.015,
        'h': 6.094,
        'i': 6.966,
        'j': 0.153,
        'k': 0.772,
        'l': 4.025,
        'm': 2.406,
        'n': 6.749,
        'o': 7.507,
        'p': 1.929,
        'q': 0.095,
        'r': 5.987,
        's': 6.327,
        't': 9.056,
        'u': 2.758,
        'v': 0.978,
        'w': 2.360,
        'x': 0.150,
        'y': 1.974,
        'z': 0.074,
        # FIXME for challenge 4 I've had to fudge this list by including the
        # below space character in order to ensure the score alg chose the
        # correct sentance. The current value (5.00) is probably a tad high.
        ' ': 5.00
    }
    occurance_count = {char: 0 for char in string.ascii_lowercase+' '}
    ignored = 0
    for character in input_str:
        if character in string.ascii_letters + ' ':
            occurance_count[character.lower()] += 1
        else:
            ignored += 1

    chi_squared = 0
    length_of_input = len(input_str)
    if ignored == length_of_input:
        return 0
    for char, occurance in occurance_count.items():
        expected = (
            float(length_of_input - ignored)
            * expected_character_frequency[char]
        )
        if not expected:
            # Sometimes the expected value is zero.
            print((
                length_of_input,
                ignored,
                expected_character_frequency[char]
            ))
            continue
        difference = occurance - expected
        chi_squared += difference * difference / expected
    return chi_squared


def challenge_1():
    print('\nChallenge 1')
    expected_output = \
        'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
    hex_input = \
        '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736\
f6e6f7573206d757368726f6f6d'
    base64_output = hex_input.decode('hex').encode('base64')
    # Theres a new line character at the end of the string that doesn't appear
    # to be in the expected output string. just strip it.
    base64_output = base64_output.strip()
    print('OUTPUT: {}'.format(base64_output))
    print('EXPECTED: {}'.format(expected_output))
    print('PASS [{}]'.format(base64_output == expected_output))


def challenge_2():
    print('\nChallenge 2')
    expected_output = '746865206b696420646f6e277420706c6179'
    hex_input1 = '1c0111001f010100061a024b53535009181c'
    hex_input2 = '686974207468652062756c6c277320657965'

    def xor(a, b):
        obuf = b''
        for a_byte, b_byte in zip(a, b):
            obuf += struct.pack('B', (ord(a_byte) ^ ord(b_byte)))
        return obuf.encode('hex')

    answer = xor(hex_input1.decode('hex'), hex_input2.decode('hex'))
    print('OUTPUT: {}'.format(answer.decode('hex')))
    print('EXPECTED: {}'.format(expected_output.decode('hex')))
    print('PASS [{}]'.format(answer == expected_output))


def challenge_3():
    print('\nChallenge 3')
    hex_input = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a3\
93b3736'

    def xor(a_byte, b_list):
        obuf = b''
        for b_byte in b_list:
            obuf += struct.pack('B', (ord(a_byte) ^ ord(b_byte)))
        return obuf

    start_byte = b'\x00'
    results = []
    while start_byte != b'\xff':
        output = xor(start_byte, hex_input.decode('hex'))
        score = character_frequency(output)
        results.append((score, output))
        start_byte = struct.pack('B', ord(start_byte) + 1)

    results.sort(key=lambda x: x[0], reverse=True)
    print('OUTPUT: {}'.format(results[0][1]))


def challenge_4():
    print('\nChallenge 4')

    def xor(a_byte, b_list):
        obuf = b''
        for b_byte in b_list:
            obuf += struct.pack('B', (ord(a_byte) ^ ord(b_byte)))
        return obuf

    scored_output = []
    raw_ = ''
    with open('4.txt', 'r') as f:
        raw_ = f.read()
    for line in raw_.split():
        buf = line.decode('hex')
        start_byte = b'\x00'
        count = (16 * 16) - 1
        while count:
            output = xor(start_byte, buf)
            score = character_frequency(output)
            scored_output.append((score, output))
            start_byte = struct.pack('B', ord(start_byte) + 1)
            count -= 1
    scored_output.sort(key=lambda x: x[0], reverse=True)
    print(scored_output[0][1])


def challenge_5():
    print('\nChallenge 5')
    expected_output = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343\
c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b202831652\
86326302e27282f'
    input_str = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
    KEY = 'ICE'
    pointer = 0
    obuf = b''
    for char in input_str:
        obuf += xor(KEY[pointer % 3], char)
        pointer += 1
    print('PASS [{}]'.format(obuf.encode('hex') == expected_output))


if __name__ == '__main__':
    challenge_1()
    challenge_2()
    challenge_3()
    challenge_4()
    challenge_5()
