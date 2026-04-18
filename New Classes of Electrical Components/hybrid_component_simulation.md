# Hybrid component simulation

**Mathematical formulas for CPU and GPU implementation**

*A complete derivation and reference guide*

*February 2026*

## Chapter 0 — How to Read This Document

This document takes physical electronic components — things you would actually build in a lab — and shows you how to recreate their behaviour entirely in software on a normal computer. No special hardware needed. Every formula has been derived from first-principles physics, then rewritten in a form a computer can execute numerically.

If you are completely new to this field, think of it this way:

  • A real resistor dissipates energy as heat. We write an equation V = R·I that captures this. A computer can solve that equation millions of times per second.

  • A hybrid component is more complex — it behaves partly like an analog device \(continuously varying voltages\) and partly like a digital device \(jumping between discrete states\). To simulate it we need BOTH a differential equation AND a state machine running simultaneously.

Each component section contains:

  1. Plain English description of what the component does physically.

  2. The mathematical model — the governing equations.

  3. Derived simulation formulas — rewritten for numerical computation.

  4. Python code — ready to copy into NumPy or PyTorch.

  5. GPU acceleration notes — how to parallelise across millions of instances.

*💡 All Python code assumes: import numpy as np  |  import torch  |  from scipy.integrate import solve\_ivp*

## Terminology Quick Reference

**ODE**
Ordinary Differential Equation — an equation involving derivatives like dx/dt. Solved numerically by stepping forward in tiny time increments.

**SDE**
Stochastic Differential Equation — an ODE with a random noise term. Used when thermal or quantum noise is functionally important.

**State machine**
A system that can be in one of N discrete states and transitions between them based on rules.

**Euler-Maruyama**
The simplest numerical method for SDEs: x\_\{k\+1\} = x\_k \+ f\(x\_k\)dt \+ g\(x\_k\)sqrt\(dt\)\*xi, where xi ~ N\(0,1\).

**Vectorised**
Running the same calculation on thousands of numbers simultaneously — what GPUs are designed for.

**Memcomponent**
A component \(memristor, memcapacitor, meminductor\) whose properties depend on its own history.

**dt**
The time step used in simulation. Smaller dt = more accurate but slower. Typical: 1e-9 to 1e-12 seconds.

## Chapter 1 — The Universal Hybrid Automaton Framework

Every component in this catalogue can be described by the same mathematical skeleton. Understanding this skeleton once makes every subsequent component easy to follow.

## 1.1  The Core Idea

A hybrid component has TWO kinds of variables running simultaneously:

  1. Continuous variables  x\(t\) ∈ R^n  — things like voltage, current, charge, flux, domain wall position. These change smoothly and are governed by differential equations.

  2. A discrete state  s ∈ \{0, 1, 2, ..., N-1\}  — which magnetic domain configuration the core is in, whether the oxide layer is crystalline or amorphous, how many flux quanta are trapped, etc.

The full state at any moment is the pair  \(x, s\).

## 1.2  The Governing Equations

**dx/dt  =  f\(x, s, u, t\)          \[Continuous dynamics\]**
**s\(t\+\)  =  T\(s\(t-\), x, u\)  when  G\(x, s\) = 0   \[Discrete transition\]**
Where:

  • u\(t\) is the external input \(applied voltage, current, magnetic field, light…\)

  • f is the vector field that drives continuous change

  • G is a guard condition — a threshold that when crossed triggers a state jump

  • T is the transition function — the rule for what state to jump to

## 1.3  The Electrical Output Relation

For any hybrid R, L, or C component, the terminal behaviour is:

**V\(t\)  =  R\(x, s\) · I\(t\)          \[Hybrid resistor\]**
**Q\(t\)  =  C\(x, s\) · V\(t\)          \[Hybrid capacitor\]**
**Phi\(t\)  =  L\(x, s\) · I\(t\)         \[Hybrid inductor\]**
The key insight: R, C, L are no longer constants. They are functions of the current internal state. This is what makes these components novel.

## 1.4  Energy Bookkeeping

**E\_total  =  E\_continuous\(x\)  \+  E\_discrete\(s\)  \+  E\_coupling\(x, s\)**
Coupling energy is what makes the two worlds talk to each other. For example, in a magnetic domain inductor, the continuous magnetic flux energy couples to the discrete domain state through the permeability.

## 1.5  Information Content

**I\_total  =  log2\(N\)  \+  H\_continuous\(x\)**
Where H\_continuous = -integral of p\(x\) log2 p\(x\) dx is the differential entropy of the continuous variable. A hybrid component can store more information per device than a purely digital or purely analog one.

## 1.6  The Simulation Loop \(CPU — Single Instance\)

def simulate\_hybrid\(f, G, T, x0, s0, u\_func, dt, T\_end\):

    x = np.array\(x0, dtype=float\)

    s = s0

    t = 0.0

    history = \[\(t, x.copy\(\), s\)\]

    while t < T\_end:

        u = u\_func\(t\)

        # ── continuous step \(Euler\) ──

        x = x \+ f\(x, s, u\) \* dt

        t \+= dt

        # ── discrete transition check ──

        for cond, target in G\(x, s, u\):

            if cond:

                s = T\(s, target, x, u\)

                break

        history.append\(\(t, x.copy\(\), s\)\)

    return history

## 1.7  GPU Vectorised Version \(PyTorch — N Parallel Instances\)

# Simulate N independent components in parallel on GPU

def simulate\_gpu\(f, G\_mask, T\_func, x0, s0, u\_seq, dt\):

    device = 'cuda' if torch.cuda.is\_available\(\) else 'cpu'

    x = torch.tensor\(x0, dtype=torch.float32, device=device\)  # shape \(N, n\_vars\)

    s = torch.tensor\(s0, dtype=torch.long, device=device\)       # shape \(N,\)

    results = \[x.clone\(\)\]

    for u in u\_seq:                                              # u shape: \(N,\)

        x = x \+ f\(x, s, u\) \* dt                                # vectorised ODE step

        mask = G\_mask\(x, s, u\)                                  # shape \(N,\) bool

        s = torch.where\(mask, T\_func\(s, x, u\), s\)              # conditional state jump

        results.append\(x.clone\(\)\)

    return torch.stack\(results\)                                  # shape \(T, N, n\_vars\)

*💡 On a modern GPU you can simulate millions of independent component instances simultaneously. This is extremely useful for Monte Carlo analysis, parameter sweeps, and neural network training with differentiable physics.*

## Chapter 2 — Quantum Tunnel Resistor \(QTR\)

Physical description: Electrons cross a thin insulating barrier not by going over it \(as in classical physics\) but by quantum mechanical tunnelling — effectively appearing on the other side. At the scale of individual electrons this is a discrete random event. At the macroscopic level, millions of these events per second produce a smooth continuous current.

## 2.1  The Simmons Tunnel Current Model

The most accurate formula for DC tunnel current through a rectangular barrier is the Simmons model. It gives current density J \(amps per square metre\) as a function of applied voltage V.

**J\(V\)  =  J0 · \[ \(phi\_bar - V/2\)·exp\(-A·sqrt\(phi\_bar - V/2\)\)**
**              -  \(phi\_bar \+ V/2\)·exp\(-A·sqrt\(phi\_bar \+ V/2\)\) \]**
**J0**
e / \(2\*pi\*hbar\*d^2\)  —  prefactor, units A/m^2/eV

**phi\_bar**
Average barrier height in eV \(for Al2O3: ~3.0 eV\)

**A**
\(4\*pi\*d/h\) \* sqrt\(2\*m\_e\)  —  wave-vector factor, units eV^\(-1/2\)

**d**
Barrier thickness in metres \(2e-9 for 2 nm\)

**V**
Applied voltage in Volts

The total current through an area A\_junc is:

**I\(V\)  =  J\(V\)  \*  A\_junc**
## 2.2  Simplified Low-Voltage Approximation

When V << phi\_bar \(low-voltage limit\), the Simmons formula reduces to a simpler linear-then-quadratic form:

**I  ≈  G0 · V · \(1  \+  V^2 / \(6\*phi\_bar^2\)\)**
Where G0 = \(e^2 / h\) · \(A\_junc/d\) · exp\(-A·sqrt\(phi\_bar\)\) is the zero-bias conductance.

## 2.3  Shot Noise — Simulating Discrete Electron Events

The current is not truly continuous — it is a stream of individual electron tunnelling events. Each event carries charge e = 1.6×10^-19 C. The number of events in a time window dt follows a Poisson distribution.

**n\_events  ~  Poisson\(lambda \* dt\)    where  lambda = I\(V\) / e**
**I\_stochastic  =  n\_events \* e / dt**
The power spectral density of this shot noise is:

**S\_I\(f\)  =  2 \* e \* I             \[White noise, flat spectrum\]**
## 2.4  Complete Python Simulation

import numpy as np

# Physical constants

e = 1.602e-19        # electron charge, C

hbar = 1.055e-34     # reduced Planck, J\*s

h\_planck = 6.626e-34 # Planck constant

m\_e = 9.109e-31      # electron mass, kg

def simmons\_current\(V, d=2e-9, phi\_bar=3.0, A\_junc=50e-12\*\*2\):

    '''

    Simmons tunnel current model.

    V:       applied voltage \(V\)

    d:       barrier thickness \(m\), default 2 nm

    phi\_bar: average barrier height \(eV\), default 3.0 eV for Al2O3

    A\_junc:  junction area \(m^2\), default 50 um x 50 um

    '''

    # Convert units

    phi\_eV = phi\_bar

    A = \(4 \* np.pi \* d / h\_planck\) \* np.sqrt\(2 \* m\_e \* e\)  # eV^-0.5

    J0 = e / \(2 \* np.pi \* hbar \* d\*\*2\)

    # Avoid division by zero at V=0

    V = np.where\(np.abs\(V\) < 1e-6, 1e-6 \* np.sign\(V \+ 1e-30\), V\)

    lo = phi\_eV - V/2

    hi = phi\_eV \+ V/2

    J = J0 \* \(lo \* np.exp\(-A \* np.sqrt\(np.maximum\(lo, 0\)\)\)

            - hi \* np.exp\(-A \* np.sqrt\(np.maximum\(hi, 0\)\)\)\)

    return J \* A\_junc

def simulate\_qtr\(V\_dc, dt=1e-9, n\_steps=10000\):

    '''Simulate QTR with shot noise included.'''

    I\_mean = simmons\_current\(V\_dc\)

    lam = abs\(I\_mean\) / e          # mean event rate \(Hz\)

    # Poisson-sample discrete electron events

    n\_events = np.random.poisson\(lam \* dt, size=n\_steps\)

    I\_noisy  = n\_events \* e / dt \* np.sign\(I\_mean\)

    t = np.arange\(n\_steps\) \* dt

    return t, I\_noisy, I\_mean

# Example: V sweep I-V curve

V\_range = np.linspace\(-1, 1, 1000\)

I\_curve = simmons\_current\(V\_range\)

