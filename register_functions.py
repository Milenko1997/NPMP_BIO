from models import *


class SIPORegister:
    def __init__(self):
        self.current_index = 0
        self.switch = False

    def model(self, Y, T, serial_input, params):

        a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3, a4, not_a4, q4, not_q4 = Y

        clk = get_clock(T)

        rise = get_clock(T-0.1) < clk   

        if (clk > 50 and rise) and self.switch:
            self.switch  = False
            self.current_index += 1 
        if clk < 50 and not self.switch :
            self.switch = True

        if self.current_index < len(serial_input):
            d1 = serial_input[self.current_index]
        else:
            d1 = 0

        d2 = q1
        d3 = q2
        d4 = q3

        Y_FF1 = [a1, not_a1, q1, not_q1, d1, clk]
        Y_FF2 = [a2, not_a2, q2, not_q2, d2, clk]
        Y_FF3 = [a3, not_a3, q3, not_q3, d3, clk]
        Y_FF4 = [a4, not_a4, q4, not_q4, d4, clk]

        dY1 = ff_ode_model(Y_FF1, T, params)
        dY2 = ff_ode_model(Y_FF2, T, params)
        dY3 = ff_ode_model(Y_FF3, T, params)
        dY4 = ff_ode_model(Y_FF4, T, params)

        dY = np.concatenate([dY1, dY2, dY3, dY4])    
        return dY

    
class PISORegister:
    def __init__(self):
        self.current_index = 0
        self.switch = False
        self.CTL_signal = 1

    def model(self, Y, T, parallel_input_list, params):
        a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3, a4, not_a4, q4, not_q4 = Y

        clk = get_clock(T)

        rise = get_clock(T-0.1) < clk   

        if (clk > 50 and rise) and self.switch:
            self.switch  = False
            self.current_index += 1         
            #control signal: loading(1) or shifting (0) 
            self.CTL_signal = 1 if (self.current_index % 5 == 0) else 0; 

        if clk < 50 and not self.switch :
            self.switch = True


        if (self.current_index%4 < len(parallel_input_list)):
            parallel_input = parallel_input_list[self.current_index%len(parallel_input_list)]
        else:        
            parallel_input = [0,0,0,0]

        if self.CTL_signal:
            d1 = parallel_input[0]
            d2 = parallel_input[1]
            d3 = parallel_input[2]
            d4 = parallel_input[3]
        else:
            d1 = 0
            d2 = q1
            d3 = q2
            d4 = q3

        Y_FF1 = [a1, not_a1, q1, not_q1, d1, clk]
        Y_FF2 = [a2, not_a2, q2, not_q2, d2, clk]
        Y_FF3 = [a3, not_a3, q3, not_q3, d3, clk]
        Y_FF4 = [a4, not_a4, q4, not_q4, d4, clk]

        dY1 = ff_ode_model(Y_FF1, T, params)
        dY2 = ff_ode_model(Y_FF2, T, params)
        dY3 = ff_ode_model(Y_FF3, T, params)
        dY4 = ff_ode_model(Y_FF4, T, params)

        dY = np.concatenate([dY1, dY2, dY3, dY4])    
        return dY


def LFSR_register_model(Y, T, feedback_taps, params):

    a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3, a4, not_a4, q4, not_q4 = Y

    clk = get_clock(T)
    rise = get_clock(T-0.1) < clk

    feedback_bit = LFSR_feedback([q1, q2, q3, q4], feedback_taps) 

    d1 = feedback_bit
    d2 = q1
    d3 = q2
    d4 = q3
    
    Y_FF1 = [a1, not_a1, q1, not_q1, d1, clk]
    Y_FF2 = [a2, not_a2, q2, not_q2, d2, clk]
    Y_FF3 = [a3, not_a3, q3, not_q3, d3, clk]
    Y_FF4 = [a4, not_a4, q4, not_q4, d4, clk]
    
    dY1 = ff_ode_model(Y_FF1, T, params)
    dY2 = ff_ode_model(Y_FF2, T, params)
    dY3 = ff_ode_model(Y_FF3, T, params)
    dY4 = ff_ode_model(Y_FF4, T, params)

    dY = np.concatenate([dY1, dY2, dY3, dY4])    
    return dY

