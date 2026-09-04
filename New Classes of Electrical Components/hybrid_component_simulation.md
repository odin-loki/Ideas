# Hybrid component simulation

**Mathematical formulas for CPU and GPU implementation**

*A complete derivation and reference guide*

*February 2026*

## Chapter 0 — How to Read This Document

This document takes physical electronic components — things you would actually build in a lab — and shows you how to recreate their behaviour entirely in software on a normal computer. No special hardware needed. Every formula has been derived from first-principles physics, then rewritten in a form a computer can execute numerically.

If you are completely new to this field, think of it this way:

  • A real resistor dissipates energy as heat. We write an equation V = R·I that captures this. A computer can solve that equation millions of times per second.

  • A hybrid component is more complex — it behaves partly like an analog device (continuously varying voltages) and partly like a digital device (jumping between discrete states). To simulate it we need BOTH a differential equation AND a state machine running simultaneously.

Each component section contains:

  1. Plain English description of what the component does physically.

  2. The mathematical model — the governing equations.

  3. Derived simulation formulas — rewritten for numerical computation.

  4. Python code — ready to copy into NumPy or PyTorch.

  5. GPU acceleration notes — how to parallelise across millions of instances.

*💡 All Python code assumes: import numpy as np  |  import torch  |  from scipy.integrate import solve_ivp*

## Terminology Quick Reference

**ODE**
Ordinary Differential Equation — an equation involving derivatives like dx/dt. Solved numerically by stepping forward in tiny time increments.

**SDE**
Stochastic Differential Equation — an ODE with a random noise term. Used when thermal or quantum noise is functionally important.

**State machine**
A system that can be in one of N discrete states and transitions between them based on rules.

**Euler-Maruyama**
The simplest numerical method for SDEs: x\_{k+1} = x_k + f(x_k)dt + g(x_k)sqrt(dt)\*xi, where xi ~ N(0,1).

**Vectorised**
Running the same calculation on thousands of numbers simultaneously — what GPUs are designed for.

**Memcomponent**
A component (memristor, memcapacitor, meminductor) whose properties depend on its own history.

**dt**
The time step used in simulation. Smaller dt = more accurate but slower. Typical: 1e-9 to 1e-12 seconds.

## Chapter 1 — The Universal Hybrid Automaton Framework

Every component in this catalogue can be described by the same mathematical skeleton. Understanding this skeleton once makes every subsequent component easy to follow.

## 1.1  The Core Idea

A hybrid component has TWO kinds of variables running simultaneously:

  1. Continuous variables  x(t) ∈ R^n  — things like voltage, current, charge, flux, domain wall position. These change smoothly and are governed by differential equations.

  2. A discrete state  s ∈ {0, 1, 2, ..., N-1}  — which magnetic domain configuration the core is in, whether the oxide layer is crystalline or amorphous, how many flux quanta are trapped, etc.

The full state at any moment is the pair  (x, s).

## 1.2  The Governing Equations

**dx/dt  =  f(x, s, u, t)          [Continuous dynamics]**
**s(t+)  =  T(s(t-), x, u)  when  G(x, s) = 0   [Discrete transition]**
Where:

  • u(t) is the external input (applied voltage, current, magnetic field, light…)

  • f is the vector field that drives continuous change

  • G is a guard condition — a threshold that when crossed triggers a state jump

  • T is the transition function — the rule for what state to jump to

## 1.3  The Electrical Output Relation

For any hybrid R, L, or C component, the terminal behaviour is:

**V(t)  =  R(x, s) · I(t)          [Hybrid resistor]**
**Q(t)  =  C(x, s) · V(t)          [Hybrid capacitor]**
**Phi(t)  =  L(x, s) · I(t)         [Hybrid inductor]**
The key insight: R, C, L are no longer constants. They are functions of the current internal state. This is what makes these components novel.

## 1.4  Energy Bookkeeping

**E_total  =  E_continuous(x)  +  E_discrete(s)  +  E_coupling(x, s)**
Coupling energy is what makes the two worlds talk to each other. For example, in a magnetic domain inductor, the continuous magnetic flux energy couples to the discrete domain state through the permeability.

## 1.5  Information Content

**I_total  =  log2(N)  +  H_continuous(x)**
Where H_continuous = -integral of p(x) log2 p(x) dx is the differential entropy of the continuous variable. A hybrid component can store more information per device than a purely digital or purely analog one.

## 1.6  The Simulation Loop (CPU — Single Instance)

def simulate_hybrid(f, G, T, x0, s0, u_func, dt, T_end):

    x = np.array(x0, dtype=float)

    s = s0

    t = 0.0

    history = [(t, x.copy(), s)]

    while t < T_end:

        u = u_func(t)

        # ── continuous step (Euler) ──

        x = x + f(x, s, u) \* dt

        t += dt

        # ── discrete transition check ──

        for cond, target in G(x, s, u):

            if cond:

                s = T(s, target, x, u)

                break

        history.append((t, x.copy(), s))

    return history

## 1.7  GPU Vectorised Version (PyTorch — N Parallel Instances)

# Simulate N independent components in parallel on GPU

def simulate_gpu(f, G_mask, T_func, x0, s0, u_seq, dt):

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    x = torch.tensor(x0, dtype=torch.float32, device=device)  # shape (N, n_vars)

    s = torch.tensor(s0, dtype=torch.long, device=device)       # shape (N,)

    results = [x.clone()]

    for u in u_seq:                                              # u shape: (N,)

        x = x + f(x, s, u) \* dt                                # vectorised ODE step

        mask = G_mask(x, s, u)                                  # shape (N,) bool

        s = torch.where(mask, T_func(s, x, u), s)              # conditional state jump

        results.append(x.clone())

    return torch.stack(results)                                  # shape (T, N, n_vars)

*💡 On a modern GPU you can simulate millions of independent component instances simultaneously. This is extremely useful for Monte Carlo analysis, parameter sweeps, and neural network training with differentiable physics.*

## Chapter 2 — Quantum Tunnel Resistor (QTR)

Physical description: Electrons cross a thin insulating barrier not by going over it (as in classical physics) but by quantum mechanical tunnelling — effectively appearing on the other side. At the scale of individual electrons this is a discrete random event. At the macroscopic level, millions of these events per second produce a smooth continuous current.

## 2.1  The Simmons Tunnel Current Model

The most accurate formula for DC tunnel current through a rectangular barrier is the Simmons model. It gives current density J (amps per square metre) as a function of applied voltage V.

**J(V)  =  J0 · [ (phi_bar - V/2)·exp(-A·sqrt(phi_bar - V/2))**
**              -  (phi_bar + V/2)·exp(-A·sqrt(phi_bar + V/2)) ]**
**J0**
e / (2\*pi\*hbar\*d^2)  —  prefactor, units A/m^2/eV

**phi_bar**
Average barrier height in eV (for Al2O3: ~3.0 eV)

**A**
(4\*pi\*d/h) \* sqrt(2\*m_e)  —  wave-vector factor, units eV^(-1/2)

**d**
Barrier thickness in metres (2e-9 for 2 nm)

**V**
Applied voltage in Volts

The total current through an area A_junc is:

**I(V)  =  J(V)  \*  A_junc**
## 2.2  Simplified Low-Voltage Approximation

When V << phi_bar (low-voltage limit), the Simmons formula reduces to a simpler linear-then-quadratic form:

**I  ≈  G0 · V · (1  +  V^2 / (6\*phi_bar^2))**
Where G0 = (e^2 / h) · (A_junc/d) · exp(-A·sqrt(phi_bar)) is the zero-bias conductance.

## 2.3  Shot Noise — Simulating Discrete Electron Events

The current is not truly continuous — it is a stream of individual electron tunnelling events. Each event carries charge e = 1.6×10^-19 C. The number of events in a time window dt follows a Poisson distribution.

**n_events  ~  Poisson(lambda \* dt)    where  lambda = I(V) / e**
**I_stochastic  =  n_events \* e / dt**
The power spectral density of this shot noise is:

**S_I(f)  =  2 \* e \* I             [White noise, flat spectrum]**
## 2.4  Complete Python Simulation

import numpy as np

# Physical constants

e = 1.602e-19        # electron charge, C

hbar = 1.055e-34     # reduced Planck, J\*s

h_planck = 6.626e-34 # Planck constant

m_e = 9.109e-31      # electron mass, kg

def simmons_current(V, d=2e-9, phi_bar=3.0, A_junc=50e-12\*\*2):

    '''

    Simmons tunnel current model.

    V:       applied voltage (V)

    d:       barrier thickness (m), default 2 nm

    phi_bar: average barrier height (eV), default 3.0 eV for Al2O3

    A_junc:  junction area (m^2), default 50 um x 50 um

    '''

    # Convert units

    phi_eV = phi_bar

    A = (4 \* np.pi \* d / h_planck) \* np.sqrt(2 \* m_e \* e)  # eV^-0.5

    J0 = e / (2 \* np.pi \* hbar \* d\*\*2)

    # Avoid division by zero at V=0

    V = np.where(np.abs(V) < 1e-6, 1e-6 \* np.sign(V + 1e-30), V)

    lo = phi_eV - V/2

    hi = phi_eV + V/2

    J = J0 \* (lo \* np.exp(-A \* np.sqrt(np.maximum(lo, 0)))

            - hi \* np.exp(-A \* np.sqrt(np.maximum(hi, 0))))

    return J \* A_junc

def simulate_qtr(V_dc, dt=1e-9, n_steps=10000):

    '''Simulate QTR with shot noise included.'''

    I_mean = simmons_current(V_dc)

    lam = abs(I_mean) / e          # mean event rate (Hz)

    # Poisson-sample discrete electron events

    n_events = np.random.poisson(lam \* dt, size=n_steps)

    I_noisy  = n_events \* e / dt \* np.sign(I_mean)

    t = np.arange(n_steps) \* dt

    return t, I_noisy, I_mean

