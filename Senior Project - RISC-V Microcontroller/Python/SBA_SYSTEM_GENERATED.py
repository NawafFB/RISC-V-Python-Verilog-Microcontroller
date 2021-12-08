from myhdl import * 
from fast_cpu_python.SBA_CPU import SBA_CPU 
from fast_cpu_python.SBA_DECODER_GENERATED import SBA_DECODER
from fast_cpu_python.SBA_BUS_GENERATED import BusSystem
from fast_cpu_python.SBA_RAM import SBA_RAM
from fast_cpu_python.IO_port import output_port
from fast_cpu_python.IO_port import input_port
from fast_cpu_python.SBA_Timer import SBA_TIMER
from fast_cpu_python.SBA_PWM import SBA_PWM
from fast_cpu_python.UART_SYS import SBA_UART_SYS

@block
def Microcontroller_GEN(clk, reset, TX, RX, Output_port_data_0, input_port_data_0, PWM_Signal_0):

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
		STB_O_1 = Signal(intbv(0)[4:])
		STB_O_2 = Signal(intbv(0)[4:])
		STB_O_3 = Signal(intbv(0)[4:])
		STB_O_4 = Signal(intbv(0)[4:])
		STB_O_5 = Signal(intbv(0)[4:])
		STB_O_6 = Signal(intbv(0)[4:])
		SLV_DAT_O_1 = Signal(intbv(0)[32:])
		SLV_DAT_O_2 = Signal(intbv(0)[32:])
		SLV_DAT_O_3 = Signal(intbv(0)[32:])
		SLV_DAT_O_4 = Signal(intbv(0)[32:])
		SLV_DAT_O_5 = Signal(intbv(0)[32:])
		SLV_DAT_O_6 = Signal(intbv(0)[32:])
		SBA_BUS_driver = BusSystem(MST_DAT_I, MST_DAT_O, SLV_DAT_I, SLV_DAT_O_1 ,SLV_DAT_O_2 ,SLV_DAT_O_3 ,SLV_DAT_O_4 ,SLV_DAT_O_5 ,SLV_DAT_O_6 , ALU_OUTPUT_ADDR_I, ADDR_O, WE_I, WE_O, DEC_STB_O, STB_O_1,STB_O_2,STB_O_3,STB_O_4,STB_O_5,STB_O_6, rest, RST_O, clk, CLK_O) 
		SBA_RAM_driver = SBA_RAM(CLK_O, STB_O_1, SLV_DAT_I, WE_O, ADDR_O, SLV_DAT_O_1 )
		SBA_UART_driver_5 = SBA_UART_SYS(CLK_O, RST_O, SLV_DAT_I, WE_O, STB_O_2, ADDR_O, SLV_DAT_O_2 , TX, RX)
		SBA_output_port_0 = output_port(STB_O_3, SLV_DAT_I, CLK_O, Output_port_data_0)
		SBA_input_port_0 = input_port(STB_O_4, input_port_data_0, SLV_DAT_O_4 )
		SBA_PWM_driver_0 = SBA_PWM(SLV_DAT_I, RST_O, CLK_O, STB_O_5, PWM_Signal_0)
		SBA_TIMER_driver_0 = SBA_TIMER(STB_O_6, SLV_DAT_I, CLK_O, RST_O, SLV_DAT_O_6 )
		return instances()