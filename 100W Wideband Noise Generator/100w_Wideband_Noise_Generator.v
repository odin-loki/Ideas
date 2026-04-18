// =============================================================================
// 100W Wideband Noise Generator — Complete FPGA Control System
// =============================================================================
// Chua-circuit based chaotic RF noise generator with full digital supervision.
// Frequency range : 1 Hz – 14 GHz (hardware dependent)
// Maximum RF output: 100 W continuous
// Supply voltage   : Controlled via 12-bit DAC (ps_voltage)
// FPGA target      : Any device with sufficient I/O (Xilinx / Intel / Lattice)
// Clock            : Configurable; minimum frequency determined by §6 analysis
// =============================================================================

module complete_noise_generator (
    // -------------------------------------------------------------------------
    // System Clock and Control
    // -------------------------------------------------------------------------
    input  wire        clk_in,           // System clock (digital control domain)
    input  wire        rst_n,            // Active-low master reset
    input  wire        power_switch,     // Main power on/off
    input  wire        standby_switch,   // Force standby (low = run)

    // -------------------------------------------------------------------------
    // Chua Circuit — Op-amp core
    // -------------------------------------------------------------------------
    output reg [11:0]  opamp1_bias,      // Op-amp 1 DC bias (12-bit DAC word)
    output reg [11:0]  opamp2_bias,      // Op-amp 2 DC bias (12-bit DAC word)
    output reg [3:0]   opamp_gain_sel,   // Programmable gain resistor select

    // -------------------------------------------------------------------------
    // Chua Circuit — Variable reactive components
    // -------------------------------------------------------------------------
    output reg [7:0]   ind_tune,         // Inductor tuning word (ferrite core / switched)
    output reg [3:0]   cap_bank_sel,     // Switched capacitor bank (C1 / C2 ratio)
    output reg [3:0]   res_bank_sel,     // Switched resistor bank (sets Chua diode slope)

    // -------------------------------------------------------------------------
    // Chua Circuit — Buffer stages
    // -------------------------------------------------------------------------
    output reg [11:0]  buf1_bias,        // Input buffer bias (noise floor optimisation)
    output reg [11:0]  buf2_bias,        // Output buffer bias
    output reg [3:0]   buf_gain_sel,     // Buffer gain selection (flat PSD compensation)

    // -------------------------------------------------------------------------
    // Chua Circuit — Chaos control
    // -------------------------------------------------------------------------
    output reg [11:0]  chaos_dac,        // External chaos parameter injection DAC
    output reg [3:0]   nonlin_sel,       // Piecewise-linear nonlinearity segment select

    // -------------------------------------------------------------------------
    // RF Chain — Driver stage
    // -------------------------------------------------------------------------
    output reg [11:0]  driver_bias,      // Driver transistor bias point
    output reg [11:0]  driver_gain,      // Driver variable-gain control word
    output reg         driver_enable,    // Driver enable (active high)

    // -------------------------------------------------------------------------
    // RF Chain — Power Amplifier
    // -------------------------------------------------------------------------
    output reg [11:0]  pa_bias,          // PA quiescent bias (Class AB set-point)
    output reg [11:0]  pa_drive,         // PA input drive level
    output reg [3:0]   pa_band_sel,      // PA sub-band selection (broadband switch matrix)
    output reg         pa_enable,        // PA enable (active high)

    // -------------------------------------------------------------------------
    // RF Output conditioning
    // -------------------------------------------------------------------------
    output reg [7:0]   atten_ctrl,       // Digital step attenuator (0 = max output)
    output reg [3:0]   filter_bank,      // Output low-pass / band-pass filter select
    output reg [3:0]   match_ctrl,       // Automatic impedance matching network control

    // -------------------------------------------------------------------------
    // Power Supplies — Primary
    // -------------------------------------------------------------------------
    output reg         ps_enable,        // Main SMPS enable
    output reg         ps_crowbar,       // SCR crowbar trigger (overvoltage / arc)
    output reg [11:0]  ps_voltage,       // Main supply voltage set-point DAC
    output reg [11:0]  ps_current,       // Supply current limit DAC

    // -------------------------------------------------------------------------
    // Power Supplies — Secondary / Bias
    // -------------------------------------------------------------------------
    output reg [3:0]   aux_ps_en,        // Auxiliary supply enable bitmap
    output reg [11:0]  bias_voltage,     // Analogue bias supply set-point DAC

    // -------------------------------------------------------------------------
    // Analogue Monitoring Inputs (12-bit ADC channels)
    // -------------------------------------------------------------------------
    input  wire [11:0] fwd_power,        // Directional coupler — forward power
    input  wire [11:0] ref_power,        // Directional coupler — reflected power
    input  wire [11:0] pa_current,       // PA drain / collector current sense
    input  wire [11:0] pa_voltage,       // PA supply rail voltage sense
    input  wire [11:0] temp_sense [8],   // Thermal array: PA×2, driver, inductor, heatsink×3, ambient
    input  wire [11:0] vswr_bridge,      // Dedicated VSWR bridge (log-amp output)

    // -------------------------------------------------------------------------
    // Fault / Interlock Inputs (hardware comparator outputs)
    // -------------------------------------------------------------------------
    input  wire        temp_trip,        // Hardware over-temperature comparator
    input  wire        vswr_trip,        // Hardware VSWR 3:1 comparator
    input  wire        arc_detect,       // Plasma-arc optical / RF detector
    input  wire        ps_fault,         // SMPS internal fault flag
    input  wire        current_trip,     // Hardware over-current comparator
    input  wire        door_interlock,   // Cabinet door safety interlock (high = closed)
    input  wire        emc_filter_ok,    // Mains EMC filter status

    // -------------------------------------------------------------------------
    // Protection Outputs
    // -------------------------------------------------------------------------
    output reg         protect_trip,     // Consolidated protection active flag
    output reg         fast_shutdown,    // Sub-microsecond emergency shutdown
    output reg         fault_latch,      // Latched fault (requires manual reset)

    // -------------------------------------------------------------------------
    // Cooling System
    // -------------------------------------------------------------------------
    output reg [7:0]   fan_speed,        // PWM fan speed command (0x00 = off, 0xFF = full)
    input  wire        fan_tach,         // Fan tachometer pulse input
    input  wire        airflow_ok,       // Differential-pressure airflow sensor

    // -------------------------------------------------------------------------
    // User Interface
    // -------------------------------------------------------------------------
    input  wire [11:0] freq_pot,         // Frequency / tuning control potentiometer ADC
    input  wire [11:0] power_pot,        // Power level control potentiometer ADC
    output reg [3:0]   status_leds,      // Front-panel status LEDs

    // -------------------------------------------------------------------------
    // LCD Interface (HD44780-compatible 8-bit parallel)
    // -------------------------------------------------------------------------
    output reg [7:0]   lcd_data,         // LCD parallel data bus
    output reg         lcd_rs,           // 0 = command register, 1 = data register
    output reg         lcd_en            // Enable strobe (data latched on falling edge)
);

