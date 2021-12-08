from myhdl import always_comb, block, Signal, intbv, instance, delay, instances

'''adder block
this block represents a two operand
adder, it will return their sum.

@input : operand1
@input : operand2
@output : result
'''


@block
def adder(operand1, operand2, result):
    @always_comb
    def add():
        result.next = operand1 + operand2

    return instances()


@block
def test():
    pc, jump, res1, res2 = [Signal(intbv(0, min=0, max=100)) for i in range(4)]

    pcCounter = adder(intbv(4), pc, res1)
    branch = adder(pc, jump, res2)

    @instance
    def run():
        pc.next = 0
        jump.next = 0b1110 << 1  # "28"
        yield delay(15)
        print(res1, int(res2))

        pc.next = 4
        jump.next = 4 << 1  # "8"
        yield delay(10)
        print(res1, int(res2))

    return instances()


#
# tb = test()
# tb.run_sim(100)

if __name__ == '__main__':
    operand1 = Signal(intbv(0, min=0, max=2 ** 32))
    operand2 = Signal(intbv(0, min=0, max=2 ** 32))
    result = Signal(intbv(0, min=0, max=2 ** 32))

    tb = adder(operand1, operand2, result)
    tb.run_sim()
    tb.convert(hdl='verilog')