def LFSR_feedback(q_values, feedback_taps):
    """Compute the feedback bit for LFSR using XOR operation."""
    return sum([q_values[tap] for tap in feedback_taps]) % 50

##repeats output
def SIPO_register_model_loopIN(Y, T, serial_input, params):
    if not hasattr(SIPO_register_model_loopIN, "current_index"):
        SIPO_register_model_loopIN.current_index = 0
    if not hasattr(SIPO_register_model_loopIN, "switch"):
        SIPO_register_model_loopIN.switch = False

    a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3, a4, not_a4, q4, not_q4 = Y
            
    clk = get_clock(T)
        
    rise = get_clock(T-0.1) < clk   
    
    if (clk > 50 and rise) and SIPO_register_model_loopIN.switch:
        SIPO_register_model_loopIN.switch  = False
        SIPO_register_model_loopIN.current_index += 1 
    if clk < 50 and not SIPO_register_model_loopIN.switch :
        SIPO_register_model_loopIN.switch = True
    
    d1 = serial_input[SIPO_register_model_loopIN.current_index % len(serial_input)]
        
    d2 = q1
    d3 = q2
    d4 = q3

    Y_FF1 = [a1, not_a1, q1, not_q1, d1, clk]
    Y_FF2 = [a2, not_a2, q2, not_q2, d2, clk]
    Y_FF3 = [a3, not_a3, q3, not_q3, d3, clk]
    Y_FF4 = [a4, not_a4, q4, not_q4, d4, clk]

    dY1 = ff_ode_model(Y_FF1, T, params)
    dY2 = ff_ode_model(Y_FF2, T, params)
    dY3 = ff_ode_model(Y_FF3, T, params)
    dY4 = ff_ode_model(Y_FF4, T, params)

    dY = np.concatenate([dY1, dY2, dY3, dY4])    
    return dY


def PISO_register_model_loopIN(Y, T, parallel_input_list, params):
    if not hasattr(PISO_register_model_loopIN, "current_index"):
        PISO_register_model_loopIN.current_index = 0
    if not hasattr(PISO_register_model_loopIN, "switch"):
        PISO_register_model_loopIN.switch = False
    if not hasattr(PISO_register_model_loopIN, "CTL_signal"):
        PISO_register_model_loopIN.CTL_signal = 1

    a1, not_a1, q1, not_q1, a2, not_a2, q2, not_q2, a3, not_a3, q3, not_q3, a4, not_a4, q4, not_q4 = Y
            
    clk = get_clock(T)
        
    rise = get_clock(T-0.1) < clk   
    
    if (clk > 50 and rise) and PISO_register_model_loopIN.switch:
        PISO_register_model_loopIN.switch  = False
        PISO_register_model_loopIN.current_index += 1 
        
        #control signal: loading(1) or shifting (0) 
        PISO_register_model_loopIN.CTL_signal = 1 if (PISO_register_model_loopIN.current_index % 5 == 0) else 0; 
        
    if clk < 50 and not PISO_register_model_loopIN.switch :
        PISO_register_model_loopIN.switch = True
    
    
    parallel_input = parallel_input_list[PISO_register_model_loopIN.current_index%len(parallel_input_list)]
        
    if PISO_register_model_loopIN.CTL_signal:
        d1 = parallel_input[0]
        d2 = parallel_input[1]
        d3 = parallel_input[2]
        d4 = parallel_input[3]
    else:
        d1 = 0
        d2 = q1
        d3 = q2
        d4 = q3
        
    Y_FF1 = [a1, not_a1, q1, not_q1, d1, clk]
    Y_FF2 = [a2, not_a2, q2, not_q2, d2, clk]
    Y_FF3 = [a3, not_a3, q3, not_q3, d3, clk]
    Y_FF4 = [a4, not_a4, q4, not_q4, d4, clk]

    dY1 = ff_ode_model(Y_FF1, T, params)
    dY2 = ff_ode_model(Y_FF2, T, params)
    dY3 = ff_ode_model(Y_FF3, T, params)
    dY4 = ff_ode_model(Y_FF4, T, params)

    dY = np.concatenate([dY1, dY2, dY3, dY4])    
    return dY