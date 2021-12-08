from myhdl import block, always, Signal, intbv, instance, delay, instances

'''program counter block
this module will simulate the pc module
inside the CPU, it will send the address
of the current instruction to the instruction
memory, and it will also wait for the address
of th next instruction.

@input : clock
@input : nextPC
@input : enable
@output : currentPC
'''


@block
def PC(clock, nextPC, currentPC):
    counter = Signal(intbv(0, min=0, max=2 ** 32))

    @always(clock.posedge)
    def seq():
        currentPC.next = nextPC

    return instances()


"""this block is a test for the previous
PC module.
"""


@block
def test():
    clk, enable, reset = [Signal(bool(0)) for i in range(3)]
    nextPC, currentPC = [Signal(intbv(0)) for i in range(2)]

    pcTest = PC(clk, nextPC, enable, currentPC, reset)

    @always(delay(5))
    def clk_driver():
        clk.next = not clk

    @instance
    def testing():
        enable.next = 0
        print(currentPC)
        yield clk.negedge
        print(currentPC)
        yield clk.negedge
        print(currentPC)
        yield clk.negedge
        print('last:', currentPC)
        # loading finished

        enable.next = not enable
        yield delay(1)
        print('currentPC:', currentPC, 'nextPC:', nextPC)
        yield clk.negedge
        print('currentPC:', currentPC, 'nextPC:', nextPC)
        nextPC.next = 4
        yield clk.negedge
        print('currentPC:', currentPC, 'nextPC:', nextPC)
        yield clk.negedge
        print('currentPC:', currentPC, 'nextPC:', nextPC)

        yield clk.negedge
        print('currentPC:', currentPC, 'nextPC:', nextPC)
        yield clk.negedge
        print('currentPC:', currentPC, 'nextPC:', nextPC)
        yield clk.negedge
        print('currentPC:', currentPC, 'nextPC:', nextPC)
        nextPC.next = 8
        yield clk.negedge
        print('currentPC:', int(currentPC), 'nextPC:', int(nextPC))

        yield clk.negedge
        print('currentPC:', currentPC, 'nextPC:', nextPC)
        yield clk.negedge
        print('currentPC:', currentPC, 'nextPC:', nextPC)
        nextPC.next = 64
        yield clk.negedge
        print('currentPC:', currentPC, 'nextPC:', int(nextPC))
        yield clk.negedge
        print('currentPC:', currentPC, 'nextPC:', int(nextPC))

        yield clk.negedge
        print('currentPC:', int(currentPC), 'nextPC:', int(nextPC))

    return instances()


#
# tb = test()
# tb.run_sim(170)

if __name__ == '__main__':
    clock = Signal(intbv(0, min=0, max=2))
    nextPC = Signal(intbv(0, min=0, max=2 ** 32))
    currentPC = Signal(intbv(0, min=0, max=2 ** 32))

    tb = PC(clock, nextPC, currentPC)
    tb.run_sim()
    tb.convert(hdl='verilog')
