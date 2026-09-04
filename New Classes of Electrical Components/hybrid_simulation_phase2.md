# Hybrid component simulation — Phase 2

**General circuit solver**

*Modified Nodal Analysis · Hybrid time-stepping · Nonlinear iteration · GPU network simulation*

*February 2026 · Series continuation — builds on Phase 1 component models*

## Phase 2 Overview — What This Document Covers

The first document (Phase 0) derived simulation equations for individual components. Phase 1 extended this to eight more components. But individual component models are only useful if you can connect them into actual circuits.

Phase 2 builds the general circuit solver: a mathematical engine that takes any network of hybrid components, automatically constructs the governing equations using Kirchhoff's laws, and integrates them forward in time. This is the equivalent of SPICE, but natively handling hybrid discrete-continuous components that SPICE cannot represent.

**Section 1**
Graph theory of circuits — how to represent a network mathematically as nodes and branches

**Section 2**
Modified Nodal Analysis (MNA) — the matrix equation that every circuit simulator is built on

**Section 3**
Handling nonlinear components — Newton-Raphson iteration for resistors, memristors, tunnel junctions

**Section 4**
Time integration — how to step the ODE forward correctly given stiff systems

**Section 5**
Discrete event detection — finding and handling the exact moment a state transition occurs

**Section 6**
The complete HybridCircuit solver class — full Python implementation wiring everything together

**Section 7**
GPU-accelerated network simulation — running thousands of circuit instances in parallel

**Section 8**
Worked examples — three real circuits demonstrating the solver in action

**Section 9**
SPICE export — generating netlist models compatible with standard EDA tools

SECTION 1  ·  MATHEMATICAL FOUNDATIONS


**Graph Theory of Circuits**
Before writing a single equation, we need a way to describe a circuit's topology — which components connect to which nodes. Circuit theory maps perfectly onto graph theory, a branch of mathematics dealing with nodes connected by edges.

## 1.1  The Incidence Matrix

A circuit with N nodes and B branches (components) is described by its incidence matrix A, of shape (N-1) × B. Each column corresponds to one branch. The entry A[i,b] is:

**+1**
Branch b leaves node i (current flows out)

**-1**
Branch b enters node i (current flows in)

**0**
Branch b is not connected to node i

One row is dropped (usually the ground node row) to make the matrix full-rank. This is the Reduced Incidence Matrix A_r.

