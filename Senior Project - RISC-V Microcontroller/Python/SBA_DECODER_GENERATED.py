from myhdl import *

@block
def SBA_DECODER(STB_I, ADDR_I, STB_O):
	@always_comb
	def decode():
		if STB_I[0]:
			if ADDR_I <= 1023:
				STB_O.next = concat(intbv(1)[6:], STB_I[4:1])  # RAM || address = 0 -> 1023 
			elif ADDR_I == 1024:
				STB_O.next = concat(intbv(2)[6:], intbv(0)[3:]) # UART ADDRESS 0 || address = 1024 
			elif ADDR_I == 1025:
				STB_O.next = concat(intbv(2)[6:], intbv(1)[3:]) # UART ADDRESS 1 || address = 1025 
			elif ADDR_I == 1026:
				STB_O.next = concat(intbv(2)[6:], intbv(2)[3:]) # UART ADDRESS 2 || address = 1026 
			elif ADDR_I == 1027:
				STB_O.next = concat(intbv(4)[6:], STB_I[4:1])  # input_port_0 || address = 1027 
			elif ADDR_I == 1028:
				STB_O.next = concat(intbv(8)[6:], STB_I[4:1])  # output_port_0 || address = 1028 
			elif ADDR_I == 1029:
				STB_O.next = concat(intbv(16)[6:], STB_I[4:1])  # timer_0 || address = 1029 
			elif ADDR_I == 1030:
				STB_O.next = concat(intbv(32)[6:], STB_I[4:1])  # pwm_0 || address = 1030 
		else:
			STB_O.next = 0  # disable all modules
	return decode