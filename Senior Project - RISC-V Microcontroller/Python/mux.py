from myhdl import always_comb, block, Signal, intbv

'''

this block represents a multiplexer 
that controls the output depending 
on the select signal.

sel = 0 >> output1 = input1
sel = 1 >> output1 = input2

'''


@block
def mux(sel, input1, input2, mux_output):
    @always_comb
    def select():
        if sel == 0:
            mux_output.next = input1
        else:
            mux_output.next = input2

    return select


if __name__ == '__main__':

    sel = Signal(bool(0))
    input1 = Signal(intbv(0, min=(-2 ** 31), max=(2 ** 31)))
    input2 = Signal(intbv(0, min=(-2 ** 31), max=(2 ** 31)))
    mux_output = Signal(intbv(0, min=(-2 ** 31), max=(2 ** 31)))

    tb = mux(sel,input1,input2,mux_output)
    tb.run_sim()
    tb.convert(hdl='verilog')