# Example: V sweep I-V curve

V_range = np.linspace(-1, 1, 1000)

I_curve = simmons_current(V_range)

R_dynamic = V_range / (I_curve + 1e-30)   # dynamic resistance

## 2.5  GPU Vectorisation (PyTorch)

import torch

def simmons_gpu(V, d=2e-9, phi_bar=3.0, A_junc=2.5e-15):

    '''Batch Simmons model on GPU. V can be any shape.'''

    device = V.device

    A  = torch.tensor((4\*3.14159\*d/6.626e-34)\*np.sqrt(2\*9.109e-31\*1.602e-19),

                       dtype=V.dtype, device=device)

    J0 = torch.tensor(1.602e-19/(2\*3.14159\*1.055e-34\*d\*\*2),

                       dtype=V.dtype, device=device)

    V  = torch.where(torch.abs(V) < 1e-6, torch.sign(V)\*1e-6, V)

    lo = phi_bar - V/2

    hi = phi_bar + V/2

    J  = J0\*(lo\*torch.exp(-A\*torch.sqrt(lo.clamp(min=0)))

           - hi\*torch.exp(-A\*torch.sqrt(hi.clamp(min=0))))

    return J \* A_junc

# Simulate 1 million junctions in parallel:

V_batch = torch.rand(1_000_000, device='cuda') \* 2 - 1

I_batch = simmons_gpu(V_batch)

*💡 Key insight: The QTR resistance R = V/I(V) varies continuously with voltage via the Simmons formula, while discrete electron events produce Poisson-distributed shot noise. You get both worlds in one equation.*

## Chapter 3 — Magnetic Domain Inductor

Physical description: A coil wound around a ferrite core. The core is a magnetic material whose atoms are grouped into domains — regions of uniform magnetisation. As you increase current, domain walls move continuously (smooth inductance change) until a domain flips abruptly (discrete Barkhausen jump). The CoFeB thin film adds extra discrete switching events with sharp thresholds.

## 3.1  The Jiles-Atherton Hysteresis Model

This is the standard industry model for magnetic hysteresis. It governs how magnetisation M varies with field H, capturing both the continuous rotation and the discrete irreversible losses.

Step 1 — The anhysteretic (ideal) magnetisation curve:

**M_an(H_eff)  =  M_s · [ coth(H_eff / a)  -  a / H_eff ]     [Langevin function]**
Step 2 — Effective field including demagnetisation and coupling:

**H_eff  =  H  +  alpha · M     where H = N\*I/l_eff**
Step 3 — The differential equation for M:

**dM/dH  =  (1-c)·(M_an - M) / [k·delta - alpha·(M_an - M)]  +  c·dM_an/dH**
**M_s**
Saturation magnetisation (A/m). NiZn ferrite: ~2.5e5 A/m

**a**
Shape parameter (A/m). Controls width of hysteresis. ~1200 A/m

**alpha**
Inter-domain coupling. Small value ~1e-4

**k**
Pinning parameter — energy to unpin a domain wall. ~400 A/m

**c**
Reversibility. c=0 fully irreversible; c=1 fully reversible. ~0.2

**delta**
+1 if dH/dt > 0 (increasing field), -1 if decreasing. KEY!

The inductance from the coil and core is then:

**L(H)  =  mu_0 · N^2 · A_e / l_e · (1 + dM/dH)**
**     =  mu_0 · mu_r_eff(H) · N^2 · A_e / l_e**
## 3.2  Discrete Domain Switching (CoFeB Film)

The thin CoFeB film creates additional discrete switching events on top of the continuous Jiles-Atherton core. Each domain in the film has a switching field drawn from a distribution:

**H_sw[i]  ~  Normal(H_mean, sigma_H)     for i = 1..N_domains**
State transitions:

**m_i(t+)  =  +1  if  H(t) > H_sw[i]**
**m_i(t+)  =  -1  if  H(t) < -H_sw[i]**
The film contribution to inductance is:

**delta_L  =  mu_0 · N^2 · A_film / l_film · (1/N_d) · sum_i(m_i)  · chi_CoFeB**
## 3.3  Complete Python Simulation

import numpy as np

class MagneticDomainInductor:

    def \_\_init\_\_(self, N=20, A_e=7.07e-9, l_e=6.28e-3,

                 Ms=2.5e5, a=1200, alpha=1e-4, k=400, c=0.2,

                 N_domains=20, H_mean=800, sigma_H=150):

        # Core geometry

        self.N = N            # turns

        self.A_e = A_e        # effective cross-section (m^2), 3mm OD toroid

        self.l_e = l_e        # effective path length (m)

        self.mu0 = 4\*np.pi\*1e-7

        # Jiles-Atherton params

        self.Ms, self.a, self.alpha, self.k, self.c = Ms, a, alpha, k, c

        # CoFeB thin-film domain array

        self.H_sw = np.abs(np.random.normal(H_mean, sigma_H, N_domains))

        self.m    = np.ones(N_domains)  # start all aligned +1

        # State

        self.M = 0.0

        self.delta = 1

        self.H_prev = 0.0

    def \_langevin(self, H_eff):

        if abs(H_eff) < 1e-6: return self.Ms \* H_eff / (3\*self.a)

        return self.Ms \* (1/np.tanh(H_eff/self.a) - self.a/H_eff)

    def step(self, I, dt):

        H = self.N \* I / self.l_e                 # Ampere's law

        self.delta = 1 if H >= self.H_prev else -1

        H_eff = H + self.alpha \* self.M

        Man   = self.\_langevin(H_eff)

        dMan_dH = (self.\_langevin(H_eff + 0.1) - self.\_langevin(H_eff - 0.1)) / 0.2

        denom = self.k \* self.delta - self.alpha \* (Man - self.M)

        if abs(denom) < 1e-10: denom = 1e-10

        dMdH  = (1-self.c)\*(Man - self.M)/denom + self.c\*dMan_dH

        dH    = H - self.H_prev

        self.M += dMdH \* dH                        # integrate

        # CoFeB discrete switching

        self.m = np.where(H > self.H_sw, 1.0,

                  np.where(H < -self.H_sw, -1.0, self.m))

        # Inductance calculation

        chi_eff  = dMdH + np.mean(self.m) \* 5000  # film adds ~chi=5000

        L = self.mu0 \* self.N\*\*2 \* self.A_e / self.l_e \* (1 + chi_eff)

        self.H_prev = H

        return L

    def simulate(self, I_array, dt):

        return np.array([self.step(I, dt) for I in I_array])

# Run: triangular current ramp

ind = MagneticDomainInductor()

t  = np.linspace(0, 1e-4, 10000)

I  = 0.1 \* np.sin(2\*np.pi\*1e4\*t)

L  = ind.simulate(I, dt=1e-8)

*💡 The discrete jumps in L correspond to real Barkhausen noise — tiny voltage spikes that appear across the coil when a magnetic domain flips. In the simulation they appear as sudden changes in the L array.*

## Chapter 4 — Memory Components: Memristor, Memcapacitor, Meminductor

Physical description: These are components whose R, C, or L value at this moment depends on everything that has happened to them in the past. The HP memristor literally has a thin film that grows or shrinks based on charge flow — the film thickness is the memory. Memcapacitors store trapped charge that shifts the capacitance. Meminductors have domain walls whose positions reflect current history.

## 4.1  The HP Memristor Model

The HP Labs memristor (titanium dioxide TiO2, 2008) is the canonical model. A thin oxide layer has a doped sub-region whose width w sets the resistance.

**R(w)  =  R_on · (w/D)  +  R_off · (1 - w/D)**
**V(t)  =  R(w) · I(t)**
**dw/dt  =  mu_v · (R_on/D^2) · I(t) · f(w)**
**R_on**
Minimum resistance (doped region fully spans device). ~100 Ohm

**R_off**
Maximum resistance (undoped region). ~16,000 Ohm

**D**
Total device thickness. 10 nm

**mu_v**
Oxygen vacancy mobility. 1e-14 m^2/(V\*s)

**f(w)**
Window function: keeps w inside [0, D]. Joglekar: f = 1 - (2w/D - 1)^(2p)

## 4.2  Dual-Mode Memristor (TaOx + HfO2)

The dual-mode design from your documents combines an analog TaOx layer (continuous resistance tuning) with a binary HfO2 layer (discrete crystalline/amorphous switching). Both mechanisms operate simultaneously:

**R_total(x_a, s_b)  =  R_analog(x_a)  \*  R_binary(s_b)**
**R_analog(x_a)  =  R_min \* exp(beta \* (1 - x_a))    x_a in [0,1]**
**R_binary(s_b)  =  1 (crystalline, low-R) or r (amorphous, high-R)**
The analog state evolves continuously:

**dx_a/dt  =  I \* x_a \* (1 - x_a) / I_ref**
The binary state switches when cumulative charge exceeds threshold:

**s_b  flips  when  |integral I dt|  >  Q_threshold**
## 4.3  Memcapacitor Model

A memcapacitor stores charge history in its internal state phi (the integral of voltage). The capacitance C depends on phi:

**q(t)  =  C(phi) · V(t)**
**phi(t)  =  integral_0^t  V(tau) dtau     [flux linkage]**
**C(phi)  =  C_0  +  dC · tanh(phi / phi_0)**
The current flowing into the capacitor is:

**I  =  dq/dt  =  C(phi)·(dV/dt)  +  V·(dC/dphi)·V**
**         =  C(phi)·dV/dt  +  V^2 · dC_dphi**
## 4.4  Meminductor Model

A meminductor's inductance depends on q (the integral of current):

**Phi(t)  =  L(q) · I(t)     where  q(t) = integral_0^t I(tau) dtau**
**L(q)  =  L_0  +  dL · tanh(q / q_0)**
**V  =  dPhi/dt  =  L(q) · dI/dt  +  I · (dL/dq) · I**
**  =  L(q) · dI/dt  +  I^2 · dL_dq**
## 4.5  Complete Python Simulation (All Three)

