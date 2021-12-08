from myhdl import *

# constant size of a single block
memory_size = 32
'''
memory bank
A single bank that represent the memory element in the RAM module. It is used to store data for future use by the CPU.
'''
@block
def MemoryBank(CLK, STB_I, WE_I, DATA_IN, ADDR, DATA_OUT):
    memory = [Signal(intbv(0)[8:]) for i in range(memory_size)]

    @always_comb
    def read():  # read doesn't require a clock
        if STB_I[3]:
            if WE_I == 0:
                DATA_OUT.next = memory[ADDR]

    @always(CLK.posedge)  # write requires a clock
    def write():
        if STB_I[3]:
            if WE_I:
                memory[ADDR].next = DATA_IN

    return instances()


@block
def Memory_block(CLK, STB_I, WE_I, DATA_IN_1, DATA_IN_2, DATA_IN_3, DATA_IN_4,
                 ADDRESS, DATA_OUT_1, DATA_OUT_2, DATA_OUT_3, DATA_OUT_4):
    bank_1 = MemoryBank(CLK, STB_I, WE_I, DATA_IN_1, ADDRESS, DATA_OUT_1)
    bank_2 = MemoryBank(CLK, STB_I, WE_I, DATA_IN_2, ADDRESS, DATA_OUT_2)
    bank_3 = MemoryBank(CLK, STB_I, WE_I, DATA_IN_3, ADDRESS, DATA_OUT_3)
    bank_4 = MemoryBank(CLK, STB_I, WE_I, DATA_IN_4, ADDRESS, DATA_OUT_4)

    return instances()

'''
write Decoder
A module that will receive a 32-bit signals, seperate them into four 8-bit signals, one for each bank
'''
@block
def WriteDecoder(WE_I, DATA_IN, STB_I,  # ADDRESS_IN, ADDRESS_OUT,
                 DATA_OUT_1, DATA_OUT_2, DATA_OUT_3, DATA_OUT_4):
    @always_comb
    def DecodeWrite():
        if WE_I:    # check if write is enabled

            if STB_I[3:] == 0b000:  # SB
                DATA_OUT_1.next = DATA_IN[8:]
                DATA_OUT_2.next = 0
                DATA_OUT_3.next = 0
                DATA_OUT_4.next = 0

            elif STB_I[3:] == 0b001:  # SH
                DATA_OUT_1.next = DATA_IN[8:]
                DATA_OUT_2.next = DATA_IN[16:8]
                DATA_OUT_3.next = 0
                DATA_OUT_4.next = 0

            elif STB_I[3:] == 0b010:  # SW
                DATA_OUT_1.next = DATA_IN[8:]
                DATA_OUT_2.next = DATA_IN[16:8]
                DATA_OUT_3.next = DATA_IN[24:16]
                DATA_OUT_4.next = DATA_IN[32:24]

    return instances()

'''
Read Decoder
A module that will combine four 8-bit signals coming from memory banks into one 32-bit signal.
'''
@block
def ReadDecoder(WE_I, STB_I, DATA_IN_1, DATA_IN_2, DATA_IN_3, DATA_IN_4, DATA_OUT):
    @always_comb
    def DecodeRead():
        if STB_I[3] == 1:
            if WE_I == 0:
                if STB_I[3:] == 0b000:  # LB
                    if DATA_IN_1[7] == 0:
                        DATA_OUT.next = concat(intbv(0)[24:], DATA_IN_1)
                    elif DATA_IN_1[7] == 1:
                        DATA_OUT.next = concat(intbv(0b111111111111111111111111)[24:], DATA_IN_1)   # extend the sign

                elif STB_I[3:] == 0b001:  # LH
                    if DATA_IN_2[7] == 0:
                        DATA_OUT.next = concat(intbv(0)[16:], DATA_IN_2, DATA_IN_1)
                    elif DATA_IN_2[7] == 1:
                        DATA_OUT.next = concat(intbv(0b1111111111111111)[16:], DATA_IN_2, DATA_IN_1)   # extend the sign

                elif STB_I[3:] == 0b010:  # LW
                    DATA_OUT.next = concat(DATA_IN_4, DATA_IN_3, DATA_IN_2, DATA_IN_1)

                elif STB_I[3:] == 0b100:  # LBU
                    DATA_OUT.next = concat(intbv(0)[24:], DATA_IN_1)

                elif STB_I[3:] == 0b101:  # LHU
                    DATA_OUT.next = concat(intbv(0)[16:], DATA_IN_2, DATA_IN_1)

    return instances()

