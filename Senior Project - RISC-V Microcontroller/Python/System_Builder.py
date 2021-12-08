import sys

ram = int(sys.argv[1])           # |
pwm = int(sys.argv[2])           # |
output_port = int(sys.argv[3])   # | <---- input from the user via commandline
input_port = int(sys.argv[4])
timer = int(sys.argv[5])         # |
uart = int(sys.argv[6])          # |

num_slaves = ram + pwm + input_port + output_port + timer + uart  ### calculated by the program

if uart > 1 or ram > 1:
    print('')

'''  python system_Builder.py RAM PWM output_Port input_port TIMER UART '''


def Busbuilder():
    default_string = "from myhdl import *\n\n@block\ndef " \
                     "BusSystem(MST_DAT_I, MST_DAT_O, SLV_DAT_I, GGG " \
                     "ALU_OUTPUT_ADDR_I, ADDR_O, WE_I, WE_O, STB_I, XXX RST_I, RST_O, CLK_I, CLK_O):" \
                     "\n\n\t@always_comb\n\tdef Bus():\n\n\t\tSLV_DAT_I.next = MST_DAT_O\n\n\t\tYYY\n\n\t\tADDR_O.next = ALU_OUTPUT_ADDR_I[9:]\n\t\t" \
                     "CLK_O.next = CLK_I\n\t\tRST_O.next = RST_I\n\t\tZZZ\n\t\tWE_I.next = WE_O\n\n\treturn instances()\n"

    '''SLV_DAT_O_1,SLV_DAT_O_2, SLV_DAT_O_3, SLV_DAT_O_4," \
                     " SLV_DAT_O_5'''
    '''STB_O_&'''

    # num_slaves = 7
    slave_wire = 'SLV_DAT_O_$, '

    wires = ''
    for i in range(num_slaves):
        wires = wires + slave_wire.replace('$', str(i + 1))
    default_string = default_string.replace('GGG', wires)

    enable_signals = ''
    slave_enables = 'STB_O_$, '
    for i in range(num_slaves):
        enable_signals = enable_signals + slave_enables.replace('$', str(i + 1))
    default_string = default_string.replace('XXX', enable_signals)
    '''
     @ for base (STB)
     $ for slave count
    '''

    base = 3
    slave_counter = 2
    firstLine = "if STB_I[3]:\n\t\t\tMST_DAT_I.next = SLV_DAT_O_1\n"
    rest = "\t\telif STB_I[@]:\n\t\t\tMST_DAT_I.next = SLV_DAT_O_$\n"

    FullString = ''
    FullString = FullString + firstLine
    for i in range(num_slaves - 1):
        FullString = FullString + rest.replace('@', str(base + 1)).replace('$', str(slave_counter))
        base = base + 1
        slave_counter = slave_counter + 1

    '''  & for peripheral number   '''
    base = 4
    YYY1 = "STB_O_1.next = concat(STB_I[3], STB_I[3:0])\n"
    YYY2 = "\t\tSTB_O_&.next = concat(STB_I[@], STB_I[3:0])\n"

    Second = ''

    for i in range(num_slaves):
        if i == 0:
            Second = Second + YYY1
        else:
            Second = Second + YYY2.replace('&', str(i + 1)).replace('@', str(base))
            base = base + 1

    default_string = default_string.replace('YYY', FullString).replace('ZZZ', Second)
    # print(default_string)
    BusFile = open('SBA_BUS_GENERATED.py', 'w')
    BusFile.write(default_string)
    BusFile.close()
    print('BUS DONE ....')


