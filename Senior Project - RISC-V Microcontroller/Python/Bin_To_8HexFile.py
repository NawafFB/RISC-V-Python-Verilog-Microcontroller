path = 'TEST_PERPH'
file = open(path, 'r')

lines = file.readlines()
bank0 = open(".\\bank0.mif", 'w')
bank1 = open(".\\bank1.mif", 'w')
bank2 = open(".\\bank2.mif", 'w')
bank3 = open(".\\bank3.mif", 'w')

option = 1

DEPTH = 32
WIDTH = 8
ADDRESS_RADIX = 'HEX'
DATA_RADIX = 'HEX'

i = 0

if option == 0:
    default_txt = 'DEPTH = ' + str(DEPTH) + ';\nWIDTH = ' + str(WIDTH) + ';\nADDRESS_RADIX = ' + str(
        ADDRESS_RADIX) + ';\nDATA_RADIX = ' + str(DATA_RADIX) + ';\nCONTENT\nBEGIN\n'
    bank0.write(default_txt + '\n')
    bank1.write(default_txt + '\n')
    bank2.write(default_txt + '\n')
    bank3.write(default_txt + '\n')
    for line in lines:
        pad = 8 - len((hex(int(line, 2)))[2:])
        hex_num = '0' * pad + hex(int(line, 2))[2:]
        bank0.write('0' + hex(i)[2:].upper() + ' : ' + hex_num[6:] + '\n')
        bank1.write('0' + hex(i)[2:].upper() + ' : ' + hex_num[4:6] + '\n')
        bank2.write('0' + hex(i)[2:].upper() + ' : ' + hex_num[2:4] + '\n')
        bank3.write('0' + hex(i)[2:].upper() + ' : ' + hex_num[0:2] + '\n')
        i = i + 1

    bank0.write('\nEND')
    bank1.write('\nEND')
    bank2.write('\nEND')
    bank3.write('\nEND')
else:
    for line in lines:
        pad = 8 - len((hex(int(line, 2)))[2:])
        hex_num = '0' * pad + hex(int(line, 2))[2:]
        bank0.write(hex_num[6:] + '\n')
        bank1.write(hex_num[4:6] + '\n')
        bank2.write(hex_num[2:4] + '\n')
        bank3.write(hex_num[0:2] + '\n')



file.close()
bank0.close()
bank1.close()
bank2.close()
bank3.close()

print('done')