import numpy as np

# ── MEMRISTOR ──────────────────────────────────────────────────────────

class Memristor:

    def \_\_init\_\_(self, Ron=100, Roff=16000, D=10e-9, mu_v=1e-14, p=1):

        self.Ron, self.Roff, self.D, self.mu_v, self.p = Ron, Roff, D, mu_v, p

        self.w = D \* 0.5   # start at 50% doped

    def \_window(self):

        return 1 - (2\*self.w/self.D - 1)\*\*(2\*self.p)

    def step(self, I, dt):

        R = self.Ron\*(self.w/self.D) + self.Roff\*(1 - self.w/self.D)

        V = R \* I

        dw = self.mu_v \* (self.Ron/self.D\*\*2) \* I \* self.\_window()

        self.w = np.clip(self.w + dw\*dt, 0, self.D)

        return V, R

# ── DUAL-MODE MEMRISTOR ─────────────────────────────────────────────────

class DualModeMemristor:

    def \_\_init\_\_(self, Rmin=50, beta=4.0, I_ref=1e-3, r_ratio=100, Q_thresh=1e-6):

        self.Rmin, self.beta, self.I_ref = Rmin, beta, I_ref

        self.r_ratio    = r_ratio     # HfO2 amorphous vs crystalline R ratio

        self.Q_thresh   = Q_thresh    # charge needed to flip binary state

        self.xa  = 0.5               # analog state

        self.sb  = 0                 # binary state (0=cryst, 1=amorphous)

        self.q_acc = 0.0             # accumulated charge

    def step(self, I, dt):

        Ra   = self.Rmin \* np.exp(self.beta \* (1 - self.xa))

        Rb   = 1 if self.sb == 0 else self.r_ratio

        R    = Ra \* Rb

        V    = R \* I

        # Analog dynamics

        dxa  = I \* self.xa \* (1 - self.xa) / self.I_ref

        self.xa = np.clip(self.xa + dxa\*dt, 0, 1)

        # Binary switching

        self.q_acc += abs(I) \* dt

        if self.q_acc > self.Q_thresh:

            self.sb = 1 - self.sb    # flip state

            self.q_acc = 0.0

        return V, R

# ── MEMCAPACITOR ────────────────────────────────────────────────────────

class Memcapacitor:

    def \_\_init\_\_(self, C0=1e-9, dC=0.8e-9, phi0=1e-6):

        self.C0, self.dC, self.phi0 = C0, dC, phi0

        self.phi = 0.0    # integral of V

        self.V   = 0.0

    def C(self): return self.C0 + self.dC \* np.tanh(self.phi / self.phi0)

    def dCdphi(self): return self.dC / (self.phi0 \* np.cosh(self.phi/self.phi0)\*\*2)

    def step(self, V_new, dt):

        dV   = (V_new - self.V) / dt

        I    = self.C() \* dV + V_new\*\*2 \* self.dCdphi()

        self.phi += V_new \* dt

        self.V    = V_new

        return I, self.C()

# ── MEMINDUCTOR ─────────────────────────────────────────────────────────

class Meminductor:

    def \_\_init\_\_(self, L0=1e-6, dL=0.8e-6, q0=1e-6):

        self.L0, self.dL, self.q0 = L0, dL, q0

        self.q = 0.0     # integral of I

        self.I = 0.0

    def L(self): return self.L0 + self.dL \* np.tanh(self.q / self.q0)

    def dLdq(self): return self.dL / (self.q0 \* np.cosh(self.q/self.q0)\*\*2)

    def step(self, I_new, dt):

        dI   = (I_new - self.I) / dt

        V    = self.L() \* dI + I_new\*\*2 \* self.dLdq()

        self.q += I_new \* dt

        self.I  = I_new

        return V, self.L()

## Chapter 5 — Stochastic Components: Brownian Resistor & Markov Chain Models

Physical description: The Brownian Resistor is a device where thermal noise is not just a nuisance — it IS the mechanism. Quantum dot charge states create a discrete energy landscape, and the resistance performs a random walk between states. This can be used for noise-based computing, physical random number generation, and stochastic signal processing.

## 5.1  The Langevin SDE Model

Within a given discrete state n with equilibrium resistance R_n, the actual resistance performs an Ornstein-Uhlenbeck random walk:

**dR  =  -gamma · (R - R_n) · dt  +  sigma · dW_t**
Where dW_t = sqrt(dt) \* xi, xi ~ N(0,1) is Gaussian white noise (the Wiener process increment).

Discretised for simulation (Euler-Maruyama method):

**R[k+1]  =  R[k]  -  gamma · (R[k] - R_n) · dt  +  sigma · sqrt(dt) · xi[k]**
## 5.2  Discrete State Transitions (Markov Chain)

The component can jump between N discrete resistance levels. The transition rate from state n to state m follows the Arrhenius rate law:

**lambda\_{n->m}  =  nu_0 · exp(-E\_{nm} / (k_B · T))**
Where E\_{nm} is the energy barrier between states and nu_0 is the attempt frequency (~10^12 Hz). The probability of transition in one timestep is:

**P(n -> m in dt)  =  lambda\_{n->m} · dt**
## 5.3  Poisson Capacitor Model

Individual electron captures are Poisson events. Charge Q and voltage V evolve as:

**N(t)  ~  Poisson(lambda · t)     where lambda = I_leakage / e**
**Q(t)  =  e · N(t)     [Discrete charge in coulombs]**
**V(t)  =  Q(t) / C     [Continuous voltage]**
## 5.4  Python Simulation (GPU-Ready)

import numpy as np

import torch

# ── BROWNIAN RESISTOR (CPU) ──────────────────────────────────────────────

class BrownianResistor:

    def \_\_init\_\_(self, R_levels=[1e3, 5e3, 20e3, 100e3],

                       gamma=1e6, sigma=50.0, T=300, kB=1.38e-23):

        self.R_levels = np.array(R_levels)

        self.gamma    = gamma   # mean reversion rate (Hz)

        self.sigma    = sigma   # noise amplitude (Ohm/sqrt(s))

        self.T        = T

        self.kB       = kB

        self.state    = 0       # current discrete state index

        self.R        = R_levels[0]

        # Energy barriers (example: uniform, in units of kBT)

        n = len(R_levels)

        self.E_barriers = np.ones((n, n)) \* 5 \* kB \* T  # 5 kBT barriers

        np.fill_diagonal(self.E_barriers, 0)

    def step(self, V, dt, nu0=1e12):

        R_n = self.R_levels[self.state]

        xi  = np.random.normal()

        # Continuous OU random walk

        self.R += -self.gamma\*(self.R - R_n)\*dt + self.sigma\*np.sqrt(dt)\*xi

        self.R  = max(1.0, self.R)  # resistance must be positive

        # Markov chain state transitions

        n = len(self.R_levels)

        for m in range(n):

            if m == self.state: continue

            E   = self.E_barriers[self.state, m]

            lam = nu0 \* np.exp(-E / (self.kB \* self.T))

            if np.random.rand() < lam \* dt:

                self.state = m

                break

        I = V / self.R

        return I, self.R

# ── POISSON CAPACITOR (GPU) ──────────────────────────────────────────────

def simulate_poisson_cap_gpu(C=1e-9, I_leak=1e-9, V0=1.0,

                              dt=1e-9, n_steps=100000, n_caps=100000):

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    e      = 1.602e-19

    lam    = I_leak / e           # mean electron rate (events/sec)

    # Each capacitor starts with the same initial charge

    Q = torch.ones(n_caps, device=device) \* C \* V0

    V_history = [Q / C]

    for \_ in range(n_steps):

        # Discrete electron captures: Poisson sampling

        rate  = (torch.abs(Q/C) \* C \* 1e6).clamp(max=1e7) / e  # dynamic rate

        delta_n = torch.poisson(rate \* dt \* torch.ones(n_caps, device=device))

        Q = Q + delta_n \* e - I_leak \* dt  # capture - leakage

        V_history.append(Q / C)

    return torch.stack(V_history)  # shape: (n_steps+1, n_caps)

*💡 The GPU version simulates 100,000 independent capacitors simultaneously. Each one undergoes different random charge capture events. This is perfect for Monte Carlo yield analysis or studying statistical distributions in noisy circuits.*

## Chapter 6 — Josephson Junction Inductor

Physical description: Two superconductors separated by a thin barrier. Quantum mechanics allows Cooper pairs (pairs of electrons) to tunnel through, creating a supercurrent. The amount of supercurrent depends sinusoidally on a phase difference phi — a continuous quantum variable. Flux, however, only enters or leaves in discrete quanta of Phi_0 = h/(2e) = 2.07 femtoWebers. This combination of continuous phase and discrete flux is the essence of the hybrid behaviour.

## 6.1  The Josephson Relations

**I(t)  =  I_c · sin(phi(t))     [Current-phase relation]**
**V(t)  =  (hbar/2e) · dphi/dt     [Voltage-phase relation]**
Where phi is the quantum phase difference across the junction. From these two equations we can derive the effective inductance:

**L_J(phi)  =  hbar / (2e · I_c · cos(phi))**
This inductance is tunable — by adjusting the DC phase bias you can set any inductance from L_min = hbar/(2e·I_c) to infinity (at phi = pi/2).

## 6.2  The RCSJ Model (Resistively and Capacitively Shunted Junction)

A real junction has parallel resistance R_J (quasiparticle tunnelling) and capacitance C_J (geometric). The full dynamics are:

**I_applied  =  I_c·sin(phi)  +  (hbar/2eR)·dphi/dt  +  C·(hbar/2e)·d^2phi/dt^2**
Normalise: divide everything by I_c, let tau = omega_p · t where omega_p = sqrt(2e·I_c/(hbar·C)) is the plasma frequency:

**I_n  =  sin(phi)  +  (1/Q)·dphi/dtau  +  d^2phi/dtau^2**
**I_n**
Normalised bias current = I_applied / I_c

**Q**
Quality factor = omega_p \* R_J \* C_J. High Q = underdamped (voltage oscillations).

**omega_p**
Plasma frequency = sqrt(2\*pi\*I_c / (Phi_0 \* C_J)). ~10-100 GHz for typical junctions.

**I_c**
Critical current. ~1 uA to 10 uA for typical junctions.

## 6.3  Discrete Flux Quantisation Guard Condition

Flux enters the junction in units of Phi_0. When the phase phi crosses a multiple of 2\*pi, one flux quantum has passed through:

**Phi  =  (Phi_0 / 2\*pi) · phi**
**n_flux  =  round(phi / (2\*pi))     [Integer number of flux quanta]**
## 6.4  Python Simulation

import numpy as np

from scipy.integrate import solve_ivp

# Physical constants

hbar  = 1.055e-34

e_q   = 1.602e-19

Phi0  = hbar \* np.pi / e_q   # = h/2e = 2.067e-15 Wb

class JosephsonJunction:

    def \_\_init\_\_(self, Ic=10e-6, R_J=50.0, C_J=1e-15):

        self.Ic  = Ic

        self.R_J = R_J

        self.C_J = C_J

        self.omega_p = np.sqrt(2\*np.pi\*Ic / (Phi0 \* C_J))

        self.Q = self.omega_p \* R_J \* C_J

        self.n_flux = 0   # discrete flux quanta count

    def rcsj_ode(self, tau, state, I_n):

        '''state = [phi, dphi/dtau]'''

        phi, dphi = state

        d2phi = I_n - np.sin(phi) - dphi/self.Q

        return [dphi, d2phi]

    def simulate(self, I_applied, t_end, dt=1e-12):

        t_norm = np.arange(0, t_end \* self.omega_p, self.omega_p \* dt)

        I_n    = I_applied / self.Ic

        sol = solve_ivp(self.rcsj_ode, [0, t_norm[-1]], [0.0, 0.0],

                        args=(I_n,), t_eval=t_norm, method='RK45',

                        rtol=1e-8, atol=1e-10)

        phi   = sol.y[0]

        t_phys = sol.t / self.omega_p

        V     = (hbar / (2\*e_q)) \* np.gradient(phi, t_phys)

        I_sc  = self.Ic \* np.sin(phi)

        # Inductance (diverges at phi = pi/2 + n\*pi)

        L_J   = hbar / (2\*e_q \* self.Ic \* np.cos(phi).clip(-0.99, 0.99))

        # Track flux quanta

        n_flux = np.round(phi / (2\*np.pi)).astype(int)

        return t_phys, phi, V, I_sc, L_J, n_flux

# Example: DC current at 0.9 Ic (subcritical — junction stays phase-locked)

jj  = JosephsonJunction(Ic=10e-6, R_J=50, C_J=1e-15)

t, phi, V, I_sc, L_J, n_flux = jj.simulate(I_applied=9e-6, t_end=1e-9)

print(f'Mean L_J = {np.mean(L_J)\*1e12:.1f} pH')

## 6.5  GPU Parallelisation (Parameter Sweep)

import torch

def josephson_sweep_gpu(I_c_array, I_bias, n_steps=10000, dt_norm=0.01):

    '''

    Sweep over many Ic values simultaneously on GPU.

    I_c_array: tensor of shape (N,) with different critical currents

    Returns: phi tensor of shape (n_steps, N)

    '''

    device = I_c_array.device

    N   = len(I_c_array)

    Q   = torch.ones(N, device=device) \* 5.0  # fixed Q for sweep

    I_n = I_bias / I_c_array                  # normalised bias per junction

    phi = torch.zeros(N, device=device)

    dphi = torch.zeros(N, device=device)

    history = [phi.clone()]

    for \_ in range(n_steps):

        d2phi = I_n - torch.sin(phi) - dphi/Q

        dphi  = dphi  + d2phi \* dt_norm

        phi   = phi   + dphi  \* dt_norm

        history.append(phi.clone())

    return torch.stack(history)  # (n_steps+1, N)

## Chapter 7 — GMR Spin Resistor

Physical description: Two ferromagnetic layers separated by a non-magnetic spacer. When the magnetisations are parallel, electrons flow easily (low resistance R_P). When antiparallel, scattering is high (R_AP). Since magnetic alignment is a discrete concept (up/down or some angle between) but resistance varies continuously with angle, this is a perfect hybrid component.

## 7.1  The GMR Resistance Formula

**R(theta)  =  R_P  +  (R_AP - R_P)/2  \*  (1 - cos(theta))**
Where theta is the angle between the two layer magnetisation vectors. For a simpler normalised form:

**R(theta)  =  R_P  \*  (1  +  GMR_ratio/2  \*  (1 - cos theta))**
**GMR_ratio  =  (R_AP - R_P) / R_P     [e.g., 0.12 = 12%]**
Using vector notation with unit magnetisation vectors m1 and m2:

**R  =  R_P  +  ΔR/2  \*  (1  -  m1 · m2)     where ΔR = R_AP - R_P**
## 7.2  Stoner-Wohlfarth Magnetisation Switching

The free layer switches discretely when the applied field exceeds the switching field. The switching astroid gives the critical field for switching at arbitrary angle theta between field and easy axis:

**H_sw(theta)  =  H_k / (sin^(2/3)(theta) + cos^(2/3)(theta))^(3/2)**
For a field applied along the easy axis (theta = 0):

**H_sw  =  H_k     [the anisotropy field]**
And the magnetisation dynamics between switching events (Landau-Lifshitz-Gilbert equation):

**dm/dt  =  -gamma \* m x H_eff  +  alpha \* m x (m x H_eff)**
**H_k**
Anisotropy field. For CoFeB ~800 A/m to 2000 A/m.

**gamma**
Gyromagnetic ratio = 2.21e5 m/(A\*s).

**alpha**
Gilbert damping. 0.01 to 0.05 for CoFeB.

**H_eff**
Total effective field = H_applied + H_exchange + H_anisotropy + H_demag.

## 7.3  Python Simulation

import numpy as np

class GMRSpinResistor:

    def \_\_init\_\_(self, RP=100.0, RAP=112.0, Hk=1000, alpha=0.02):

        self.RP    = RP

        self.RAP   = RAP

        self.dR    = RAP - RP

        self.Hk    = Hk

        self.alpha = alpha

        self.gamma = 2.21e5           # m/(A\*s)

        # Start with free layer pinned (parallel)

        self.m = np.array([1.0, 0.0, 0.0])   # free layer (unit vector)

        self.m_pin = np.array([1.0, 0.0, 0.0])  # fixed reference layer

    def \_llg_step(self, H_eff, dt):

        '''Landau-Lifshitz-Gilbert step.'''

        m    = self.m

        mxH  = np.cross(m, H_eff)

        mxmxH = np.cross(m, mxH)

        dm_dt = -self.gamma / (1 + self.alpha\*\*2) \* (mxH + self.alpha \* mxmxH)

        self.m = m + dm_dt \* dt

        self.m /= np.linalg.norm(self.m)   # re-normalise

    def resistance(self):

        cos_theta = np.dot(self.m, self.m_pin)

        return self.RP + self.dR/2 \* (1 - cos_theta)

    def step(self, I, H_ext, dt=1e-12):

        '''

        I:     current through device (A) — causes Oersted + spin-transfer torque

        H_ext: external field array [Hx, Hy, Hz] in A/m

        '''

        # Anisotropy field (easy axis = x)

        H_anis = np.array([self.Hk \* self.m[0], 0.0, 0.0])

        # Spin-transfer torque field (simplified: proportional to I)

        H_stt  = np.array([0.0, I \* 1e6, 0.0])   # rough scaling

        H_eff  = H_ext + H_anis + H_stt

        self.\_llg_step(H_eff, dt)

        R  = self.resistance()

        V  = R \* I

        return V, R, self.m.copy()

# Example: field switching from +H to -H

gmr = GMRSpinResistor()

H_values = np.concatenate([np.linspace(2000, -2000, 500),

                            np.linspace(-2000, 2000, 500)])

R_curve = []

for H in H_values:

    for \_ in range(100):  # let it settle

        gmr.step(1e-3, np.array([H, 0, 0]), dt=1e-12)

    R_curve.append(gmr.resistance())

## Chapter 8 — Time-Domain Hybrid Components

## 8.1  Switched-Capacitor Resistor

Physical description: A capacitor connected by two switches. Every clock cycle, it transfers a packet of charge from one node to another. From the outside it looks like a resistor, but internally it is a sequence of discrete charge transfers (quantised by the clock). This is how switched-capacitor filters work.

**R_eff  =  1 / (f_clock · C)**
The current averaged over one clock cycle T = 1/f is:

**I_avg  =  C · (V1 - V2) · f_clock  =  (V1 - V2) / R_eff**
Per-cycle charge transfer:

**Delta_Q[k]  =  C · (V1[k\*T] - V2[k\*T])**
Between clock edges the output is sample-and-held at the last transferred charge.

## 8.2  Sample-Hold Capacitor

Physical description: A capacitor with a switch. When the switch closes (sample mode), V_out follows V_in. When it opens (hold mode), V_out freezes at the last sampled value. The sampling instants are discrete, the held voltage is continuous.

During sampling (switch closed, time constant tau = R_sw · C):

**V_out(t)  =  V_in  +  (V_out_prev - V_in) · exp(-(t - t_k) / tau)**
During hold (switch open):

**V_out(t)  =  V_out(t_k)   [constant until next sample]**
With non-ideal leakage (resistance R_leak across cap during hold):

**V_out(t)  =  V_sample · exp(-(t - t_k) / (R_leak · C))**
## 8.3  PWM Integrating Capacitor