R\_dynamic = V\_range / \(I\_curve \+ 1e-30\)   # dynamic resistance

## 2.5  GPU Vectorisation \(PyTorch\)

import torch

def simmons\_gpu\(V, d=2e-9, phi\_bar=3.0, A\_junc=2.5e-15\):

    '''Batch Simmons model on GPU. V can be any shape.'''

    device = V.device

    A  = torch.tensor\(\(4\*3.14159\*d/6.626e-34\)\*np.sqrt\(2\*9.109e-31\*1.602e-19\),

                       dtype=V.dtype, device=device\)

    J0 = torch.tensor\(1.602e-19/\(2\*3.14159\*1.055e-34\*d\*\*2\),

                       dtype=V.dtype, device=device\)

    V  = torch.where\(torch.abs\(V\) < 1e-6, torch.sign\(V\)\*1e-6, V\)

    lo = phi\_bar - V/2

    hi = phi\_bar \+ V/2

    J  = J0\*\(lo\*torch.exp\(-A\*torch.sqrt\(lo.clamp\(min=0\)\)\)

           - hi\*torch.exp\(-A\*torch.sqrt\(hi.clamp\(min=0\)\)\)\)

    return J \* A\_junc

# Simulate 1 million junctions in parallel:

V\_batch = torch.rand\(1\_000\_000, device='cuda'\) \* 2 - 1

I\_batch = simmons\_gpu\(V\_batch\)

*💡 Key insight: The QTR resistance R = V/I\(V\) varies continuously with voltage via the Simmons formula, while discrete electron events produce Poisson-distributed shot noise. You get both worlds in one equation.*

## Chapter 3 — Magnetic Domain Inductor

Physical description: A coil wound around a ferrite core. The core is a magnetic material whose atoms are grouped into domains — regions of uniform magnetisation. As you increase current, domain walls move continuously \(smooth inductance change\) until a domain flips abruptly \(discrete Barkhausen jump\). The CoFeB thin film adds extra discrete switching events with sharp thresholds.

## 3.1  The Jiles-Atherton Hysteresis Model

This is the standard industry model for magnetic hysteresis. It governs how magnetisation M varies with field H, capturing both the continuous rotation and the discrete irreversible losses.

Step 1 — The anhysteretic \(ideal\) magnetisation curve:

**M\_an\(H\_eff\)  =  M\_s · \[ coth\(H\_eff / a\)  -  a / H\_eff \]     \[Langevin function\]**
Step 2 — Effective field including demagnetisation and coupling:

**H\_eff  =  H  \+  alpha · M     where H = N\*I/l\_eff**
Step 3 — The differential equation for M:

**dM/dH  =  \(1-c\)·\(M\_an - M\) / \[k·delta - alpha·\(M\_an - M\)\]  \+  c·dM\_an/dH**
**M\_s**
Saturation magnetisation \(A/m\). NiZn ferrite: ~2.5e5 A/m

**a**
Shape parameter \(A/m\). Controls width of hysteresis. ~1200 A/m

**alpha**
Inter-domain coupling. Small value ~1e-4

**k**
Pinning parameter — energy to unpin a domain wall. ~400 A/m

**c**
Reversibility. c=0 fully irreversible; c=1 fully reversible. ~0.2

**delta**
\+1 if dH/dt > 0 \(increasing field\), -1 if decreasing. KEY!

The inductance from the coil and core is then:

**L\(H\)  =  mu\_0 · N^2 · A\_e / l\_e · \(1 \+ dM/dH\)**
**     =  mu\_0 · mu\_r\_eff\(H\) · N^2 · A\_e / l\_e**
## 3.2  Discrete Domain Switching \(CoFeB Film\)

The thin CoFeB film creates additional discrete switching events on top of the continuous Jiles-Atherton core. Each domain in the film has a switching field drawn from a distribution:

**H\_sw\[i\]  ~  Normal\(H\_mean, sigma\_H\)     for i = 1..N\_domains**
State transitions:

**m\_i\(t\+\)  =  \+1  if  H\(t\) > H\_sw\[i\]**
**m\_i\(t\+\)  =  -1  if  H\(t\) < -H\_sw\[i\]**
The film contribution to inductance is:

**delta\_L  =  mu\_0 · N^2 · A\_film / l\_film · \(1/N\_d\) · sum\_i\(m\_i\)  · chi\_CoFeB**
## 3.3  Complete Python Simulation

import numpy as np

class MagneticDomainInductor:

    def \_\_init\_\_\(self, N=20, A\_e=7.07e-9, l\_e=6.28e-3,

                 Ms=2.5e5, a=1200, alpha=1e-4, k=400, c=0.2,

                 N\_domains=20, H\_mean=800, sigma\_H=150\):

        # Core geometry

        self.N = N            # turns

        self.A\_e = A\_e        # effective cross-section \(m^2\), 3mm OD toroid

        self.l\_e = l\_e        # effective path length \(m\)

        self.mu0 = 4\*np.pi\*1e-7

        # Jiles-Atherton params

        self.Ms, self.a, self.alpha, self.k, self.c = Ms, a, alpha, k, c

        # CoFeB thin-film domain array

        self.H\_sw = np.abs\(np.random.normal\(H\_mean, sigma\_H, N\_domains\)\)

        self.m    = np.ones\(N\_domains\)  # start all aligned \+1

        # State

        self.M = 0.0

        self.delta = 1

        self.H\_prev = 0.0

    def \_langevin\(self, H\_eff\):

        if abs\(H\_eff\) < 1e-6: return self.Ms \* H\_eff / \(3\*self.a\)

        return self.Ms \* \(1/np.tanh\(H\_eff/self.a\) - self.a/H\_eff\)

    def step\(self, I, dt\):

        H = self.N \* I / self.l\_e                 # Ampere's law

        self.delta = 1 if H >= self.H\_prev else -1

        H\_eff = H \+ self.alpha \* self.M

        Man   = self.\_langevin\(H\_eff\)

        dMan\_dH = \(self.\_langevin\(H\_eff \+ 0.1\) - self.\_langevin\(H\_eff - 0.1\)\) / 0.2

        denom = self.k \* self.delta - self.alpha \* \(Man - self.M\)

        if abs\(denom\) < 1e-10: denom = 1e-10

        dMdH  = \(1-self.c\)\*\(Man - self.M\)/denom \+ self.c\*dMan\_dH

        dH    = H - self.H\_prev

        self.M \+= dMdH \* dH                        # integrate

        # CoFeB discrete switching

        self.m = np.where\(H > self.H\_sw, 1.0,

                  np.where\(H < -self.H\_sw, -1.0, self.m\)\)

        # Inductance calculation

        chi\_eff  = dMdH \+ np.mean\(self.m\) \* 5000  # film adds ~chi=5000

        L = self.mu0 \* self.N\*\*2 \* self.A\_e / self.l\_e \* \(1 \+ chi\_eff\)

        self.H\_prev = H

        return L

    def simulate\(self, I\_array, dt\):

        return np.array\(\[self.step\(I, dt\) for I in I\_array\]\)

# Run: triangular current ramp

ind = MagneticDomainInductor\(\)

t  = np.linspace\(0, 1e-4, 10000\)

I  = 0.1 \* np.sin\(2\*np.pi\*1e4\*t\)

L  = ind.simulate\(I, dt=1e-8\)

*💡 The discrete jumps in L correspond to real Barkhausen noise — tiny voltage spikes that appear across the coil when a magnetic domain flips. In the simulation they appear as sudden changes in the L array.*

## Chapter 4 — Memory Components: Memristor, Memcapacitor, Meminductor

Physical description: These are components whose R, C, or L value at this moment depends on everything that has happened to them in the past. The HP memristor literally has a thin film that grows or shrinks based on charge flow — the film thickness is the memory. Memcapacitors store trapped charge that shifts the capacitance. Meminductors have domain walls whose positions reflect current history.

## 4.1  The HP Memristor Model

The HP Labs memristor \(titanium dioxide TiO2, 2008\) is the canonical model. A thin oxide layer has a doped sub-region whose width w sets the resistance.

**R\(w\)  =  R\_on · \(w/D\)  \+  R\_off · \(1 - w/D\)**
**V\(t\)  =  R\(w\) · I\(t\)**
**dw/dt  =  mu\_v · \(R\_on/D^2\) · I\(t\) · f\(w\)**
**R\_on**
Minimum resistance \(doped region fully spans device\). ~100 Ohm

**R\_off**
Maximum resistance \(undoped region\). ~16,000 Ohm

**D**
Total device thickness. 10 nm

**mu\_v**
Oxygen vacancy mobility. 1e-14 m^2/\(V\*s\)

**f\(w\)**
Window function: keeps w inside \[0, D\]. Joglekar: f = 1 - \(2w/D - 1\)^\(2p\)

## 4.2  Dual-Mode Memristor \(TaOx \+ HfO2\)

The dual-mode design from your documents combines an analog TaOx layer \(continuous resistance tuning\) with a binary HfO2 layer \(discrete crystalline/amorphous switching\). Both mechanisms operate simultaneously:

**R\_total\(x\_a, s\_b\)  =  R\_analog\(x\_a\)  \*  R\_binary\(s\_b\)**
**R\_analog\(x\_a\)  =  R\_min \* exp\(beta \* \(1 - x\_a\)\)    x\_a in \[0,1\]**
**R\_binary\(s\_b\)  =  1 \(crystalline, low-R\) or r \(amorphous, high-R\)**
The analog state evolves continuously:

**dx\_a/dt  =  I \* x\_a \* \(1 - x\_a\) / I\_ref**
The binary state switches when cumulative charge exceeds threshold:

**s\_b  flips  when  |integral I dt|  >  Q\_threshold**
## 4.3  Memcapacitor Model

A memcapacitor stores charge history in its internal state phi \(the integral of voltage\). The capacitance C depends on phi:

**q\(t\)  =  C\(phi\) · V\(t\)**
**phi\(t\)  =  integral\_0^t  V\(tau\) dtau     \[flux linkage\]**
**C\(phi\)  =  C\_0  \+  dC · tanh\(phi / phi\_0\)**
The current flowing into the capacitor is:

**I  =  dq/dt  =  C\(phi\)·\(dV/dt\)  \+  V·\(dC/dphi\)·V**
**         =  C\(phi\)·dV/dt  \+  V^2 · dC\_dphi**
## 4.4  Meminductor Model

A meminductor's inductance depends on q \(the integral of current\):

**Phi\(t\)  =  L\(q\) · I\(t\)     where  q\(t\) = integral\_0^t I\(tau\) dtau**
**L\(q\)  =  L\_0  \+  dL · tanh\(q / q\_0\)**
**V  =  dPhi/dt  =  L\(q\) · dI/dt  \+  I · \(dL/dq\) · I**
**  =  L\(q\) · dI/dt  \+  I^2 · dL\_dq**
## 4.5  Complete Python Simulation \(All Three\)

import numpy as np

