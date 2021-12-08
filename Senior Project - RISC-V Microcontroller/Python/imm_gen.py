from myhdl import block, always, instance, instances, always_comb, Signal, intbv, delay, bin, always_comb


@block
def imm_generator(opcode, imm, imm_extended):
    @always_comb
    def extend():
        if 0b0000011 == opcode or opcode == 0b0010011 or opcode == 0b1100111 or opcode == 0b0100011 or opcode == 0b1100011:
            imm_extended.next = imm[20:].signed()
        elif opcode == 0b0110111 or opcode == 0b0010111 or opcode == 0b1101111:
            imm_extended.next = imm[20:].signed()

    return instances()


if __name__ == '__main__':
    imm = Signal(intbv(0, min=0, max=2 ** 20))
    imm_extended = Signal(intbv(0, min=0, max=2 ** 32))
    opcode = Signal(intbv(0, min=0, max=2 ** 7))

    tb = imm_generator(opcode, imm, imm_extended)
    tb.run_sim()
    tb.convert(hdl='verilog')

# module imm_generator(opcode, imm, imm_extended);
#
# input [6:0] opcode;
# input [19:0] imm;
# output [31:0] imm_extended;
# reg [31:0] imm_extended;
#
# always@(opcode, imm) begin
# 	// I type and S type and B type
# 	if ((opcode == 7'b0000011) || (opcode == 7'b0010011) || (opcode == 7'b1100111) || (opcode == 7'b0100011) || (opcode == 7'b1100011)) begin
# 		imm_extended <= $signed(imm);
# 	end
# 	// J type U type
# 	else if ((opcode == 7'b0110111) || (opcode == 7'b0010111) || (opcode == 7'b1101111)) begin
# 		imm_extended <= $signed(imm);
# 	end
# 	else
# 		imm_extended = 0;
# end // always end
# endmodule