A capacitor driven by a pulse-width modulated (PWM) signal with duty cycle D. The average voltage across the capacitor integrates towards the mean input:

**V_C(t)  =  V_CC · D  ·  (1  -  exp(-t / (RC)))     for constant D**
For time-varying D(t) (the general case):

**dV_C/dt  =  (V_CC · D(t)  -  V_C) / (R · C)**
## 8.4  Python Simulation

import numpy as np

# ── SWITCHED-CAPACITOR RESISTOR ─────────────────────────────────────────

def simulate_sc_resistor(V1_func, V2_func, C=1e-9, f_clock=1e6,

                          t_end=1e-4, dt=1e-9):

    R_eff = 1 / (f_clock \* C)

    T_clk = 1 / f_clock

    t = np.arange(0, t_end, dt)

    V1  = V1_func(t)

    V2  = V2_func(t)

    I_discrete = np.zeros_like(t)

    I_avg      = np.zeros_like(t)

    # Discrete charge transfer at each clock edge

    for k, tk in enumerate(np.arange(0, t_end, T_clk)):

        idx = int(tk / dt)

        if idx < len(t):

            dQ = C \* (V1[idx] - V2[idx])

            I_discrete[idx] = dQ / dt   # impulse of charge

    # Running average (RC filter on output)

    tau = T_clk \* 3

    for i in range(1, len(t)):

        I_avg[i] = I_avg[i-1] + (I_discrete[i] - I_avg[i-1]) \* dt/tau

    return t, I_discrete, I_avg, R_eff

# ── SAMPLE-HOLD CAPACITOR ───────────────────────────────────────────────

def simulate_sample_hold(V_in, t, f_sample, C=100e-12, R_sw=100,

                          R_leak=1e12):

    '''

    V_in:     input signal array

    t:        time array

    f_sample: sampling frequency (Hz)

    '''

    dt       = t[1] - t[0]

    tau_samp = R_sw \* C

    tau_hold = R_leak \* C

    T_samp   = 1 / f_sample

    V_out    = np.zeros_like(V_in)

    V_held   = 0.0

    t_last   = -T_samp

    in_hold  = False

    for i, ti in enumerate(t):

        # New sample event?

        if ti - t_last >= T_samp:

            V_held   = V_out[i-1] if i > 0 else V_in[0]

            t_last   = ti

            in_hold  = False

        if not in_hold:

            # Sampling: exponential approach to V_in

            V_out[i] = V_in[i] + (V_held - V_in[i]) \* np.exp(-(ti-t_last)/tau_samp)

            if (ti - t_last) > 5 \* tau_samp:   # settled enough

                V_held  = V_in[i]

                in_hold = True

                t_last  = ti

        else:

            # Hold: slow exponential decay (leakage)

            V_out[i] = V_held \* np.exp(-(ti - t_last) / tau_hold)

    return V_out

## Chapter 9 — Quantum Dot Array Resistor

Physical description: A chain of nanoscale semiconductor islands (quantum dots) in series. Each dot can hold only a specific number of electrons. Electrons must tunnel one at a time from dot to dot (Coulomb blockade). The net current depends on which discrete energy levels are available for transport, making this a fundamentally hybrid device.

## 9.1  Landauer-Büttiker Transmission Formula

The current through a quantum dot array is given by the Landauer formula. It sums over all quantum energy levels, weighting each by how easily it transmits electrons (the transmission coefficient T_n):

**I  =  (e/h) · integral T(E) · [f_L(E) - f_R(E)] dE**
Where f_L and f_R are Fermi-Dirac distributions on the left and right leads:

**f(E)  =  1 / (1 + exp((E - mu) / (k_B · T)))**
Each energy level n contributes a Lorentzian peak to T(E):

**T(E)  =  sum_n  [Gamma_n^2 / ((E - E_n)^2 + Gamma_n^2)]**
**E_n**
Energy of level n in the quantum dot (eV). Set by dot size and gate voltage.

**Gamma_n**
Level broadening — how strongly level n couples to leads. In eV.

**mu_L, mu_R**
Electrochemical potential of left and right leads. mu_L - mu_R = eV_bias.

**k_B**
Boltzmann constant = 8.617e-5 eV/K

## 9.2  Coulomb Blockade (Discrete Charging Energy)

Each dot has a geometric capacitance C_dot. Adding one electron costs energy:

**E_charge  =  e^2 / (2 · C_dot)**
The current is blocked (zero) until the bias exceeds this charging energy. The conductance resonances appear at:

**V_gate[N]  =  (N + 1/2) · e / C_gate     for N = 0, 1, 2, ...**
## 9.3  Python Simulation

import numpy as np

def fermi(E, mu, T_K=4.0, kB=8.617e-5):

    '''Fermi-Dirac distribution. E, mu in eV, T in Kelvin.'''

    x = (E - mu) / (kB \* T_K)

    return 1.0 / (1.0 + np.exp(np.clip(x, -500, 500)))

def transmission(E, levels, broadenings):

    '''

    T(E) = sum of Lorentzians for each energy level.

    levels:      array of level energies (eV)

    broadenings: array of Gamma values (eV)

    '''

    T = np.zeros_like(E)

    for En, Gn in zip(levels, broadenings):

        T += Gn\*\*2 / ((E - En)\*\*2 + Gn\*\*2)

    return T

def quantum_dot_current(V_bias, E_levels, Gammas, mu0=0.0, T_K=4.0,

                         E_min=-0.5, E_max=0.5, n_E=10000):

    '''

    Compute current through a quantum dot array vs V_bias.

    Uses Landauer-Buttiker formula.

    '''

    e  = 1.602e-19  # C

    h  = 6.626e-34  # J\*s

    eV_to_J = e

    E  = np.linspace(E_min, E_max, n_E)  # energy grid in eV

    dE = E[1] - E[0]

    I  = np.zeros_like(V_bias)

    for i, V in enumerate(V_bias):

        mu_L = mu0 + V/2

        mu_R = mu0 - V/2

        T    = transmission(E, E_levels, Gammas)

        fL   = fermi(E, mu_L, T_K)

        fR   = fermi(E, mu_R, T_K)

        # Integrate: current in Amps

        I[i] = (e/h) \* np.sum(T \* (fL - fR)) \* dE \* eV_to_J

    return I

# Example: Single quantum dot with Coulomb blockade

V_bias = np.linspace(-0.05, 0.05, 1000)   # 50 mV sweep

# Energy levels tuned by gate: two levels near Fermi

E_levels  = np.array([-0.01, 0.01, 0.03])  # eV

Gammas    = np.array([0.002, 0.002, 0.002]) # eV broadening

I_QD = quantum_dot_current(V_bias, E_levels, Gammas)

# Coulomb blockade: charging energy gaps

C_dot = 1e-18   # 1 aF

E_c   = (1.602e-19)\*\*2 / (2 \* C_dot) / 1.602e-19  # in eV ~0.08 eV

print(f'Charging energy E_c = {E_c\*1000:.1f} meV')

*💡 The Coulomb blockade means current is ZERO until the gate voltage is tuned to a resonance. This creates discrete conductance peaks — a completely digital-looking output from a continuous physical process. This is the purest example of the discrete-continuous hybrid in nature.*

## Chapter 10 — Fractal Components: Koch Inductor & Sierpinski Capacitor

Physical description: Wire bent into a fractal shape (Koch snowflake for the inductor, Sierpinski triangle for the capacitor). The self-similar geometry creates resonances at a discrete set of frequencies forming a geometric series, while the electromagnetic response between resonances is smoothly continuous.

## 10.1  Koch Fractal Inductor — Length and Inductance

The Koch curve replaces each line segment with 4 segments each 1/3 the length. After n iterations:

**L_wire(n)  =  L_0 · (4/3)^n     [Total wire length]**
The self-resonant frequencies follow a geometric sequence with ratio 3:

**f_res(k)  =  f_0 / (3/4)^k  =  f_0 · (4/3)^k     k = 0, 1, 2, ...**
The inductance of a straight wire of length l, radius r, in free space:

**L_wire  =  (mu_0 / 2\*pi) · l · [ln(2l/r) - 3/4]**
After n Koch iterations, substitute l = L_0 \* (4/3)^n:

**L_Koch(n)  =  (mu_0/2\*pi) · L_0·(4/3)^n · [ln(2\*L_0\*(4/3)^n / r) - 3/4]**
## 10.2  Sierpinski Capacitor — Fractal Dimension and Capacitance

The Sierpinski triangle removes triangular holes from a metal plate. After n iterations, the remaining area fraction is:

**A_n  =  A_0 · (3/4)^n**
The capacitance scales with area:

**C_n  =  epsilon_0 · epsilon_r · A_n / d  =  C_0 · (3/4)^n**
But the effective fringe capacitance from the fractal edges scales with the perimeter:

**P_n  =  P_0 · (3/2)^n     [Perimeter grows with fractal dimension D = log3/log2 ~ 1.585]**
**C_fringe(n)  ≈  epsilon_0 · P_n · d_fringe**
The total capacitance is a sum of plate and fringe components — a characteristic signature of fractal geometry.

## 10.3  Frequency-Domain Response (Multi-Resonant Spectrum)

The fractal inductor in a circuit with capacitance C_par produces resonances at:

**omega_res(k)  =  1 / sqrt(L_Koch(n) · (3/4)^k · C_par)  for k = 0, 1, 2, ..., n**
## 10.4  Python Simulation

import numpy as np

def koch_inductance(n_iter, L0=0.1, r=0.5e-3, mu0=4\*np.pi\*1e-7):

    '''

    Inductance of Koch fractal inductor.

    n_iter: number of Koch iterations (0=straight wire)

    L0:     initial wire length (m)

    r:      wire radius (m)

    Returns: inductance in Henries

    '''

    l_eff = L0 \* (4/3)\*\*n_iter

    L = (mu0 / (2\*np.pi)) \* l_eff \* (np.log(2\*l_eff/r) - 0.75)

    return L

