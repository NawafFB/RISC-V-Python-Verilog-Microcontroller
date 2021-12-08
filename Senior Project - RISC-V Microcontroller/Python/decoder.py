from myhdl import block, always_comb, instances, Signal, instance, intbv, delay, bin, now, concat

'''
next block represents a decoder, it will receive 
an instruction as an input and wll output decoded
signals.

all print statements are used to help with the
simulation process

@input : instruction
@output : opcode
@output : rd
@output : rs1
@output : rs2
@output : imm
@output : funct3
@output : funct7
'''


@block
def decoder(instruction, opcode, rd, rs1, rs2, imm, funct3, funct7):
    @always_comb
    def decode():
        opcode.next = instruction[7:]
        # print('opcode:', bin(instruction[7:], 7),'time:',now())
        funct3.next = instruction[15:12]
        funct7.next = instruction[:25]

        # r-type done
        if instruction[7:] == 0b0110011:
            rd.next = instruction[12:7]
            rs1.next = instruction[20:15]
            rs2.next = instruction[25:20]
            imm.next = 0
            # print('time: %s | next instruction is r type' % now())

        # i-type done
        elif (instruction[7:] == 0b0000011) or (instruction[7:] == 0b0010011) or (instruction[7:] == 0b1100111):
            rd.next = instruction[12:7]
            rs1.next = instruction[20:15]
            rs2.next = 0
            if (instruction[15:12] == 0b001) or (instruction[15:12] == 0b101):
                # imm.next = instruction[25:20]  # for shift instructions
                imm.next = instruction[26:20]
            else:
                # imm.next = intbv(instruction[32:20])
                imm.next = instruction[32:20]
            # print('time: %s | next instruction is i type' % now())

        # s-type done
        elif instruction[7:] == 0b0100011:
            rd.next = 0
            rs1.next = instruction[20:15]
            rs2.next = instruction[25:20]
            # imm.next = int(bin(instruction[32:25], 7) + bin(instruction[12:7], 5), 2)
            # imm.next = concat(instruction[32:25], instruction[12:7])
            imm.next = concat(instruction[32:25], instruction[12:7]).signed()

            # print('time: %s | next instruction is s type' % now())

        # b-type done
        elif instruction[7:] == 0b1100011:
            rd.next = 0
            rs1.next = instruction[20:15]
            rs2.next = instruction[25:20]
            # imm.next = int(bin(instruction[32:31], 1) + bin(instruction[8:7], 1) + bin(instruction[31:25], 6)
            #                + bin(instruction[12:8], 4), 2)
            # no sign extension (wrong way) >>
            # imm.next = concat(instruction[32:31], instruction[8:7], instruction[31:25], instruction[12:8])
            imm.next = concat(instruction[32:31], instruction[8:7], instruction[31:25],
                              instruction[12:8]).signed()

            # print('time: %s | next instruction is b type' % now())

        # u-type
        elif (instruction[7:] == 0b0110111) or (instruction[7:] == 0b0010111):
            rd.next = instruction[12:7]
            rs1.next = 0
            rs2.next = 0
            # imm.next = instruction[32:12] # no sign extension (wrong way)
            imm.next = intbv(instruction[32:12].signed(), min=(-2 ** 31), max=2 ** 31)  # sign extend imm value

            # print('time: %s | next instruction is u type' % now())

        # j-type done
        elif instruction[7:] == 0b1101111:
            rd.next = instruction[12:7]
            rs1.next = 0
            rs2.next = 0
            # imm.next = int(bin(instruction[32:31], 1) + bin(instruction[20:12], 8) + bin(instruction[21:20], 1) + bin(instruction[31:21], 10), 2)
            # imm.next = concat(instruction[32:31], instruction[20:12], instruction[21:20], instruction[31:21])
            imm.next = concat(instruction[32:31], instruction[20:12], instruction[21:20], instruction[31:21]).signed()

            # print('time: %s | next instruction is j type' % now())

        elif instruction[7:] == 0b0000000:
            rd.next = 0
            rs1.next = 0
            rs2.next = 0
            imm.next = 0
            # print('time: %s | next instruction is a invalid' % now())

    return instances()


'''
add x27,x30,x11
srai x22, x12,30
sw x16, 100(x14)
beq x13, x26, equal
lui x12, 88
equal: jalr x0, x1,0
'''