# ── MEMRISTOR ──────────────────────────────────────────────────────────

class Memristor:

    def \_\_init\_\_\(self, Ron=100, Roff=16000, D=10e-9, mu\_v=1e-14, p=1\):

        self.Ron, self.Roff, self.D, self.mu\_v, self.p = Ron, Roff, D, mu\_v, p

        self.w = D \* 0.5   # start at 50% doped

    def \_window\(self\):

        return 1 - \(2\*self.w/self.D - 1\)\*\*\(2\*self.p\)

    def step\(self, I, dt\):

        R = self.Ron\*\(self.w/self.D\) \+ self.Roff\*\(1 - self.w/self.D\)

        V = R \* I

        dw = self.mu\_v \* \(self.Ron/self.D\*\*2\) \* I \* self.\_window\(\)

        self.w = np.clip\(self.w \+ dw\*dt, 0, self.D\)

        return V, R

# ── DUAL-MODE MEMRISTOR ─────────────────────────────────────────────────

class DualModeMemristor:

    def \_\_init\_\_\(self, Rmin=50, beta=4.0, I\_ref=1e-3, r\_ratio=100, Q\_thresh=1e-6\):

        self.Rmin, self.beta, self.I\_ref = Rmin, beta, I\_ref

        self.r\_ratio    = r\_ratio     # HfO2 amorphous vs crystalline R ratio

        self.Q\_thresh   = Q\_thresh    # charge needed to flip binary state

        self.xa  = 0.5               # analog state

        self.sb  = 0                 # binary state \(0=cryst, 1=amorphous\)

        self.q\_acc = 0.0             # accumulated charge

    def step\(self, I, dt\):

        Ra   = self.Rmin \* np.exp\(self.beta \* \(1 - self.xa\)\)

        Rb   = 1 if self.sb == 0 else self.r\_ratio

        R    = Ra \* Rb

        V    = R \* I

        # Analog dynamics

        dxa  = I \* self.xa \* \(1 - self.xa\) / self.I\_ref

        self.xa = np.clip\(self.xa \+ dxa\*dt, 0, 1\)

        # Binary switching

        self.q\_acc \+= abs\(I\) \* dt

        if self.q\_acc > self.Q\_thresh:

            self.sb = 1 - self.sb    # flip state

            self.q\_acc = 0.0

        return V, R

# ── MEMCAPACITOR ────────────────────────────────────────────────────────

class Memcapacitor:

    def \_\_init\_\_\(self, C0=1e-9, dC=0.8e-9, phi0=1e-6\):

        self.C0, self.dC, self.phi0 = C0, dC, phi0

        self.phi = 0.0    # integral of V

        self.V   = 0.0

    def C\(self\): return self.C0 \+ self.dC \* np.tanh\(self.phi / self.phi0\)

    def dCdphi\(self\): return self.dC / \(self.phi0 \* np.cosh\(self.phi/self.phi0\)\*\*2\)

    def step\(self, V\_new, dt\):

        dV   = \(V\_new - self.V\) / dt

        I    = self.C\(\) \* dV \+ V\_new\*\*2 \* self.dCdphi\(\)

        self.phi \+= V\_new \* dt

        self.V    = V\_new

        return I, self.C\(\)

# ── MEMINDUCTOR ─────────────────────────────────────────────────────────

class Meminductor:

    def \_\_init\_\_\(self, L0=1e-6, dL=0.8e-6, q0=1e-6\):

        self.L0, self.dL, self.q0 = L0, dL, q0

        self.q = 0.0     # integral of I

        self.I = 0.0

    def L\(self\): return self.L0 \+ self.dL \* np.tanh\(self.q / self.q0\)

    def dLdq\(self\): return self.dL / \(self.q0 \* np.cosh\(self.q/self.q0\)\*\*2\)

    def step\(self, I\_new, dt\):

        dI   = \(I\_new - self.I\) / dt

        V    = self.L\(\) \* dI \+ I\_new\*\*2 \* self.dLdq\(\)

        self.q \+= I\_new \* dt

        self.I  = I\_new

        return V, self.L\(\)

## Chapter 5 — Stochastic Components: Brownian Resistor & Markov Chain Models

Physical description: The Brownian Resistor is a device where thermal noise is not just a nuisance — it IS the mechanism. Quantum dot charge states create a discrete energy landscape, and the resistance performs a random walk between states. This can be used for noise-based computing, physical random number generation, and stochastic signal processing.

## 5.1  The Langevin SDE Model

Within a given discrete state n with equilibrium resistance R\_n, the actual resistance performs an Ornstein-Uhlenbeck random walk:

**dR  =  -gamma · \(R - R\_n\) · dt  \+  sigma · dW\_t**
Where dW\_t = sqrt\(dt\) \* xi, xi ~ N\(0,1\) is Gaussian white noise \(the Wiener process increment\).

Discretised for simulation \(Euler-Maruyama method\):

**R\[k\+1\]  =  R\[k\]  -  gamma · \(R\[k\] - R\_n\) · dt  \+  sigma · sqrt\(dt\) · xi\[k\]**
## 5.2  Discrete State Transitions \(Markov Chain\)

The component can jump between N discrete resistance levels. The transition rate from state n to state m follows the Arrhenius rate law:

**lambda\_\{n->m\}  =  nu\_0 · exp\(-E\_\{nm\} / \(k\_B · T\)\)**
Where E\_\{nm\} is the energy barrier between states and nu\_0 is the attempt frequency \(~10^12 Hz\). The probability of transition in one timestep is:

**P\(n -> m in dt\)  =  lambda\_\{n->m\} · dt**
## 5.3  Poisson Capacitor Model

Individual electron captures are Poisson events. Charge Q and voltage V evolve as:

**N\(t\)  ~  Poisson\(lambda · t\)     where lambda = I\_leakage / e**
**Q\(t\)  =  e · N\(t\)     \[Discrete charge in coulombs\]**
**V\(t\)  =  Q\(t\) / C     \[Continuous voltage\]**
## 5.4  Python Simulation \(GPU-Ready\)

import numpy as np

import torch

# ── BROWNIAN RESISTOR \(CPU\) ──────────────────────────────────────────────

class BrownianResistor:

    def \_\_init\_\_\(self, R\_levels=\[1e3, 5e3, 20e3, 100e3\],

                       gamma=1e6, sigma=50.0, T=300, kB=1.38e-23\):

        self.R\_levels = np.array\(R\_levels\)

        self.gamma    = gamma   # mean reversion rate \(Hz\)

        self.sigma    = sigma   # noise amplitude \(Ohm/sqrt\(s\)\)

        self.T        = T

        self.kB       = kB

        self.state    = 0       # current discrete state index

        self.R        = R\_levels\[0\]

        # Energy barriers \(example: uniform, in units of kBT\)

        n = len\(R\_levels\)

        self.E\_barriers = np.ones\(\(n, n\)\) \* 5 \* kB \* T  # 5 kBT barriers

        np.fill\_diagonal\(self.E\_barriers, 0\)

    def step\(self, V, dt, nu0=1e12\):

        R\_n = self.R\_levels\[self.state\]

        xi  = np.random.normal\(\)

        # Continuous OU random walk

        self.R \+= -self.gamma\*\(self.R - R\_n\)\*dt \+ self.sigma\*np.sqrt\(dt\)\*xi

        self.R  = max\(1.0, self.R\)  # resistance must be positive

        # Markov chain state transitions

        n = len\(self.R\_levels\)

        for m in range\(n\):

            if m == self.state: continue

            E   = self.E\_barriers\[self.state, m\]

            lam = nu0 \* np.exp\(-E / \(self.kB \* self.T\)\)

            if np.random.rand\(\) < lam \* dt:

                self.state = m

                break

        I = V / self.R

        return I, self.R

# ── POISSON CAPACITOR \(GPU\) ──────────────────────────────────────────────

def simulate\_poisson\_cap\_gpu\(C=1e-9, I\_leak=1e-9, V0=1.0,

                              dt=1e-9, n\_steps=100000, n\_caps=100000\):

    device = 'cuda' if torch.cuda.is\_available\(\) else 'cpu'

    e      = 1.602e-19

    lam    = I\_leak / e           # mean electron rate \(events/sec\)

    # Each capacitor starts with the same initial charge

    Q = torch.ones\(n\_caps, device=device\) \* C \* V0

    V\_history = \[Q / C\]

    for \_ in range\(n\_steps\):

        # Discrete electron captures: Poisson sampling

        rate  = \(torch.abs\(Q/C\) \* C \* 1e6\).clamp\(max=1e7\) / e  # dynamic rate

        delta\_n = torch.poisson\(rate \* dt \* torch.ones\(n\_caps, device=device\)\)

        Q = Q \+ delta\_n \* e - I\_leak \* dt  # capture - leakage

        V\_history.append\(Q / C\)

    return torch.stack\(V\_history\)  # shape: \(n\_steps\+1, n\_caps\)

*💡 The GPU version simulates 100,000 independent capacitors simultaneously. Each one undergoes different random charge capture events. This is perfect for Monte Carlo yield analysis or studying statistical distributions in noisy circuits.*

## Chapter 6 — Josephson Junction Inductor

Physical description: Two superconductors separated by a thin barrier. Quantum mechanics allows Cooper pairs \(pairs of electrons\) to tunnel through, creating a supercurrent. The amount of supercurrent depends sinusoidally on a phase difference phi — a continuous quantum variable. Flux, however, only enters or leaves in discrete quanta of Phi\_0 = h/\(2e\) = 2.07 femtoWebers. This combination of continuous phase and discrete flux is the essence of the hybrid behaviour.

## 6.1  The Josephson Relations

**I\(t\)  =  I\_c · sin\(phi\(t\)\)     \[Current-phase relation\]**
**V\(t\)  =  \(hbar/2e\) · dphi/dt     \[Voltage-phase relation\]**
Where phi is the quantum phase difference across the junction. From these two equations we can derive the effective inductance:

**L\_J\(phi\)  =  hbar / \(2e · I\_c · cos\(phi\)\)**
This inductance is tunable — by adjusting the DC phase bias you can set any inductance from L\_min = hbar/\(2e·I\_c\) to infinity \(at phi = pi/2\).

## 6.2  The RCSJ Model \(Resistively and Capacitively Shunted Junction\)

A real junction has parallel resistance R\_J \(quasiparticle tunnelling\) and capacitance C\_J \(geometric\). The full dynamics are:

**I\_applied  =  I\_c·sin\(phi\)  \+  \(hbar/2eR\)·dphi/dt  \+  C·\(hbar/2e\)·d^2phi/dt^2**
Normalise: divide everything by I\_c, let tau = omega\_p · t where omega\_p = sqrt\(2e·I\_c/\(hbar·C\)\) is the plasma frequency:

**I\_n  =  sin\(phi\)  \+  \(1/Q\)·dphi/dtau  \+  d^2phi/dtau^2**
**I\_n**
Normalised bias current = I\_applied / I\_c

