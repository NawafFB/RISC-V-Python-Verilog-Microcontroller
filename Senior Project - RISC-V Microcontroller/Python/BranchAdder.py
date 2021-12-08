from myhdl import always_comb, block, instances, Signal, intbv

'''adder block
this block an adder that will output
the sum of the pc and an immediate value.

@input : pc
@input : imm
@output : result
'''


@block
def braAdder(pc, imm, result):
    @always_comb
    def add():
        result.next = pc + (imm << 1)

    return instances()


if __name__ == '__main__':
    pc = Signal(intbv(0, min=0, max=(2 ** 32)))
    imm = Signal(intbv(0, min=0, max=(2 ** 32)))
    result = Signal(intbv(0, min=0, max=(2 ** 32)))

    tb = braAdder(pc, imm, result)
    tb.run_sim()
    tb.convert(hdl='verilog')