@block
def testBench():
    inst, opcode, rd, rs1, rs2, imm, funct3, funct7 = [Signal(intbv(0)) for i in range(8)]
    decoder_driver = decoder(inst, opcode, rd, rs1, rs2, imm, funct3, funct7)

    @instance
    def simulate():
        yield delay(1)  # starter delay
        # print default values
        print(bin(inst, width=32))
        print('rd:', int(rd), 'rs1:', int(rs1), 'rs2:', int(rs2), 'imm:', int(imm), 'funct3:', int(funct3), 'funct7:',
              int(funct7))
        print()

        # this should be r type instruction
        # add x27,x30,x11
        inst.next = 0b00000000101111110000110110110011
        yield delay(10)
        print(bin(inst, width=32))
        print('rd:', int(rd), 'rs1:', int(rs1), 'rs2:', int(rs2), 'imm:', int(imm), 'funct3:', int(funct3), 'funct7:',
              int(funct7))
        print()

        # this should be i type instruction
        # srai x22, x12,30
        inst.next = 0b01000001111001100101101100010011
        yield delay(10)
        print(bin(inst, width=32))
        print('rd:', int(rd), 'rs1:', int(rs1), 'rs2:', int(rs2), 'imm:', int(imm), 'funct3:', int(funct3), 'funct7:',
              int(funct7))
        print()

        # this should be s type instruction
        # sw x16, 100(x14)
        inst.next = 0b00000111000001110010001000100011
        yield delay(10)
        print(bin(inst, width=32))
        print('rd:', bin(rd, width=5), 'rs1:', bin(rs1, width=5), 'rs2', bin(rs2, width=5), 'imm:', bin(imm, width=5))
        print('rd:', int(rd), 'rs1:', int(rs1), 'rs2:', int(rs2), 'imm:', int(imm), 'funct3:', int(funct3), 'funct7:',
              int(funct7))
        print()

        # this should be b type instruction
        # beq x13, x26, equal
        inst.next = 0b000000001101001101000010001100011
        yield delay(10)
        print(bin(inst, width=32))
        print('rd:', bin(rd, width=5), 'rs1:', bin(rs1, width=5), 'rs2', bin(rs2, width=5), 'imm:', bin(imm, width=5))
        print('rd:', int(rd), 'rs1:', int(rs1), 'rs2:', int(rs2), 'imm:', int(imm), 'funct3:', int(funct3), 'funct7:',
              int(funct7))
        print()

        # this should be u type instruction
        # lui x12, 88
        inst.next = 0b00000000000001011000011000110111
        yield delay(10)
        print(bin(inst, width=32))
        print('rd:', bin(rd, width=5), 'rs1:', bin(rs1, width=5), 'rs2', bin(rs2, width=5), 'imm:', bin(imm, width=5))
        print('rd:', int(rd), 'rs1:', int(rs1), 'rs2:', int(rs2), 'imm:', int(imm), 'funct3:', int(funct3), 'funct7:',
              int(funct7))
        print()

        # this should be jalr instruction
        # equal: jalr x1, x5,0
        inst.next = 0b00000000000000001000000001100111
        yield delay(10)
        print(bin(inst, width=32))
        print('rd:', bin(rd, width=5), 'rs1:', bin(rs1, width=5), 'rs2', bin(rs2, width=5), 'imm:', bin(imm, width=5))
        print('rd:', int(rd), 'rs1:', int(rs1), 'rs2:', int(rs2), 'imm:', int(imm), 'funct3:', int(funct3), 'funct7:',
              int(funct7))
        print()

    return instances()
#
# test = testBench()
# test.run_sim(100)

# Verilog Conversion #


# if __name__ == '__main__':
#
#     opcode = Signal(intbv(0, min=0, max=2 ** 7))
#     rs1 = Signal(intbv(0, min=0, max=2 ** 5))
#     rs2 = Signal(intbv(0, min=0, max=2 ** 5))
#     rd = Signal(intbv(0, min=0, max=2 ** 5))
#     funct3 = Signal(intbv(0, min=0, max=2 ** 3))
#     funct7 = Signal(intbv(0, min=0, max=2 ** 7))
#     imm = Signal(intbv(0, min=-2**19, max=2 ** 19))
#     instruction = Signal(intbv(0, min=0, max=2 ** 32))
#
#     tb = decoder(instruction, opcode, rd, rs1, rs2, imm, funct3, funct7)
#     tb.run_sim()
#     tb.convert(hdl='verilog')
#