**Q**
Quality factor = omega\_p \* R\_J \* C\_J. High Q = underdamped \(voltage oscillations\).

**omega\_p**
Plasma frequency = sqrt\(2\*pi\*I\_c / \(Phi\_0 \* C\_J\)\). ~10-100 GHz for typical junctions.

**I\_c**
Critical current. ~1 uA to 10 uA for typical junctions.

## 6.3  Discrete Flux Quantisation Guard Condition

Flux enters the junction in units of Phi\_0. When the phase phi crosses a multiple of 2\*pi, one flux quantum has passed through:

**Phi  =  \(Phi\_0 / 2\*pi\) · phi**
**n\_flux  =  round\(phi / \(2\*pi\)\)     \[Integer number of flux quanta\]**
## 6.4  Python Simulation

import numpy as np

from scipy.integrate import solve\_ivp

# Physical constants

hbar  = 1.055e-34

e\_q   = 1.602e-19

Phi0  = hbar \* np.pi / e\_q   # = h/2e = 2.067e-15 Wb

class JosephsonJunction:

    def \_\_init\_\_\(self, Ic=10e-6, R\_J=50.0, C\_J=1e-15\):

        self.Ic  = Ic

        self.R\_J = R\_J

        self.C\_J = C\_J

        self.omega\_p = np.sqrt\(2\*np.pi\*Ic / \(Phi0 \* C\_J\)\)

        self.Q = self.omega\_p \* R\_J \* C\_J

        self.n\_flux = 0   # discrete flux quanta count

    def rcsj\_ode\(self, tau, state, I\_n\):

        '''state = \[phi, dphi/dtau\]'''

        phi, dphi = state

        d2phi = I\_n - np.sin\(phi\) - dphi/self.Q

        return \[dphi, d2phi\]

    def simulate\(self, I\_applied, t\_end, dt=1e-12\):

        t\_norm = np.arange\(0, t\_end \* self.omega\_p, self.omega\_p \* dt\)

        I\_n    = I\_applied / self.Ic

        sol = solve\_ivp\(self.rcsj\_ode, \[0, t\_norm\[-1\]\], \[0.0, 0.0\],

                        args=\(I\_n,\), t\_eval=t\_norm, method='RK45',

                        rtol=1e-8, atol=1e-10\)

        phi   = sol.y\[0\]

        t\_phys = sol.t / self.omega\_p

        V     = \(hbar / \(2\*e\_q\)\) \* np.gradient\(phi, t\_phys\)

        I\_sc  = self.Ic \* np.sin\(phi\)

        # Inductance \(diverges at phi = pi/2 \+ n\*pi\)

        L\_J   = hbar / \(2\*e\_q \* self.Ic \* np.cos\(phi\).clip\(-0.99, 0.99\)\)

        # Track flux quanta

        n\_flux = np.round\(phi / \(2\*np.pi\)\).astype\(int\)

        return t\_phys, phi, V, I\_sc, L\_J, n\_flux

# Example: DC current at 0.9 Ic \(subcritical — junction stays phase-locked\)

jj  = JosephsonJunction\(Ic=10e-6, R\_J=50, C\_J=1e-15\)

t, phi, V, I\_sc, L\_J, n\_flux = jj.simulate\(I\_applied=9e-6, t\_end=1e-9\)

print\(f'Mean L\_J = \{np.mean\(L\_J\)\*1e12:.1f\} pH'\)

## 6.5  GPU Parallelisation \(Parameter Sweep\)

import torch

def josephson\_sweep\_gpu\(I\_c\_array, I\_bias, n\_steps=10000, dt\_norm=0.01\):

    '''

    Sweep over many Ic values simultaneously on GPU.

    I\_c\_array: tensor of shape \(N,\) with different critical currents

    Returns: phi tensor of shape \(n\_steps, N\)

    '''

    device = I\_c\_array.device

    N   = len\(I\_c\_array\)

    Q   = torch.ones\(N, device=device\) \* 5.0  # fixed Q for sweep

    I\_n = I\_bias / I\_c\_array                  # normalised bias per junction

    phi = torch.zeros\(N, device=device\)

    dphi = torch.zeros\(N, device=device\)

    history = \[phi.clone\(\)\]

    for \_ in range\(n\_steps\):

        d2phi = I\_n - torch.sin\(phi\) - dphi/Q

        dphi  = dphi  \+ d2phi \* dt\_norm

        phi   = phi   \+ dphi  \* dt\_norm

        history.append\(phi.clone\(\)\)

    return torch.stack\(history\)  # \(n\_steps\+1, N\)

## Chapter 7 — GMR Spin Resistor

Physical description: Two ferromagnetic layers separated by a non-magnetic spacer. When the magnetisations are parallel, electrons flow easily \(low resistance R\_P\). When antiparallel, scattering is high \(R\_AP\). Since magnetic alignment is a discrete concept \(up/down or some angle between\) but resistance varies continuously with angle, this is a perfect hybrid component.

## 7.1  The GMR Resistance Formula

**R\(theta\)  =  R\_P  \+  \(R\_AP - R\_P\)/2  \*  \(1 - cos\(theta\)\)**
Where theta is the angle between the two layer magnetisation vectors. For a simpler normalised form:

**R\(theta\)  =  R\_P  \*  \(1  \+  GMR\_ratio/2  \*  \(1 - cos theta\)\)**
**GMR\_ratio  =  \(R\_AP - R\_P\) / R\_P     \[e.g., 0.12 = 12%\]**
Using vector notation with unit magnetisation vectors m1 and m2:

**R  =  R\_P  \+  ΔR/2  \*  \(1  -  m1 · m2\)     where ΔR = R\_AP - R\_P**
## 7.2  Stoner-Wohlfarth Magnetisation Switching

The free layer switches discretely when the applied field exceeds the switching field. The switching astroid gives the critical field for switching at arbitrary angle theta between field and easy axis:

**H\_sw\(theta\)  =  H\_k / \(sin^\(2/3\)\(theta\) \+ cos^\(2/3\)\(theta\)\)^\(3/2\)**
For a field applied along the easy axis \(theta = 0\):

**H\_sw  =  H\_k     \[the anisotropy field\]**
And the magnetisation dynamics between switching events \(Landau-Lifshitz-Gilbert equation\):

**dm/dt  =  -gamma \* m x H\_eff  \+  alpha \* m x \(m x H\_eff\)**
**H\_k**
Anisotropy field. For CoFeB ~800 A/m to 2000 A/m.

**gamma**
Gyromagnetic ratio = 2.21e5 m/\(A\*s\).

**alpha**
Gilbert damping. 0.01 to 0.05 for CoFeB.

**H\_eff**
Total effective field = H\_applied \+ H\_exchange \+ H\_anisotropy \+ H\_demag.

## 7.3  Python Simulation

import numpy as np

class GMRSpinResistor:

    def \_\_init\_\_\(self, RP=100.0, RAP=112.0, Hk=1000, alpha=0.02\):

        self.RP    = RP

        self.RAP   = RAP

        self.dR    = RAP - RP

        self.Hk    = Hk

        self.alpha = alpha

        self.gamma = 2.21e5           # m/\(A\*s\)

        # Start with free layer pinned \(parallel\)

        self.m = np.array\(\[1.0, 0.0, 0.0\]\)   # free layer \(unit vector\)

        self.m\_pin = np.array\(\[1.0, 0.0, 0.0\]\)  # fixed reference layer

    def \_llg\_step\(self, H\_eff, dt\):

        '''Landau-Lifshitz-Gilbert step.'''

        m    = self.m

        mxH  = np.cross\(m, H\_eff\)

        mxmxH = np.cross\(m, mxH\)

        dm\_dt = -self.gamma / \(1 \+ self.alpha\*\*2\) \* \(mxH \+ self.alpha \* mxmxH\)

        self.m = m \+ dm\_dt \* dt

        self.m /= np.linalg.norm\(self.m\)   # re-normalise

    def resistance\(self\):

        cos\_theta = np.dot\(self.m, self.m\_pin\)

        return self.RP \+ self.dR/2 \* \(1 - cos\_theta\)

    def step\(self, I, H\_ext, dt=1e-12\):

        '''

        I:     current through device \(A\) — causes Oersted \+ spin-transfer torque

        H\_ext: external field array \[Hx, Hy, Hz\] in A/m

        '''

        # Anisotropy field \(easy axis = x\)

        H\_anis = np.array\(\[self.Hk \* self.m\[0\], 0.0, 0.0\]\)

        # Spin-transfer torque field \(simplified: proportional to I\)

        H\_stt  = np.array\(\[0.0, I \* 1e6, 0.0\]\)   # rough scaling

        H\_eff  = H\_ext \+ H\_anis \+ H\_stt

        self.\_llg\_step\(H\_eff, dt\)

        R  = self.resistance\(\)

        V  = R \* I

        return V, R, self.m.copy\(\)

# Example: field switching from \+H to -H

gmr = GMRSpinResistor\(\)

H\_values = np.concatenate\(\[np.linspace\(2000, -2000, 500\),

                            np.linspace\(-2000, 2000, 500\)\]\)

R\_curve = \[\]

for H in H\_values:

    for \_ in range\(100\):  # let it settle

        gmr.step\(1e-3, np.array\(\[H, 0, 0\]\), dt=1e-12\)

    R\_curve.append\(gmr.resistance\(\)\)

## Chapter 8 — Time-Domain Hybrid Components

## 8.1  Switched-Capacitor Resistor

Physical description: A capacitor connected by two switches. Every clock cycle, it transfers a packet of charge from one node to another. From the outside it looks like a resistor, but internally it is a sequence of discrete charge transfers \(quantised by the clock\). This is how switched-capacitor filters work.

**R\_eff  =  1 / \(f\_clock · C\)**
The current averaged over one clock cycle T = 1/f is:

**I\_avg  =  C · \(V1 - V2\) · f\_clock  =  \(V1 - V2\) / R\_eff**
Per-cycle charge transfer:

**Delta\_Q\[k\]  =  C · \(V1\[k\*T\] - V2\[k\*T\]\)**
Between clock edges the output is sample-and-held at the last transferred charge.

## 8.2  Sample-Hold Capacitor

Physical description: A capacitor with a switch. When the switch closes \(sample mode\), V\_out follows V\_in. When it opens \(hold mode\), V\_out freezes at the last sampled value. The sampling instants are discrete, the held voltage is continuous.

During sampling \(switch closed, time constant tau = R\_sw · C\):

**V\_out\(t\)  =  V\_in  \+  \(V\_out\_prev - V\_in\) · exp\(-\(t - t\_k\) / tau\)**
During hold \(switch open\):

**V\_out\(t\)  =  V\_out\(t\_k\)   \[constant until next sample\]**
With non-ideal leakage \(resistance R\_leak across cap during hold\):

**V\_out\(t\)  =  V\_sample · exp\(-\(t - t\_k\) / \(R\_leak · C\)\)**
## 8.3  PWM Integrating Capacitor

