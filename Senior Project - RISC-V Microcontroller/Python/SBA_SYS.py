from myhdl import *
from SBA_CPU import SBA_CPU
from SBA_DECODER import SBA_DECODER
from SBA_bus import BusSystem
from SBA_RAM import SBA_RAM
from IO_port import output_port
from IO_port import input_port
from SBA_Timer import SBA_TIMER
from SBA_PWM import SBA_PWM
from UART_SYS import SBA_UART_SYS


@block
def Microcontroller(clk, rest, PWM_Signal, TX, RX, input_port_data, Output_port_data):
    # CPU Signal

    STB_O = Signal(intbv(0)[4:])
    WE_O = Signal(bool(0))


    # Decoder Signals
    DEC_STB_O = Signal(intbv(0)[9:])

    # Bus Signals
    MST_DAT_I, MST_DAT_O, SLV_DAT_I, ALU_OUTPUT_ADDR_I = [Signal(intbv(0)[32:]) for i in range(4)]
    ADDR_O = Signal(intbv(0)[9:])
    WE_I, RST_O, CLK_O = [Signal(bool(0)) for i in range(3)]

    SBA_CPU_driver = SBA_CPU(clk, MST_DAT_I, WE_O, STB_O, ALU_OUTPUT_ADDR_I, MST_DAT_O)

    SBA_DECODER_driver = SBA_DECODER(STB_O, ALU_OUTPUT_ADDR_I, DEC_STB_O)

    SLV_DAT_O_1, SLV_DAT_O_2, SLV_DAT_O_3, SLV_DAT_O_4, SLV_DAT_O_5, SLV_DAT_O_6 = [Signal(intbv(0)[32:]) for i in range(6)]

    STB_O_1, STB_O_2, STB_O_3, STB_O_4, STB_O_5, STB_O_6 = [Signal(intbv(0)[4:]) for i in range(6)]  # ###

    SBA_BUS_driver = BusSystem(MST_DAT_I, MST_DAT_O, SLV_DAT_I,
              SLV_DAT_O_1, SLV_DAT_O_2, SLV_DAT_O_3, SLV_DAT_O_4, SLV_DAT_O_5, SLV_DAT_O_6,
              ALU_OUTPUT_ADDR_I, ADDR_O, WE_I, WE_O, DEC_STB_O, STB_O_1, STB_O_2,
              STB_O_3, STB_O_4, STB_O_5, STB_O_6, rest, RST_O, clk, CLK_O)

    SBA_RAM_driver = SBA_RAM(CLK_O, STB_O_1, SLV_DAT_I, WE_O, ADDR_O, SLV_DAT_O_1)
    #
    SBA_Output_PORT = output_port(STB_O_2, SLV_DAT_I, CLK_O, Output_port_data)

    SBA_PWM_driver = SBA_PWM(SLV_DAT_I, RST_O, CLK_O, STB_O_3, PWM_Signal)

    SBA_TIMER_driver = SBA_TIMER(STB_O_4, SLV_DAT_I, CLK_O, RST_O, SLV_DAT_O_4)
    #
    SBA_UART_driver = SBA_UART_SYS(CLK_O, RST_O, SLV_DAT_I, WE_O, STB_O_5, ADDR_O, SLV_DAT_O_5, TX, RX)
    #
    SBA_input_port = input_port(STB_O_6, input_port_data, SLV_DAT_O_6)

    return instances()


if __name__ == '__main__':
    clk = Signal(bool(0))
    reset = Signal(bool(0))
    PWM_Signal = Signal(bool(0))

    TX = Signal(bool(0))
    RX = Signal(bool(0))

    input_port_data, Output_port_data = [Signal(intbv(0)[8:]) for _ in range(2)]

    MICRO = Microcontroller(clk, reset, PWM_Signal, TX, RX, input_port_data, Output_port_data)

    toVerilog.initial_values = True
    toVerilog.timescale = "0"
    MICRO.run_sim()
    MICRO.convert(hdl='verilog')

