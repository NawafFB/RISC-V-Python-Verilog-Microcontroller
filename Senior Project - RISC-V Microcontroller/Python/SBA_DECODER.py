from myhdl import *

'''
@input : STB_I : 3 bit coming from the master to the decoder + 1-bit to enable read/write : {funct3,en}
@input : ADDR_I : 32-bit address coming from the master to the decoder
@output : STB : 9 bit STB signal going to the control bus
'''


@block
def SBA_DECODER(STB_I, ADDR_I, STB_O):
    @always_comb
    def decode():
        if STB_I[0]:
            if ADDR_I <= 1023:  # Main Memory    ##### Edit to 256
                STB_O.next = concat(intbv(1)[6:], STB_I[4:1])
            elif ADDR_I == 1024:  # output ports
                STB_O.next = concat(intbv(2)[6:], STB_I[4:1])    # 00010 000
            elif ADDR_I == 1025:  # PWM
                STB_O.next = concat(intbv(4)[6:], STB_I[4:1])
            elif ADDR_I == 1026:  # TIMER
                STB_O.next = concat(intbv(8)[6:], STB_I[4:1])

            elif ADDR_I == 1027:  # UART
                STB_O.next = concat(intbv(16)[6:], intbv(0)[3:])   # 1 000
            elif ADDR_I == 1028:  # UART
                STB_O.next = concat(intbv(16)[6:], intbv(1)[3:])   # 1 001
            elif ADDR_I == 1029:  # UART
                STB_O.next = concat(intbv(16)[6:], intbv(2)[3:])   # 1 010

            elif ADDR_I == 1030:  # input port
                STB_O.next = concat(intbv(32)[6:], STB_I[4:1])
        else:
            STB_O.next = 0  # disable all modules

    return decode


if __name__ == '__main__':
    STB_I = Signal(intbv(0)[4:])
    ADDR_I = Signal(intbv(0)[32:])
    STB_O = Signal(intbv(0)[9:])

    tb = SBA_DECODER(STB_I, ADDR_I, STB_O)
    tb.run_sim()
    tb.convert(hdl='verilog')