'''
shift the address coming from the CPU 2 bits to the right, since the first two LSBs are not used.
'''
@block
def ADDR_REG(ADDR_IN, ADDR_OUT):
    @always_comb
    def calc():
        ADDR_OUT.next = ADDR_IN >> 2

    return instances()

'''
SBA Random Access Memory Module

@input: CLK - clock to drive the RAM module
@input: STB - enable signal and optional bits
@input: DATA_IN - input data to be stored
@input: ADDRESS_IN - address of the desired memory element
@output: DATA_OUT - output data
'''
@block
def SBA_RAM(CLK, STB_I, DATA_IN, WE_I, ADDRESS_IN, DATA_OUT):
    WR_DATA_OUT_1 = Signal(intbv(0)[8:])
    WR_DATA_OUT_2 = Signal(intbv(0)[8:])
    WR_DATA_OUT_3 = Signal(intbv(0)[8:])
    WR_DATA_OUT_4 = Signal(intbv(0)[8:])

    Sliced_Address = Signal(intbv(0)[12:])

    MEM_DATA_OUT_1 = Signal(intbv(0)[8:])
    MEM_DATA_OUT_2 = Signal(intbv(0)[8:])
    MEM_DATA_OUT_3 = Signal(intbv(0)[8:])
    MEM_DATA_OUT_4 = Signal(intbv(0)[8:])

    addr_reg = ADDR_REG(ADDRESS_IN, Sliced_Address)

    WR_DECODER = WriteDecoder(WE_I, DATA_IN, STB_I, WR_DATA_OUT_1, WR_DATA_OUT_2, WR_DATA_OUT_3, WR_DATA_OUT_4)

    MEM_BANKS = Memory_block(CLK, STB_I, WE_I, WR_DATA_OUT_1, WR_DATA_OUT_2, WR_DATA_OUT_3, WR_DATA_OUT_4,
                             Sliced_Address, MEM_DATA_OUT_1, MEM_DATA_OUT_2, MEM_DATA_OUT_3, MEM_DATA_OUT_4)

    RD_DECODER = ReadDecoder(WE_I, STB_I, MEM_DATA_OUT_1, MEM_DATA_OUT_2, MEM_DATA_OUT_3, MEM_DATA_OUT_4, DATA_OUT)

    return instances()


@block
def Testbench():
    CLK = Signal(bool(0))
    DATA_IN = Signal(intbv(0)[32:])
    WE_I = Signal(bool(0))
    STB_I = Signal(intbv(0)[4:])
    ADDRESS_IN = Signal(intbv(0)[12:])
    DATA_OUT = Signal(intbv(0)[32:])

    MEM = SBA_RAM(CLK, STB_I, DATA_IN, WE_I, ADDRESS_IN, DATA_OUT)

    @always(delay(5))
    def clk_driver():
        CLK.next = not CLK

    @instance
    def run():
        yield delay(1)
        STB_I.next = 0b1010  # STB enable + whole word
        DATA_IN.next = 0b11111111111111111111111111111111
        WE_I.next = 1   # enable write
        ADDRESS_IN.next = 8

        yield delay(5)

        WE_I.next = 0   # read write
        STB_I.next = 0b1001  # STB enable + half word
        ADDRESS_IN.next = 8

        yield CLK.negedge

        print("outData is", int(DATA_OUT))

    return instances()


# tb = Testbench()
# tb.run_sim(100)

if __name__ == '__main__':
    CLK = Signal(bool(0))
    DATA_IN = Signal(intbv(0)[32:])
    WE_I = Signal(bool(0))
    STB_I = Signal(intbv(0)[4:])
    ADDRESS_IN = Signal(intbv(0)[12:])
    DATA_OUT = Signal(intbv(0)[32:])

    MEM = SBA_RAM(CLK, STB_I, DATA_IN, WE_I, ADDRESS_IN, DATA_OUT)

    MEM.run_sim()
    MEM.convert(hdl='verilog')