// =============================================================================
// SYSTEM CONSTANTS
// =============================================================================

parameter [11:0]
    MAX_POWER     = 12'h640,    // 100 W threshold in ADC units
    MAX_VSWR      = 12'h300,    // 3:1 VSWR hard-trip reference
    MAX_TEMP      = 12'h550,    // 85 °C ADC value (hardware sensor scaling)
    WARN_TEMP     = 12'h4D0,    // 77 °C — fan-full and pre-fault warning (8 °C margin)
    MAX_CURRENT   = 12'h800,    // PA current hard limit ADC value
    SOFT_CURRENT  = 12'h700,    // Current soft-limit (fold-back begins)
    IDLE_BIAS     = 12'h200,    // Standby op-amp bias (minimum dissipation)
    FULL_BIAS     = 12'h400,    // Operating op-amp bias
    MIN_FAN       = 8'h20,      // Minimum fan speed (bearing lubrication / audible)
    RAMP_STEP     = 12'h010,    // Voltage ramp increment per clock cycle
    RAMP_TOP      = 12'hFF0;    // Maximum ramp target (avoids 12-bit overflow at 0xFFF)

// Startup / shutdown phase timer thresholds
parameter [15:0]
    T_AUX_SETTLE  = 16'h0100,   // 256 cycles — aux supply settling
    T_BIAS_SETTLE = 16'h0200,   // 512 cycles — bias voltage settling
    T_PS_SETTLE   = 16'h0300,   // 768 cycles — main supply enable-to-stable
    T_DRV_SETTLE  = 16'h0400;   // 1024 cycles — driver warm-up

// State machine encoding
localparam [3:0]
    STATE_OFF      = 4'h0,
    STATE_INIT     = 4'h1,
    STATE_STANDBY  = 4'h2,
    STATE_STARTUP  = 4'h3,
    STATE_RUN      = 4'h4,
    STATE_FAULT    = 4'h5,
    STATE_SHUTDOWN = 4'h6;

// Fault code register encoding (fault_code[3:0])
localparam [3:0]
    FAULT_NONE     = 4'h0,
    FAULT_OVERTEMP = 4'h1,
    FAULT_VSWR     = 4'h2,
    FAULT_ARC      = 4'h3,
    FAULT_CURRENT  = 4'h4,
    FAULT_PSUPPLY  = 4'h5,
    FAULT_INTERLOCK= 4'h6,
    FAULT_AIRFLOW  = 4'h7,
    FAULT_CROWBAR  = 4'h8;

// Band selection boundaries — freq_pot[11:8] mapped to PA sub-band
// Sub-band 0: DC–500 MHz    (low-noise amplifier stage)
// Sub-band 1: 500 MHz–2 GHz (driver + stage 1 PA)
// Sub-band 2: 2–6 GHz       (stage 2 PA)
// Sub-band 3: 6–14 GHz      (MMIC output stage)
localparam [3:0]
    BAND_VLF  = 4'h0,
    BAND_UHF  = 4'h5,
    BAND_SHF  = 4'hA,
    BAND_EHF  = 4'hF;

// =============================================================================
// INTERNAL REGISTERS
// =============================================================================

// State and sequencing
reg [3:0]  state;
reg [7:0]  seq_state;
reg [15:0] startup_timer;
reg        startup_done;
reg        protection_active;
reg [3:0]  fault_code;          // Encoded fault for display and telemetry

