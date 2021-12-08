from myhdl import *

'''
SBA bus system

this class/module represents the bus that will connect the CPU with other peripherals.
the master (CPU) is in control of the MST_XX_O, STB_I, ALU_OUTPUT_ADDR_I, WE_O signals.
slaves are in control of the SLV_DAT_O_X signal.
'''


@block
def BusSystem(MST_DAT_I, MST_DAT_O, SLV_DAT_I, SLV_DAT_O_1,
              SLV_DAT_O_2, SLV_DAT_O_3, SLV_DAT_O_4, SLV_DAT_O_5, SLV_DAT_O_6,
              ALU_OUTPUT_ADDR_I, ADDR_O, WE_I, WE_O, STB_I, STB_O_1, STB_O_2,
              STB_O_3, STB_O_4, STB_O_5, STB_O_6, RST_I, RST_O, CLK_I, CLK_O):
    @always_comb
    def Bus():

        SLV_DAT_I.next = MST_DAT_O  # Data Output Bus

        if STB_I[3]:
            MST_DAT_I.next = SLV_DAT_O_1  # data from device 1
        elif STB_I[5]:
            MST_DAT_I.next = SLV_DAT_O_3  # data from device 1
        elif STB_I[6]:
            MST_DAT_I.next = SLV_DAT_O_4  # data from device 1
        elif STB_I[7]:
            MST_DAT_I.next = SLV_DAT_O_5  # data from device 1
        elif STB_I[8]:
            MST_DAT_I.next = SLV_DAT_O_6  # data from device 1

        ADDR_O.next = ALU_OUTPUT_ADDR_I[9:]  # Address BUS

        CLK_O.next = CLK_I
        RST_O.next = RST_I
        STB_O_1.next = concat(STB_I[3], STB_I[3:0])  # signal to device 1
        STB_O_2.next = concat(STB_I[4], STB_I[3:0])  # signal to device 2
        STB_O_3.next = concat(STB_I[5], STB_I[3:0])  # signal to device 3
        STB_O_4.next = concat(STB_I[6], STB_I[3:0])  # signal to device 4
        STB_O_5.next = concat(STB_I[7], STB_I[3:0])  # signal to device 5
        STB_O_6.next = concat(STB_I[8], STB_I[3:0])  # signal to device 6

        WE_I.next = WE_O

    return instances()