def DECODER(ram, num_slaves):
    Decoder = "from myhdl import *\n\n@block\ndef SBA_DECODER(STB_I, ADDR_I, STB_O):\n\t@always_comb\n\tdef decode():\n\t\tif STB_I[0]:\nxxx" \
              "\t\telse:\n\t\t\tSTB_O.next = 0  # disable all modules\n\treturn decode"

    DEC_firstLine_RAM = '\t\t\tif ADDR_I <= 1023:\n\t\t\t\tSTB_O.next = concat(intbv(1)[AAA:], STB_I[4:1])  # RAM || address = 0 -> 1023 \n'.replace('AAA',str(num_slaves))
    DEC_firstLine_NoRAM = '\t\t\tif ADDR_I == &:\n\t\t\t\tSTB_O.next = concat(intbv($)[AAA:], STB_I[4:1])  \n'.replace('AAA',str(num_slaves))
    DEC_rest = '\t\t\telif ADDR_I == &:\n\t\t\t\tSTB_O.next = concat(intbv($)[AAA:], STB_I[4:1])  # HHH \n'.replace('AAA',str(num_slaves))
    DEC_UART = '\t\t\telif ADDR_I == &:\n\t\t\t\tSTB_O.next = concat(intbv($)[AAA:], intbv(XXX)[3:]) # UART ADDRESS SSS \n'.replace('AAA',str(num_slaves))

    fullDecode = ''
    base = 0
    indication_bit = 1
    if ram:
        fullDecode += DEC_firstLine_RAM
        base += 1024
        indication_bit *= 2
    else:
        fullDecode += (DEC_firstLine_NoRAM.replace('&', str(base)).replace('$', str(indication_bit)))
        base += 1
        indication_bit *= 2
    if uart:
        fullDecode += (
            DEC_UART.replace('&', str(base)).replace('$', str(indication_bit)).replace('XXX','0').replace('SSS','0 || address = {}'.format(base)))
        base += 1
        fullDecode += (
            DEC_UART.replace('&', str(base) ).replace('$', str(indication_bit))).replace('XXX','1').replace('SSS','1 || address = {}'.format(base))
        base += 1
        fullDecode += (
            DEC_UART.replace('&', str(base) ).replace('$', str(indication_bit))).replace('XXX','2').replace('SSS','2 || address = {}'.format(base))
        base += 1
        indication_bit *= 2
        num_slaves -= 1

    if input_port > 0:
        for i in range(input_port):
            fullDecode += (DEC_rest.replace('&', str(base)).replace('$', str(indication_bit))).replace('HHH','input_port_{} || address = {}'.format(i,base))
            base += 1
            indication_bit *= 2
    if output_port > 0:
        for i in range(output_port):
            fullDecode += (DEC_rest.replace('&', str(base)).replace('$', str(indication_bit))).replace('HHH','output_port_{} || address = {}'.format(i,base))
            base += 1
            indication_bit *= 2
    if timer > 0:
        for i in range(timer):
            fullDecode += (DEC_rest.replace('&', str(base)).replace('$', str(indication_bit))).replace('HHH','timer_{} || address = {}'.format(i,base))
            base += 1
            indication_bit *= 2
    if pwm > 0:
        for i in range(pwm):
            fullDecode += (DEC_rest.replace('&', str(base)).replace('$', str(indication_bit))).replace('HHH','pwm_{} || address = {}'.format(i,base))
            base += 1
            indication_bit *= 2

    # for i in range(num_slaves - 1):
    #     fullDecode += (DEC_rest.replace('&', str(base)).replace('$', str(indication_bit)))
    #     base += 1
    #     indication_bit *= 2

    Decoder = Decoder.replace('xxx', fullDecode)
    # print(Decoder)
    DecoderFile = open('SBA_DECODER_GENERATED.py', 'w')
    DecoderFile.write(Decoder)
    DecoderFile.close()
    print('DECODER DONE ....')