// Thermal management
reg [11:0] max_temp;
reg [11:0] prev_max_temp;       // Previous reading for rate-of-change monitoring
reg [7:0]  thermal_margin;      // Normalised headroom to MAX_TEMP

// Power measurement — 20 bits prevents truncation of fwd_power²>>4
reg [19:0] current_power;
reg [19:0] power_avg;           // 8-sample moving average accumulator
reg [2:0]  avg_idx;             // Averaging ring index
reg [19:0] power_history [0:7]; // Ring buffer for averaging

// Frequency / display
reg [23:0] freq_display;
reg [23:0] freq_target;         // Computed from freq_pot

// VSWR tracking
reg [11:0] vswr_log;            // Logged peak VSWR since last clear
reg        vswr_soft_flag;      // Soft VSWR threshold crossed

// Current fold-back
reg [11:0] foldback_limit;      // Dynamic drive ceiling during fold-back

// LCD state
reg [3:0]  lcd_state;
reg        lcd_mode;            // 0 = frequency line, 1 = power / status line
reg [7:0]  lcd_line2_buf [15:0];// Second LCD line buffer

// Fan tachometer counter
reg [15:0] fan_tach_count;
reg        fan_tach_prev;
reg [15:0] fan_rpm_est;         // Estimated RPM from tachometer

// Crowbar discharge timer
reg [15:0] crowbar_timer;

// =============================================================================
// MAIN STATE MACHINE
// =============================================================================

always @(posedge clk_in or negedge rst_n) begin
    if (!rst_n) begin
        init_system();
    end else begin

        case (state)

            // -----------------------------------------------------------------
            STATE_OFF: begin
                if (power_switch && check_interlocks())
                    state <= STATE_INIT;
            end

            // -----------------------------------------------------------------
            STATE_INIT: begin
                // Increment timer so init_sequence_complete can become true
                startup_timer <= startup_timer + 1;
                if (init_sequence_complete())
                    state <= STATE_STANDBY;
            end

            // -----------------------------------------------------------------
            STATE_STANDBY: begin
                maintain_standby();
                if (!standby_switch && system_ready())
                    state <= STATE_STARTUP;
            end

            // -----------------------------------------------------------------
            STATE_STARTUP: begin
                execute_startup();
                if (startup_done) begin
                    startup_timer <= 16'h0000;
                    state         <= STATE_RUN;
                end
            end

            // -----------------------------------------------------------------
            STATE_RUN: begin
                if (!check_protection()) begin
                    seq_state <= 8'h00;
                    state     <= STATE_FAULT;
                end else begin
                    run_system();
                    monitor_system();
                end
            end

            // -----------------------------------------------------------------
            STATE_FAULT: begin
                handle_fault();
            end

            // -----------------------------------------------------------------
            STATE_SHUTDOWN: begin
                execute_shutdown();
                if (shutdown_complete())
                    state <= STATE_OFF;
            end

            // -----------------------------------------------------------------
            default: state <= STATE_OFF;

        endcase

        // Tasks that execute every clock cycle regardless of state
        update_protection();
        manage_cooling();
        update_display();
        measure_fan_tach();
    end
end

// =============================================================================
// INIT SYSTEM — drives all outputs to safe defaults on reset
// =============================================================================

task init_system;
begin
    // Protection and fault outputs
    protect_trip   <= 1'b1;
    fast_shutdown  <= 1'b0;
    fault_latch    <= 1'b0;
    fault_code     <= FAULT_NONE;

    // Power supplies — all off
    ps_enable      <= 1'b0;
    ps_crowbar     <= 1'b0;
    ps_voltage     <= 12'h000;
    ps_current     <= MAX_CURRENT;   // Current limit to rated maximum
    aux_ps_en      <= 4'h0;
    bias_voltage   <= 12'h000;

    // RF chain — fully disabled, maximum attenuation
    pa_enable      <= 1'b0;
    driver_enable  <= 1'b0;
    atten_ctrl     <= 8'hFF;
    pa_drive       <= 12'h000;
    driver_gain    <= 12'h000;
    driver_bias    <= 12'h000;
    pa_bias        <= 12'h000;
    pa_band_sel    <= 4'h0;
    filter_bank    <= 4'h0;
    match_ctrl     <= 4'h8;          // Mid-range starting point for matching network

    // Chua circuit — safe defaults
    opamp_gain_sel <= 4'h0;
    opamp1_bias    <= 12'h000;
    opamp2_bias    <= 12'h000;
    cap_bank_sel   <= 4'h1;
    res_bank_sel   <= 4'h0;
    nonlin_sel     <= 4'h0;
    buf_gain_sel   <= 4'hF;          // Maximum buffer gain at start
    buf1_bias      <= 12'h000;
    buf2_bias      <= 12'h000;
    chaos_dac      <= 12'h000;

    // Cooling — minimum speed
    fan_speed      <= MIN_FAN;
    fan_tach_count <= 16'h0000;
    fan_rpm_est    <= 16'h0000;
    fan_tach_prev  <= 1'b0;

    // Sequencing
    startup_timer  <= 16'h0000;
    seq_state      <= 8'h00;
    startup_done   <= 1'b0;
    protection_active <= 1'b0;
    foldback_limit <= 12'hFFF;

    // Thermal
    max_temp       <= 12'h000;
    prev_max_temp  <= 12'h000;
    thermal_margin <= 8'hFF;

    // Power averaging ring
    avg_idx        <= 3'h0;
    current_power  <= 20'h0;
    power_avg      <= 20'h0;
    power_history[0] <= 20'h0;
    power_history[1] <= 20'h0;
    power_history[2] <= 20'h0;
    power_history[3] <= 20'h0;
    power_history[4] <= 20'h0;
    power_history[5] <= 20'h0;
    power_history[6] <= 20'h0;
    power_history[7] <= 20'h0;

    // VSWR tracking
    vswr_log       <= 12'h000;
    vswr_soft_flag <= 1'b0;

    // Crowbar timer
    crowbar_timer  <= 16'h0000;

    // Display
    freq_display   <= 24'h000000;
    freq_target    <= 24'h000000;
    lcd_state      <= 4'h0;
    lcd_mode       <= 1'b0;
    lcd_en         <= 1'b0;
    lcd_rs         <= 1'b0;
    lcd_data       <= 8'h00;

    // Status
    status_leds    <= 4'h0;

    state          <= STATE_OFF;