def koch_resonances(n_iter, L0=0.1, r=0.5e-3, C_par=1e-12):

    '''Returns array of self-resonant frequencies.'''

    f_res = []

    for k in range(n_iter+1):

        L_k = koch_inductance(k, L0, r)

        f_k = 1 / (2\*np.pi\*np.sqrt(L_k \* C_par))

        f_res.append(f_k)

    return np.array(f_res)

def sierpinski_capacitance(n_iter, A0=1e-4, d=1e-3, eps_r=4.5):

    '''

    Capacitance of Sierpinski triangle capacitor.

    A0: initial plate area (m^2)

    d:  dielectric thickness (m)

    eps_r: relative permittivity

    '''

    eps0 = 8.854e-12

    A_n  = A0 \* (3/4)\*\*n_iter

    C_plate  = eps0 \* eps_r \* A_n / d

    # Fringe: rough estimate, perimeter grows as (3/2)^n

    P0   = np.sqrt(3) \* A0\*\*0.5  # equilateral triangle

    P_n  = P0 \* (3/2)\*\*n_iter

    C_fringe = eps0 \* P_n \* d \* 0.1    # crude fringe model

    return C_plate + C_fringe

def fractal_impedance_spectrum(freqs, n_iter, L0=0.1, C_par=1e-12, R_loss=1.0):

    '''Compute Z(f) for Koch inductor with parallel capacitance.'''

    Z = np.zeros(len(freqs), dtype=complex)

    for k in range(n_iter+1):

        L_k = koch_inductance(k, L0)

        # Each iteration adds a series RLC branch

        for f in range(len(freqs)):

            omega = 2\*np.pi\*freqs[f]

            Z_branch = R_loss + 1j\*omega\*L_k + 1/(1j\*omega\*C_par)

            Z[f] += 1/Z_branch

    return 1/Z

# Print resonance frequencies for 4-iteration Koch inductor

f_res = koch_resonances(4)

for k, f in enumerate(f_res):

    print(f'Resonance k={k}: {f/1e6:.2f} MHz')

## Chapter 11 — Phase-Change Resistors (GST Chalcogenides)

Physical description: Germanium-Antimony-Telluride (GST) alloy. This material has two stable phases: amorphous (disordered, high resistance ~1 MOhm) and crystalline (ordered, low resistance ~1 kOhm). The phase can be switched with a voltage pulse — a fast/short pulse amorphises it (RESET), a longer/lower pulse crystallises it (SET). Between these discrete phase states, the resistance is a continuous analog quantity during the phase transition itself.

## 11.1  The Johnson-Kolmogorov-Avrami-Mehl (JKAM) Crystallisation Model

The fraction of material crystallised, xi, follows the JKAM equation during the transition:

**xi(t)  =  1  -  exp(-K_0 · exp(-E_a/(k_B·T)) · t^n_Avrami)**
**K_0**
Pre-exponential rate constant. ~10^26 s^(-n) for GST

**E_a**
Activation energy for crystallisation. ~2.2 eV for GST

**n_Avrami**
Avrami exponent: 3D growth n=4, 2D growth n=3. ~2.5 for thin films.

**xi**
Crystallised fraction in [0,1]. xi=0 amorphous, xi=1 fully crystal.

## 11.2  Resistance-Temperature Relation

The total resistance combines amorphous and crystalline contributions via the phase fraction:

**R(xi, T)  =  R_cryst(T)^xi  ·  R_amorph(T)^(1-xi)**
Each phase has its own temperature dependence:

**R_amorph(T)  =  R_a0 · exp(+E_cond_a / (k_B·T))   [semiconducting, R rises as T falls]**
**R_cryst(T)   =  R_c0 · (1 + TCR · (T - T_0))        [metallic, R rises as T rises]**
## 11.3  Thermal Model (Self-Heating)

The device heats itself through Joule heating. Temperature evolves according to:

**C_th · dT/dt  =  P_joule  -  (T - T_amb) / R_th**
**P_joule  =  I^2 · R(xi, T)**
## 11.4  Python Simulation

import numpy as np

class PhaseChangeResistor:

    def \_\_init\_\_(self, Ra0=1e6, Rc0=1e3, Ea_cond=0.4, TCR=2e-3,

                 K0=1e26, Ea_cryst=2.2, n_av=2.5,

                 C_th=1e-12, R_th=1e5, T_amb=300):

        self.Ra0, self.Rc0   = Ra0, Rc0

        self.Ea_cond, self.TCR = Ea_cond, TCR

        self.K0, self.Ea_cryst, self.n_av = K0, Ea_cryst, n_av

        self.C_th, self.R_th  = C_th, R_th

        self.T_amb = T_amb

        self.kB    = 8.617e-5   # eV/K

        # State variables

        self.xi  = 0.0    # start amorphous

        self.T   = T_amb

        self.t_crystal = 0.0   # time in crystallising phase

    def R_amorph(self):

        return self.Ra0 \* np.exp(self.Ea_cond / (self.kB \* self.T))

    def R_cryst(self):

        return self.Rc0 \* (1 + self.TCR \* (self.T - 300))

    def resistance(self):

        Ra = self.R_amorph()

        Rc = self.R_cryst()

        return Ra\*\*(1 - self.xi) \* Rc\*\*self.xi

    def step(self, I, dt):

        R    = self.resistance()

        V    = R \* I

        P    = I\*\*2 \* R

        # Thermal dynamics

        dT   = (P - (self.T - self.T_amb)/self.R_th) / self.C_th

        self.T = max(self.T_amb, self.T + dT\*dt)

        # Crystallisation (only if T > 400 K and currently partially amorphous)

        if self.T > 400 and self.xi < 1.0:

            self.t_crystal += dt

            rate = self.K0 \* np.exp(-self.Ea_cryst/(self.kB\*self.T))

            self.xi = max(self.xi, 1 - np.exp(-rate \* self.t_crystal\*\*self.n_av))

        # RESET: rapid heating above T_melt amorphises

        if self.T > 900:

            self.xi = 0.0

            self.t_crystal = 0.0

        return V, R, self.xi, self.T

# Simulate SET pulse (long, low current)

pcr = PhaseChangeResistor()

t   = np.arange(0, 500e-9, 0.5e-9)    # 500 ns window

I_pulse = np.where((t > 10e-9) & (t < 300e-9), 1e-3, 0)  # 1 mA SET pulse

results = [pcr.step(I_pulse[i], 0.5e-9) for i in range(len(t))]

xi_arr = [r[2] for r in results]

## Chapter 12 — Piezo-Quantum Capacitor

Physical description: A piezoelectric crystal sandwiched with a quantum well semiconductor. Mechanical strain (continuous) shifts the quantum well energy levels (discrete). The energy level shifts change the density of available charge states and thus the capacitance. One physical effect with two outputs — both continuous (strain) and discrete (level crossings).

## 12.1  Quantum Well Energy Levels Under Strain

For an infinite square quantum well of width L_QW, the energy levels are:

**E_n  =  (hbar^2 \* pi^2 \* n^2) / (2 \* m\* \* L_QW^2)     n = 1, 2, 3, ...**
Under applied strain eps (from piezoelectric effect), the well width shifts as:

**L_QW(eps)  =  L_QW0 \* (1 + eps)**
And there is an additional deformation potential energy shift:

**delta_E_n(eps)  =  a_c \* eps + b \* (eps_xx - eps_zz)**
So the level energies under strain are:

**E_n(eps)  =  E_n0 / (1 + eps)^2  +  a_c \* eps**
## 12.2  Strain-Dependent Capacitance

The capacitance is the derivative of stored charge with voltage. Near a quantum level E_n, the charge density has a sharp increase (subband filling). The total capacitance is:

**C(V, eps)  =  C_geom  +  C_quantum(V, eps)**
**C_quantum  =  e^2 \* rho_2D  \*  sum_n  Theta(mu(V) - E_n(eps))**
Where rho_2D = m\*/(pi\*hbar^2) is the 2D density of states per subband, Theta is the Heaviside step (a subband contributes only when Fermi energy mu is above it), and mu(V) = mu_0 + eV.

## 12.3  Python Simulation

import numpy as np

def piezo_quantum_cap(V_array, eps_mech, L_QW0=10e-9, m_eff=0.067\*9.11e-31,

                       C_geom=50e-15, A_area=100e-12, n_levels=5,

                       a_c=-5.0, T=300):

    '''

    V_array:  voltage sweep (V)

    eps_mech: mechanical strain from piezo (dimensionless, e.g. 0.001 = 0.1%)

    L_QW0:    unstrained quantum well width (m)

    m_eff:    effective mass (kg). GaAs = 0.067 me

    Returns:  C(V) array in Farads

    '''

    hbar  = 1.055e-34

    e_q   = 1.602e-19

    kB    = 1.381e-23

    # Quantum well levels under strain

    L_eff = L_QW0 \* (1 + eps_mech)

    E0_n  = [(hbar\*np.pi\*n)\*\*2 / (2\*m_eff\*L_QW0\*\*2) / e_q  # eV

             for n in range(1, n_levels+1)]

    E_n   = np.array([E / (1 + eps_mech)\*\*2 + a_c\*eps_mech for E in E0_n])

    print(f'Energy levels under strain={eps_mech}: {[f"{e:.4f}" for e in E_n]} eV')

    # 2D density of states per subband (constant)

    rho2D = m_eff / (np.pi \* hbar\*\*2)  # states/(m^2 \* J)

    rho2D_eV = rho2D \* e_q / A_area

    # C(V) calculation

    C_total = np.zeros_like(V_array)

    for i, V in enumerate(V_array):

        mu = V   # Fermi level shift = eV (referenced to 0)

        # Quantum capacitance: sum over subbands below Fermi level

        # Use Fermi-Dirac for finite T

        C_q = 0.0

        for En in E_n:

            x = (mu - En) / (kB\*T/e_q)

            f = 1/(1 + np.exp(-np.clip(x, -500, 500)))

            C_q += e_q\*\*2 \* rho2D_eV \* f

        C_total[i] = C_geom + C_q

    return C_total

