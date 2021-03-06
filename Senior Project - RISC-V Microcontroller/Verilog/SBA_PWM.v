// File: SBA_PWM.v
// Generated by MyHDL 0.11
// Date: Tue Jun 22 21:48:34 2021


`timescale 1ns/10ps

module SBA_PWM (
    data,
    reset,
    clk,
    STB,
    pwmSignal
);


input [31:0] data;
input reset;
input clk;
input [3:0] STB;
output pwmSignal;
reg pwmSignal;

reg load_comp = 0;
reg loadCNT = 0;
reg EN_CNT = 0;
reg is_zero = 0;
wire [15:0] DataPath0_COMP0_out;
wire [15:0] DataPath0_COMP1_out;
wire [15:0] DataPath0_CNT_out;
reg [15:0] DataPath0_active = 0;
wire DataPath0_load_enable;
reg [15:0] DataPath0_period = 0;
reg [15:0] DataPath0_REG_16bit0_storage = 0;
reg [15:0] DataPath0_REG_16bit1_storage = 0;
reg [15:0] DataPath0_CountDown_REG0_value = 0;
wire ControlUnit0_D_edge;
reg [1:0] ControlUnit0_R_edge = 0;
reg [0:0] ControlUnit0_state = 0;



always @(posedge clk, posedge reset) begin: SBA_PWM_DATAPATH0_REG_16BIT0_REG
    if (reset) begin
        DataPath0_REG_16bit0_storage <= 1'b0;
    end
    else begin
        if (load_comp) begin
            DataPath0_REG_16bit0_storage <= DataPath0_period;
        end
    end
end



assign DataPath0_COMP0_out = DataPath0_REG_16bit0_storage;


always @(posedge clk, posedge reset) begin: SBA_PWM_DATAPATH0_REG_16BIT1_REG
    if (reset) begin
        DataPath0_REG_16bit1_storage <= 1'b0;
    end
    else begin
        if (load_comp) begin
            DataPath0_REG_16bit1_storage <= DataPath0_active;
        end
    end
end



assign DataPath0_COMP1_out = DataPath0_REG_16bit1_storage;



assign DataPath0_CNT_out = DataPath0_CountDown_REG0_value;


always @(posedge clk) begin: SBA_PWM_DATAPATH0_COUNTDOWN_REG0_LD
    if (reset) begin
        DataPath0_CountDown_REG0_value <= 0;
    end
    else begin
        if (loadCNT) begin
            DataPath0_CountDown_REG0_value <= DataPath0_period;
        end
        else if (EN_CNT) begin
            DataPath0_CountDown_REG0_value <= (DataPath0_CountDown_REG0_value - 1);
        end
    end
end


always @(DataPath0_CNT_out) begin: SBA_PWM_DATAPATH0_ZERO_COMP0_COMP
    if ((DataPath0_CNT_out == 0)) begin
        is_zero = 1;
    end
    else begin
        is_zero = 0;
    end
end


always @(DataPath0_CNT_out, DataPath0_COMP1_out) begin: SBA_PWM_DATAPATH0_ACTIVE_COMPARATOR0_COMP
    if ((DataPath0_CNT_out < DataPath0_COMP1_out)) begin
        pwmSignal = 1;
    end
    else begin
        pwmSignal = 0;
    end
end



assign DataPath0_load_enable = STB[3];


always @(posedge DataPath0_load_enable) begin: SBA_PWM_DATAPATH0_CONNECT
    if (STB[3]) begin
        DataPath0_period <= data[32-1:16];
        DataPath0_active <= data[16-1:0];
    end
end


always @(posedge clk) begin: SBA_PWM_CONTROLUNIT0_CU
    if (reset) begin
        load_comp <= 1'b0;
        loadCNT <= 1'b0;
        EN_CNT <= 1'b0;
        ControlUnit0_state <= 1'b0;
    end
    else begin
        load_comp <= 1'b0;
        loadCNT <= 1'b0;
        EN_CNT <= 1'b0;
        case (ControlUnit0_state)
            'h0: begin
                EN_CNT <= 1'b0;
                load_comp <= 1'b1;
                loadCNT <= 1'b1;
                if (ControlUnit0_D_edge) begin
                    ControlUnit0_state <= 1'b1;
                end
                else begin
                    ControlUnit0_state <= 0;
                end
            end
            'h1: begin
                EN_CNT <= 1'b1;
                if (is_zero) begin
                    loadCNT <= 1'b1;
                end
                else if (((STB[1] == 0) && (STB[3] == 1))) begin
                    ControlUnit0_state <= 1'b0;
                end
            end
            default: begin
                ControlUnit0_state <= 1'b0;
            end
        endcase
        if ((ControlUnit0_D_edge && STB[3])) begin
            loadCNT <= 1'b1;
            load_comp <= 1'b1;
        end
    end
end


always @(posedge clk, posedge reset) begin: SBA_PWM_CONTROLUNIT0_INPUT_DETECT
    if (reset) begin
        ControlUnit0_R_edge <= 0;
    end
    else begin
        if (STB[3]) begin
            ControlUnit0_R_edge <= {ControlUnit0_R_edge[0], STB[1]};
        end
    end
end



assign ControlUnit0_D_edge = ((!ControlUnit0_R_edge[1]) && ControlUnit0_R_edge[0]);

endmodule