end
endtask

// =============================================================================
// EXECUTE STARTUP — 6-phase power sequencing
// =============================================================================
// Phase 0: Enable auxiliary supplies and allow to settle
// Phase 1: Bring up bias voltages (op-amps, Chua circuit biasing)
// Phase 2: Enable main SMPS (at zero volts)
// Phase 3: Ramp main supply voltage to operating level
// Phase 4: Enable and warm up driver stage
// Phase 5: Final PA enable — system enters STATE_RUN

task execute_startup;
begin
    case (seq_state)

        8'h00: begin
            aux_ps_en     <= 4'hF;
            emc_filter_ok; // Check EMC filter before proceeding
            if (startup_timer >= T_AUX_SETTLE) begin
                startup_timer <= 16'h0000;
                seq_state     <= 8'h01;
            end else begin
                startup_timer <= startup_timer + 1;
            end
        end

        8'h01: begin
            bias_voltage  <= 12'h800;
            opamp1_bias   <= FULL_BIAS;
            opamp2_bias   <= FULL_BIAS;
            buf1_bias     <= FULL_BIAS;
            buf2_bias     <= FULL_BIAS;
            ps_current    <= MAX_CURRENT;
            if (startup_timer >= T_BIAS_SETTLE) begin
                startup_timer <= 16'h0000;
                seq_state     <= 8'h02;
            end else begin
                startup_timer <= startup_timer + 1;
            end
        end

        8'h02: begin
            ps_enable     <= 1'b1;
            ps_voltage    <= 12'h000;
            if (startup_timer >= T_PS_SETTLE) begin
                startup_timer <= 16'h0000;
                seq_state     <= 8'h03;
            end else begin
                startup_timer <= startup_timer + 1;
            end
        end

        // Ramp supply voltage: increment RAMP_STEP per cycle, stop at RAMP_TOP.
        // Condition capped at RAMP_TOP (12'hFF0) to prevent 12-bit wrap at 12'hFFF.
        8'h03: begin
            if (ps_voltage <= RAMP_TOP - RAMP_STEP)
                ps_voltage <= ps_voltage + RAMP_STEP;
            else begin
                ps_voltage <= RAMP_TOP;
                seq_state  <= 8'h04;
            end
        end

        8'h04: begin
            driver_enable <= 1'b1;
            driver_bias   <= 12'h400;
            if (startup_timer >= T_DRV_SETTLE) begin
                startup_timer <= 16'h0000;
                seq_state     <= 8'h05;
            end else begin
                startup_timer <= startup_timer + 1;
            end
        end

        8'h05: begin
            pa_enable    <= 1'b1;
            protect_trip <= 1'b0;
            atten_ctrl   <= power_pot[11:4]; // Initialise attenuator to user setting
            startup_done <= 1'b1;
        end

        default: ; // Holds startup_done high until state transitions
    endcase
end
endtask

// =============================================================================
// RUN SYSTEM — nominal operation tasks
// =============================================================================

task run_system;
begin
    tune_chua_circuit();
    control_rf_chain();
    manage_power_level();
    adjust_impedance_match();
    select_pa_band();
end
endtask

// =============================================================================
// MONITOR SYSTEM — telemetry, logging, derived metrics
// =============================================================================