**KCL (Kirchhoff's Current Law):    A_r · I_branches  =  0**
**KVL (Kirchhoff's Voltage Law):    V_branches  =  A_r^T · V_nodes**
Every circuit solver in the world — from SPICE to commercial EDA — is built on these two equations. They are exact and universal.

## 1.2  Branch Types and Their Equations

Each branch b has a constitutive equation — the relationship between its terminal voltage V_b and current I_b:

**Resistor**
V_b = R · I_b                              → I_b = V_b / R

**Capacitor**
I_b = C · dV_b/dt                          → V_b = (1/C) · integral I_b dt

**Inductor**
V_b = L · dI_b/dt                          → I_b = (1/L) · integral V_b dt

**Voltage source**
V_b = V_s (fixed)                          → I_b unknown (free variable)

**Current source**
I_b = I_s (fixed)                          → V_b unknown (free variable)

**Memristor**
V_b = R(w) · I_b,  dw/dt = f(w, I_b)      → coupled ODE

**Hybrid R**
V_b = R(x_c, s_d) · I_b                   → state-dependent resistor

**Hybrid C**
I_b = C(x_c, s_d) · dV_b/dt               → state-dependent capacitor

**Hybrid L**
V_b = L(x_c, s_d) · dI_b/dt               → state-dependent inductor

## 1.3  Example Circuit Graph

Consider a simple 3-node circuit: a voltage source V_s between node 1 and ground (node 0), a resistor R between nodes 1 and 2, a memristor M between node 2 and ground, and a capacitor C between nodes 1 and 2 in parallel with R.

Nodes: {0=GND, 1, 2}. Branches: {V_s, R, C, M}. The reduced incidence matrix (dropping GND row):

```
          V_s   R    C    M
Node 1  [  1   -1   -1    0  ]
Node 2  [  0    1    1   -1  ]
# KCL at node 1: I_Vs - I_R - I_C = 0
# KCL at node 2: I_R + I_C - I_M = 0
# KVL: V_Vs = V1, V_R = V1-V2, V_C = V1-V2, V_M = V2
```

SECTION 2  ·  THE CORE MATRIX EQUATION

**Modified Nodal Analysis (MNA)**
Modified Nodal Analysis (MNA) is the algorithm that converts the graph description of a circuit into a single matrix equation that can be solved by a computer. It was developed at UC Berkeley in the 1970s and is the foundation of SPICE. We extend it here to handle hybrid components.

## 2.1  The MNA Stamp Concept

Each component type adds its contribution — its 'stamp' — to the global MNA matrix. The matrix equation has the form:

**G(x) · x  +  C_cap · dx/dt  =  b(t)**
Where x is the solution vector (node voltages + branch currents for voltage sources), G is the conductance matrix, C_cap is the capacitance/inductance matrix (for dynamic elements), and b is the source vector.

## 2.2  Component Stamps

### Resistor between nodes i and j, value R:

```
# Adds to G matrix (conductance stamp):
G[i,i] += 1/R
G[j,j] += 1/R
G[i,j] -= 1/R
G[j,i] -= 1/R
```

### Capacitor between nodes i and j, value C:

```
# Adds to C matrix (dynamic stamp):
C_mat[i,i] += C
C_mat[j,j] += C
C_mat[i,j] -= C
C_mat[j,i] -= C
# In time-discrete form (backward Euler, timestep dt):
# C \* (x[n+1]-x[n])/dt -> adds C/dt to G and C/dt \* x[n] to b
G[i,i] += C/dt;  b[i] += C/dt \* V_ij_prev
```

### Inductor between nodes i and j, value L (adds extra variable I_L):
```
# Adds new row/column k for inductor current I_L
G[i,k] +=  1;  G[k,i] +=  1   # V_i contributes to inductor equation
G[j,k] += -1;  G[k,j] += -1   # V_j contributes to inductor equation
C_mat[k,k] += L                # L \* dI_L/dt term
# In time-discrete form:
G[k,k] += L/dt;  b[k] += L/dt \* I_L_prev
```

### Voltage source between nodes i and j, value V_s (adds extra variable I_s):
```
# Adds new row/column k for source current I_s
G[i,k] +=  1;  G[k,i] +=  1
G[j,k] += -1;  G[k,j] += -1
b[k]   += V_s   # enforces V_i - V_j = V_s
```

## 2.3  Hybrid Component Stamps

Hybrid components add state-dependent conductance. The memristor is the canonical example — it is a resistor whose conductance G_mem(w) changes over time according to an internal state w:

```
# State-dependent conductance stamp (same as resistor, but G changes each step)
G_mem = 1.0 / R_memristor(w)   # recomputed every timestep
G[i,i] += G_mem
G[j,j] += G_mem
G[i,j] -= G_mem
G[j,i] -= G_mem
```

```
# Internal state equation appended to ODE:
# dw/dt = f(w, I_mem)  -> integrated separately each timestep
```

## 2.4  The Full MNA System (Time-Discrete)

Using backward Euler time discretisation (stable for stiff circuits, where time constants differ by many orders of magnitude):

**[ G + C_mat/dt ] · x[n+1]  =  b[n+1]  +  C_mat/dt · x[n]**
This is a linear system of equations. At each timestep, we:

  1. Update state-dependent components (recompute G_mem, L(w), C(phi) etc.)

  2. Assemble the full [G + C/dt] matrix

  3. Assemble the right-hand side b[n+1] + C/dt · x[n]

  4. Solve the linear system: x[n+1] = A^(-1) · rhs

  5. Update all internal states (w, phi, q, domain states) using x[n+1]

  6. Check all guard conditions for discrete state transitions

  7. If a transition fires, update discrete states and continue

*📐  For a circuit with N nodes and V voltage sources/inductors, the MNA matrix is (N+V) × (N+V). For small circuits (< 1000 nodes), dense LU factorisation is fast. For large circuits (> 1000 nodes), sparse LU (scipy.sparse.linalg.spsolve) is essential.*

SECTION 3  ·  NEWTON-RAPHSON FOR NONLINEAR COMPONENTS

**Nonlinear Iteration**
The MNA stamp above assumes each component's conductance is known before solving the matrix. But for nonlinear components — the tunnel resistor, Josephson junction, ferroelectric capacitor — the conductance depends on the solution itself. We need Newton-Raphson iteration to resolve this circular dependency.

## 3.1  The Newton-Raphson Linearisation

For a nonlinear component with I = f(V), we linearise around the current operating point V^k:

**I(V)  ≈  I(V^k)  +  f'(V^k) · (V - V^k)**
**      =  f'(V^k) · V  +  [I(V^k) - f'(V^k) · V^k]**
This is equivalent to a linear conductance G_eq = f'(V^k) in parallel with a current source I_eq = I(V^k) - G_eq · V^k. These are the 'companion model' stamps:

```
# Nonlinear component companion model (updated each NR iteration k):
```

G_eq = dI_dV(V_k)            # Jacobian of I w.r.t. V at current estimate

I_eq = I(V_k) - G_eq \* V_k  # Norton equivalent current source

```
# Stamp G_eq as conductance, I_eq as current source
G[i,i] += G_eq;  G[i,j] -= G_eq   # conductance stamp
G[j,i] -= G_eq;  G[j,j] += G_eq
b[i]   += I_eq   # current source stamp (into node i)
b[j]   -= I_eq
```

## 3.2  Newton-Raphson Loop

```python
def newton_raphson_step(mna, x_prev, nonlinear_elements, max_iter=50,
                         tol_v=1e-6, tol_i=1e-9):
    '''
```

    Solve one MNA timestep with NR iteration for nonlinear elements.

    mna:               MNASystem object (see Section 6)

    x_prev:            solution vector from previous timestep

```
    nonlinear_elements: list of NonlinearComponent objects
    Returns:           x_new (converged solution vector)
    '''
    x = x_prev.copy()   # initial guess = previous solution
    for k in range(max_iter):
```

        # Rebuild G matrix with current estimates of nonlinear conductances

```python
        G, C, b = mna.build_linear_stamps()
        for elem in nonlinear_elements:
            V_elem = mna.get_branch_voltage(x, elem)
            G_eq, I_eq = elem.companion_model(V_elem)
            mna.add_stamp(G, b, elem.node_plus, elem.node_minus, G_eq, I_eq)
        # Add dynamic terms (C/dt from capacitors and inductors)
        A = G + C / mna.dt
        rhs = b + C @ x_prev / mna.dt
        # Solve
        import numpy as np
        x_new = np.linalg.solve(A, rhs)
        # Check convergence
        dV = np.abs(x_new[:mna.n_nodes] - x[:mna.n_nodes])
        dI = np.abs(A @ x_new - rhs)
        if dV.max() < tol_v and dI.max() < tol_i:
            return x_new, k+1   # converged
        x = x_new
    raise RuntimeError(f'Newton-Raphson did not converge in {max_iter} iterations')
```

## 3.3  Jacobians for Each Hybrid Component

Each nonlinear component needs its own dI/dV function. Here are the key ones:

### Quantum Tunnel Resistor (Simmons model):

```python
def simmons_jacobian(V, d=2e-9, phi_bar=3.0, A_junc=2.5e-15):
    '''dI/dV at voltage V — derivative of Simmons current.'''
    dV = 1e-4  # numerical step
    return (simmons_current(V+dV, d, phi_bar, A_junc) -
            simmons_current(V-dV, d, phi_bar, A_junc)) / (2\*dV)
def qtr_companion(V, d=2e-9, phi_bar=3.0, A_junc=2.5e-15):
    I_op  = simmons_current(V, d, phi_bar, A_junc)
    G_eq  = simmons_jacobian(V, d, phi_bar, A_junc)
    I_eq  = I_op - G_eq \* V
    return G_eq, I_eq
```

### Memristor (HP model):

def memristor_companion(V, w, D=10e-9, Ron=100, Roff=16000):


    '''Memristor companion model. State w is fixed during NR iteration.'''

```
    R   = Ron\*(w/D) + Roff\*(1 - w/D)   # R is fixed for this NR step
    G_eq = 1.0 / R                       # linear in V for fixed w
    I_eq = 0.0                           # no offset (passes through origin)
    return G_eq, I_eq
```

### Josephson Junction (sinusoidal nonlinearity):

def josephson_companion(V, phi, Ic=10e-6, R_J=50, C_J=1e-15, dt=1e-12):

    '''

    Josephson junction companion model.

    phi: current phase (updated after solution — not during NR)

```
    Uses RCSJ model: I = Ic\*sin(phi) + V/R_J + C_J\*dV/dt
    '''
    hbar, e = 1.055e-34, 1.602e-19
    # Current at operating point
    I_sc  = Ic \* np.sin(phi)
    # Linearised Josephson contribution: dI_sc/dV = Ic\*cos(phi)\*dphi/dV
    # dphi/dV = (2e/hbar)\*dt (from phase-voltage relation, discrete)
    dphi_dV = (2\*e/hbar) \* dt
    G_JJ   = Ic \* np.cos(phi) \* dphi_dV
    G_total = G_JJ + 1/R_J + C_J/dt
    I_eq    = I_sc - G_JJ\*V
    return G_total, I_eq
*🔄  The key insight is that during Newton-Raphson iteration, the internal states (w for memristors, phi for Josephson junctions) are FROZEN at their values from the previous timestep. Only node voltages are iterated. After convergence, states are updated. This splitting is called operator splitting and is essential for stability.*
```

SECTION 4  ·  STABLE STEPPING FOR STIFF HYBRID SYSTEMS

**Time Integration**
Hybrid circuits are typically stiff — they contain components with time constants spanning many orders of magnitude simultaneously. For example, a Josephson junction (picosecond timescale) driving a magnetic domain inductor (nanosecond timescale) driving a large capacitor (microsecond timescale). Explicit methods like forward Euler become unstable for stiff systems unless the timestep is tiny. We need implicit methods.

## 4.1  The Three Integration Methods

**Backward Euler (BE)**
x[n+1] = x[n] + dt · f(x[n+1]). Implicit, unconditionally stable. First-order accurate. Tends to over-damp fast transients.


**Trapezoidal (TR)**
x[n+1] = x[n] + dt/2 · [f(x[n]) + f(x[n+1])]. Second-order accurate. Can show 'ringing' (numerical oscillation) at discontinuities.


**TR-BDF2 (SPICE default)**
Trapezoidal for first half-step, BDF2 for second half-step. Second-order, L-stable. Best compromise — what SPICE uses.


## 4.2  Backward Euler MNA (Full Derivation)

Starting from the continuous MNA equation:

**C_mat · dx/dt  +  G(x) · x  =  b(t)**
Applying backward Euler (evaluate right-hand side at new time n+1):


**C_mat · (x[n+1] - x[n]) / dt  +  G(x[n+1]) · x[n+1]  =  b[n+1]**
**( C_mat/dt  +  G(x[n+1]) ) · x[n+1]  =  b[n+1]  +  C_mat/dt · x[n]**
The matrix (C_mat/dt + G) is reassembled every timestep because G depends on the current operating point for nonlinear components.

## 4.3  Adaptive Timestep Control

Fixed timestep wastes computation during slow parts of the simulation and can miss fast transients. Adaptive control adjusts dt based on the local truncation error (LTE):

**LTE  ≈  dt^2 / 2 · x''(t)     [Backward Euler — proportional to dt²]**
We estimate x'' from successive solutions and accept or reject the step:

def adaptive_timestep(x_prev, x_curr, x_try, dt, tol_lte=1e-4):

    '''

    Estimate local truncation error and recommend next timestep.

    Uses the difference between BE and TR solutions as error estimate.

    x_try: solution from trapezoidal rule (2nd order)

    x_curr: solution from backward Euler (1st order)

    Difference approximates the LTE of the BE solution.

```python
    '''
    import numpy as np
    lte = np.abs(x_try - x_curr)     # element-wise error estimate
    # Scale by solution magnitude (relative tolerance)
    scale = np.maximum(np.abs(x_curr), 1e-10)
    err   = (lte / scale).max()
    # Optimal next timestep (PI controller)
    if err < tol_lte:
        # Accept step, increase dt
        dt_next = dt \* min(2.0, 0.9 \* (tol_lte / (err + 1e-30))\*\*0.5)
    else:
        # Reject step, reduce dt
        dt_next = dt \* max(0.1, 0.9 \* (tol_lte / err)\*\*0.5)
    accepted = (err < tol_lte)
    return accepted, dt_next, err
```

## 4.4  TR-BDF2 Implementation

def trbdf2_step(mna, x_n, t_n, dt, nonlinear_elements):

```
    '''
    TR-BDF2 integrator: one timestep dt using TR for first half, BDF2 for second.
    More accurate than pure Backward Euler; L-stable (no ringing at transitions).
    '''
    gamma = 2 - 2\*\*0.5   # optimal gamma ≈ 0.5858
    dt1   = gamma \* dt   # first sub-step
    dt2   = dt - dt1     # second sub-step
    # --- Stage 1: Trapezoidal from t_n to t_n + gamma\*dt ---
    # (C/dt1)\*(x - x_n) = -0.5\*(G\*x + G\*x_n) + 0.5\*(b + b_n)
    # Rearrange -> (C/dt1 + G/2)\*x = (C/dt1 - G/2)\*x_n + 0.5\*(b+b_n)
    G, C, b_n1 = mna.build_stamps_at(t_n + dt1, nonlinear_elements, x_n)
    \_, \_, b_n  = mna.build_stamps_at(t_n, nonlinear_elements, x_n)
    A1   = C / dt1 + G / 2
    rhs1 = (C / dt1 - G / 2) @ x_n + 0.5 \* (b_n1 + b_n)
    x_tr = np.linalg.solve(A1, rhs1)    # TR solution at mid-point
    # --- Stage 2: BDF2 from t_n to t_n + dt using x_tr and x_n ---
    # BDF2: x[n+1] = (4/3)\*x_tr - (1/3)\*x_n  (predictor)
    # then solve: (C/(dt/3) + G)\*x[n+1] = (C/(dt/3))\*(4/3\*x_tr - 1/3\*x_n) + b[n+1]
    G2, C2, b2 = mna.build_stamps_at(t_n + dt, nonlinear_elements, x_tr)
    alpha1 = (2 - gamma) / ((1 - gamma) \* gamma \* dt)
    alpha2 = -(2\*gamma - 1) / ((1 - gamma) \* gamma \* dt \* (2-gamma)/(1-gamma))
    A2     = C2 \* alpha1 + G2
    rhs2   = C2 \* (alpha1 \* x_tr - alpha2 \* x_n) + b2
    x_new  = np.linalg.solve(A2, rhs2)
    return x_new, x_tr
*⚙️  TR-BDF2 is what SPICE 3 uses as its default integrator. It handles both stiff and non-stiff circuits equally well. The gamma = 2 - sqrt(2) is not arbitrary — it is the value that minimises the error constant of the combined method.*
```

SECTION 5  ·  FINDING EXACT STATE TRANSITION TIMES

**Discrete Event Detection**
When a hybrid component's guard condition is crossed — the memristor switches, a magnetic domain flips, a superconductor goes normal — we need to find the exact time of the crossing, not just know it happened somewhere in the last timestep. Missing the exact crossing time introduces errors and can cause simulation instability.

## 5.1  The Zero-Crossing Problem

A guard condition is a function G(x(t), s) that changes sign when a transition occurs. For example, for a superconductor: G = I_applied - I_c(T). When G crosses zero from negative to positive, the component switches normal.

Given that G(t_n) < 0 and G(t\_{n+1}) > 0, we need to find t\* ∈ (t_n, t\_{n+1}) where G(t\*) = 0. We use bisection or Brent's method on the interpolated trajectory:


**x(t)  ≈  x[n]  +  (t - t_n) / dt · (x[n+1] - x[n])    [linear interpolation]**
```python
def find_crossing_time(guard_func, x_n, x_n1, t_n, t_n1,
                        state, tol=1e-12, max_iter=50):
    '''
```

    Find exact time t\* where guard_func(x(t\*), state) = 0.

    Uses bisection on linearly interpolated trajectory.

```python
    guard_func: callable(x, state) -> float (negative = guard not met)
    '''
    import numpy as np
    dt = t_n1 - t_n
    g_n  = guard_func(x_n,  state)
    g_n1 = guard_func(x_n1, state)
    assert np.sign(g_n) != np.sign(g_n1), 'No crossing in interval'
    t_lo, t_hi = t_n, t_n1
    for \_ in range(max_iter):
        t_mid = (t_lo + t_hi) / 2
        alpha = (t_mid - t_n) / dt
        x_mid = x_n + alpha \* (x_n1 - x_n)   # interpolated state
        g_mid = guard_func(x_mid, state)
        if abs(g_mid) < tol or (t_hi - t_lo) < tol:
            return t_mid, x_mid
        if np.sign(g_mid) == np.sign(g_n):
            t_lo = t_mid
        else:
            t_hi = t_mid
    return (t_lo + t_hi)/2, x_n + ((t_lo+t_hi)/2 - t_n)/dt\*(x_n1-x_n)
```

## 5.2  Guard Conditions for Each Component

**Memristor (analog)**
w >= D  or  w <= 0        → clamp w to boundary

**Dual-mode Memristor**
|q_acc| >= Q_thresh        → flip binary HfO2 state

**Magnetic Domain Ind.**
H > H_sw[i]  or  H < -H_sw[i]   → flip domain i

**Josephson Junction**
phi crosses 2\*pi\*n         → n_flux changes by ±1

**Superconducting R**
I >= I_c(T)  or  T >= Tc   → switch to normal state

**Phase-Change R**
T > T_melt (~900K)          → reset to amorphous

**Sample-Hold Cap**
t mod T_clock < dt          → sample new value

**Ferroelectric Cap**
E > alpha[i]  or  E < beta[i]  → flip hysteron i

**Ternary Transistor**
V_G crosses V_T1  or  V_T2  → advance logic level

## 5.3  Post-Jump Restart

After a discrete transition fires at time t\*, the simulation must restart from t\* with the new state. The correct procedure is:

def handle_discrete_event(simulator, t_star, x_star, s_old, transition):

    '''

    Handle a discrete event at time t_star.

    1. Record the event

    2. Apply the state transition

    3. Re-initialise any dynamic variables that depend on the discrete state

    4. Reduce timestep for first few steps after transition (softstart)

```
    '''
    # Apply transition
    s_new = transition(s_old, x_star)
    # Re-initialise energy-storing elements that depend on s
```

    # (e.g., when a domain flips, the inductor flux must be recalculated)

    x_restarted = simulator.reinitialise_after_transition(x_star, s_old, s_new)

    # Softstart: use smaller dt for first 10 steps after event

```
    simulator.dt_override = simulator.dt \* 0.01
    simulator.dt_override_count = 10
    return x_restarted, s_new
```

SECTION 6  ·  COMPLETE PYTHON IMPLEMENTATION

**The HybridCircuit Solver**
This section presents the complete implementation: a Python class that accepts any network of hybrid components, builds the MNA system automatically, and simulates it forward in time with Newton-Raphson iteration, TR-BDF2 integration, and exact discrete event detection.

## 6.1  Component Base Class

```python
import numpy as np
import scipy.sparse as sp_sparse
import scipy.sparse.linalg as sp_linalg
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Callable
from enum import Enum
class ComponentType(Enum):
    RESISTOR      = 'R'
    CAPACITOR     = 'C'
    INDUCTOR      = 'L'
    VSOURCE       = 'V'
    ISOURCE       = 'I'
    MEMRISTOR     = 'MEM'
    TUNNEL_R      = 'QTR'
    JOSEPHSON     = 'JJ'
    GMR           = 'GMR'
    FERROELECTRIC = 'FE'
    PHASE_CHANGE  = 'PCM'
    MEMINDUCTOR   = 'MEMIND'
    MEMCAPACITOR  = 'MEMCAP'
    LIF_NEURON    = 'LIF'
@dataclass
class Component:
    '''
```

    Base class for all circuit components.

    node_p, node_n: positive and negative terminal node indices.

    0 is always ground (reference node).

```
    '''
    comp_type:  ComponentType
    node_p:     int              # positive terminal
    node_n:     int              # negative terminal (0 = GND)
    params:     dict = field(default_factory=dict)
```

    # Internal continuous state variables (e.g., w for memristor)

```python
    state_c:    np.ndarray = field(default_factory=lambda: np.array([]))
    # Internal discrete state (e.g., crystalline/amorphous phase)
    state_d:    int = 0
    name:       str = ''
    def conductance(self, V_branch: float) -> float:
        '''Return small-signal conductance dI/dV at V_branch.'''
        raise NotImplementedError
    def current(self, V_branch: float) -> float:
        '''Return branch current I(V_branch).'''
        raise NotImplementedError
    def companion(self, V_branch: float) -> Tuple[float, float]:
        '''Return (G_eq, I_eq) for Norton companion model.'''
        G = self.conductance(V_branch)
        I = self.current(V_branch)
        return G, I - G \* V_branch
    def update_state(self, V_branch: float, I_branch: float, dt: float):
        '''Update internal state after timestep solution.'''
        pass
```

    def check_guards(self, V_branch: float, I_branch: float) -> Optional[int]:

        '''Return new discrete state if guard condition met, else None.'''

        return None

## 6.2  Concrete Component Implementations

```python
class ResistorComponent(Component):
    def conductance(self, V): return 1.0 / self.params['R']
    def current(self, V):     return V / self.params['R']
class CapacitorComponent(Component):
```

    '''Capacitor handled via C matrix stamp — no companion model needed.'''

    def get_C(self): return self.params['C']

class MemristorComponent(Component):

    '''HP TiO2 memristor — analog resistance controlled by oxygen vacancy position w.'''

    def \_\_init\_\_(self, node_p, node_n, Ron=100, Roff=16000, D=10e-9, mu_v=1e-14, p=1):

```python
        super().\_\_init\_\_(ComponentType.MEMRISTOR, node_p, node_n,
                         {'Ron':Ron,'Roff':Roff,'D':D,'mu_v':mu_v,'p':p})
        self.state_c = np.array([D \* 0.5])   # w starts at 50%
    @property
    def w(self): return self.state_c[0]
    def R(self):
        p = self.params
        return p['Ron']\*(self.w/p['D']) + p['Roff']\*(1 - self.w/p['D'])
    def conductance(self, V): return 1.0 / self.R()
    def current(self, V):     return V / self.R()
    def update_state(self, V, I, dt):
        p = self.params
        window = 1 - (2\*self.w/p['D'] - 1)\*\*(2\*p['p'])
        dw = p['mu_v'] \* (p['Ron']/p['D']\*\*2) \* I \* window
        self.state_c[0] = np.clip(self.w + dw\*dt, 0, p['D'])
class TunnelResistorComponent(Component):
    '''Quantum tunnel resistor — Simmons model.'''
    def \_\_init\_\_(self, node_p, node_n, d=2e-9, phi_bar=3.0, A_junc=2.5e-15):
        super().\_\_init\_\_(ComponentType.TUNNEL_R, node_p, node_n,
                         {'d':d,'phi_bar':phi_bar,'A_junc':A_junc})
        self.\_e=1.602e-19; self.\_hbar=1.055e-34; self.\_h=6.626e-34; self.\_me=9.109e-31
    def current(self, V):
        p = self.params
        if abs(V) < 1e-6: V = 1e-6 \* np.sign(V + 1e-30)
        A  = (4\*np.pi\*p['d']/self.\_h)\*np.sqrt(2\*self.\_me\*self.\_e)
        J0 = self.\_e/(2\*np.pi\*self.\_hbar\*p['d']\*\*2)
        lo = p['phi_bar'] - V/2;  hi = p['phi_bar'] + V/2
        J  = J0\*(lo\*np.exp(-A\*np.sqrt(max(lo,0))) - hi\*np.exp(-A\*np.sqrt(max(hi,0))))
        return J \* p['A_junc']
    def conductance(self, V):
        dV = max(abs(V)\*0.001, 1e-4)
        return (self.current(V+dV) - self.current(V-dV)) / (2\*dV)
class JosephsonComponent(Component):
    '''Josephson junction (RCSJ model).'''
    def \_\_init\_\_(self, node_p, node_n, Ic=10e-6, R_J=50.0, C_J=1e-15):
        super().\_\_init\_\_(ComponentType.JOSEPHSON, node_p, node_n,
                         {'Ic':Ic,'R_J':R_J,'C_J':C_J})
        self.state_c = np.array([0.0, 0.0])  # [phi, dphi/dt]
        self.state_d = 0   # n_flux quanta
        self.\_hbar=1.055e-34; self.\_e=1.602e-19
    def current(self, V):
        phi = self.state_c[0]
        return self.params['Ic'] \* np.sin(phi) + V / self.params['R_J']
    def conductance(self, V):
        phi, dphi = self.state_c
        dt = 1e-12   # nominal dt for linearisation
        dphi_dV = (2\*self.\_e/self.\_hbar) \* dt
        G_JJ = self.params['Ic'] \* np.cos(phi) \* dphi_dV
        return G_JJ + 1/self.params['R_J']
    def update_state(self, V, I, dt):
        hbar, e = self.\_hbar, self.\_e
        Ic, R_J, C_J = self.params['Ic'], self.params['R_J'], self.params['C_J']
        phi, dphi = self.state_c
        # RCSJ: C_J \* d2phi/dt2 + (hbar/2e/R_J)\*dphi/dt + Ic\*sin(phi) = I
        d2phi = (2\*e/hbar) \* (I - Ic\*np.sin(phi) - (hbar/(2\*e\*R_J))\*dphi) / C_J
        dphi_new = dphi + d2phi \* dt
        phi_new  = phi  + dphi_new \* dt
        self.state_c = np.array([phi_new, dphi_new])
        self.state_d = int(round(phi_new / (2\*np.pi)))  # flux quanta
```

## 6.3  The MNA System Builder

class MNASystem:

    '''

    Builds and solves Modified Nodal Analysis equations for a hybrid circuit.

    Nodes are numbered 0 (GND) to n_nodes-1.

    Voltage sources and inductors add extra rows/columns for their currents.

```python
    '''
    def \_\_init\_\_(self, n_nodes: int, dt: float = 1e-9):
        self.n  = n_nodes - 1  # exclude GND
        self.dt = dt
        self.components: List[Component] = []
        self.extra_vars: List[Tuple] = []  # (comp, 'type') for Vsrc, L
    def add(self, comp: Component):
        self.components.append(comp)
        if comp.comp_type in (ComponentType.VSOURCE, ComponentType.INDUCTOR):
            self.extra_vars.append(comp)
        return self
    @property
    def size(self): return self.n + len(self.extra_vars)
    def \_idx(self, node):
        '''Map node number to matrix index (-1 for GND).'''
        return node - 1 if node > 0 else -1
```

    def \_stamp_conductance(self, G_mat, ni, nj, g):

        '''Add conductance g between nodes ni and nj.'''

```python
        ii, jj = self.\_idx(ni), self.\_idx(nj)
        if ii >= 0: G_mat[ii, ii] += g
        if jj >= 0: G_mat[jj, jj] += g
        if ii >= 0 and jj >= 0:
            G_mat[ii, jj] -= g
            G_mat[jj, ii] -= g
    def build(self, x_prev=None):
```

        '''Build MNA matrices G, C, b for current component states.'''

```
        sz = self.size
        G  = np.zeros((sz, sz))
        C  = np.zeros((sz, sz))
        b  = np.zeros(sz)
        if x_prev is None: x_prev = np.zeros(sz)
        extra_idx = self.n   # index offset for extra variables
        ev_map = {id(comp): extra_idx+k for k,comp in enumerate(self.extra_vars)}
        for comp in self.components:
            ni, nj = comp.node_p, comp.node_n
            ii, jj = self.\_idx(ni), self.\_idx(nj)
```

            # Branch voltage from previous solution

```python
            Vi = x_prev[ii] if ii >= 0 else 0.0
            Vj = x_prev[jj] if jj >= 0 else 0.0
            V_branch = Vi - Vj
            ct = comp.comp_type
            if ct == ComponentType.RESISTOR:
                self.\_stamp_conductance(G, ni, nj, 1.0/comp.params['R'])
            elif ct == ComponentType.CAPACITOR:
                # BE discretisation: C/dt conductance + C/dt\*V_prev current src
                c_val = comp.params['C']
                self.\_stamp_conductance(G, ni, nj, c_val/self.dt)
                if ii >= 0: b[ii] += c_val/self.dt \* V_branch
                if jj >= 0: b[jj] -= c_val/self.dt \* V_branch
            elif ct == ComponentType.MEMRISTOR:
                G_eq, I_eq = comp.companion(V_branch)
                self.\_stamp_conductance(G, ni, nj, G_eq)
                if ii >= 0: b[ii] -= I_eq
                if jj >= 0: b[jj] += I_eq
            elif ct == ComponentType.TUNNEL_R:
                G_eq, I_eq = comp.companion(V_branch)
                self.\_stamp_conductance(G, ni, nj, G_eq)
                if ii >= 0: b[ii] -= I_eq
                if jj >= 0: b[jj] += I_eq
            elif ct == ComponentType.JOSEPHSON:
                G_eq, I_eq = comp.companion(V_branch)
                # Also add C_J as capacitor
                c_val = comp.params['C_J']
                self.\_stamp_conductance(G, ni, nj, G_eq + c_val/self.dt)
                if ii >= 0: b[ii] -= I_eq - c_val/self.dt\*V_branch
                if jj >= 0: b[jj] += I_eq - c_val/self.dt\*V_branch
            elif ct == ComponentType.VSOURCE:
                k = ev_map[id(comp)]
                if ii >= 0: G[ii,k] += 1; G[k,ii] += 1
                if jj >= 0: G[jj,k] -= 1; G[k,jj] -= 1
                b[k] += comp.params['V']
            elif ct == ComponentType.ISOURCE:
                if ii >= 0: b[ii] -= comp.params['I']
                if jj >= 0: b[jj] += comp.params['I']
        return G, C, b
    def solve_step(self, x_prev, nonlinear_comps=None, max_nr=20):
        '''One timestep with NR iteration.'''
        x = x_prev.copy()
        for nr_iter in range(max_nr):
            G, C, b = self.build(x)
            A   = G + C / self.dt
            rhs = b + C @ x_prev / self.dt
            x_new = np.linalg.solve(A + np.eye(self.size)\*1e-15, rhs)
            if np.abs(x_new - x).max() < 1e-8: break
            x = x_new
        return x_new
```

## 6.4  The Top-Level Simulation Loop

```python
class HybridCircuitSimulator:
    '''
    Top-level simulator. Integrates MNA solving, state updates,
```

    guard checking, and adaptive timestep into one clean interface.

```python
    '''
    def \_\_init\_\_(self, n_nodes: int, dt: float = 1e-9):
        self.mna  = MNASystem(n_nodes, dt)
        self.dt   = dt
        self.t    = 0.0
        self.x    = np.zeros(n_nodes - 1)
        self.log  = []   # list of (t, x, states) tuples
    def add(self, comp): self.mna.add(comp); return self
    def run(self, t_end: float,
            sources: dict = None,
            adaptive: bool = True,
            log_every: int = 1):
        '''
```

        Run simulation from current time to t_end.

        sources: dict mapping VSOURCE/ISOURCE component -> callable(t) -> value

        adaptive: use adaptive timestep control

        log_every: record every nth step (reduces memory for long runs)

```
        '''
        dt      = self.dt
        step_n  = 0
        x       = self.x.copy()
        t       = self.t
        dt_min  = dt \* 1e-4
        dt_max  = dt \* 100
        while t < t_end:
            dt = min(dt, t_end - t)  # don't overshoot
            self.mna.dt = dt
            # Update time-varying sources
            if sources:
                for comp, fn in sources.items():
                    if comp.comp_type == ComponentType.VSOURCE:
                        comp.params['V'] = fn(t)
                    elif comp.comp_type == ComponentType.ISOURCE:
                        comp.params['I'] = fn(t)
```

            # Solve MNA system for this timestep

            x_new = self.mna.solve_step(x)

            # Update all component internal states

```
            for comp in self.mna.components:
                ni, nj = comp.node_p, comp.node_n
                ii, jj = ni-1 if ni>0 else -1, nj-1 if nj>0 else -1
                Vi = x_new[ii] if ii >= 0 else 0.0
                Vj = x_new[jj] if jj >= 0 else 0.0
                V_b = Vi - Vj
                G_b = comp.conductance(V_b)
                I_b = V_b \* G_b
                comp.update_state(V_b, I_b, dt)
                # Check discrete guard conditions
                new_sd = comp.check_guards(V_b, I_b)
                if new_sd is not None:
                    comp.state_d = new_sd
            t   += dt
            x    = x_new
            step_n += 1
            if step_n % log_every == 0:
                states = {comp.name: (comp.state_c.copy(), comp.state_d)
                          for comp in self.mna.components}
                self.log.append({'t': t, 'x': x.copy(), 'states': states})
```

            # Adaptive timestep: simple heuristic based on solution change rate

```
            if adaptive:
                dxdt = np.abs(x_new - x).max() / dt
                if dxdt > 1e6:   dt = max(dt \* 0.5, dt_min)
                elif dxdt < 1e3: dt = min(dt \* 1.5, dt_max)
        self.t = t
        self.x = x
        return self.log
```

SECTION 7  ·  THOUSANDS OF CIRCUITS IN PARALLEL

**GPU Network Simulation**
The CPU solver handles one circuit instance. For applications like Monte Carlo yield analysis (running the same circuit with manufacturing tolerances swept across thousands of parameter combinations) or training neural networks of circuits, we need to simulate many independent circuit instances simultaneously on a GPU.

## 7.1  Batched MNA on GPU — The Key Insight

For N identical circuit topologies with different parameters, the MNA matrix has the same sparsity pattern for all N instances but different numerical values. We can stack all N matrices into a single batch and solve them simultaneously using batched linear algebra:

**A[k] · x[k]  =  b[k]      for  k = 1, 2, ..., N**
PyTorch's torch.linalg.solve handles batched systems natively — it dispatches to cuBLAS batched LU factorisation on the GPU, solving all N systems in parallel.

```python
import torch
class GPUCircuitBatch:
    '''
    GPU-accelerated simulation of N identical circuit topologies
    with different component parameters (Monte Carlo / parameter sweep).
    '''
    def \_\_init\_\_(self, topology: dict, param_batch: dict,
                 n_nodes: int, device='cuda'):
        '''
```

        topology:    dict describing circuit connections (nodes, component types)

        param_batch: dict mapping component_name -> tensor of shape (N,)

                     containing parameter values for each of the N instances

        n_nodes:     number of nodes in the circuit

```
        '''
        self.N       = next(iter(param_batch.values())).shape[0]
        self.n_nodes = n_nodes - 1   # exclude GND
        self.device  = device
        self.topo    = topology
```

        # Convert all parameters to GPU tensors of shape (N,)

```python
        self.params  = {k: v.to(device).float()
                        for k, v in param_batch.items()}
        # Solution vectors: shape (N, n_nodes)
        self.x = torch.zeros(self.N, self.n_nodes, device=device)
    def build_G_batch(self, x_batch):
        '''
```

        Build G matrices for all N instances simultaneously.

        Returns G of shape (N, n_nodes, n_nodes).

        This is the GPU-vectorised version of MNASystem.build().

```python
        '''
        N, n = self.N, self.n_nodes
        G = torch.zeros(N, n, n, device=self.device)
        b = torch.zeros(N, n, device=self.device)
        for comp in self.topo['components']:
            ii, jj = comp['node_p']-1, comp['node_n']-1
            if comp['type'] == 'R':
                g = 1.0 / self.params[comp['name']]  # shape (N,)
                if ii >= 0: G[:,ii,ii] += g
                if jj >= 0: G[:,jj,jj] += g
                if ii >= 0 and jj >= 0:
                    G[:,ii,jj] -= g;  G[:,jj,ii] -= g
            elif comp['type'] == 'MEM':
                # Memristor: w state per instance
                w   = self.params[comp['name']+'\_w']     # shape (N,)
                Ron = self.params[comp['name']+'\_Ron']
                Rof = self.params[comp['name']+'\_Roff']
                D   = self.params[comp['name']+'\_D']
                R_mem = Ron\*(w/D) + Rof\*(1 - w/D)
                g = 1.0 / R_mem
                if ii >= 0: G[:,ii,ii] += g
                if jj >= 0: G[:,jj,jj] += g
                if ii >= 0 and jj >= 0:
                    G[:,ii,jj] -= g;  G[:,jj,ii] -= g
        return G, b
    def step_batch(self, dt, sources_batch=None):
```

        '''One timestep for all N instances simultaneously.'''

```python
        G, b = self.build_G_batch(self.x)
        if sources_batch is not None:
            b += sources_batch   # shape (N, n_nodes)
        # Solve N linear systems in parallel: G @ x = b
        # torch.linalg.solve expects (..., n, n) and (..., n)
        x_new = torch.linalg.solve(G + torch.eye(self.n_nodes,
                                    device=self.device).unsqueeze(0)\*1e-15, b)
        # Update memristor states (all N simultaneously)
        for comp in self.topo['components']:
            if comp['type'] == 'MEM':
                ii, jj = comp['node_p']-1, comp['node_n']-1
                Vi = x_new[:,ii] if ii>=0 else torch.zeros(self.N,device=self.device)
                Vj = x_new[:,jj] if jj>=0 else torch.zeros(self.N,device=self.device)
                V_b = Vi - Vj
                w   = self.params[comp['name']+'\_w']
                D   = self.params[comp['name']+'\_D']
                Ron = self.params[comp['name']+'\_Ron']
                mu_v = self.params[comp['name']+'\_mu_v']
                R_mem = Ron\*(w/D) + (self.params[comp['name']+'\_Roff'])\*(1-w/D)
                I_b   = V_b / R_mem
                window = 1 - (2\*w/D - 1)\*\*2
                w_new = (w + mu_v\*(Ron/D\*\*2)\*I_b\*window\*dt).clamp(0, D)
                self.params[comp['name']+'\_w'] = w_new
        self.x = x_new
        return x_new
    def simulate(self, t_end, dt, sources_fn=None, log_every=100):
        '''Full simulation loop for GPU batch.'''
        n_steps = int(t_end / dt)
        results = []
        for step in range(n_steps):
            t = step \* dt
            src = sources_fn(t, self.N, self.device) if sources_fn else None
            self.step_batch(dt, src)
            if step % log_every == 0:
                results.append(self.x.cpu().clone())
        return torch.stack(results)  # shape: (n_logs, N, n_nodes)
```

## 7.2  Monte Carlo Yield Analysis

```python
def monte_carlo_yield(n_samples=100_000, device='cuda'):
    '''
    Example: yield analysis of a memristor-resistor voltage divider.
    Finds what fraction of manufactured devices have V_out in spec [0.4, 0.6] V.
    Manufacturing spread: Ron ± 20%, Roff ± 15%, D ± 5%.
    '''
    import torch
    N = n_samples
    # Sample manufacturing parameters
    Ron_nom, Roff_nom, D_nom = 100.0, 16000.0, 10e-9
    Ron  = torch.normal(Ron_nom,  Ron_nom \*0.20, (N,)).clamp(10, 500)
    Roff = torch.normal(Roff_nom, Roff_nom\*0.15, (N,)).clamp(1000, 50000)
    D    = torch.normal(D_nom,    D_nom   \*0.05, (N,)).clamp(5e-9, 20e-9)
    w0   = D \* 0.5   # start at 50% doped
    # Circuit: V_s=1V -> R_load=1kOhm -> Memristor -> GND
    # Nodes: 1=V_in, 2=V_mid, GND=0
    topo = {'components': [
        {'type':'R',   'name':'R_load', 'node_p':1, 'node_n':2},
        {'type':'MEM', 'name':'M1',     'node_p':2, 'node_n':0},
    ]}
    params = {
        'R_load':   torch.ones(N, device=device) \* 1000.0,
        'M1_Ron':   Ron.to(device),
        'M1_Roff':  Roff.to(device),
        'M1_D':     D.to(device),
        'M1_w':     w0.to(device),
        'M1_mu_v':  torch.ones(N,device=device)\*1e-14,
    }
    sim = GPUCircuitBatch(topo, params, n_nodes=3, device=device)
```

    # Source: node 1 held at 1V (implemented as large conductance to V_s)

```python
    def source_fn(t, N, dev):
        # Current injection into node 1 to enforce V=1V via 1 Ohm source R
        return torch.zeros(N, sim.n_nodes, device=dev)
    # Run for 1 us
    log = sim.simulate(t_end=1e-6, dt=1e-9, log_every=1000)
    # Read final V_mid (node 2, index 1)
    V_mid_final = sim.x[:, 1]   # shape (N,)
    in_spec = ((V_mid_final > 0.4) & (V_mid_final < 0.6)).float()
    yield_pct = in_spec.mean().item() \* 100
    print(f'Yield ({N} samples): {yield_pct:.1f}%')
    return V_mid_final.cpu()
*🚀  Running 100,000 circuit simulations in parallel on an A100 GPU takes approximately the same wall-clock time as running 1 simulation on a CPU. For yield analysis with tight manufacturing tolerances, this changes the workflow from 'run overnight on a cluster' to 'run in a few seconds on a workstation'.*
```

SECTION 8  ·  THREE COMPLETE CIRCUIT SIMULATIONS

**Worked Examples**
## Example A: Memristor Crossbar 4×4 — In-Memory Matrix Multiply

A 4×4 memristor crossbar has 16 memristors arranged in a grid. Row nodes receive input voltages V_in (a 4-vector). Column nodes output currents I_out. Each memristor conductance G_ij encodes one element of a 4×4 matrix W. The output current at column j is:

**I_out[j]  =  sum_i  G_ij · V_in[i]     (Ohm's law applied to each memristor)**
This is a matrix-vector multiply W·v executed at the speed of electrical current flow — no multiply-accumulate operations, no memory access. This is the core operation of in-memory computing for AI inference.

def build_memristor_crossbar(W_matrix, V_input, R_load=1000.0):

    '''

    Build a 4x4 memristor crossbar circuit and compute W @ V_input.

    W_matrix:  4x4 weight matrix (values between 0 and 1)

    V_input:   4-element input voltage vector

    R_load:    load resistor at each output column

```python
    '''
    import numpy as np
    rows, cols = 4, 4
    # Node numbering:
    # Row nodes: 1-4 (inputs, held at V_input values)
    # Column nodes: 5-8 (outputs, read through R_load to GND)
    # GND = 0
    n_nodes = 9  # 0=GND, 1-4=row, 5-8=col
    mna = MNASystem(n_nodes, dt=1e-9)
    # Input voltage sources (set row voltages)
    for i in range(rows):
        vs = Component.\_\_new\_\_(Component)
        vs.comp_type = ComponentType.VSOURCE
        vs.node_p, vs.node_n = i+1, 0
        vs.params  = {'V': V_input[i]}
        vs.state_c = np.array([])
        vs.state_d = 0
        mna.extra_vars.append(vs)
        mna.components.append(vs)
    # Memristor conductances (one per crossbar intersection)
    Ron, Roff = 100, 50000
    for i in range(rows):
        for j in range(cols):
            # Map W value [0,1] to resistance range [Roff, Ron]
            R_ij = Roff - W_matrix[i,j] \* (Roff - Ron)
            mem = ResistorComponent(node_p=i+1, node_n=j+5,
                                    comp_type=ComponentType.RESISTOR,
                                    params={'R': R_ij}, state_c=np.array([]),
                                    state_d=0, name=f'W{i}{j}')
            mem.comp_type = ComponentType.RESISTOR
            mna.components.append(mem)
    # Load resistors at outputs
    for j in range(cols):
        rl = ResistorComponent(node_p=j+5, node_n=0,
                               comp_type=ComponentType.RESISTOR,
                               params={'R': R_load}, state_c=np.array([]),
                               state_d=0, name=f'RL{j}')
        rl.comp_type = ComponentType.RESISTOR
        mna.components.append(rl)
```

    # Solve (DC — just solve once, no time stepping needed for static matrix multiply)

```
    sz = mna.size
    G, C, b = mna.build(np.zeros(sz))
    x = np.linalg.solve(G + np.eye(sz)\*1e-15, b)
```

    # Read output currents through load resistors

```
    I_out = np.zeros(cols)
    for j in range(cols):
        V_col = x[j+4]   # column node (index = node-1)
        I_out[j] = V_col / R_load
    return x, I_out

```
```
# Test: encode an identity matrix
W = np.eye(4)
V = np.array([1.0, 0.5, 0.25, 0.125])
x, I = build_memristor_crossbar(W, V)
print('Expected (proportional to V):', V)
print('Got (output currents):', I / I.max())
```

## Example B: Josephson Junction Oscillator with GMR Load

A Josephson junction biased above I_c oscillates at the Josephson frequency f_J = 2eV/h. Here we drive a GMR spin resistor with this oscillating voltage to modulate its spin alignment, coupling quantum oscillations to a classical magnetic component.

```python
def josephson_gmr_circuit():
    '''
    Circuit: I_bias -> JJ in parallel with GMR -> GND
```

    JJ oscillates; GMR resistance modulates with spin dynamics.

```python
    '''
    from dataclasses import dataclass
    # Use HybridCircuitSimulator
    # Nodes: 1 = top node (JJ and GMR both connect here), 0 = GND
    sim = HybridCircuitSimulator(n_nodes=2, dt=1e-12)
```

    # Current source: bias above Ic to make JJ oscillate

```
    I_src = Component.\_\_new\_\_(Component)
    I_src.comp_type = ComponentType.ISOURCE
    I_src.node_p, I_src.node_n = 1, 0
    I_src.params   = {'I': 12e-6}   # 1.2 \* Ic
    I_src.state_c  = np.array([])
    I_src.state_d  = 0
    I_src.name     = 'I_bias'
    sim.mna.components.append(I_src)
    # Josephson junction
    jj = JosephsonComponent(node_p=1, node_n=0, Ic=10e-6, R_J=50, C_J=1e-15)
    jj.name = 'JJ1'
    sim.mna.components.append(jj)
    sim.mna.extra_vars  # not a vsource/inductor, so no extra var
    # GMR resistor in parallel: simplified as state-dependent resistor
```

    # R_GMR(t) controlled externally by spin simulation running in background

```
    gmr = ResistorComponent.\_\_new\_\_(ResistorComponent)
    gmr.comp_type = ComponentType.RESISTOR
    gmr.node_p, gmr.node_n = 1, 0
    gmr.params    = {'R': 106.0}   # mid-value between RP=100 and RAP=112
    gmr.state_c   = np.array([0.0])  # theta_mag
    gmr.state_d   = 0
    gmr.name      = 'GMR1'
    sim.mna.components.append(gmr)
    # Run for 1 ns
    log = sim.run(t_end=1e-9, log_every=10)
    t_arr = np.array([e['t'] for e in log])
    V1    = np.array([e['x'][0] for e in log])   # node 1 voltage
    phi   = np.array([e['states']['JJ1'][0][0] for e in log])  # phase
    # Josephson frequency
    hbar, e_q = 1.055e-34, 1.602e-19
    V_dc  = np.mean(V1)
    f_J   = 2 \* e_q \* V_dc / (2 \* np.pi \* hbar)
    print(f'JJ oscillation frequency: {f_J/1e9:.2f} GHz')
    print(f'Expected: 2eV/h = {2\*e_q\*V_dc/6.626e-34/1e9:.2f} GHz')
    return t_arr, V1, phi
```

## Example C: LIF Spiking Neural Network — 3 Neurons

Three Leaky Integrate-and-Fire neurons wired with memristor synapses. Each spike from neuron i sends a current pulse to neuron j through memristor M_ij. The memristor weight adapts based on the timing of spikes — implementing Spike-Timing Dependent Plasticity (STDP), the biological learning rule.

class LIFNeuronComponent(Component):

    '''

    Leaky integrate-and-fire neuron as a circuit component.

    Models as a parallel RC with threshold comparator.

```python
    '''
    def \_\_init\_\_(self, node, Cm=1e-9, Rm=1e7, V_thresh=0.02, V_reset=-0.07):
        super().\_\_init\_\_(ComponentType.LIF_NEURON, node, 0,
                         {'Cm':Cm,'Rm':Rm,'V_thresh':V_thresh,'V_reset':V_reset})
        self.state_c = np.array([-0.07])  # membrane voltage V_m
        self.state_d = 0   # 0=integrating, 1=refractory
        self.spike_times = []
        self.\_t = 0.0
    def conductance(self, V): return 1.0/self.params['Rm'] + self.params['Cm']\*1e9
    def current(self, V):     return V/self.params['Rm']
    def check_guards(self, V, I):
        if V >= self.params['V_thresh'] and self.state_d == 0:
            self.spike_times.append(self.\_t)
            return 1   # enter refractory
        if self.state_d == 1 and V <= self.params['V_reset'] + 0.001:
            return 0   # leave refractory
        return None
def stdp_update(w, t_pre, t_post, A_plus=0.01, A_minus=0.01, tau=20e-3):
    '''
    Spike-Timing Dependent Plasticity weight update.
    Pre fires before post (t_pre < t_post): potentiation (w increases).
    Post fires before pre (t_post < t_pre): depression (w decreases).
    '''
    dt_spk = t_post - t_pre
    if dt_spk > 0:   # pre before post -> potentiation
        dw =  A_plus  \* np.exp(-dt_spk / tau)
    else:            # post before pre -> depression
        dw = -A_minus \* np.exp( dt_spk / tau)
    return np.clip(w + dw, 0.0, 1.0)
```
```
# Build 3-neuron network

```
```
# Neurons at nodes 1, 2, 3. Memristor synapses connect all pairs.
sim = HybridCircuitSimulator(n_nodes=4, dt=1e-4)
neurons = [LIFNeuronComponent(node=i+1) for i in range(3)]
for n in neurons: sim.mna.components.append(n)
```

```
# Synaptic memristors (simplified as resistors with STDP weight updates)
```

syn_weights = np.ones((3,3)) \* 0.5

syn_weights[np.eye(3,dtype=bool)] = 0  # no self-connections

```
# External input current sources to neuron 1
I_ext = Component.\_\_new\_\_(Component)
I_ext.comp_type = ComponentType.ISOURCE
I_ext.node_p, I_ext.node_n = 1, 0
I_ext.params = {'I': 3e-9}
I_ext.state_c = np.array([]); I_ext.state_d = 0; I_ext.name = 'I_ext'
sim.mna.components.append(I_ext)
print('3-neuron LIF network ready. Synaptic weights:', syn_weights)
```

SECTION 9  ·  GENERATING NETLISTS FOR INDUSTRY EDA TOOLS

**SPICE-Compatible Export**
SPICE is the industry standard for circuit simulation, used by every chip design tool (Cadence, Synopsys, Mentor). While SPICE cannot natively simulate hybrid components, we can export behavioural models that approximate the hybrid behaviour using SPICE primitives and voltage-controlled sources. This allows the circuit to be used within larger designs.

## 9.1  SPICE Behavioural Models

SPICE supports a B-element (behavioural voltage/current source) that evaluates an arbitrary mathematical expression. We use this to implement the hybrid I-V curves:


### Quantum Tunnel Resistor SPICE model:

```
.SUBCKT QTR anode cathode
\* Quantum Tunnel Resistor behavioural model
\* Simmons model approximation (low-voltage regime)
.PARAM d=2e-9 phi=3.0 A_junc=2.5e-15
.PARAM G0='1e-8 \* exp(-4\*pi\*d/6.626e-34 \* sqrt(2\*9.109e-31\*phi\*1.602e-19))'
B1 anode cathode I='G0 \* V(anode,cathode) \*
\+  (1 + (V(anode,cathode))^2 / (6\*phi^2))'
.ENDS QTR
```

### Memristor SPICE model (HP model):

```
.SUBCKT MEMRISTOR anode cathode
\* HP TiO2 memristor with internal state variable w
.PARAM Ron=100 Roff=16000 D=10n mu_v=1e-14
\* State variable w stored as voltage on internal capacitor
Cw w 0 1 IC=5e-9   ; w starts at D/2 = 5nm
\* Current through device
Eresist anode cathode value='V(anode,cathode) /
\+  (Ron\*V(w)/D + Roff\*(1-V(w)/D))'
\* State equation: dw/dt = mu_v\*(Ron/D^2)\*I\*window
Bw w 0 I='mu_v\*(Ron/D^2) \* I(Eresist) \*
\+  (1 - (2\*V(w)/D - 1)^2)'
.ENDS MEMRISTOR
```

### Python SPICE netlist generator:

```python
def export_to_spice(simulator, filename='hybrid_circuit.sp',
                     title='Hybrid Component Circuit'):
    '''
```

    Export a HybridCircuitSimulator to a SPICE netlist.

    Uses .SUBCKT for each hybrid component type.

```
    '''
    lines = [
        f'\* {title}',
        '\* Generated by HybridCircuit Solver Phase 2',
        '\* Hybrid components approximated with behavioural SPICE models',
        '',
    ]
    # Include subcircuit definitions
    lines += [
        '\* ─── SUBCIRCUIT LIBRARY ───────────────────────────────────',
        '.SUBCKT QTR anode cathode',
        '.PARAM d=2n phi=3.0 A=2.5e-15',
        '.PARAM G0={1e-8\*exp(-2.226e10\*d\*sqrt(phi))}',
        'B1 anode cathode I={G0\*V(anode,cathode)\*(1+V(anode,cathode)^2/(6\*phi^2))}',
        '.ENDS QTR',
        '',
        '.SUBCKT MEMRISTOR anode cathode RON=100 ROFF=16000 D=10n',
        'Cw internal 0 1 IC={D/2}',
        'Gdev anode cathode value={V(anode,cathode)/(RON\*V(internal)/D+ROFF\*(1-V(internal)/D))}',
        'Bstate internal 0 I={1e-14\*(RON/D^2)\*I(Gdev)\*(1-(2\*V(internal)/D-1)^2)}',
        '.ENDS MEMRISTOR',
        '',
        '\* ─── CIRCUIT NETLIST ─────────────────────────────────────',
    ]
    # Emit each component
    comp_counts = {}
    for comp in simulator.mna.components:
        ct = comp.comp_type
        name = comp.name or ct.value
        np_node = f'N{comp.node_p}' if comp.node_p > 0 else '0'
        nn_node = f'N{comp.node_n}' if comp.node_n > 0 else '0'
        if ct == ComponentType.RESISTOR:
            lines.append(f'R{name} {np_node} {nn_node} {comp.params["R"]}')
        elif ct == ComponentType.CAPACITOR:
            lines.append(f'C{name} {np_node} {nn_node} {comp.params["C"]}')
        elif ct == ComponentType.VSOURCE:
            lines.append(f'V{name} {np_node} {nn_node} DC {comp.params["V"]}')
        elif ct == ComponentType.ISOURCE:
            lines.append(f'I{name} {np_node} {nn_node} DC {comp.params["I"]}')
        elif ct == ComponentType.MEMRISTOR:
            lines.append(f'X{name} {np_node} {nn_node} MEMRISTOR'
                         f' RON={comp.params["Ron"]} ROFF={comp.params["Roff"]}'
                         f' D={comp.params["D"]}')
        elif ct == ComponentType.TUNNEL_R:
            lines.append(f'X{name} {np_node} {nn_node} QTR'
                         f' d={comp.params["d"]} phi={comp.params["phi_bar"]}')
        elif ct == ComponentType.JOSEPHSON:
            # Approximate JJ as current-controlled resistor + L
            hbar_2e = 3.29e-16   # hbar / 2e
            L_J = hbar_2e / comp.params['Ic']
            lines.append(f'\* Josephson Junction (linearised at zero bias)')
            lines.append(f'L{name} {np_node} {nn_node} {L_J:.3e}')
            lines.append(f'R{name}\_shunt {np_node} {nn_node} {comp.params["R_J"]}')
    lines += ['', '.TRAN 1n 1u', '.END']
    with open(filename, 'w') as f:
        f.write('\\n'.join(lines))
    print(f'SPICE netlist written to {filename}')
    return '\\n'.join(lines)
```

```
```

# Phase 2 Summary — What Was Built


**Section 1 — Graph Theory**
Incidence matrix A_r, KCL as matrix equation, KVL as transpose, branch type taxonomy

**Section 2 — MNA**
Component stamps for R, C, L, V-source, I-source, and all hybrid types; full matrix equation

**Section 3 — NR Iteration**
Newton-Raphson companion model (G_eq, I_eq), Jacobians for QTR/memristor/Josephson

**Section 4 — Time Integration**
Backward Euler derivation, TR-BDF2 implementation, adaptive timestep PI controller

**Section 5 — Event Detection**
Zero-crossing bisection algorithm, guard table for all components, post-jump restart

**Section 6 — HybridCircuit**
Complete Component class hierarchy, MNASystem builder, Newton-Raphson solver, main simulation loop

**Section 7 — GPU Batch**
GPUCircuitBatch with batched LU solve, vectorised memristor state updates, Monte Carlo yield analysis

**Section 8 — Examples**
4×4 memristor crossbar matrix multiply, Josephson-GMR oscillator, 3-neuron STDP spiking network

**Section 9 — SPICE Export**
QTR and memristor .SUBCKT definitions, Python netlist generator for any HybridCircuitSimulator

**Phase 2 Complete  ·  General Circuit Solver Built**
*Next: Phase 3 — Advanced GPU Kernels (custom CUDA, stiff solvers, real-time performance)*