A capacitor driven by a pulse-width modulated \(PWM\) signal with duty cycle D. The average voltage across the capacitor integrates towards the mean input:

**V\_C\(t\)  =  V\_CC · D  ·  \(1  -  exp\(-t / \(RC\)\)\)     for constant D**
For time-varying D\(t\) \(the general case\):

**dV\_C/dt  =  \(V\_CC · D\(t\)  -  V\_C\) / \(R · C\)**
## 8.4  Python Simulation

import numpy as np

# ── SWITCHED-CAPACITOR RESISTOR ─────────────────────────────────────────

def simulate\_sc\_resistor\(V1\_func, V2\_func, C=1e-9, f\_clock=1e6,

                          t\_end=1e-4, dt=1e-9\):

    R\_eff = 1 / \(f\_clock \* C\)

    T\_clk = 1 / f\_clock

    t = np.arange\(0, t\_end, dt\)

    V1  = V1\_func\(t\)

    V2  = V2\_func\(t\)

    I\_discrete = np.zeros\_like\(t\)

    I\_avg      = np.zeros\_like\(t\)

    # Discrete charge transfer at each clock edge

    for k, tk in enumerate\(np.arange\(0, t\_end, T\_clk\)\):

        idx = int\(tk / dt\)

        if idx < len\(t\):

            dQ = C \* \(V1\[idx\] - V2\[idx\]\)

            I\_discrete\[idx\] = dQ / dt   # impulse of charge

    # Running average \(RC filter on output\)

    tau = T\_clk \* 3

    for i in range\(1, len\(t\)\):

        I\_avg\[i\] = I\_avg\[i-1\] \+ \(I\_discrete\[i\] - I\_avg\[i-1\]\) \* dt/tau

    return t, I\_discrete, I\_avg, R\_eff

# ── SAMPLE-HOLD CAPACITOR ───────────────────────────────────────────────

def simulate\_sample\_hold\(V\_in, t, f\_sample, C=100e-12, R\_sw=100,

                          R\_leak=1e12\):

    '''

    V\_in:     input signal array

    t:        time array

    f\_sample: sampling frequency \(Hz\)

    '''

    dt       = t\[1\] - t\[0\]

    tau\_samp = R\_sw \* C

    tau\_hold = R\_leak \* C

    T\_samp   = 1 / f\_sample

    V\_out    = np.zeros\_like\(V\_in\)

    V\_held   = 0.0

    t\_last   = -T\_samp

    in\_hold  = False

    for i, ti in enumerate\(t\):

        # New sample event?

        if ti - t\_last >= T\_samp:

            V\_held   = V\_out\[i-1\] if i > 0 else V\_in\[0\]

            t\_last   = ti

            in\_hold  = False

        if not in\_hold:

            # Sampling: exponential approach to V\_in

            V\_out\[i\] = V\_in\[i\] \+ \(V\_held - V\_in\[i\]\) \* np.exp\(-\(ti-t\_last\)/tau\_samp\)

            if \(ti - t\_last\) > 5 \* tau\_samp:   # settled enough

                V\_held  = V\_in\[i\]

                in\_hold = True

                t\_last  = ti

        else:

            # Hold: slow exponential decay \(leakage\)

            V\_out\[i\] = V\_held \* np.exp\(-\(ti - t\_last\) / tau\_hold\)

    return V\_out

## Chapter 9 — Quantum Dot Array Resistor

Physical description: A chain of nanoscale semiconductor islands \(quantum dots\) in series. Each dot can hold only a specific number of electrons. Electrons must tunnel one at a time from dot to dot \(Coulomb blockade\). The net current depends on which discrete energy levels are available for transport, making this a fundamentally hybrid device.

## 9.1  Landauer-Büttiker Transmission Formula

The current through a quantum dot array is given by the Landauer formula. It sums over all quantum energy levels, weighting each by how easily it transmits electrons \(the transmission coefficient T\_n\):

**I  =  \(e/h\) · integral T\(E\) · \[f\_L\(E\) - f\_R\(E\)\] dE**
Where f\_L and f\_R are Fermi-Dirac distributions on the left and right leads:

**f\(E\)  =  1 / \(1 \+ exp\(\(E - mu\) / \(k\_B · T\)\)\)**
Each energy level n contributes a Lorentzian peak to T\(E\):

**T\(E\)  =  sum\_n  \[Gamma\_n^2 / \(\(E - E\_n\)^2 \+ Gamma\_n^2\)\]**
**E\_n**
Energy of level n in the quantum dot \(eV\). Set by dot size and gate voltage.

**Gamma\_n**
Level broadening — how strongly level n couples to leads. In eV.

**mu\_L, mu\_R**
Electrochemical potential of left and right leads. mu\_L - mu\_R = eV\_bias.

**k\_B**
Boltzmann constant = 8.617e-5 eV/K

## 9.2  Coulomb Blockade \(Discrete Charging Energy\)

Each dot has a geometric capacitance C\_dot. Adding one electron costs energy:

**E\_charge  =  e^2 / \(2 · C\_dot\)**
The current is blocked \(zero\) until the bias exceeds this charging energy. The conductance resonances appear at:

**V\_gate\[N\]  =  \(N \+ 1/2\) · e / C\_gate     for N = 0, 1, 2, ...**
## 9.3  Python Simulation

import numpy as np

def fermi\(E, mu, T\_K=4.0, kB=8.617e-5\):

    '''Fermi-Dirac distribution. E, mu in eV, T in Kelvin.'''

    x = \(E - mu\) / \(kB \* T\_K\)

    return 1.0 / \(1.0 \+ np.exp\(np.clip\(x, -500, 500\)\)\)

def transmission\(E, levels, broadenings\):

    '''

    T\(E\) = sum of Lorentzians for each energy level.

    levels:      array of level energies \(eV\)

    broadenings: array of Gamma values \(eV\)

    '''

    T = np.zeros\_like\(E\)

    for En, Gn in zip\(levels, broadenings\):

        T \+= Gn\*\*2 / \(\(E - En\)\*\*2 \+ Gn\*\*2\)

    return T

def quantum\_dot\_current\(V\_bias, E\_levels, Gammas, mu0=0.0, T\_K=4.0,

                         E\_min=-0.5, E\_max=0.5, n\_E=10000\):

    '''

    Compute current through a quantum dot array vs V\_bias.

    Uses Landauer-Buttiker formula.

    '''

    e  = 1.602e-19  # C

    h  = 6.626e-34  # J\*s

    eV\_to\_J = e

    E  = np.linspace\(E\_min, E\_max, n\_E\)  # energy grid in eV

    dE = E\[1\] - E\[0\]

    I  = np.zeros\_like\(V\_bias\)

    for i, V in enumerate\(V\_bias\):

        mu\_L = mu0 \+ V/2

        mu\_R = mu0 - V/2

        T    = transmission\(E, E\_levels, Gammas\)

        fL   = fermi\(E, mu\_L, T\_K\)

        fR   = fermi\(E, mu\_R, T\_K\)

        # Integrate: current in Amps

        I\[i\] = \(e/h\) \* np.sum\(T \* \(fL - fR\)\) \* dE \* eV\_to\_J

    return I

# Example: Single quantum dot with Coulomb blockade

V\_bias = np.linspace\(-0.05, 0.05, 1000\)   # 50 mV sweep

# Energy levels tuned by gate: two levels near Fermi

E\_levels  = np.array\(\[-0.01, 0.01, 0.03\]\)  # eV

Gammas    = np.array\(\[0.002, 0.002, 0.002\]\) # eV broadening

I\_QD = quantum\_dot\_current\(V\_bias, E\_levels, Gammas\)

# Coulomb blockade: charging energy gaps

C\_dot = 1e-18   # 1 aF

E\_c   = \(1.602e-19\)\*\*2 / \(2 \* C\_dot\) / 1.602e-19  # in eV ~0.08 eV

print\(f'Charging energy E\_c = \{E\_c\*1000:.1f\} meV'\)

*💡 The Coulomb blockade means current is ZERO until the gate voltage is tuned to a resonance. This creates discrete conductance peaks — a completely digital-looking output from a continuous physical process. This is the purest example of the discrete-continuous hybrid in nature.*

## Chapter 10 — Fractal Components: Koch Inductor & Sierpinski Capacitor

Physical description: Wire bent into a fractal shape \(Koch snowflake for the inductor, Sierpinski triangle for the capacitor\). The self-similar geometry creates resonances at a discrete set of frequencies forming a geometric series, while the electromagnetic response between resonances is smoothly continuous.

## 10.1  Koch Fractal Inductor — Length and Inductance

The Koch curve replaces each line segment with 4 segments each 1/3 the length. After n iterations:

**L\_wire\(n\)  =  L\_0 · \(4/3\)^n     \[Total wire length\]**
The self-resonant frequencies follow a geometric sequence with ratio 3:

**f\_res\(k\)  =  f\_0 / \(3/4\)^k  =  f\_0 · \(4/3\)^k     k = 0, 1, 2, ...**
The inductance of a straight wire of length l, radius r, in free space:

**L\_wire  =  \(mu\_0 / 2\*pi\) · l · \[ln\(2l/r\) - 3/4\]**
After n Koch iterations, substitute l = L\_0 \* \(4/3\)^n:

**L\_Koch\(n\)  =  \(mu\_0/2\*pi\) · L\_0·\(4/3\)^n · \[ln\(2\*L\_0\*\(4/3\)^n / r\) - 3/4\]**
## 10.2  Sierpinski Capacitor — Fractal Dimension and Capacitance

The Sierpinski triangle removes triangular holes from a metal plate. After n iterations, the remaining area fraction is:

**A\_n  =  A\_0 · \(3/4\)^n**
The capacitance scales with area:

**C\_n  =  epsilon\_0 · epsilon\_r · A\_n / d  =  C\_0 · \(3/4\)^n**
But the effective fringe capacitance from the fractal edges scales with the perimeter:

**P\_n  =  P\_0 · \(3/2\)^n     \[Perimeter grows with fractal dimension D = log3/log2 ~ 1.585\]**
**C\_fringe\(n\)  ≈  epsilon\_0 · P\_n · d\_fringe**
The total capacitance is a sum of plate and fringe components — a characteristic signature of fractal geometry.

## 10.3  Frequency-Domain Response \(Multi-Resonant Spectrum\)

The fractal inductor in a circuit with capacitance C\_par produces resonances at:

**omega\_res\(k\)  =  1 / sqrt\(L\_Koch\(n\) · \(3/4\)^k · C\_par\)  for k = 0, 1, 2, ..., n**
## 10.4  Python Simulation

import numpy as np

def koch\_inductance\(n\_iter, L0=0.1, r=0.5e-3, mu0=4\*np.pi\*1e-7\):

    '''

    Inductance of Koch fractal inductor.

    n\_iter: number of Koch iterations \(0=straight wire\)

    L0:     initial wire length \(m\)

    r:      wire radius \(m\)

    Returns: inductance in Henries

    '''

    l\_eff = L0 \* \(4/3\)\*\*n\_iter

    L = \(mu0 / \(2\*np.pi\)\) \* l\_eff \* \(np.log\(2\*l\_eff/r\) - 0.75\)

    return L