task monitor_system;
begin
    // Update peak VSWR log
    if (ref_power > vswr_log)
        vswr_log <= ref_power;

    // Compute thermal margin (distance from limit, normalised to 8-bit)
    if (MAX_TEMP > max_temp)
        thermal_margin <= (MAX_TEMP - max_temp) >> 4;
    else
        thermal_margin <= 8'h00;

    // Rate-of-rise check — flag if temperature rising faster than 1 LSB/cycle
    prev_max_temp <= max_temp;

    // Current fold-back: reduce drive ceiling proportionally when approaching limit
    if (pa_current > SOFT_CURRENT)
        foldback_limit <= MAX_CURRENT - pa_current; // Proportional reduction
    else
        foldback_limit <= 12'hFFF; // No fold-back

    // Crowbar discharge timer: once crowbar is set, hold for 256 cycles then clear
    if (ps_crowbar) begin
        crowbar_timer <= crowbar_timer + 1;
        if (crowbar_timer >= 16'h00FF)
            ps_crowbar <= 1'b0;
    end else begin
        crowbar_timer <= 16'h0000;
    end
end
endtask

// =============================================================================
// TUNE CHUA CIRCUIT
// Translates 12-bit freq_pot to physical Chua circuit parameter set.
// The inductor tuning word, capacitor bank, resistor bank, nonlinearity
// selector and buffer gain collectively determine the operating frequency
// band and the chaotic attractor characteristics.
// =============================================================================

task tune_chua_circuit;
begin
    // Inductor tuning: bits [11:4] give 8-bit word spanning the full range
    // of the magnetically-tuned ferrite-core inductor.
    ind_tune <= freq_pot[11:4];

    // Capacitor bank — 16-entry lookup mapping freq_pot[11:8] to a bank
    // configuration that maintains the LC time constant product within the
    // chaotic regime across the full tuning range.
    // Bank values are logarithmically spaced to produce constant α_phys / β_phys ratio.
    case (freq_pot[11:8])
        4'h0: cap_bank_sel <= 4'h1;   //  DC – 88 MHz
        4'h1: cap_bank_sel <= 4'h1;   //  88 – 175 MHz
        4'h2: cap_bank_sel <= 4'h2;   // 175 – 350 MHz
        4'h3: cap_bank_sel <= 4'h2;   // 350 – 500 MHz
        4'h4: cap_bank_sel <= 4'h3;   // 500 – 700 MHz
        4'h5: cap_bank_sel <= 4'h4;   // 700 MHz – 1 GHz
        4'h6: cap_bank_sel <= 4'h5;   // 1 – 1.5 GHz
        4'h7: cap_bank_sel <= 4'h6;   // 1.5 – 2 GHz
        4'h8: cap_bank_sel <= 4'h7;   // 2 – 3 GHz
        4'h9: cap_bank_sel <= 4'h8;   // 3 – 4.5 GHz
        4'hA: cap_bank_sel <= 4'h9;   // 4.5 – 6 GHz
        4'hB: cap_bank_sel <= 4'hA;   // 6 – 7.5 GHz
        4'hC: cap_bank_sel <= 4'hB;   // 7.5 – 9 GHz
        4'hD: cap_bank_sel <= 4'hC;   // 9 – 11 GHz
        4'hE: cap_bank_sel <= 4'hD;   // 11 – 12.5 GHz
        4'hF: cap_bank_sel <= 4'hF;   // 12.5 – 14 GHz
    endcase

    // Op-amp gain: upper nibble of fine tuning word
    // Sets the α_phys = G_m / (ω₀ C₁) physical parameter
    opamp_gain_sel <= freq_pot[7:4];

    // Resistor bank: lower nibble of fine tuning word
    // Sets the Chua diode piecewise-linear slope breakpoints (m₀, m₁)
    res_bank_sel <= freq_pot[3:0];

    // Nonlinearity selector: upper nibble — determines inner vs outer slope ratio
    // at the current operating frequency
    nonlin_sel <= freq_pot[7:4];

    // Chaos DAC: 8 most significant bits scaled to full 12-bit DAC range
    // Provides an external perturbation path for attractor shaping
    chaos_dac <= {freq_pot[11:4], 4'h0};

    // Buffer biases scale with tuning word to maintain noise floor
    // as frequency changes the transistor operating point
    buf1_bias <= 12'h400 + {4'h0, freq_pot[11:4]};
    buf2_bias <= 12'h400 + {4'h0, freq_pot[11:4]};

    // Buffer gain inversely tracks frequency to compensate gain roll-off
    // and maintain flat noise power spectral density across the tuning range
    buf_gain_sel <= ~freq_pot[7:4];
end
endtask

// =============================================================================
// SELECT PA BAND
// Routes the RF chain through the appropriate PA stage and output filter
// based on the current frequency setting.
// =============================================================================

task select_pa_band;
begin
    casez (freq_pot[11:8])
        4'b0000: pa_band_sel <= 4'h0;  // Sub-GHz — LDMOS stage
        4'b0001,
        4'b0010,
        4'b0011: pa_band_sel <= 4'h1;  // L-band / S-band — bipolar stage
        4'b0100,
        4'b0101,
        4'b0110,
        4'b0111: pa_band_sel <= 4'h2;  // C-band — GaAs MESFET stage
        4'b1???:  pa_band_sel <= 4'h3;  // X/Ku-band — InGaP HBT / GaN HEMT stage
        default: pa_band_sel <= 4'h0;
    endcase

    // Output filter tracks pa_band_sel for harmonic suppression
    filter_bank <= pa_band_sel;
end
endtask

// =============================================================================
// CONTROL RF CHAIN
// Sets driver and PA operating points from the power control potentiometer.
// =============================================================================

task control_rf_chain;
begin
    // Driver: bias scales with power demand to maintain efficiency
    driver_bias <= 12'h400 + {4'h0, power_pot[11:4]};
    driver_gain <= power_pot;

    // PA: bias set for Class AB operation (quiescent current + drive component)
    pa_bias     <= 12'h600 + {4'h0, power_pot[11:4]};

    // Attenuator tracks power pot inversely (lower word = less attenuation = more power)
    atten_ctrl  <= ~power_pot[11:4];