# Simulate: voltage sweep at different strain levels

V = np.linspace(-0.5, 0.5, 1000)

C_zero_strain = piezo_quantum_cap(V, eps_mech=0.0)

C_strained    = piezo_quantum_cap(V, eps_mech=0.002)

# Discrete jumps visible at each subband crossing

## Chapter 13 — Quantum Hall Resistor

Physical description: A 2D electron gas (electrons confined to a surface) in a strong perpendicular magnetic field at low temperature. The Hall resistance — the voltage transverse to current divided by that current — takes on exactly quantised values. This is one of the most precisely quantised phenomena in all of physics, used to define the Ohm itself.

## 13.1  The Quantised Hall Resistance

**R_H  =  h / (nu · e^2)  =  25812.807 / nu   Ohms**
Where nu (the filling factor) is an integer and h/e^2 = 25812.807... Ohm is the von Klitzing constant R_K. Current flow is continuous and lossless (zero longitudinal resistance R_xx = 0) along the edge.

## 13.2  Filling Factor as a Function of Field

**nu(B)  =  n_2D · h / (e · B)**
Where n_2D is the 2D electron density. As the magnetic field increases, nu decreases. Whenever nu crosses an integer, a new Landau level empties and R_H jumps to the next plateau value.

## 13.3  Broadened Plateau Model for Simulation

Real devices have disorder, which broadens the plateaux. A smooth model for R_H as a function of B uses a sum of arctangent transitions:

**R_H(B)  =  R_K · sum_nu  [ arctan((nu(B) - nu) / delta_nu) / pi  +  1/2 ]  \*  (1/nu - 1/(nu+1))**
## 13.4  Python Simulation

import numpy as np

def quantum_hall_resistance(B_field, n_2D=2e15, delta_nu=0.05, T=1.0,

                              nu_max=8):

    '''

    Simulate Quantum Hall resistance vs magnetic field.

    B_field: array of B values (Tesla)

    n_2D:    2D electron density (m^-2)

    delta_nu: plateau width (disorder broadening)

    T:       temperature (K) -- affects plateau sharpness

    '''

    h  = 6.626e-34

    e  = 1.602e-19

    RK = h / e\*\*2   # 25812.807 Ohm

    # Filling factor

    nu_B = n_2D \* h / (e \* np.abs(B_field) + 1e-10)

    R_H  = np.zeros_like(B_field)

    R_xx = np.zeros_like(B_field)

    for i, nu_val in enumerate(nu_B):

        # Find nearest integer filling factor

        nu_int = int(round(nu_val))

        nu_int = max(1, min(nu_max, nu_int))

        # Smooth step to plateau: tanh broadening

        dist   = (nu_val - nu_int) / delta_nu

        weight = 0.5 \* (1 + np.tanh(dist))   # 0=lower plateau, 1=upper plateau

        if nu_int >= nu_max:

            R_H[i] = RK / nu_int

        else:

            R_H[i] = RK \* (weight/nu_int + (1-weight)/(nu_int+1))

        # Longitudinal resistance: peaks between plateaux, zero on plateau

        R_xx[i] = RK \* np.exp(-dist\*\*2 / 2) \* 0.001   # small activated resistance

    return R_H, R_xx

# Simulate field sweep from 0 to 15 Tesla

B = np.linspace(0.1, 15, 10000)

R_H, R_xx = quantum_hall_resistance(B, n_2D=3e15)

print(f'Plateau values (Ohm): {25812.8/np.array([1,2,3,4,5])}')

## Chapter 14 — Integrate-and-Fire Components (Neuron-Inspired)

Physical description: A device that integrates incoming current continuously until an internal variable reaches a threshold, then fires (discrete spike) and resets. This is exactly how biological neurons work. It is the simplest possible hybrid component — one continuous variable (voltage), one discrete event (spike), one threshold (the guard condition).

## 14.1  The Leaky Integrate-and-Fire (LIF) Model

**C_m · dV/dt  =  -V/R_m  +  I_input(t)**
Guard condition (discrete event):

**WHEN  V >= V_threshold:   V -> V_reset   AND  emit spike**
**C_m**
Membrane capacitance. Sets how quickly voltage changes. ~1 nF for a component.

**R_m**
Membrane resistance (leak). Sets the time constant tau = R_m \* C_m.

**V_threshold**
Threshold voltage. When V crosses this, the component fires.

**V_reset**
Reset voltage after firing. Usually V_reset < V_threshold.

**tau = R_m\*C_m**
Time constant — how quickly V decays back to rest.

## 14.2  Adaptive Exponential (AdEx) Model — More Realistic

The AdEx model adds a subthreshold resonance (exponential term) and adaptation (variable w that increases with each spike):

**C · dV/dt  =  -g_L·(V-E_L)  +  g_L·DT·exp((V-V_T)/DT)  -  w  +  I**
**tau_w · dw/dt  =  a·(V - E_L)  -  w**
When V >= V_peak: V -> V_reset, w -> w + b (spike + adaptation increment)

## 14.3  Python Simulation (GPU-Ready)

import numpy as np

import torch

# ── LIF (CPU) ────────────────────────────────────────────────────────────

def simulate_lif(I_input, dt=1e-4, Cm=1e-9, Rm=1e7,

                  V_thresh=0.02, V_reset=-0.07, V_rest=-0.07):

    '''

    I_input: array of input current (A)

    dt:      timestep (s)

    Returns: V(t), spike_times

    '''

    V = V_rest

    V_hist   = np.zeros(len(I_input))

    spikes   = []

    for i, I in enumerate(I_input):

        dV  = (-V/Rm + I) / Cm

        V   = V + dV \* dt

        if V >= V_thresh:

            spikes.append(i \* dt)

            V = V_reset

        V_hist[i] = V

    return V_hist, np.array(spikes)

# ── LIF GPU (N neurons in parallel) ─────────────────────────────────────

def simulate_lif_gpu(I_batch, dt=1e-4, Cm=1e-9, Rm=1e7,

                      V_thresh=0.02, V_reset=-0.07):

    '''

    I_batch: shape (T, N) - T timesteps, N parallel neurons

    Returns: V shape (T, N), spike_count shape (N,)

    '''

    device = I_batch.device

    N = I_batch.shape[1]

    V = torch.ones(N, device=device) \* (-0.07)   # rest potential

    V_hist     = torch.zeros_like(I_batch)

    spike_count = torch.zeros(N, device=device)

    for t in range(I_batch.shape[0]):

        dV = (-V/Rm + I_batch[t]) / Cm

        V  = V + dV \* dt

        # Vectorised threshold check and reset

        fired = (V >= V_thresh)

        spike_count += fired.float()

        V = torch.where(fired, torch.ones_like(V) \* V_reset, V)

        V_hist[t] = V

    return V_hist, spike_count

# Example: 10,000 neurons with different input currents

T_steps = 1000

N_neurons = 10_000

I_batch = torch.rand(T_steps, N_neurons, device='cuda') \* 3e-9

V_hist, n_spikes = simulate_lif_gpu(I_batch)

print(f'Mean spike rate: {n_spikes.mean().item() / (T_steps\*1e-4):.1f} Hz')

## Chapter 15 — GPU Acceleration: Unified Strategy

This chapter explains the general principles for running any of the models above at massive scale on a GPU. GPUs are ideal for these hybrid simulations because they can execute the same operation on millions of numbers in parallel.

## 15.1  Why GPUs Suit Hybrid Simulations

**Vectorised ODEs**
The same differential equation for all N instances, different initial conditions/parameters. 1 GPU can replace 1000 CPU cores.

**Monte Carlo**
Run N=10^6 realisations of a stochastic component to get full distributions rather than single trajectories.

**Parameter sweeps**
Sweep R, C, L, barrier height, etc. simultaneously — get a full map in one GPU run.

**Neural training**
Differentiable models (PyTorch autograd) allow gradients to flow back through the physics, enabling circuit-level learning.

**Real-time**
For dt=1ns and 1024 components, a GPU can run 1000x real-time — perfect for interactive design tools.

## 15.2  Differentiable Physics (Autograd)

Any model written in PyTorch with no in-place operations is automatically differentiable. This means you can compute d(output)/d(parameter) with one backward() call:

import torch

# Make parameters differentiable

d_barrier = torch.tensor(2e-9, requires_grad=True)

phi_bar   = torch.tensor(3.0,  requires_grad=True)

# Run simulation

V = torch.linspace(-0.5, 0.5, 1000)

I = simmons_gpu(V, d=d_barrier, phi_bar=phi_bar)  # uses torch ops

# Compute gradient of total current power w.r.t. barrier thickness

P_total = (I \* V).sum()

P_total.backward()

print(f'd(Power)/d(barrier_thickness) = {d_barrier.grad:.2e}')

# This enables inverse design: find barrier thickness that gives target R

# Using gradient descent:

optimizer = torch.optim.Adam([d_barrier], lr=1e-11)

R_target = 5e5   # target 500 kOhm

for step in range(500):

    optimizer.zero_grad()

    I_pred = simmons_gpu(torch.tensor(0.1), d=d_barrier, phi_bar=phi_bar)

    R_pred = 0.1 / (I_pred + 1e-30)

    loss   = (R_pred - R_target)\*\*2

    loss.backward()

    optimizer.step()

    d_barrier.data.clamp\_(0.5e-9, 5e-9)   # physical bounds

print(f'Optimal barrier thickness: {d_barrier.item()\*1e9:.2f} nm')

## 15.3  Batch Simulation Template (Universal)

import torch

from dataclasses import dataclass

from typing import Callable

@dataclass