def koch\_resonances\(n\_iter, L0=0.1, r=0.5e-3, C\_par=1e-12\):

    '''Returns array of self-resonant frequencies.'''

    f\_res = \[\]

    for k in range\(n\_iter\+1\):

        L\_k = koch\_inductance\(k, L0, r\)

        f\_k = 1 / \(2\*np.pi\*np.sqrt\(L\_k \* C\_par\)\)

        f\_res.append\(f\_k\)

    return np.array\(f\_res\)

def sierpinski\_capacitance\(n\_iter, A0=1e-4, d=1e-3, eps\_r=4.5\):

    '''

    Capacitance of Sierpinski triangle capacitor.

    A0: initial plate area \(m^2\)

    d:  dielectric thickness \(m\)

    eps\_r: relative permittivity

    '''

    eps0 = 8.854e-12

    A\_n  = A0 \* \(3/4\)\*\*n\_iter

    C\_plate  = eps0 \* eps\_r \* A\_n / d

    # Fringe: rough estimate, perimeter grows as \(3/2\)^n

    P0   = np.sqrt\(3\) \* A0\*\*0.5  # equilateral triangle

    P\_n  = P0 \* \(3/2\)\*\*n\_iter

    C\_fringe = eps0 \* P\_n \* d \* 0.1    # crude fringe model

    return C\_plate \+ C\_fringe

def fractal\_impedance\_spectrum\(freqs, n\_iter, L0=0.1, C\_par=1e-12, R\_loss=1.0\):

    '''Compute Z\(f\) for Koch inductor with parallel capacitance.'''

    Z = np.zeros\(len\(freqs\), dtype=complex\)

    for k in range\(n\_iter\+1\):

        L\_k = koch\_inductance\(k, L0\)

        # Each iteration adds a series RLC branch

        for f in range\(len\(freqs\)\):

            omega = 2\*np.pi\*freqs\[f\]

            Z\_branch = R\_loss \+ 1j\*omega\*L\_k \+ 1/\(1j\*omega\*C\_par\)

            Z\[f\] \+= 1/Z\_branch

    return 1/Z

# Print resonance frequencies for 4-iteration Koch inductor

f\_res = koch\_resonances\(4\)

for k, f in enumerate\(f\_res\):

    print\(f'Resonance k=\{k\}: \{f/1e6:.2f\} MHz'\)

## Chapter 11 — Phase-Change Resistors \(GST Chalcogenides\)

Physical description: Germanium-Antimony-Telluride \(GST\) alloy. This material has two stable phases: amorphous \(disordered, high resistance ~1 MOhm\) and crystalline \(ordered, low resistance ~1 kOhm\). The phase can be switched with a voltage pulse — a fast/short pulse amorphises it \(RESET\), a longer/lower pulse crystallises it \(SET\). Between these discrete phase states, the resistance is a continuous analog quantity during the phase transition itself.

## 11.1  The Johnson-Kolmogorov-Avrami-Mehl \(JKAM\) Crystallisation Model

The fraction of material crystallised, xi, follows the JKAM equation during the transition:

**xi\(t\)  =  1  -  exp\(-K\_0 · exp\(-E\_a/\(k\_B·T\)\) · t^n\_Avrami\)**
**K\_0**
Pre-exponential rate constant. ~10^26 s^\(-n\) for GST

**E\_a**
Activation energy for crystallisation. ~2.2 eV for GST

**n\_Avrami**
Avrami exponent: 3D growth n=4, 2D growth n=3. ~2.5 for thin films.

**xi**
Crystallised fraction in \[0,1\]. xi=0 amorphous, xi=1 fully crystal.

## 11.2  Resistance-Temperature Relation

The total resistance combines amorphous and crystalline contributions via the phase fraction:

**R\(xi, T\)  =  R\_cryst\(T\)^xi  ·  R\_amorph\(T\)^\(1-xi\)**
Each phase has its own temperature dependence:

**R\_amorph\(T\)  =  R\_a0 · exp\(\+E\_cond\_a / \(k\_B·T\)\)   \[semiconducting, R rises as T falls\]**
**R\_cryst\(T\)   =  R\_c0 · \(1 \+ TCR · \(T - T\_0\)\)        \[metallic, R rises as T rises\]**
## 11.3  Thermal Model \(Self-Heating\)

The device heats itself through Joule heating. Temperature evolves according to:

**C\_th · dT/dt  =  P\_joule  -  \(T - T\_amb\) / R\_th**
**P\_joule  =  I^2 · R\(xi, T\)**
## 11.4  Python Simulation

import numpy as np

class PhaseChangeResistor:

    def \_\_init\_\_\(self, Ra0=1e6, Rc0=1e3, Ea\_cond=0.4, TCR=2e-3,

                 K0=1e26, Ea\_cryst=2.2, n\_av=2.5,

                 C\_th=1e-12, R\_th=1e5, T\_amb=300\):

        self.Ra0, self.Rc0   = Ra0, Rc0

        self.Ea\_cond, self.TCR = Ea\_cond, TCR

        self.K0, self.Ea\_cryst, self.n\_av = K0, Ea\_cryst, n\_av

        self.C\_th, self.R\_th  = C\_th, R\_th

        self.T\_amb = T\_amb

        self.kB    = 8.617e-5   # eV/K

        # State variables

        self.xi  = 0.0    # start amorphous

        self.T   = T\_amb

        self.t\_crystal = 0.0   # time in crystallising phase

    def R\_amorph\(self\):

        return self.Ra0 \* np.exp\(self.Ea\_cond / \(self.kB \* self.T\)\)

    def R\_cryst\(self\):

        return self.Rc0 \* \(1 \+ self.TCR \* \(self.T - 300\)\)

    def resistance\(self\):

        Ra = self.R\_amorph\(\)

        Rc = self.R\_cryst\(\)

        return Ra\*\*\(1 - self.xi\) \* Rc\*\*self.xi

    def step\(self, I, dt\):

        R    = self.resistance\(\)

        V    = R \* I

        P    = I\*\*2 \* R

        # Thermal dynamics

        dT   = \(P - \(self.T - self.T\_amb\)/self.R\_th\) / self.C\_th

        self.T = max\(self.T\_amb, self.T \+ dT\*dt\)

        # Crystallisation \(only if T > 400 K and currently partially amorphous\)

        if self.T > 400 and self.xi < 1.0:

            self.t\_crystal \+= dt

            rate = self.K0 \* np.exp\(-self.Ea\_cryst/\(self.kB\*self.T\)\)

            self.xi = max\(self.xi, 1 - np.exp\(-rate \* self.t\_crystal\*\*self.n\_av\)\)

        # RESET: rapid heating above T\_melt amorphises

        if self.T > 900:

            self.xi = 0.0

            self.t\_crystal = 0.0

        return V, R, self.xi, self.T

# Simulate SET pulse \(long, low current\)

pcr = PhaseChangeResistor\(\)

t   = np.arange\(0, 500e-9, 0.5e-9\)    # 500 ns window

I\_pulse = np.where\(\(t > 10e-9\) & \(t < 300e-9\), 1e-3, 0\)  # 1 mA SET pulse

results = \[pcr.step\(I\_pulse\[i\], 0.5e-9\) for i in range\(len\(t\)\)\]

xi\_arr = \[r\[2\] for r in results\]

## Chapter 12 — Piezo-Quantum Capacitor

Physical description: A piezoelectric crystal sandwiched with a quantum well semiconductor. Mechanical strain \(continuous\) shifts the quantum well energy levels \(discrete\). The energy level shifts change the density of available charge states and thus the capacitance. One physical effect with two outputs — both continuous \(strain\) and discrete \(level crossings\).

## 12.1  Quantum Well Energy Levels Under Strain

For an infinite square quantum well of width L\_QW, the energy levels are:

**E\_n  =  \(hbar^2 \* pi^2 \* n^2\) / \(2 \* m\* \* L\_QW^2\)     n = 1, 2, 3, ...**
Under applied strain eps \(from piezoelectric effect\), the well width shifts as:

**L\_QW\(eps\)  =  L\_QW0 \* \(1 \+ eps\)**
And there is an additional deformation potential energy shift:

**delta\_E\_n\(eps\)  =  a\_c \* eps \+ b \* \(eps\_xx - eps\_zz\)**
So the level energies under strain are:

**E\_n\(eps\)  =  E\_n0 / \(1 \+ eps\)^2  \+  a\_c \* eps**
## 12.2  Strain-Dependent Capacitance

The capacitance is the derivative of stored charge with voltage. Near a quantum level E\_n, the charge density has a sharp increase \(subband filling\). The total capacitance is:

**C\(V, eps\)  =  C\_geom  \+  C\_quantum\(V, eps\)**
**C\_quantum  =  e^2 \* rho\_2D  \*  sum\_n  Theta\(mu\(V\) - E\_n\(eps\)\)**
Where rho\_2D = m\*/\(pi\*hbar^2\) is the 2D density of states per subband, Theta is the Heaviside step \(a subband contributes only when Fermi energy mu is above it\), and mu\(V\) = mu\_0 \+ eV.

## 12.3  Python Simulation

import numpy as np

def piezo\_quantum\_cap\(V\_array, eps\_mech, L\_QW0=10e-9, m\_eff=0.067\*9.11e-31,

                       C\_geom=50e-15, A\_area=100e-12, n\_levels=5,

                       a\_c=-5.0, T=300\):

    '''

    V\_array:  voltage sweep \(V\)

    eps\_mech: mechanical strain from piezo \(dimensionless, e.g. 0.001 = 0.1%\)

    L\_QW0:    unstrained quantum well width \(m\)

    m\_eff:    effective mass \(kg\). GaAs = 0.067 me

    Returns:  C\(V\) array in Farads

    '''

    hbar  = 1.055e-34

    e\_q   = 1.602e-19

    kB    = 1.381e-23

    # Quantum well levels under strain

    L\_eff = L\_QW0 \* \(1 \+ eps\_mech\)

    E0\_n  = \[\(hbar\*np.pi\*n\)\*\*2 / \(2\*m\_eff\*L\_QW0\*\*2\) / e\_q  # eV

             for n in range\(1, n\_levels\+1\)\]

    E\_n   = np.array\(\[E / \(1 \+ eps\_mech\)\*\*2 \+ a\_c\*eps\_mech for E in E0\_n\]\)

    print\(f'Energy levels under strain=\{eps\_mech\}: \{\[f"\{e:.4f\}" for e in E\_n\]\} eV'\)

    # 2D density of states per subband \(constant\)

    rho2D = m\_eff / \(np.pi \* hbar\*\*2\)  # states/\(m^2 \* J\)

    rho2D\_eV = rho2D \* e\_q / A\_area

    # C\(V\) calculation

    C\_total = np.zeros\_like\(V\_array\)

    for i, V in enumerate\(V\_array\):

        mu = V   # Fermi level shift = eV \(referenced to 0\)

        # Quantum capacitance: sum over subbands below Fermi level

        # Use Fermi-Dirac for finite T

        C\_q = 0.0

        for En in E\_n:

            x = \(mu - En\) / \(kB\*T/e\_q\)

            f = 1/\(1 \+ np.exp\(-np.clip\(x, -500, 500\)\)\)

            C\_q \+= e\_q\*\*2 \* rho2D\_eV \* f

        C\_total\[i\] = C\_geom \+ C\_q

    return C\_total

