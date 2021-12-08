from myhdl import *

'''
SBA Read Only Memory Module

@input: mem_write - write enable signal (never used)
@input: data_in - input data to be stored (never used)
@input: PC - address of the desired instruction
@output: DATA_OUT - output instruction
'''
@block
def ROM(mem_write, data_in, PC, INST_OUt):
    ADDR = Signal(intbv(0)[32:])
    DATA_OUT_1, DATA_OUT_2, DATA_OUT_3, DATA_OUT_4 = [Signal(intbv(0)[8:]) for i in range(4)]

    ADDR_reg = ADDR_REG(PC, ADDR)
    RAM_BLOCKS = Memory_block(mem_write, data_in, ADDR, DATA_OUT_1, DATA_OUT_2, DATA_OUT_3, DATA_OUT_4)
    DEC = INST_DEC(DATA_OUT_1, DATA_OUT_2, DATA_OUT_3, DATA_OUT_4, INST_OUt)

    return instances()


'''
combining the output of all four banks into one 32-bit signal.
'''
@block
def INST_DEC(INST_1, INST_2, INST_3, INST_4, INST_out):
    @always_comb
    def out():
        INST_out.next = concat(INST_4, INST_3, INST_2, INST_1)

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
memory bank
A single bank that represent the memory element in the ROM module. It is used to store instructions.
'''
@block
def MemoryBank(mem_write, data_in, ADDR, DATA_OUT):
    memory = [Signal(intbv(0)[8:]) for i in range(32)]

    # memory[0] = 0b11111111

    @always_comb
    def out():
        DATA_OUT.next = memory[ADDR]

    @always(mem_write.posedge)
    def write():
        memory[ADDR].next = data_in

    return instances()


@block
def Memory_block(mem_write, data_in, ADDR, DATA_OUT_1, DATA_OUT_2, DATA_OUT_3, DATA_OUT_4):
    bank_1 = MemoryBank(mem_write, data_in, ADDR, DATA_OUT_1)
    bank_2 = MemoryBank(mem_write, data_in, ADDR, DATA_OUT_2)
    bank_3 = MemoryBank(mem_write, data_in, ADDR, DATA_OUT_3)
    bank_4 = MemoryBank(mem_write, data_in, ADDR, DATA_OUT_4)

    return instances()


@block
def test():
    CLK = Signal(bool(0))
    PC = Signal(intbv(0)[32:])
    INST_OUt = Signal(intbv(0)[32:])

    inst = ROM(CLK, PC, INST_OUt)

    @always(delay(5))
    def clk_driver():
        CLK.next = not CLK

    @instance
    def run():
        yield delay(1)

        yield CLK.negedge

        print("instruction", INST_OUt)

    return instances()


# tb = test()
# tb.run_sim(100)


if __name__ == '__main__':
    PC = Signal(intbv(0)[32:])
    INST_OUt = Signal(intbv(0)[32:])
    mem_write = Signal(bool(0))
    data_in = Signal(intbv(0)[32:])

    inst = ROM(mem_write, data_in, PC, INST_OUt)

    inst.run_sim()
    inst.convert(hdl='verilog')