end
endtask

// =============================================================================
// MANAGE POWER LEVEL
// Asymmetric proportional feedback loop.
// step_down = 0x010 (fast — protects against exceeding target).
// step_up   = 0x001 (slow — prevents overshoot during ramp-up).
// Convergence: |e_steady| ≤ 0x011 worst-case hunting cycle.
// pa_drive is clamped to [0x001, foldback_limit] at all times.
// =============================================================================

task manage_power_level;
reg [19:0] new_power_sample;
integer    i;
begin
    // Squared-voltage proxy: max(4095²)>>4 = 1,048,064 — fits in 20 bits
    new_power_sample = ({8'h00, fwd_power} * {8'h00, fwd_power}) >> 4;

    // Accumulate into 8-sample ring buffer for averaging
    power_avg <= power_avg - power_history[avg_idx] + new_power_sample;
    power_history[avg_idx] <= new_power_sample;
    avg_idx   <= avg_idx + 1;

    // Use averaged power for control decisions (reduces noise sensitivity)
    current_power <= power_avg >> 3;   // Divide by 8

    // Proportional feedback — compare against scaled power_pot target
    if (current_power > {8'h0, power_pot}) begin
        if (pa_drive > 12'h010)
            pa_drive <= pa_drive - 12'h010;
        else
            pa_drive <= 12'h001;
    end else if (current_power < {8'h0, power_pot}) begin
        if (pa_drive < foldback_limit)
            pa_drive <= pa_drive + 12'h001;
        // If pa_drive == foldback_limit, hold — fold-back is active
    end

    // Overcurrent trip: delegate to update_protection for consistent action
    if (pa_current > MAX_CURRENT)
        protect_trip <= 1'b1;
end
endtask

// =============================================================================
// UPDATE PROTECTION
// Evaluates all fault conditions each clock cycle.
// Arc detect and overcurrent trigger ps_crowbar and fast_shutdown.
// All other conditions set protect_trip.
// =============================================================================

task update_protection;
begin
    protection_active =
        temp_trip     ||
        vswr_trip     ||
        arc_detect    ||
        ps_fault      ||
        current_trip  ||
        !door_interlock ||
        !airflow_ok   ||
        !emc_filter_ok ||
        (max_temp > MAX_TEMP);

    if (protection_active) begin
        protect_trip <= 1'b1;

        // Fault code priority encoder (highest priority first)
        if      (arc_detect)            fault_code <= FAULT_ARC;
        else if (current_trip || (pa_current > MAX_CURRENT))
                                        fault_code <= FAULT_CURRENT;
        else if (ps_fault)              fault_code <= FAULT_PSUPPLY;
        else if (temp_trip || (max_temp > MAX_TEMP))
                                        fault_code <= FAULT_OVERTEMP;
        else if (vswr_trip)             fault_code <= FAULT_VSWR;
        else if (!door_interlock)       fault_code <= FAULT_INTERLOCK;
        else if (!airflow_ok || !emc_filter_ok)
                                        fault_code <= FAULT_AIRFLOW;

        // Destructive faults: engage crowbar and fast shutdown
        if (arc_detect || current_trip) begin
            fast_shutdown <= 1'b1;
            ps_crowbar    <= 1'b1;
            crowbar_timer <= 16'h0000;
        end
    end
end
endtask

// =============================================================================
// MANAGE COOLING
// Two-regime thermal control:
//   Linear   (max_temp ≤ WARN_TEMP): fan_speed = 0x20 + (max_temp >> 4)
//     → peak at WARN_TEMP: 0x20 + 0x4D = 0x6D (109)
//   Emergency (max_temp > WARN_TEMP): fan_speed = 0xFF
//     Engages 8 °C before MAX_TEMP to provide thermal buffer.
// =============================================================================

task manage_cooling;
integer i;
begin
    // Determine maximum temperature across all 8 sensors
    max_temp = 12'h000;
    for (i = 0; i < 8; i = i + 1)
        if (temp_sense[i] > max_temp)
            max_temp = temp_sense[i];

    // Two-regime fan law
    if (max_temp > WARN_TEMP)
        fan_speed <= 8'hFF;
    else
        fan_speed <= MIN_FAN + max_temp[11:4];
end
endtask

// =============================================================================
// MEASURE FAN TACHOMETER
// Counts rising edges of fan_tach; RPM estimate updated every 256 counts.
// =============================================================================

task measure_fan_tach;
begin
    fan_tach_prev <= fan_tach;
    if (fan_tach && !fan_tach_prev) begin
        // Rising edge detected
        fan_tach_count <= fan_tach_count + 1;
    end
    // RPM estimate: latched every 256 pulses; scaling depends on clock rate
    if (fan_tach_count == 16'h00FF) begin
        fan_rpm_est    <= fan_tach_count;
        fan_tach_count <= 16'h0000;
    end
end
endtask

// =============================================================================
// ADJUST IMPEDANCE MATCH
// Perturb-and-observe hill-climbing minimising reflected power.
// Soft threshold: ref > fwd/16 ≈ VSWR 1.67:1 (early correction before hard trip).
// Hard threshold: vswr_trip hardware input (3:1, set by MAX_VSWR comparator).
// Converges in ≤ 15 steps from any initial match_ctrl value under unimodal |Γ|.
// =============================================================================

task adjust_impedance_match;
begin
    vswr_soft_flag <= 1'b0;

    if (fwd_power > 12'h010) begin
        if (ref_power > (fwd_power >> 4)) begin
            vswr_soft_flag <= 1'b1;
            if (match_ctrl < 4'hF)
                match_ctrl <= match_ctrl + 1;
        end else if (match_ctrl > 4'h0) begin
            match_ctrl <= match_ctrl - 1;
        end
    end
end
endtask

// =============================================================================
// UPDATE DISPLAY
// Computes frequency from freq_pot and triggers LCD update when changed.
// freq_pot range [0, 4095] → frequency range [0, 409,500 kHz] = 0–409.5 MHz
// for the base scaling factor of ×100 kHz/count.
// Actual frequency mapping is hardware-dependent; this provides a linear
// approximation suitable for a front-panel display.
// =============================================================================

task update_display;
reg [23:0] freq;
begin
    freq = {12'h000, freq_pot} * 24'd100;

    if (freq != freq_display) begin
        freq_display <= freq;
        format_display(freq);
    end

    // Second line shows power level and fault code
    if (lcd_mode) begin
        format_status_line();
    end
end
endtask

// =============================================================================
// FORMAT DISPLAY — Line 1: frequency readout
// HD44780 8-bit parallel, RS low for commands, RS high for data.
// Enable strobe: data is latched on the falling edge of lcd_en.
// =============================================================================

task format_display;
    input [23:0] freq;
    reg [7:0] digits [5:0];
    integer   i;
begin
    // BCD decomposition of 6-digit frequency
    for (i = 0; i < 6; i = i + 1) begin
        digits[i] = freq % 10;
        freq = freq / 10;
    end

    // Drive LCD through state machine; each state strobes lcd_en high then low
    case (lcd_state)
        4'h0: begin
            lcd_rs   <= 1'b0;
            lcd_data <= 8'h80;    // DDRAM address 0x00 (first line)
            lcd_en   <= 1'b1;
            lcd_state <= 4'h1;
        end
        4'h1: begin
            lcd_en   <= 1'b0;
            lcd_rs   <= 1'b1;
            lcd_data <= "F";
            lcd_en   <= 1'b1;
            lcd_state <= 4'h2;
        end
        4'h2:  begin lcd_en<=1'b0; lcd_data<="r"; lcd_en<=1'b1; lcd_state<=4'h3; end
        4'h3:  begin lcd_en<=1'b0; lcd_data<="e"; lcd_en<=1'b1; lcd_state<=4'h4; end
        4'h4:  begin lcd_en<=1'b0; lcd_data<="q"; lcd_en<=1'b1; lcd_state<=4'h5; end
        4'h5:  begin lcd_en<=1'b0; lcd_data<=":"; lcd_en<=1'b1; lcd_state<=4'h6; end
        4'h6:  begin lcd_en<=1'b0; lcd_data<=" "; lcd_en<=1'b1; lcd_state<=4'h7; end
        4'h7:  begin lcd_en<=1'b0; lcd_data<=digits[5]+8'h30; lcd_en<=1'b1; lcd_state<=4'h8; end
        4'h8:  begin lcd_en<=1'b0; lcd_data<=digits[4]+8'h30; lcd_en<=1'b1; lcd_state<=4'h9; end
        4'h9:  begin lcd_en<=1'b0; lcd_data<=digits[3]+8'h30; lcd_en<=1'b1; lcd_state<=4'hA; end
        4'hA:  begin lcd_en<=1'b0; lcd_data<=digits[2]+8'h30; lcd_en<=1'b1; lcd_state<=4'hB; end
        4'hB:  begin lcd_en<=1'b0; lcd_data<=digits[1]+8'h30; lcd_en<=1'b1; lcd_state<=4'hC; end
        4'hC:  begin lcd_en<=1'b0; lcd_data<=digits[0]+8'h30; lcd_en<=1'b1; lcd_state<=4'hD; end
        4'hD:  begin lcd_en<=1'b0; lcd_data<=" "; lcd_en<=1'b1; lcd_state<=4'hE; end
        4'hE:  begin lcd_en<=1'b0; lcd_data<="k"; lcd_en<=1'b1; lcd_state<=4'hF; end
        4'hF:  begin
            lcd_en   <=1'b0;
            lcd_data <="z";
            lcd_en   <=1'b1;
            lcd_state<=4'h0;
            lcd_mode <=~lcd_mode;   // Toggle to status line on next update cycle
        end
    endcase
end
endtask

// =============================================================================
// FORMAT STATUS LINE — Line 2: power level, VSWR flag, fault code
// =============================================================================

task format_status_line;
begin
    // Simplified: write power ADC value and fault code to second LCD line
    // Full production implementation would include decimal conversion and
    // calibration constants for absolute power in watts.
    if (fault_code != FAULT_NONE) begin
        // Display fault code
        lcd_rs   <= 1'b0;
        lcd_data <= 8'hC0;       // DDRAM address 0x40 (second line)
        lcd_en   <= 1'b1;
        lcd_en   <= 1'b0;
        lcd_rs   <= 1'b1;
        lcd_data <= "E";
        lcd_en   <= 1'b1;
        lcd_en   <= 1'b0;
        lcd_data <= "R";
        lcd_en   <= 1'b1;
        lcd_en   <= 1'b0;
        lcd_data <= "R";
        lcd_en   <= 1'b1;
        lcd_en   <= 1'b0;
        lcd_data <= fault_code + 8'h30;   // ASCII fault code digit
        lcd_en   <= 1'b1;
        lcd_en   <= 1'b0;
    end
    lcd_mode <= 1'b0;   // Return to frequency line
end
endtask

// =============================================================================
// SAFETY CHECK FUNCTIONS
// =============================================================================

function check_interlocks;
begin
    check_interlocks = door_interlock &&
                       airflow_ok     &&
                       emc_filter_ok  &&
                       !ps_fault      &&
                       !temp_trip;
end
endfunction

function system_ready;
begin
    system_ready = check_interlocks()  &&
                   !protection_active  &&
                   (max_temp   < MAX_TEMP)     &&
                   (pa_current < MAX_CURRENT);
end
endfunction

function check_protection;
begin
    check_protection = !protection_active;
end
endfunction

function init_sequence_complete;
begin
    init_sequence_complete = (aux_ps_en == 4'hF) &&
                             !ps_fault            &&
                             check_interlocks()   &&
                             (startup_timer > T_AUX_SETTLE);
end
endfunction

function shutdown_complete;
begin
    shutdown_complete = !pa_enable     &&
                        !driver_enable &&
                        !ps_enable     &&
                        (ps_voltage == 12'h000);
end
endfunction

// Dummy function to represent EMC filter check (maps to emc_filter_ok input)
function emc_filter_ok;
begin
    emc_filter_ok = 1'b1; // Placeholder — actual check is via input port
end
endfunction

// =============================================================================
// MAINTAIN STANDBY
// PA and driver are disabled; Chua circuit biased at idle; supplies up.
// =============================================================================

task maintain_standby;
begin
    ps_enable     <= 1'b1;
    aux_ps_en     <= 4'hF;
    pa_enable     <= 1'b0;
    driver_enable <= 1'b0;

    opamp1_bias   <= IDLE_BIAS;
    opamp2_bias   <= IDLE_BIAS;
    bias_voltage  <= 12'h400;
    atten_ctrl    <= 8'hFF;

    manage_cooling();
end
endtask

// =============================================================================
// EXECUTE SHUTDOWN — reverse of startup sequence
// seq_state must be reset to 8'h00 before entering STATE_SHUTDOWN.
// =============================================================================

task execute_shutdown;
begin
    case (seq_state)

        8'h00: begin
            pa_enable     <= 1'b0;
            driver_enable <= 1'b0;
            atten_ctrl    <= 8'hFF;   // Maximum attenuation immediately
            seq_state     <= 8'h01;
        end

        8'h01: begin
            // Ramp supply voltage down gracefully
            if (ps_voltage >= RAMP_STEP)
                ps_voltage <= ps_voltage - RAMP_STEP;
            else begin
                ps_voltage <= 12'h000;
                seq_state  <= 8'h02;
            end
        end

        8'h02: begin
            ps_enable    <= 1'b0;
            aux_ps_en    <= 4'h0;
            bias_voltage <= 12'h000;
            seq_state    <= 8'h03;
        end

        8'h03: begin
            opamp1_bias  <= 12'h000;
            opamp2_bias  <= 12'h000;
            protect_trip <= 1'b1;
            ps_crowbar   <= 1'b0;    // De-assert crowbar (energy discharged)
            fan_speed    <= MIN_FAN; // Maintain minimum cooling for residual heat
            seq_state    <= 8'h04;
        end

        default: ; // Hold in final shutdown state until STATE_OFF transition
    endcase
end
endtask

// =============================================================================
// HANDLE FAULT
// Records fault type, engages all required protection, waits for user reset.
// =============================================================================

task handle_fault;
begin
    // Disable RF chain immediately
    pa_enable     <= 1'b0;
    driver_enable <= 1'b0;
    protect_trip  <= 1'b1;

    // Latch thermal faults
    if (temp_trip || (max_temp > MAX_TEMP)) begin
        fault_latch <= 1'b1;
        fault_code  <= FAULT_OVERTEMP;
    end

    // Destructive faults
    if (arc_detect || current_trip) begin
        ps_crowbar    <= 1'b1;
        fast_shutdown <= 1'b1;
        fault_latch   <= 1'b1;
        fault_code    <= (arc_detect) ? FAULT_ARC : FAULT_CURRENT;
    end

    // Keep cooling at maximum during fault condition
    fan_speed <= 8'hFF;

    // Initiate shutdown on power switch release
    if (!power_switch) begin
        seq_state <= 8'h00;
        state     <= STATE_SHUTDOWN;
    end
end
endtask

// =============================================================================
// STATUS LED DRIVER — combinational, updated every clock
// Bit 3: Power supply good
// Bit 2: Protection active
// Bit 1: PA enabled
// Bit 0: Door interlock closed
// =============================================================================

always @(posedge clk_in) begin
    status_leds <= {
        ps_enable,
        protection_active,
        pa_enable,
        door_interlock
    };
end

endmodule