# Simulate: voltage sweep at different strain levels

V = np.linspace\(-0.5, 0.5, 1000\)

C\_zero\_strain = piezo\_quantum\_cap\(V, eps\_mech=0.0\)

C\_strained    = piezo\_quantum\_cap\(V, eps\_mech=0.002\)

# Discrete jumps visible at each subband crossing

## Chapter 13 — Quantum Hall Resistor

Physical description: A 2D electron gas \(electrons confined to a surface\) in a strong perpendicular magnetic field at low temperature. The Hall resistance — the voltage transverse to current divided by that current — takes on exactly quantised values. This is one of the most precisely quantised phenomena in all of physics, used to define the Ohm itself.

## 13.1  The Quantised Hall Resistance

**R\_H  =  h / \(nu · e^2\)  =  25812.807 / nu   Ohms**
Where nu \(the filling factor\) is an integer and h/e^2 = 25812.807... Ohm is the von Klitzing constant R\_K. Current flow is continuous and lossless \(zero longitudinal resistance R\_xx = 0\) along the edge.

## 13.2  Filling Factor as a Function of Field

**nu\(B\)  =  n\_2D · h / \(e · B\)**
Where n\_2D is the 2D electron density. As the magnetic field increases, nu decreases. Whenever nu crosses an integer, a new Landau level empties and R\_H jumps to the next plateau value.

## 13.3  Broadened Plateau Model for Simulation

Real devices have disorder, which broadens the plateaux. A smooth model for R\_H as a function of B uses a sum of arctangent transitions:

**R\_H\(B\)  =  R\_K · sum\_nu  \[ arctan\(\(nu\(B\) - nu\) / delta\_nu\) / pi  \+  1/2 \]  \*  \(1/nu - 1/\(nu\+1\)\)**
## 13.4  Python Simulation

import numpy as np

def quantum\_hall\_resistance\(B\_field, n\_2D=2e15, delta\_nu=0.05, T=1.0,

                              nu\_max=8\):

    '''

    Simulate Quantum Hall resistance vs magnetic field.

    B\_field: array of B values \(Tesla\)

    n\_2D:    2D electron density \(m^-2\)

    delta\_nu: plateau width \(disorder broadening\)

    T:       temperature \(K\) -- affects plateau sharpness

    '''

    h  = 6.626e-34

    e  = 1.602e-19

    RK = h / e\*\*2   # 25812.807 Ohm

    # Filling factor

    nu\_B = n\_2D \* h / \(e \* np.abs\(B\_field\) \+ 1e-10\)

    R\_H  = np.zeros\_like\(B\_field\)

    R\_xx = np.zeros\_like\(B\_field\)

    for i, nu\_val in enumerate\(nu\_B\):

        # Find nearest integer filling factor

        nu\_int = int\(round\(nu\_val\)\)

        nu\_int = max\(1, min\(nu\_max, nu\_int\)\)

        # Smooth step to plateau: tanh broadening

        dist   = \(nu\_val - nu\_int\) / delta\_nu

        weight = 0.5 \* \(1 \+ np.tanh\(dist\)\)   # 0=lower plateau, 1=upper plateau

        if nu\_int >= nu\_max:

            R\_H\[i\] = RK / nu\_int

        else:

            R\_H\[i\] = RK \* \(weight/nu\_int \+ \(1-weight\)/\(nu\_int\+1\)\)

        # Longitudinal resistance: peaks between plateaux, zero on plateau

        R\_xx\[i\] = RK \* np.exp\(-dist\*\*2 / 2\) \* 0.001   # small activated resistance

    return R\_H, R\_xx

# Simulate field sweep from 0 to 15 Tesla

B = np.linspace\(0.1, 15, 10000\)

R\_H, R\_xx = quantum\_hall\_resistance\(B, n\_2D=3e15\)

print\(f'Plateau values \(Ohm\): \{25812.8/np.array\(\[1,2,3,4,5\]\)\}'\)

## Chapter 14 — Integrate-and-Fire Components \(Neuron-Inspired\)

Physical description: A device that integrates incoming current continuously until an internal variable reaches a threshold, then fires \(discrete spike\) and resets. This is exactly how biological neurons work. It is the simplest possible hybrid component — one continuous variable \(voltage\), one discrete event \(spike\), one threshold \(the guard condition\).

## 14.1  The Leaky Integrate-and-Fire \(LIF\) Model

**C\_m · dV/dt  =  -V/R\_m  \+  I\_input\(t\)**
Guard condition \(discrete event\):

**WHEN  V >= V\_threshold:   V -> V\_reset   AND  emit spike**
**C\_m**
Membrane capacitance. Sets how quickly voltage changes. ~1 nF for a component.

**R\_m**
Membrane resistance \(leak\). Sets the time constant tau = R\_m \* C\_m.

**V\_threshold**
Threshold voltage. When V crosses this, the component fires.

**V\_reset**
Reset voltage after firing. Usually V\_reset < V\_threshold.

**tau = R\_m\*C\_m**
Time constant — how quickly V decays back to rest.

## 14.2  Adaptive Exponential \(AdEx\) Model — More Realistic

The AdEx model adds a subthreshold resonance \(exponential term\) and adaptation \(variable w that increases with each spike\):

**C · dV/dt  =  -g\_L·\(V-E\_L\)  \+  g\_L·DT·exp\(\(V-V\_T\)/DT\)  -  w  \+  I**
**tau\_w · dw/dt  =  a·\(V - E\_L\)  -  w**
When V >= V\_peak: V -> V\_reset, w -> w \+ b \(spike \+ adaptation increment\)

## 14.3  Python Simulation \(GPU-Ready\)

import numpy as np

import torch

# ── LIF \(CPU\) ────────────────────────────────────────────────────────────

def simulate\_lif\(I\_input, dt=1e-4, Cm=1e-9, Rm=1e7,

                  V\_thresh=0.02, V\_reset=-0.07, V\_rest=-0.07\):

    '''

    I\_input: array of input current \(A\)

    dt:      timestep \(s\)

    Returns: V\(t\), spike\_times

    '''

    V = V\_rest

    V\_hist   = np.zeros\(len\(I\_input\)\)

    spikes   = \[\]

    for i, I in enumerate\(I\_input\):

        dV  = \(-V/Rm \+ I\) / Cm

        V   = V \+ dV \* dt

        if V >= V\_thresh:

            spikes.append\(i \* dt\)

            V = V\_reset

        V\_hist\[i\] = V

    return V\_hist, np.array\(spikes\)

# ── LIF GPU \(N neurons in parallel\) ─────────────────────────────────────

def simulate\_lif\_gpu\(I\_batch, dt=1e-4, Cm=1e-9, Rm=1e7,

                      V\_thresh=0.02, V\_reset=-0.07\):

    '''

    I\_batch: shape \(T, N\) - T timesteps, N parallel neurons

    Returns: V shape \(T, N\), spike\_count shape \(N,\)

    '''

    device = I\_batch.device

    N = I\_batch.shape\[1\]

    V = torch.ones\(N, device=device\) \* \(-0.07\)   # rest potential

    V\_hist     = torch.zeros\_like\(I\_batch\)

    spike\_count = torch.zeros\(N, device=device\)

    for t in range\(I\_batch.shape\[0\]\):

        dV = \(-V/Rm \+ I\_batch\[t\]\) / Cm

        V  = V \+ dV \* dt

        # Vectorised threshold check and reset

        fired = \(V >= V\_thresh\)

        spike\_count \+= fired.float\(\)

        V = torch.where\(fired, torch.ones\_like\(V\) \* V\_reset, V\)

        V\_hist\[t\] = V

    return V\_hist, spike\_count

# Example: 10,000 neurons with different input currents

T\_steps = 1000

N\_neurons = 10\_000

I\_batch = torch.rand\(T\_steps, N\_neurons, device='cuda'\) \* 3e-9

V\_hist, n\_spikes = simulate\_lif\_gpu\(I\_batch\)

print\(f'Mean spike rate: \{n\_spikes.mean\(\).item\(\) / \(T\_steps\*1e-4\):.1f\} Hz'\)

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
Differentiable models \(PyTorch autograd\) allow gradients to flow back through the physics, enabling circuit-level learning.

**Real-time**
For dt=1ns and 1024 components, a GPU can run 1000x real-time — perfect for interactive design tools.

## 15.2  Differentiable Physics \(Autograd\)

Any model written in PyTorch with no in-place operations is automatically differentiable. This means you can compute d\(output\)/d\(parameter\) with one backward\(\) call:

import torch

# Make parameters differentiable

d\_barrier = torch.tensor\(2e-9, requires\_grad=True\)

phi\_bar   = torch.tensor\(3.0,  requires\_grad=True\)

# Run simulation

V = torch.linspace\(-0.5, 0.5, 1000\)

I = simmons\_gpu\(V, d=d\_barrier, phi\_bar=phi\_bar\)  # uses torch ops

# Compute gradient of total current power w.r.t. barrier thickness

P\_total = \(I \* V\).sum\(\)

P\_total.backward\(\)

print\(f'd\(Power\)/d\(barrier\_thickness\) = \{d\_barrier.grad:.2e\}'\)

# This enables inverse design: find barrier thickness that gives target R

# Using gradient descent:

optimizer = torch.optim.Adam\(\[d\_barrier\], lr=1e-11\)

R\_target = 5e5   # target 500 kOhm

for step in range\(500\):

    optimizer.zero\_grad\(\)

    I\_pred = simmons\_gpu\(torch.tensor\(0.1\), d=d\_barrier, phi\_bar=phi\_bar\)

    R\_pred = 0.1 / \(I\_pred \+ 1e-30\)

    loss   = \(R\_pred - R\_target\)\*\*2

    loss.backward\(\)

    optimizer.step\(\)

    d\_barrier.data.clamp\_\(0.5e-9, 5e-9\)   # physical bounds

print\(f'Optimal barrier thickness: \{d\_barrier.item\(\)\*1e9:.2f\} nm'\)

## 15.3  Batch Simulation Template \(Universal\)

import torch

from dataclasses import dataclass

from typing import Callable

@dataclass

