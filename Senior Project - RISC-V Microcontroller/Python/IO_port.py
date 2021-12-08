from myhdl import *


@block
def output_port(STB, inputData, clk, Q1):

    REG = EightBitReg(STB, inputData, clk, Q1)

    return instances()


@block
def input_port(STB, inputData, Q1):

    @always_comb
    def send():
        if STB[3]:
            Q1.next = inputData
    return instances()


@block
def EightBitReg(STB, D, clk, Q):

    data = Signal(intbv(0)[8:])

    @always(clk.posedge)
    def J():
        if STB[3]:
            data.next = D

    @always_comb
    def JJ():
        Q.next = data

    return instances()


@block
def tristate(input_data, enable, output_data):

    OutputDriver = output_data.driver()

    @always_comb
    def TRI():
        if enable:
            OutputDriver.next = input_data
        else:
            OutputDriver.next = None

    return instances()


# @block
# def test():
#     input_data = Signal(intbv(0))
#     enable = Signal(bool(0))
#     output_data = TristateSignal(intbv(0))
#
#     tri = tristate(input_data, enable, output_data)
#
#     @instance
#     def T():
#         input_data.next = 8
#         enable.next = 1
#         yield delay(1)
#         print(output_data)
#         enable.next = 0
#         yield delay(1)
#         print(output_data)
#
#     return instances()


@block
def test_output():
    IN = Signal(intbv(0)[8:])
    CLK = Signal(bool(0))
    out_data = Signal(intbv(0)[8:])
    STB = Signal(intbv(0)[5:])

    port = output_port(STB, IN, CLK, out_data)

    @always(delay(5))
    def clk_driver():
        CLK.next = not CLK

    @instance
    def T():
        IN.next = 8
        # print(out_data)

        yield CLK.negedge
        print(int(out_data))
        IN.next = 16
        STB.next = 0b1000
        yield CLK.negedge
        print(int(out_data))

    return instances()


# t = test_output()
# t.run_sim(50)

if __name__ == '__main__':
    IN = Signal(intbv(0)[8:])
    CLK = Signal(bool(0))
    out_data = Signal(intbv(0)[8:])
    STB = Signal(intbv(0)[4:])

    port = IO_port(STB, IN, CLK, out_data)

    port.run_sim()
    port.convert(hdl='verilog')