Busbuilder()
# print('-------------------------------------------------------------------------------------')
DECODER(ram, num_slaves)
# print('-------------------------------------------------------------------------------------')
def Top_Level_Build():
    imports = 'from myhdl import * \nfrom SBA_CPU import SBA_CPU \n' \
              'from SBA_DECODER_GENERATED import SBA_DECODER\n' \
              'from SBA_BUS_GENERATED import BusSystem\n' \
              'from SBA_RAM import SBA_RAM\n' \
              'from IO_port import output_port\n' \
              'from IO_port import input_port\n' \
              'from SBA_Timer import SBA_TIMER\n' \
              'from SBA_PWM import SBA_PWM\n' \
              'from UART_SYS import SBA_UART_SYS\n\n'

    NETLIST = 'def Microcontroller_GEN(clk, reset'

    beginning = '@block\nRRR):\n\n\t    # CPU Signal\n\t' \
                '    STB_O = Signal(intbv(0)[4:])\n\t    WE_O = Signal(bool(0))\n\n\t    # Decoder Signals\n\t' \
                '    DEC_STB_O = Signal(intbv(0)[BBB:])\n\n\t    # Bus Signals\n\t' \
                '    MST_DAT_I, MST_DAT_O, SLV_DAT_I, ALU_OUTPUT_ADDR_I = [Signal(intbv(0)[32:]) for i in range(4)]\n\t' \
                '    ADDR_O = Signal(intbv(0)[9:])\n\t' \
                '    WE_I, RST_O, CLK_O = [Signal(bool(0)) for i in range(3)]\n\t' \
                '    SBA_CPU_driver = SBA_CPU(clk, MST_DAT_I, WE_O, STB_O, ALU_OUTPUT_ADDR_I, MST_DAT_O)\n\t' \
                '    SBA_DECODER_driver = SBA_DECODER(STB_O, ALU_OUTPUT_ADDR_I, DEC_STB_O)\n'.replace('BBB', str(num_slaves+3))
    # print(beginning)
    slave_wires = ''
    slave_ports = ''
    slave_enables = ''
    slave_enables_ports = ''

    for i in range(num_slaves):
        slave_wires += '\t\tSLV_DAT_O_'+str(i+1) + ' = Signal(intbv(0)[32:])\n'
        slave_ports += 'SLV_DAT_O_'+str(i+1)+ ' ,'
        slave_enables += '\t\tSTB_O_'+str(i+1) + ' = Signal(intbv(0)[4:])\n'
        slave_enables_ports += 'STB_O_'+str(i+1) + ','


    busDriver = '\t\tSBA_BUS_driver = BusSystem(MST_DAT_I, MST_DAT_O,' \
                ' SLV_DAT_I, XXX ' \
                'ALU_OUTPUT_ADDR_I, ADDR_O, WE_I, WE_O, DEC_STB_O,' \
                ' YYY' \
                ' rest, RST_O, clk, CLK_O) \n'

    busDriver = busDriver.replace('XXX', slave_ports).replace('YYY', slave_enables_ports)

    STB_O_list = slave_enables_ports.split(',')
    SLV_O_list = slave_ports.split(',')
    # print(STB_O_list,'----------')
    # print(SLV_O_list,'---------')


    drivers = ''

    if ram:
        drivers += '\t\tSBA_RAM_driver = SBA_RAM(CLK_O, XXX, SLV_DAT_I, WE_O, ADDR_O, YYY)\n'.replace('XXX',STB_O_list.pop(0)).replace('YYY',SLV_O_list.pop(0))

    if uart > 0:
        NETLIST += ', TX, RX'
        drivers += '\t\tSBA_UART_driver_zzz = SBA_UART_SYS(CLK_O, RST_O, SLV_DAT_I, WE_O, XXX, ADDR_O, YYY, TX, RX)\n'.replace('XXX',STB_O_list.pop(0)).replace('YYY',SLV_O_list.pop(0)).replace('zzz',str(i))

    if output_port > 0:
        for i in range(output_port):
            NETLIST += ', Output_port_data_{}'.format(i)
            drivers += '\t\tSBA_output_port_zzz = output_port(XXX, SLV_DAT_I, CLK_O, YYY)\n'.replace('XXX',STB_O_list.pop(0)).replace('zzz',str(i)).replace('YYY','Output_port_data_{}'.format(i))
            SLV_O_list.pop(0)

    if input_port > 0:
        for i in range(input_port):
            NETLIST += ', input_port_data_{}'.format(i)
            drivers += '\t\tSBA_input_port_zzz = input_port(XXX, GGG, YYY)\n'.replace('XXX',STB_O_list.pop(0)).replace('zzz',str(i)).replace('GGG','input_port_data_{}'.format(i)).replace('YYY',SLV_O_list.pop(0))

    if pwm > 0:
        for i in range(pwm):
            NETLIST += ', PWM_Signal_{}'.format(i)
            drivers += '\t\tSBA_PWM_driver_zzz = SBA_PWM(SLV_DAT_I, RST_O, CLK_O, XXX, YYY)\n'.replace('XXX',STB_O_list.pop(0))\
                .replace('zzz',str(i)).replace('YYY','PWM_Signal_{}'.format(i))
            SLV_O_list.pop(0)

    if timer > 0:
        for i in range(timer):
            drivers += '\t\tSBA_TIMER_driver_zzz = SBA_TIMER(XXX, SLV_DAT_I, CLK_O, RST_O, YYY)\n'.replace('XXX',STB_O_list.pop(0)).replace('YYY',SLV_O_list.pop(0)).replace('zzz',str(i))

    beginning = beginning.replace('RRR', NETLIST)

    # print(imports)
    # print(beginning)
    # print(slave_enables)
    # print(slave_wires)
    #
    # print(busDriver)
    # print(drivers)
    # print('\t\treturn instances()')

    DecoderFile = open('SBA_SYSTEM_GENERATED.py', 'w')
    DecoderFile.write(imports)
    DecoderFile.write(beginning)
    DecoderFile.write(slave_enables)
    DecoderFile.write(slave_wires)
    DecoderFile.write(busDriver)
    DecoderFile.write(drivers)
    DecoderFile.write('\t\treturn instances()')
    DecoderFile.close()
    print('TOP LEVEL DONE ...')

Top_Level_Build()