class HybridComponentGPU:

    '''Universal GPU framework for any hybrid component.'''

    f:        Callable   # continuous dynamics: (x, s, u) -> dx_dt

    G:        Callable   # guard function: (x, s, u) -> bool tensor

    T_func:   Callable   # transition: (s, x, u) -> s_new

    n_vars:   int        # number of continuous state variables

    n_states: int        # number of discrete states

    def run(self, x0: torch.Tensor, s0: torch.Tensor,

            u_seq: torch.Tensor, dt: float) -> dict:

        '''

        x0:    (N, n_vars)   initial continuous state

        s0:    (N,)          initial discrete state (int)

        u_seq: (T, N)        input sequence

        dt:    float         timestep

        '''

        device = x0.device

        x = x0.clone()

        s = s0.clone()

        x_log, s_log = [x.clone()], [s.clone()]

        for t in range(u_seq.shape[0]):

            u  = u_seq[t]

            # Runge-Kutta 4th order (more accurate than Euler)

            k1 = self.f(x,           s, u)

            k2 = self.f(x + dt/2\*k1, s, u)

            k3 = self.f(x + dt/2\*k2, s, u)

            k4 = self.f(x + dt\*k3,   s, u)

            x  = x + dt/6 \* (k1 + 2\*k2 + 2\*k3 + k4)

            # Check discrete transitions

            guard = self.G(x, s, u)

            s     = torch.where(guard, self.T_func(s, x, u), s)

            x_log.append(x.clone())

            s_log.append(s.clone())

        return {'x': torch.stack(x_log), 's': torch.stack(s_log)}

## 15.4  Performance Reference

## 1 CPU core

~10^6 ODE steps per second (simple scalar ODE)

**RTX 3090 GPU**
~10^11 float32 ops/sec -> ~10^9 ODE steps/sec for N=10^3 batch

**A100 GPU**
~3x10^11 ops/sec, FP16 tensor cores: up to 10^12 for simple kernels

**Speedup rule of thumb**
For N > 1000 independent components, GPU typically 100-1000x faster than CPU

**Memory limit**
A100: 80 GB. Each component with 10 float32 vars = 40 bytes. Fit 2x10^9 state vars.

**Recommended dt**
ODE stability: dt < tau_min/10 where tau_min is the fastest time constant in system

## Chapter 16 — Complete Worked Example: Mixed Circuit Simulation

This chapter shows how to combine multiple hybrid components into a single circuit and simulate it on a GPU. The example circuit is: Josephson Junction Inductor in series with a Memristor, driven by an AC current, with a GMR Spin Resistor in parallel.

## 16.1  Circuit Equations (Kirchhoff's Laws)

For a series connection of impedances Z_JJ (Josephson) and Z_Memristor with parallel Z_GMR:

**V_total  =  V_JJ(phi, I)  +  V_mem(w, I)**
**I_GMR    =  V_total / R_GMR(theta)**
**I_source =  I_JJ  +  I_GMR**
## 16.2  Full Coupled ODE System

State vector: x = [phi, w, theta_m1, theta_m2, theta_m3]  (5 continuous variables)

Discrete states: s = [n_flux, s_binary_memristor, m1_state, m2_state]

import numpy as np

import torch

class MixedCircuit:

    '''

    Series: Josephson Junction + Dual-Mode Memristor

    Parallel: GMR Spin Resistor

    '''

    def \_\_init\_\_(self):

        # JJ params

        self.Ic   = 10e-6

        self.hbar = 1.055e-34

        self.e_q  = 1.602e-19

        self.Phi0 = 2.067e-15

        self.R_JJ = 50.0

        self.C_JJ = 1e-15

        self.phi  = 0.0

        self.dphi = 0.0

        # Memristor params

        self.Ron, self.Roff, self.D = 100, 16000, 10e-9

        self.mu_v = 1e-14

        self.w   = 5e-9

        # GMR params

        self.RP, self.RAP = 100, 112

        self.theta_mag = 0.0

        self.omega_prec = 2\*np.pi \* 5e9   # precession freq

        # Discrete state

        self.n_flux = 0

    def step(self, I_source, dt):

        # ── JOSEPHSON JUNCTION ──

        I_JJ  = self.Ic \* np.sin(self.phi)

        V_JJ  = (self.hbar/(2\*self.e_q)) \* self.dphi

        # RCSJ current balance

        d2phi = (2\*self.e_q/self.hbar) \* (I_source - I_JJ

                  - V_JJ/self.R_JJ) / self.C_JJ

        self.dphi += d2phi \* dt

        self.phi  += self.dphi \* dt

        # Discrete flux tracking

        self.n_flux = int(round(self.phi / (2\*np.pi)))

        # ── MEMRISTOR ──

        R_mem = (self.Ron\*(self.w/self.D)

                \+ self.Roff\*(1 - self.w/self.D))

        I_mem = (I_source \* R_mem) / (R_mem + 0.001)  # approx

        V_mem = R_mem \* I_source

        win   = 1 - (2\*self.w/self.D - 1)\*\*2

        self.w = np.clip(self.w

                         \+ self.mu_v\*(self.Ron/self.D\*\*2)\*I_source\*win\*dt,

                         0, self.D)

        # ── GMR (parallel) ──

        V_total = V_JJ + V_mem

        self.theta_mag += self.omega_prec \* dt \* 0.01  # simplified

        R_GMR = self.RP + (self.RAP-self.RP)/2\*(1 - np.cos(self.theta_mag))

        I_GMR = V_total / R_GMR

        return {'V': V_total, 'R_mem': R_mem, 'R_GMR': R_GMR,

                'phi': self.phi, 'n_flux': self.n_flux, 'w': self.w}

# Run the mixed circuit

ckt = MixedCircuit()

t   = np.arange(0, 10e-9, 1e-12)

I_ac = 9e-6 \* np.sin(2\*np.pi\*5e9\*t)

results = [ckt.step(I_ac[i], 1e-12) for i in range(len(t))]

V_out   = np.array([r['V'] for r in results])

n_flux  = np.array([r['n_flux'] for r in results])

## Chapter 17 — Summary: All Models at a Glance

This table provides a complete reference for every component, its governing equation, discrete mechanism, and simulation approach.

**Component**
**Key Equation**
**Discrete Mechanism**
**Continuous Variable**
**Python Class / Function**
QTR

J = J0[(phi-V/2)e^(-A√(phi-V/2)) - ...]

Poisson tunnel events

Macroscopic current I

simmons_current()

Mag Domain Inductor

dM/dH = (1-c)(Man-M)/(k·delta-alpha(Man-M)) + c·dMan/dH

Barkhausen domain flips

Inductance L(H)

MagneticDomainInductor

Memristor

dw/dt = mu_v·(Ron/D²)·I·f(w)

Binary oxide film flip

Analog w (doping width)

Memristor, DualModeMemristor

Memcapacitor

I = C(phi)·dV/dt + V²·dC/dphi

Trapped charge states

phi = integral V dt

Memcapacitor

Meminductor

V = L(q)·dI/dt + I²·dL/dq

Domain wall pinning

q = integral I dt

Meminductor

Brownian Resistor

dR = -gamma(R-Rn)dt + sigma·dW

Markov state jumps

R(t) random walk

BrownianResistor

Josephson Junction

dphi/dt = 2eV/hbar, I = Ic·sin(phi)

Flux quanta n·Phi0

Phase phi (continuous)

JosephsonJunction

GMR Spin Resistor

R = RP + dR/2·(1-m1·m2)

Stoner-Wohlfarth switching

LLG magnetisation m

GMRSpinResistor

Switched Cap

R_eff = 1/(f·C)

Clock edge charge transfer

Averaged current I_avg

simulate_sc_resistor()

Sample-Hold Cap

V = V_in·(1-exp(-t/tau))

Discrete sample instants

Held voltage V_hold

simulate_sample_hold()

QD Array Resistor

I = (e/h)·integral T(E)·(fL-fR)dE

Coulomb blockade steps

Lorentzian T(E)

quantum_dot_current()

Fractal Inductor

L_n = L0·(4/3)^n·[ln(2L/r)-0.75]

Discrete resonances f0·(4/3)^k

L(f) between resonances

koch_inductance()

Phase-Change R

xi = 1-exp(-K0·exp(-Ea/kBT)·t^n)

Amorphous/Crystal phase

R(xi, T) continuous

PhaseChangeResistor

Piezo-Quantum Cap

C = C_geo + e²·rho2D·sum f(mu-En)

Subband level crossings

C(V, eps) smooth

piezo_quantum_cap()

Quantum Hall R

R_H = h/(nu·e²)

Integer Landau levels nu

Current flow continuous

quantum_hall_resistance()

Integrate-and-Fire

C·dV/dt = -V/R + I

Spike when V > V_thresh

Membrane voltage V(t)

simulate_lif(), simulate_lif_gpu()

# Appendix — Constants and Unit Conversions

**e (electron charge)**
1.602176634 × 10^-19 C

**hbar (reduced Planck)**
1.054571817 × 10^-34 J·s

**h (Planck constant)**
6.626070040 × 10^-34 J·s

**m_e (electron mass)**
9.109383702 × 10^-31 kg

**mu_0 (permeability)**
1.256637 × 10^-6 H/m

**epsilon_0 (permittivity)**
8.854187817 × 10^-12 F/m

**k_B (Boltzmann)**
1.380649 × 10^-23 J/K  =  8.617333 × 10^-5 eV/K

**Phi_0 (flux quantum)**
2.067833848 × 10^-15 Wb  =  h/(2e)

**R_K (von Klitzing)**
25812.807 Ohm  =  h/e^2

## 1 eV in Joules

1.602 × 10^-19 J

## 1 nm

1 × 10^-9 m

## 1 ps

1 × 10^-12 s

## 1 fF (femtofarad)

1 × 10^-15 F

## 1 pH (picohenry)

1 × 10^-12 H

*End of Document  —  All formulas derived from first-principles physics*