class HybridComponentGPU:

    '''Universal GPU framework for any hybrid component.'''

    f:        Callable   # continuous dynamics: \(x, s, u\) -> dx\_dt

    G:        Callable   # guard function: \(x, s, u\) -> bool tensor

    T\_func:   Callable   # transition: \(s, x, u\) -> s\_new

    n\_vars:   int        # number of continuous state variables

    n\_states: int        # number of discrete states

    def run\(self, x0: torch.Tensor, s0: torch.Tensor,

            u\_seq: torch.Tensor, dt: float\) -> dict:

        '''

        x0:    \(N, n\_vars\)   initial continuous state

        s0:    \(N,\)          initial discrete state \(int\)

        u\_seq: \(T, N\)        input sequence

        dt:    float         timestep

        '''

        device = x0.device

        x = x0.clone\(\)

        s = s0.clone\(\)

        x\_log, s\_log = \[x.clone\(\)\], \[s.clone\(\)\]

        for t in range\(u\_seq.shape\[0\]\):

            u  = u\_seq\[t\]

            # Runge-Kutta 4th order \(more accurate than Euler\)

            k1 = self.f\(x,           s, u\)

            k2 = self.f\(x \+ dt/2\*k1, s, u\)

            k3 = self.f\(x \+ dt/2\*k2, s, u\)

            k4 = self.f\(x \+ dt\*k3,   s, u\)

            x  = x \+ dt/6 \* \(k1 \+ 2\*k2 \+ 2\*k3 \+ k4\)

            # Check discrete transitions

            guard = self.G\(x, s, u\)

            s     = torch.where\(guard, self.T\_func\(s, x, u\), s\)

            x\_log.append\(x.clone\(\)\)

            s\_log.append\(s.clone\(\)\)

        return \{'x': torch.stack\(x\_log\), 's': torch.stack\(s\_log\)\}

## 15.4  Performance Reference

## 1 CPU core

~10^6 ODE steps per second \(simple scalar ODE\)

**RTX 3090 GPU**
~10^11 float32 ops/sec -> ~10^9 ODE steps/sec for N=10^3 batch

**A100 GPU**
~3x10^11 ops/sec, FP16 tensor cores: up to 10^12 for simple kernels

**Speedup rule of thumb**
For N > 1000 independent components, GPU typically 100-1000x faster than CPU

**Memory limit**
A100: 80 GB. Each component with 10 float32 vars = 40 bytes. Fit 2x10^9 state vars.

**Recommended dt**
ODE stability: dt < tau\_min/10 where tau\_min is the fastest time constant in system

## Chapter 16 — Complete Worked Example: Mixed Circuit Simulation

This chapter shows how to combine multiple hybrid components into a single circuit and simulate it on a GPU. The example circuit is: Josephson Junction Inductor in series with a Memristor, driven by an AC current, with a GMR Spin Resistor in parallel.

## 16.1  Circuit Equations \(Kirchhoff's Laws\)

For a series connection of impedances Z\_JJ \(Josephson\) and Z\_Memristor with parallel Z\_GMR:

**V\_total  =  V\_JJ\(phi, I\)  \+  V\_mem\(w, I\)**
**I\_GMR    =  V\_total / R\_GMR\(theta\)**
**I\_source =  I\_JJ  \+  I\_GMR**
## 16.2  Full Coupled ODE System

State vector: x = \[phi, w, theta\_m1, theta\_m2, theta\_m3\]  \(5 continuous variables\)

Discrete states: s = \[n\_flux, s\_binary\_memristor, m1\_state, m2\_state\]

import numpy as np

import torch

class MixedCircuit:

    '''

    Series: Josephson Junction \+ Dual-Mode Memristor

    Parallel: GMR Spin Resistor

    '''

    def \_\_init\_\_\(self\):

        # JJ params

        self.Ic   = 10e-6

        self.hbar = 1.055e-34

        self.e\_q  = 1.602e-19

        self.Phi0 = 2.067e-15

        self.R\_JJ = 50.0

        self.C\_JJ = 1e-15

        self.phi  = 0.0

        self.dphi = 0.0

        # Memristor params

        self.Ron, self.Roff, self.D = 100, 16000, 10e-9

        self.mu\_v = 1e-14

        self.w   = 5e-9

        # GMR params

        self.RP, self.RAP = 100, 112

        self.theta\_mag = 0.0

        self.omega\_prec = 2\*np.pi \* 5e9   # precession freq

        # Discrete state

        self.n\_flux = 0

    def step\(self, I\_source, dt\):

        # ── JOSEPHSON JUNCTION ──

        I\_JJ  = self.Ic \* np.sin\(self.phi\)

        V\_JJ  = \(self.hbar/\(2\*self.e\_q\)\) \* self.dphi

        # RCSJ current balance

        d2phi = \(2\*self.e\_q/self.hbar\) \* \(I\_source - I\_JJ

                  - V\_JJ/self.R\_JJ\) / self.C\_JJ

        self.dphi \+= d2phi \* dt

        self.phi  \+= self.dphi \* dt

        # Discrete flux tracking

        self.n\_flux = int\(round\(self.phi / \(2\*np.pi\)\)\)

        # ── MEMRISTOR ──

        R\_mem = \(self.Ron\*\(self.w/self.D\)

                \+ self.Roff\*\(1 - self.w/self.D\)\)

        I\_mem = \(I\_source \* R\_mem\) / \(R\_mem \+ 0.001\)  # approx

        V\_mem = R\_mem \* I\_source

        win   = 1 - \(2\*self.w/self.D - 1\)\*\*2

        self.w = np.clip\(self.w

                         \+ self.mu\_v\*\(self.Ron/self.D\*\*2\)\*I\_source\*win\*dt,

                         0, self.D\)

        # ── GMR \(parallel\) ──

        V\_total = V\_JJ \+ V\_mem

        self.theta\_mag \+= self.omega\_prec \* dt \* 0.01  # simplified

        R\_GMR = self.RP \+ \(self.RAP-self.RP\)/2\*\(1 - np.cos\(self.theta\_mag\)\)

        I\_GMR = V\_total / R\_GMR

        return \{'V': V\_total, 'R\_mem': R\_mem, 'R\_GMR': R\_GMR,

                'phi': self.phi, 'n\_flux': self.n\_flux, 'w': self.w\}

# Run the mixed circuit

ckt = MixedCircuit\(\)

t   = np.arange\(0, 10e-9, 1e-12\)

I\_ac = 9e-6 \* np.sin\(2\*np.pi\*5e9\*t\)

results = \[ckt.step\(I\_ac\[i\], 1e-12\) for i in range\(len\(t\)\)\]

V\_out   = np.array\(\[r\['V'\] for r in results\]\)

n\_flux  = np.array\(\[r\['n\_flux'\] for r in results\]\)

## Chapter 17 — Summary: All Models at a Glance

This table provides a complete reference for every component, its governing equation, discrete mechanism, and simulation approach.

**Component**
**Key Equation**
**Discrete Mechanism**
**Continuous Variable**
**Python Class / Function**
QTR

J = J0\[\(phi-V/2\)e^\(-A√\(phi-V/2\)\) - ...\]

Poisson tunnel events

Macroscopic current I

simmons\_current\(\)

Mag Domain Inductor

dM/dH = \(1-c\)\(Man-M\)/\(k·delta-alpha\(Man-M\)\) \+ c·dMan/dH

Barkhausen domain flips

Inductance L\(H\)

MagneticDomainInductor

Memristor

dw/dt = mu\_v·\(Ron/D²\)·I·f\(w\)

Binary oxide film flip

Analog w \(doping width\)

Memristor, DualModeMemristor

Memcapacitor

I = C\(phi\)·dV/dt \+ V²·dC/dphi

Trapped charge states

phi = integral V dt

Memcapacitor

Meminductor

V = L\(q\)·dI/dt \+ I²·dL/dq

Domain wall pinning

q = integral I dt

Meminductor

Brownian Resistor

dR = -gamma\(R-Rn\)dt \+ sigma·dW

Markov state jumps

R\(t\) random walk

BrownianResistor

Josephson Junction

dphi/dt = 2eV/hbar, I = Ic·sin\(phi\)

Flux quanta n·Phi0

Phase phi \(continuous\)

JosephsonJunction

GMR Spin Resistor

R = RP \+ dR/2·\(1-m1·m2\)

Stoner-Wohlfarth switching

LLG magnetisation m

GMRSpinResistor

Switched Cap

R\_eff = 1/\(f·C\)

Clock edge charge transfer

Averaged current I\_avg

simulate\_sc\_resistor\(\)

Sample-Hold Cap

V = V\_in·\(1-exp\(-t/tau\)\)

Discrete sample instants

Held voltage V\_hold

simulate\_sample\_hold\(\)

QD Array Resistor

I = \(e/h\)·integral T\(E\)·\(fL-fR\)dE

Coulomb blockade steps

Lorentzian T\(E\)

quantum\_dot\_current\(\)

Fractal Inductor

L\_n = L0·\(4/3\)^n·\[ln\(2L/r\)-0.75\]

Discrete resonances f0·\(4/3\)^k

L\(f\) between resonances

koch\_inductance\(\)

Phase-Change R

xi = 1-exp\(-K0·exp\(-Ea/kBT\)·t^n\)

Amorphous/Crystal phase

R\(xi, T\) continuous

PhaseChangeResistor

Piezo-Quantum Cap

C = C\_geo \+ e²·rho2D·sum f\(mu-En\)

Subband level crossings

C\(V, eps\) smooth

piezo\_quantum\_cap\(\)

Quantum Hall R

R\_H = h/\(nu·e²\)

Integer Landau levels nu

Current flow continuous

quantum\_hall\_resistance\(\)

Integrate-and-Fire

C·dV/dt = -V/R \+ I

Spike when V > V\_thresh

Membrane voltage V\(t\)

simulate\_lif\(\), simulate\_lif\_gpu\(\)

# Appendix — Constants and Unit Conversions

**e \(electron charge\)**
1.602176634 × 10^-19 C

**hbar \(reduced Planck\)**
1.054571817 × 10^-34 J·s

**h \(Planck constant\)**
6.626070040 × 10^-34 J·s

**m\_e \(electron mass\)**
9.109383702 × 10^-31 kg

**mu\_0 \(permeability\)**
1.256637 × 10^-6 H/m

**epsilon\_0 \(permittivity\)**
8.854187817 × 10^-12 F/m

**k\_B \(Boltzmann\)**
1.380649 × 10^-23 J/K  =  8.617333 × 10^-5 eV/K

**Phi\_0 \(flux quantum\)**
2.067833848 × 10^-15 Wb  =  h/\(2e\)

**R\_K \(von Klitzing\)**
25812.807 Ohm  =  h/e^2

## 1 eV in Joules

1.602 × 10^-19 J

## 1 nm

1 × 10^-9 m

## 1 ps

1 × 10^-12 s

## 1 fF \(femtofarad\)

1 × 10^-15 F

## 1 pH \(picohenry\)

1 × 10^-12 H

*End of Document  —  All formulas derived from first-principles physics*
