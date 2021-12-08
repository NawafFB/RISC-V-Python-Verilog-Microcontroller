from myhdl import block, always, instances, instance, Signal, intbv, delay, bin, now, always_comb

'''

file register block
this block represents a file register component in the CPU
it will hold 32-bit x 32 memory elements.
this block is clock sensitive (sequential)

'''


@block
def file_register(clk, regWrite, data, rs1address, rs2address, rdaddress, rs1out, rs2out):
    # 32-bit x 32 list representing a temporary memory for the CPU
    register = [Signal(intbv(0, min=(-2 ** 31), max=(2 ** 31))) for i in range(32)]

    @always(clk.posedge)
    def registerUpdate():

        if regWrite == 0b1:
            register[rdaddress].next = data  # update the rd location

        # print('now %s registers: ' % now())
        # for i in range(13):
        #     print('register', i, ':', int(register[i]))
        # print('end')

    @always_comb
    def out():
        rs1out.next = register[rs1address]  # output the value of register at rs1
        rs2out.next = register[rs2address]  # output the value of register at rs2

    return instances()


'''

clock driver block.
this block will generate a high and low pulses
depending on the period, default = 10.

this block will generate clock pulses until the 
simulation is over.

'''


@block
def clock_driver(clk, period=10):
    lowTime = int(period / 2)
    highTime = period - lowTime

    @instance
    def drive_clk():
        while True:
            yield delay(lowTime)
            clk.next = 1
            yield delay(highTime)
            clk.next = 0

    return drive_clk


'''

test bench block
this block is simply to test whether or not 
the file register block is working or not
by following these steps:

1 - store integer value (200) at location 21
    and store (450) at location 22 by using 
    rdAddress, data and writeEnable signals

2- select the previous locations as the input
    for the rs1Address and rs2Address variables
    
3 - print the values of rs1Out and rs2Out

'''


@block
def testBench():
    clock = Signal(bool(0))
    rs1Address = Signal(intbv(0))
    rs2Address = Signal(intbv(0))
    rdAddress = Signal(intbv(0))
    writeEnable = Signal(bool(0))
    data = Signal(intbv(0))
    rs1Out = Signal(intbv(0))
    rs2Out = Signal(intbv(0))

    clk = clock_driver(clock)
    AllRegisters = file_register(clock, writeEnable, data, rs1Address, rs2Address, rdAddress, rs1Out, rs2Out)

    @instance
    def test():
        rs2Address.next = 22  # rs2 address is set to 22
        rs1Address.next = 21  # rs1 address is set to 21

        writeEnable.next = 1  # enable the writing mode
        rdAddress.next = 21  # update the value of rdAddress to 21
        data.next = 200  # the input data to the register at rd is 200
        yield clock.negedge  # wait for the clock
        print(int(rs1Out), int(rs2Out))

        # test the file register by trying to write 450 at address at 20
        writeEnable.next = 1  # enable the writing mode
        rdAddress.next = 22  # update the value of rdAddress to 22
        data.next = 450  # the input data to the register at rd is 450
        yield clock.negedge  # wait for the clock
        print(int(rs1Out), int(rs2Out))

        writeEnable.next = 1  # disable the writing mode
        yield clock.negedge  # wait for the clock
        print(int(rs1Out), int(rs2Out))

    return instances()


# example = testBench()
# example.run_sim(100)

# Verilog Conversion #

if __name__ == '__main__':
    rs1in1 = Signal(intbv(0, min=0, max=2 ** 5))
    rs2in1 = Signal(intbv(0, min=0, max=2 ** 5))
    rdin1 = Signal(intbv(0, min=0, max=2 ** 5))
    rs1Out1 = Signal(intbv(0, min=(-2 ** 31), max=(2 ** 31)))
    rs2Out1 = Signal(intbv(0, min=(-2 ** 31), max=(2 ** 31)))
    writeEnable1 = Signal(bool(0))
    clock1 = Signal(bool(0))
    data1 = Signal(intbv(0, min=(-2 ** 31), max=(2 ** 31)))

    tb = file_register(clock1, writeEnable1, data1, rs1in1, rs2in1, rdin1, rs1Out1, rs2Out1)
    tb.run_sim()
    tb.convert(hdl='verilog')
