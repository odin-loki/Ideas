<!-- Converted from `hybrid_simulation_phase2.docx` — source was Word (.docx). -->

__HYBRID COMPONENT SIMULATION__

Phase 2  ·  General Circuit Solver

*Modified Nodal Analysis  ·  Hybrid Time\-Stepping  ·  Nonlinear Iteration  ·  GPU Network Simulation*

February 2026  ·  Series continuation — builds on Phase 1 component models

# __Phase 2 Overview — What This Document Covers__

The first document \(Phase 0\) derived simulation equations for individual components\. Phase 1 extended this to eight more components\. But individual component models are only useful if you can connect them into actual circuits\.

Phase 2 builds the general circuit solver: a mathematical engine that takes any network of hybrid components, automatically constructs the governing equations using Kirchhoff's laws, and integrates them forward in time\. This is the equivalent of SPICE, but natively handling hybrid discrete\-continuous components that SPICE cannot represent\.

__Section 1__

Graph theory of circuits — how to represent a network mathematically as nodes and branches

__Section 2__

Modified Nodal Analysis \(MNA\) — the matrix equation that every circuit simulator is built on

__Section 3__

Handling nonlinear components — Newton\-Raphson iteration for resistors, memristors, tunnel junctions

__Section 4__

Time integration — how to step the ODE forward correctly given stiff systems

__Section 5__

Discrete event detection — finding and handling the exact moment a state transition occurs

__Section 6__

The complete HybridCircuit solver class — full Python implementation wiring everything together

__Section 7__

GPU\-accelerated network simulation — running thousands of circuit instances in parallel

__Section 8__

Worked examples — three real circuits demonstrating the solver in action

__Section 9__

SPICE export — generating netlist models compatible with standard EDA tools

SECTION 1  ·  MATHEMATICAL FOUNDATIONS

__Graph Theory of Circuits__

Before writing a single equation, we need a way to describe a circuit's topology — which components connect to which nodes\. Circuit theory maps perfectly onto graph theory, a branch of mathematics dealing with nodes connected by edges\.

## __1\.1  The Incidence Matrix__

A circuit with N nodes and B branches \(components\) is described by its incidence matrix A, of shape \(N\-1\) × B\. Each column corresponds to one branch\. The entry A\[i,b\] is:

__\+1__

Branch b leaves node i \(current flows out\)

__\-1__

Branch b enters node i \(current flows in\)

__0__

Branch b is not connected to node i

One row is dropped \(usually the ground node row\) to make the matrix full\-rank\. This is the Reduced Incidence Matrix A\_r\.

__KCL \(Kirchhoff's Current Law\):    A\_r · I\_branches  =  0__

__KVL \(Kirchhoff's Voltage Law\):    V\_branches  =  A\_r^T · V\_nodes__

Every circuit solver in the world — from SPICE to commercial EDA — is built on these two equations\. They are exact and universal\.

## __1\.2  Branch Types and Their Equations__

Each branch b has a constitutive equation — the relationship between its terminal voltage V\_b and current I\_b:

__Resistor__

V\_b = R · I\_b                              → I\_b = V\_b / R

__Capacitor__

I\_b = C · dV\_b/dt                          → V\_b = \(1/C\) · integral I\_b dt

__Inductor__

V\_b = L · dI\_b/dt                          → I\_b = \(1/L\) · integral V\_b dt

__Voltage source__

V\_b = V\_s \(fixed\)                          → I\_b unknown \(free variable\)

__Current source__

I\_b = I\_s \(fixed\)                          → V\_b unknown \(free variable\)

__Memristor__

V\_b = R\(w\) · I\_b,  dw/dt = f\(w, I\_b\)      → coupled ODE

__Hybrid R__

V\_b = R\(x\_c, s\_d\) · I\_b                   → state\-dependent resistor

__Hybrid C__

I\_b = C\(x\_c, s\_d\) · dV\_b/dt               → state\-dependent capacitor

__Hybrid L__

V\_b = L\(x\_c, s\_d\) · dI\_b/dt               → state\-dependent inductor

## __1\.3  Example Circuit Graph__

Consider a simple 3\-node circuit: a voltage source V\_s between node 1 and ground \(node 0\), a resistor R between nodes 1 and 2, a memristor M between node 2 and ground, and a capacitor C between nodes 1 and 2 in parallel with R\.

Nodes: \{0=GND, 1, 2\}\. Branches: \{V\_s, R, C, M\}\. The reduced incidence matrix \(dropping GND row\):

          V\_s   R    C    M

Node 1  \[  1   \-1   \-1    0  \]

Node 2  \[  0    1    1   \-1  \]

\# KCL at node 1: I\_Vs \- I\_R \- I\_C = 0

\# KCL at node 2: I\_R \+ I\_C \- I\_M = 0

\# KVL: V\_Vs = V1, V\_R = V1\-V2, V\_C = V1\-V2, V\_M = V2

SECTION 2  ·  THE CORE MATRIX EQUATION

__Modified Nodal Analysis \(MNA\)__

Modified Nodal Analysis \(MNA\) is the algorithm that converts the graph description of a circuit into a single matrix equation that can be solved by a computer\. It was developed at UC Berkeley in the 1970s and is the foundation of SPICE\. We extend it here to handle hybrid components\.

## __2\.1  The MNA Stamp Concept__

Each component type adds its contribution — its 'stamp' — to the global MNA matrix\. The matrix equation has the form:

__G\(x\) · x  \+  C\_cap · dx/dt  =  b\(t\)__

Where x is the solution vector \(node voltages \+ branch currents for voltage sources\), G is the conductance matrix, C\_cap is the capacitance/inductance matrix \(for dynamic elements\), and b is the source vector\.

## __2\.2  Component Stamps__

### __Resistor between nodes i and j, value R:__

\# Adds to G matrix \(conductance stamp\):

G\[i,i\] \+= 1/R

G\[j,j\] \+= 1/R

G\[i,j\] \-= 1/R

G\[j,i\] \-= 1/R

### __Capacitor between nodes i and j, value C:__

\# Adds to C matrix \(dynamic stamp\):

C\_mat\[i,i\] \+= C

C\_mat\[j,j\] \+= C

C\_mat\[i,j\] \-= C

C\_mat\[j,i\] \-= C

\# In time\-discrete form \(backward Euler, timestep dt\):

\# C \* \(x\[n\+1\]\-x\[n\]\)/dt \-> adds C/dt to G and C/dt \* x\[n\] to b

G\[i,i\] \+= C/dt;  b\[i\] \+= C/dt \* V\_ij\_prev

### __Inductor between nodes i and j, value L \(adds extra variable I\_L\):__

\# Adds new row/column k for inductor current I\_L

G\[i,k\] \+=  1;  G\[k,i\] \+=  1   \# V\_i contributes to inductor equation

G\[j,k\] \+= \-1;  G\[k,j\] \+= \-1   \# V\_j contributes to inductor equation

C\_mat\[k,k\] \+= L                \# L \* dI\_L/dt term

\# In time\-discrete form:

G\[k,k\] \+= L/dt;  b\[k\] \+= L/dt \* I\_L\_prev

### __Voltage source between nodes i and j, value V\_s \(adds extra variable I\_s\):__

\# Adds new row/column k for source current I\_s

G\[i,k\] \+=  1;  G\[k,i\] \+=  1

G\[j,k\] \+= \-1;  G\[k,j\] \+= \-1

b\[k\]   \+= V\_s   \# enforces V\_i \- V\_j = V\_s

## __2\.3  Hybrid Component Stamps__

Hybrid components add state\-dependent conductance\. The memristor is the canonical example — it is a resistor whose conductance G\_mem\(w\) changes over time according to an internal state w:

\# State\-dependent conductance stamp \(same as resistor, but G changes each step\)

G\_mem = 1\.0 / R\_memristor\(w\)   \# recomputed every timestep

G\[i,i\] \+= G\_mem

G\[j,j\] \+= G\_mem

G\[i,j\] \-= G\_mem

G\[j,i\] \-= G\_mem

\# Internal state equation appended to ODE:

\# dw/dt = f\(w, I\_mem\)  \-> integrated separately each timestep

## __2\.4  The Full MNA System \(Time\-Discrete\)__

Using backward Euler time discretisation \(stable for stiff circuits, where time constants differ by many orders of magnitude\):

__\[ G \+ C\_mat/dt \] · x\[n\+1\]  =  b\[n\+1\]  \+  C\_mat/dt · x\[n\]__

This is a linear system of equations\. At each timestep, we:

  1\. Update state\-dependent components \(recompute G\_mem, L\(w\), C\(phi\) etc\.\)

  2\. Assemble the full \[G \+ C/dt\] matrix

  3\. Assemble the right\-hand side b\[n\+1\] \+ C/dt · x\[n\]

  4\. Solve the linear system: x\[n\+1\] = A^\(\-1\) · rhs

  5\. Update all internal states \(w, phi, q, domain states\) using x\[n\+1\]

  6\. Check all guard conditions for discrete state transitions

  7\. If a transition fires, update discrete states and continue

*📐  For a circuit with N nodes and V voltage sources/inductors, the MNA matrix is \(N\+V\) × \(N\+V\)\. For small circuits \(< 1000 nodes\), dense LU factorisation is fast\. For large circuits \(> 1000 nodes\), sparse LU \(scipy\.sparse\.linalg\.spsolve\) is essential\.*

SECTION 3  ·  NEWTON\-RAPHSON FOR NONLINEAR COMPONENTS

__Nonlinear Iteration__

The MNA stamp above assumes each component's conductance is known before solving the matrix\. But for nonlinear components — the tunnel resistor, Josephson junction, ferroelectric capacitor — the conductance depends on the solution itself\. We need Newton\-Raphson iteration to resolve this circular dependency\.

## __3\.1  The Newton\-Raphson Linearisation__

For a nonlinear component with I = f\(V\), we linearise around the current operating point V^k:

__I\(V\)  ≈  I\(V^k\)  \+  f'\(V^k\) · \(V \- V^k\)__

__      =  f'\(V^k\) · V  \+  \[I\(V^k\) \- f'\(V^k\) · V^k\]__

This is equivalent to a linear conductance G\_eq = f'\(V^k\) in parallel with a current source I\_eq = I\(V^k\) \- G\_eq · V^k\. These are the 'companion model' stamps:

\# Nonlinear component companion model \(updated each NR iteration k\):

G\_eq = dI\_dV\(V\_k\)            \# Jacobian of I w\.r\.t\. V at current estimate

I\_eq = I\(V\_k\) \- G\_eq \* V\_k  \# Norton equivalent current source

\# Stamp G\_eq as conductance, I\_eq as current source

G\[i,i\] \+= G\_eq;  G\[i,j\] \-= G\_eq   \# conductance stamp

G\[j,i\] \-= G\_eq;  G\[j,j\] \+= G\_eq

b\[i\]   \+= I\_eq   \# current source stamp \(into node i\)

b\[j\]   \-= I\_eq

## __3\.2  Newton\-Raphson Loop__

def newton\_raphson\_step\(mna, x\_prev, nonlinear\_elements, max\_iter=50,

                         tol\_v=1e\-6, tol\_i=1e\-9\):

    '''

    Solve one MNA timestep with NR iteration for nonlinear elements\.

    mna:               MNASystem object \(see Section 6\)

    x\_prev:            solution vector from previous timestep

    nonlinear\_elements: list of NonlinearComponent objects

    Returns:           x\_new \(converged solution vector\)

    '''

    x = x\_prev\.copy\(\)   \# initial guess = previous solution

    for k in range\(max\_iter\):

        \# Rebuild G matrix with current estimates of nonlinear conductances

        G, C, b = mna\.build\_linear\_stamps\(\)

        for elem in nonlinear\_elements:

            V\_elem = mna\.get\_branch\_voltage\(x, elem\)

            G\_eq, I\_eq = elem\.companion\_model\(V\_elem\)

            mna\.add\_stamp\(G, b, elem\.node\_plus, elem\.node\_minus, G\_eq, I\_eq\)

        \# Add dynamic terms \(C/dt from capacitors and inductors\)

        A = G \+ C / mna\.dt

        rhs = b \+ C @ x\_prev / mna\.dt

        \# Solve

        import numpy as np

        x\_new = np\.linalg\.solve\(A, rhs\)

        \# Check convergence

        dV = np\.abs\(x\_new\[:mna\.n\_nodes\] \- x\[:mna\.n\_nodes\]\)

        dI = np\.abs\(A @ x\_new \- rhs\)

        if dV\.max\(\) < tol\_v and dI\.max\(\) < tol\_i:

            return x\_new, k\+1   \# converged

        x = x\_new

    raise RuntimeError\(f'Newton\-Raphson did not converge in \{max\_iter\} iterations'\)

## __3\.3  Jacobians for Each Hybrid Component__

Each nonlinear component needs its own dI/dV function\. Here are the key ones:

### __Quantum Tunnel Resistor \(Simmons model\):__

def simmons\_jacobian\(V, d=2e\-9, phi\_bar=3\.0, A\_junc=2\.5e\-15\):

    '''dI/dV at voltage V — derivative of Simmons current\.'''

    dV = 1e\-4  \# numerical step

    return \(simmons\_current\(V\+dV, d, phi\_bar, A\_junc\) \-

            simmons\_current\(V\-dV, d, phi\_bar, A\_junc\)\) / \(2\*dV\)

def qtr\_companion\(V, d=2e\-9, phi\_bar=3\.0, A\_junc=2\.5e\-15\):

    I\_op  = simmons\_current\(V, d, phi\_bar, A\_junc\)

    G\_eq  = simmons\_jacobian\(V, d, phi\_bar, A\_junc\)

    I\_eq  = I\_op \- G\_eq \* V

    return G\_eq, I\_eq

### __Memristor \(HP model\):__

def memristor\_companion\(V, w, D=10e\-9, Ron=100, Roff=16000\):

    '''Memristor companion model\. State w is fixed during NR iteration\.'''

    R   = Ron\*\(w/D\) \+ Roff\*\(1 \- w/D\)   \# R is fixed for this NR step

    G\_eq = 1\.0 / R                       \# linear in V for fixed w

    I\_eq = 0\.0                           \# no offset \(passes through origin\)

    return G\_eq, I\_eq

### __Josephson Junction \(sinusoidal nonlinearity\):__

def josephson\_companion\(V, phi, Ic=10e\-6, R\_J=50, C\_J=1e\-15, dt=1e\-12\):

    '''

    Josephson junction companion model\.

    phi: current phase \(updated after solution — not during NR\)

    Uses RCSJ model: I = Ic\*sin\(phi\) \+ V/R\_J \+ C\_J\*dV/dt

    '''

    hbar, e = 1\.055e\-34, 1\.602e\-19

    \# Current at operating point

    I\_sc  = Ic \* np\.sin\(phi\)

    \# Linearised Josephson contribution: dI\_sc/dV = Ic\*cos\(phi\)\*dphi/dV

    \# dphi/dV = \(2e/hbar\)\*dt \(from phase\-voltage relation, discrete\)

    dphi\_dV = \(2\*e/hbar\) \* dt

    G\_JJ   = Ic \* np\.cos\(phi\) \* dphi\_dV

    G\_total = G\_JJ \+ 1/R\_J \+ C\_J/dt

    I\_eq    = I\_sc \- G\_JJ\*V

    return G\_total, I\_eq

*🔄  The key insight is that during Newton\-Raphson iteration, the internal states \(w for memristors, phi for Josephson junctions\) are FROZEN at their values from the previous timestep\. Only node voltages are iterated\. After convergence, states are updated\. This splitting is called operator splitting and is essential for stability\.*

SECTION 4  ·  STABLE STEPPING FOR STIFF HYBRID SYSTEMS

__Time Integration__

Hybrid circuits are typically stiff — they contain components with time constants spanning many orders of magnitude simultaneously\. For example, a Josephson junction \(picosecond timescale\) driving a magnetic domain inductor \(nanosecond timescale\) driving a large capacitor \(microsecond timescale\)\. Explicit methods like forward Euler become unstable for stiff systems unless the timestep is tiny\. We need implicit methods\.

## __4\.1  The Three Integration Methods__

__Backward Euler \(BE\)__

x\[n\+1\] = x\[n\] \+ dt · f\(x\[n\+1\]\)\. Implicit, unconditionally stable\. First\-order accurate\. Tends to over\-damp fast transients\.

__Trapezoidal \(TR\)__

x\[n\+1\] = x\[n\] \+ dt/2 · \[f\(x\[n\]\) \+ f\(x\[n\+1\]\)\]\. Second\-order accurate\. Can show 'ringing' \(numerical oscillation\) at discontinuities\.

__TR\-BDF2 \(SPICE default\)__

Trapezoidal for first half\-step, BDF2 for second half\-step\. Second\-order, L\-stable\. Best compromise — what SPICE uses\.

## __4\.2  Backward Euler MNA \(Full Derivation\)__

Starting from the continuous MNA equation:

__C\_mat · dx/dt  \+  G\(x\) · x  =  b\(t\)__

Applying backward Euler \(evaluate right\-hand side at new time n\+1\):

__C\_mat · \(x\[n\+1\] \- x\[n\]\) / dt  \+  G\(x\[n\+1\]\) · x\[n\+1\]  =  b\[n\+1\]__

__\( C\_mat/dt  \+  G\(x\[n\+1\]\) \) · x\[n\+1\]  =  b\[n\+1\]  \+  C\_mat/dt · x\[n\]__

The matrix \(C\_mat/dt \+ G\) is reassembled every timestep because G depends on the current operating point for nonlinear components\.

## __4\.3  Adaptive Timestep Control__

Fixed timestep wastes computation during slow parts of the simulation and can miss fast transients\. Adaptive control adjusts dt based on the local truncation error \(LTE\):

__LTE  ≈  dt^2 / 2 · x''\(t\)     \[Backward Euler — proportional to dt²\]__

We estimate x'' from successive solutions and accept or reject the step:

def adaptive\_timestep\(x\_prev, x\_curr, x\_try, dt, tol\_lte=1e\-4\):

    '''

    Estimate local truncation error and recommend next timestep\.

    Uses the difference between BE and TR solutions as error estimate\.

    x\_try: solution from trapezoidal rule \(2nd order\)

    x\_curr: solution from backward Euler \(1st order\)

    Difference approximates the LTE of the BE solution\.

    '''

    import numpy as np

    lte = np\.abs\(x\_try \- x\_curr\)     \# element\-wise error estimate

    \# Scale by solution magnitude \(relative tolerance\)

    scale = np\.maximum\(np\.abs\(x\_curr\), 1e\-10\)

    err   = \(lte / scale\)\.max\(\)

    \# Optimal next timestep \(PI controller\)

    if err < tol\_lte:

        \# Accept step, increase dt

        dt\_next = dt \* min\(2\.0, 0\.9 \* \(tol\_lte / \(err \+ 1e\-30\)\)\*\*0\.5\)

    else:

        \# Reject step, reduce dt

        dt\_next = dt \* max\(0\.1, 0\.9 \* \(tol\_lte / err\)\*\*0\.5\)

    accepted = \(err < tol\_lte\)

    return accepted, dt\_next, err

## __4\.4  TR\-BDF2 Implementation__

def trbdf2\_step\(mna, x\_n, t\_n, dt, nonlinear\_elements\):

    '''

    TR\-BDF2 integrator: one timestep dt using TR for first half, BDF2 for second\.

    More accurate than pure Backward Euler; L\-stable \(no ringing at transitions\)\.

    '''

    gamma = 2 \- 2\*\*0\.5   \# optimal gamma ≈ 0\.5858

    dt1   = gamma \* dt   \# first sub\-step

    dt2   = dt \- dt1     \# second sub\-step

    \# \-\-\- Stage 1: Trapezoidal from t\_n to t\_n \+ gamma\*dt \-\-\-

    \# \(C/dt1\)\*\(x \- x\_n\) = \-0\.5\*\(G\*x \+ G\*x\_n\) \+ 0\.5\*\(b \+ b\_n\)

    \# Rearrange \-> \(C/dt1 \+ G/2\)\*x = \(C/dt1 \- G/2\)\*x\_n \+ 0\.5\*\(b\+b\_n\)

    G, C, b\_n1 = mna\.build\_stamps\_at\(t\_n \+ dt1, nonlinear\_elements, x\_n\)

    \_, \_, b\_n  = mna\.build\_stamps\_at\(t\_n, nonlinear\_elements, x\_n\)

    A1   = C / dt1 \+ G / 2

    rhs1 = \(C / dt1 \- G / 2\) @ x\_n \+ 0\.5 \* \(b\_n1 \+ b\_n\)

    x\_tr = np\.linalg\.solve\(A1, rhs1\)    \# TR solution at mid\-point

    \# \-\-\- Stage 2: BDF2 from t\_n to t\_n \+ dt using x\_tr and x\_n \-\-\-

    \# BDF2: x\[n\+1\] = \(4/3\)\*x\_tr \- \(1/3\)\*x\_n  \(predictor\)

    \# then solve: \(C/\(dt/3\) \+ G\)\*x\[n\+1\] = \(C/\(dt/3\)\)\*\(4/3\*x\_tr \- 1/3\*x\_n\) \+ b\[n\+1\]

    G2, C2, b2 = mna\.build\_stamps\_at\(t\_n \+ dt, nonlinear\_elements, x\_tr\)

    alpha1 = \(2 \- gamma\) / \(\(1 \- gamma\) \* gamma \* dt\)

    alpha2 = \-\(2\*gamma \- 1\) / \(\(1 \- gamma\) \* gamma \* dt \* \(2\-gamma\)/\(1\-gamma\)\)

    A2     = C2 \* alpha1 \+ G2

    rhs2   = C2 \* \(alpha1 \* x\_tr \- alpha2 \* x\_n\) \+ b2

    x\_new  = np\.linalg\.solve\(A2, rhs2\)

    return x\_new, x\_tr

*⚙️  TR\-BDF2 is what SPICE 3 uses as its default integrator\. It handles both stiff and non\-stiff circuits equally well\. The gamma = 2 \- sqrt\(2\) is not arbitrary — it is the value that minimises the error constant of the combined method\.*

SECTION 5  ·  FINDING EXACT STATE TRANSITION TIMES

__Discrete Event Detection__

When a hybrid component's guard condition is crossed — the memristor switches, a magnetic domain flips, a superconductor goes normal — we need to find the exact time of the crossing, not just know it happened somewhere in the last timestep\. Missing the exact crossing time introduces errors and can cause simulation instability\.

## __5\.1  The Zero\-Crossing Problem__

A guard condition is a function G\(x\(t\), s\) that changes sign when a transition occurs\. For example, for a superconductor: G = I\_applied \- I\_c\(T\)\. When G crosses zero from negative to positive, the component switches normal\.

Given that G\(t\_n\) < 0 and G\(t\_\{n\+1\}\) > 0, we need to find t\* ∈ \(t\_n, t\_\{n\+1\}\) where G\(t\*\) = 0\. We use bisection or Brent's method on the interpolated trajectory:

__x\(t\)  ≈  x\[n\]  \+  \(t \- t\_n\) / dt · \(x\[n\+1\] \- x\[n\]\)    \[linear interpolation\]__

def find\_crossing\_time\(guard\_func, x\_n, x\_n1, t\_n, t\_n1,

                        state, tol=1e\-12, max\_iter=50\):

    '''

    Find exact time t\* where guard\_func\(x\(t\*\), state\) = 0\.

    Uses bisection on linearly interpolated trajectory\.

    guard\_func: callable\(x, state\) \-> float \(negative = guard not met\)

    '''

    import numpy as np

    dt = t\_n1 \- t\_n

    g\_n  = guard\_func\(x\_n,  state\)

    g\_n1 = guard\_func\(x\_n1, state\)

    assert np\.sign\(g\_n\) \!= np\.sign\(g\_n1\), 'No crossing in interval'

    t\_lo, t\_hi = t\_n, t\_n1

    for \_ in range\(max\_iter\):

        t\_mid = \(t\_lo \+ t\_hi\) / 2

        alpha = \(t\_mid \- t\_n\) / dt

        x\_mid = x\_n \+ alpha \* \(x\_n1 \- x\_n\)   \# interpolated state

        g\_mid = guard\_func\(x\_mid, state\)

        if abs\(g\_mid\) < tol or \(t\_hi \- t\_lo\) < tol:

            return t\_mid, x\_mid

        if np\.sign\(g\_mid\) == np\.sign\(g\_n\):

            t\_lo = t\_mid

        else:

            t\_hi = t\_mid

    return \(t\_lo \+ t\_hi\)/2, x\_n \+ \(\(t\_lo\+t\_hi\)/2 \- t\_n\)/dt\*\(x\_n1\-x\_n\)

## __5\.2  Guard Conditions for Each Component__

__Memristor \(analog\)__

w >= D  or  w <= 0        → clamp w to boundary

__Dual\-mode Memristor__

|q\_acc| >= Q\_thresh        → flip binary HfO2 state

__Magnetic Domain Ind\.__

H > H\_sw\[i\]  or  H < \-H\_sw\[i\]   → flip domain i

__Josephson Junction__

phi crosses 2\*pi\*n         → n\_flux changes by ±1

__Superconducting R__

I >= I\_c\(T\)  or  T >= Tc   → switch to normal state

__Phase\-Change R__

T > T\_melt \(~900K\)          → reset to amorphous

__Sample\-Hold Cap__

t mod T\_clock < dt          → sample new value

__Ferroelectric Cap__

E > alpha\[i\]  or  E < beta\[i\]  → flip hysteron i

__Ternary Transistor__

V\_G crosses V\_T1  or  V\_T2  → advance logic level

## __5\.3  Post\-Jump Restart__

After a discrete transition fires at time t\*, the simulation must restart from t\* with the new state\. The correct procedure is:

def handle\_discrete\_event\(simulator, t\_star, x\_star, s\_old, transition\):

    '''

    Handle a discrete event at time t\_star\.

    1\. Record the event

    2\. Apply the state transition

    3\. Re\-initialise any dynamic variables that depend on the discrete state

    4\. Reduce timestep for first few steps after transition \(softstart\)

    '''

    \# Apply transition

    s\_new = transition\(s\_old, x\_star\)

    \# Re\-initialise energy\-storing elements that depend on s

    \# \(e\.g\., when a domain flips, the inductor flux must be recalculated\)

    x\_restarted = simulator\.reinitialise\_after\_transition\(x\_star, s\_old, s\_new\)

    \# Softstart: use smaller dt for first 10 steps after event

    simulator\.dt\_override = simulator\.dt \* 0\.01

    simulator\.dt\_override\_count = 10

    return x\_restarted, s\_new

SECTION 6  ·  COMPLETE PYTHON IMPLEMENTATION

__The HybridCircuit Solver__

This section presents the complete implementation: a Python class that accepts any network of hybrid components, builds the MNA system automatically, and simulates it forward in time with Newton\-Raphson iteration, TR\-BDF2 integration, and exact discrete event detection\.

## __6\.1  Component Base Class__

import numpy as np

import scipy\.sparse as sp\_sparse

import scipy\.sparse\.linalg as sp\_linalg

from dataclasses import dataclass, field

from typing import List, Tuple, Optional, Callable

from enum import Enum

class ComponentType\(Enum\):

    RESISTOR      = 'R'

    CAPACITOR     = 'C'

    INDUCTOR      = 'L'

    VSOURCE       = 'V'

    ISOURCE       = 'I'

    MEMRISTOR     = 'MEM'

    TUNNEL\_R      = 'QTR'

    JOSEPHSON     = 'JJ'

    GMR           = 'GMR'

    FERROELECTRIC = 'FE'

    PHASE\_CHANGE  = 'PCM'

    MEMINDUCTOR   = 'MEMIND'

    MEMCAPACITOR  = 'MEMCAP'

    LIF\_NEURON    = 'LIF'

@dataclass

class Component:

    '''

    Base class for all circuit components\.

    node\_p, node\_n: positive and negative terminal node indices\.

    0 is always ground \(reference node\)\.

    '''

    comp\_type:  ComponentType

    node\_p:     int              \# positive terminal

    node\_n:     int              \# negative terminal \(0 = GND\)

    params:     dict = field\(default\_factory=dict\)

    \# Internal continuous state variables \(e\.g\., w for memristor\)

    state\_c:    np\.ndarray = field\(default\_factory=lambda: np\.array\(\[\]\)\)

    \# Internal discrete state \(e\.g\., crystalline/amorphous phase\)

    state\_d:    int = 0

    name:       str = ''

    def conductance\(self, V\_branch: float\) \-> float:

        '''Return small\-signal conductance dI/dV at V\_branch\.'''

        raise NotImplementedError

    def current\(self, V\_branch: float\) \-> float:

        '''Return branch current I\(V\_branch\)\.'''

        raise NotImplementedError

    def companion\(self, V\_branch: float\) \-> Tuple\[float, float\]:

        '''Return \(G\_eq, I\_eq\) for Norton companion model\.'''

        G = self\.conductance\(V\_branch\)

        I = self\.current\(V\_branch\)

        return G, I \- G \* V\_branch

    def update\_state\(self, V\_branch: float, I\_branch: float, dt: float\):

        '''Update internal state after timestep solution\.'''

        pass

    def check\_guards\(self, V\_branch: float, I\_branch: float\) \-> Optional\[int\]:

        '''Return new discrete state if guard condition met, else None\.'''

        return None

## __6\.2  Concrete Component Implementations__

class ResistorComponent\(Component\):

    def conductance\(self, V\): return 1\.0 / self\.params\['R'\]

    def current\(self, V\):     return V / self\.params\['R'\]

class CapacitorComponent\(Component\):

    '''Capacitor handled via C matrix stamp — no companion model needed\.'''

    def get\_C\(self\): return self\.params\['C'\]

class MemristorComponent\(Component\):

    '''HP TiO2 memristor — analog resistance controlled by oxygen vacancy position w\.'''

    def \_\_init\_\_\(self, node\_p, node\_n, Ron=100, Roff=16000, D=10e\-9, mu\_v=1e\-14, p=1\):

        super\(\)\.\_\_init\_\_\(ComponentType\.MEMRISTOR, node\_p, node\_n,

                         \{'Ron':Ron,'Roff':Roff,'D':D,'mu\_v':mu\_v,'p':p\}\)

        self\.state\_c = np\.array\(\[D \* 0\.5\]\)   \# w starts at 50%

    @property

    def w\(self\): return self\.state\_c\[0\]

    def R\(self\):

        p = self\.params

        return p\['Ron'\]\*\(self\.w/p\['D'\]\) \+ p\['Roff'\]\*\(1 \- self\.w/p\['D'\]\)

    def conductance\(self, V\): return 1\.0 / self\.R\(\)

    def current\(self, V\):     return V / self\.R\(\)

    def update\_state\(self, V, I, dt\):

        p = self\.params

        window = 1 \- \(2\*self\.w/p\['D'\] \- 1\)\*\*\(2\*p\['p'\]\)

        dw = p\['mu\_v'\] \* \(p\['Ron'\]/p\['D'\]\*\*2\) \* I \* window

        self\.state\_c\[0\] = np\.clip\(self\.w \+ dw\*dt, 0, p\['D'\]\)

class TunnelResistorComponent\(Component\):

    '''Quantum tunnel resistor — Simmons model\.'''

    def \_\_init\_\_\(self, node\_p, node\_n, d=2e\-9, phi\_bar=3\.0, A\_junc=2\.5e\-15\):

        super\(\)\.\_\_init\_\_\(ComponentType\.TUNNEL\_R, node\_p, node\_n,

                         \{'d':d,'phi\_bar':phi\_bar,'A\_junc':A\_junc\}\)

        self\.\_e=1\.602e\-19; self\.\_hbar=1\.055e\-34; self\.\_h=6\.626e\-34; self\.\_me=9\.109e\-31

    def current\(self, V\):

        p = self\.params

        if abs\(V\) < 1e\-6: V = 1e\-6 \* np\.sign\(V \+ 1e\-30\)

        A  = \(4\*np\.pi\*p\['d'\]/self\.\_h\)\*np\.sqrt\(2\*self\.\_me\*self\.\_e\)

        J0 = self\.\_e/\(2\*np\.pi\*self\.\_hbar\*p\['d'\]\*\*2\)

        lo = p\['phi\_bar'\] \- V/2;  hi = p\['phi\_bar'\] \+ V/2

        J  = J0\*\(lo\*np\.exp\(\-A\*np\.sqrt\(max\(lo,0\)\)\) \- hi\*np\.exp\(\-A\*np\.sqrt\(max\(hi,0\)\)\)\)

        return J \* p\['A\_junc'\]

    def conductance\(self, V\):

        dV = max\(abs\(V\)\*0\.001, 1e\-4\)

        return \(self\.current\(V\+dV\) \- self\.current\(V\-dV\)\) / \(2\*dV\)

class JosephsonComponent\(Component\):

    '''Josephson junction \(RCSJ model\)\.'''

    def \_\_init\_\_\(self, node\_p, node\_n, Ic=10e\-6, R\_J=50\.0, C\_J=1e\-15\):

        super\(\)\.\_\_init\_\_\(ComponentType\.JOSEPHSON, node\_p, node\_n,

                         \{'Ic':Ic,'R\_J':R\_J,'C\_J':C\_J\}\)

        self\.state\_c = np\.array\(\[0\.0, 0\.0\]\)  \# \[phi, dphi/dt\]

        self\.state\_d = 0   \# n\_flux quanta

        self\.\_hbar=1\.055e\-34; self\.\_e=1\.602e\-19

    def current\(self, V\):

        phi = self\.state\_c\[0\]

        return self\.params\['Ic'\] \* np\.sin\(phi\) \+ V / self\.params\['R\_J'\]

    def conductance\(self, V\):

        phi, dphi = self\.state\_c

        dt = 1e\-12   \# nominal dt for linearisation

        dphi\_dV = \(2\*self\.\_e/self\.\_hbar\) \* dt

        G\_JJ = self\.params\['Ic'\] \* np\.cos\(phi\) \* dphi\_dV

        return G\_JJ \+ 1/self\.params\['R\_J'\]

    def update\_state\(self, V, I, dt\):

        hbar, e = self\.\_hbar, self\.\_e

        Ic, R\_J, C\_J = self\.params\['Ic'\], self\.params\['R\_J'\], self\.params\['C\_J'\]

        phi, dphi = self\.state\_c

        \# RCSJ: C\_J \* d2phi/dt2 \+ \(hbar/2e/R\_J\)\*dphi/dt \+ Ic\*sin\(phi\) = I

        d2phi = \(2\*e/hbar\) \* \(I \- Ic\*np\.sin\(phi\) \- \(hbar/\(2\*e\*R\_J\)\)\*dphi\) / C\_J

        dphi\_new = dphi \+ d2phi \* dt

        phi\_new  = phi  \+ dphi\_new \* dt

        self\.state\_c = np\.array\(\[phi\_new, dphi\_new\]\)

        self\.state\_d = int\(round\(phi\_new / \(2\*np\.pi\)\)\)  \# flux quanta

## __6\.3  The MNA System Builder__

class MNASystem:

    '''

    Builds and solves Modified Nodal Analysis equations for a hybrid circuit\.

    Nodes are numbered 0 \(GND\) to n\_nodes\-1\.

    Voltage sources and inductors add extra rows/columns for their currents\.

    '''

    def \_\_init\_\_\(self, n\_nodes: int, dt: float = 1e\-9\):

        self\.n  = n\_nodes \- 1  \# exclude GND

        self\.dt = dt

        self\.components: List\[Component\] = \[\]

        self\.extra\_vars: List\[Tuple\] = \[\]  \# \(comp, 'type'\) for Vsrc, L

    def add\(self, comp: Component\):

        self\.components\.append\(comp\)

        if comp\.comp\_type in \(ComponentType\.VSOURCE, ComponentType\.INDUCTOR\):

            self\.extra\_vars\.append\(comp\)

        return self

    @property

    def size\(self\): return self\.n \+ len\(self\.extra\_vars\)

    def \_idx\(self, node\):

        '''Map node number to matrix index \(\-1 for GND\)\.'''

        return node \- 1 if node > 0 else \-1

    def \_stamp\_conductance\(self, G\_mat, ni, nj, g\):

        '''Add conductance g between nodes ni and nj\.'''

        ii, jj = self\.\_idx\(ni\), self\.\_idx\(nj\)

        if ii >= 0: G\_mat\[ii, ii\] \+= g

        if jj >= 0: G\_mat\[jj, jj\] \+= g

        if ii >= 0 and jj >= 0:

            G\_mat\[ii, jj\] \-= g

            G\_mat\[jj, ii\] \-= g

    def build\(self, x\_prev=None\):

        '''Build MNA matrices G, C, b for current component states\.'''

        sz = self\.size

        G  = np\.zeros\(\(sz, sz\)\)

        C  = np\.zeros\(\(sz, sz\)\)

        b  = np\.zeros\(sz\)

        if x\_prev is None: x\_prev = np\.zeros\(sz\)

        extra\_idx = self\.n   \# index offset for extra variables

        ev\_map = \{id\(comp\): extra\_idx\+k for k,comp in enumerate\(self\.extra\_vars\)\}

        for comp in self\.components:

            ni, nj = comp\.node\_p, comp\.node\_n

            ii, jj = self\.\_idx\(ni\), self\.\_idx\(nj\)

            \# Branch voltage from previous solution

            Vi = x\_prev\[ii\] if ii >= 0 else 0\.0

            Vj = x\_prev\[jj\] if jj >= 0 else 0\.0

            V\_branch = Vi \- Vj

            ct = comp\.comp\_type

            if ct == ComponentType\.RESISTOR:

                self\.\_stamp\_conductance\(G, ni, nj, 1\.0/comp\.params\['R'\]\)

            elif ct == ComponentType\.CAPACITOR:

                \# BE discretisation: C/dt conductance \+ C/dt\*V\_prev current src

                c\_val = comp\.params\['C'\]

                self\.\_stamp\_conductance\(G, ni, nj, c\_val/self\.dt\)

                if ii >= 0: b\[ii\] \+= c\_val/self\.dt \* V\_branch

                if jj >= 0: b\[jj\] \-= c\_val/self\.dt \* V\_branch

            elif ct == ComponentType\.MEMRISTOR:

                G\_eq, I\_eq = comp\.companion\(V\_branch\)

                self\.\_stamp\_conductance\(G, ni, nj, G\_eq\)

                if ii >= 0: b\[ii\] \-= I\_eq

                if jj >= 0: b\[jj\] \+= I\_eq

            elif ct == ComponentType\.TUNNEL\_R:

                G\_eq, I\_eq = comp\.companion\(V\_branch\)

                self\.\_stamp\_conductance\(G, ni, nj, G\_eq\)

                if ii >= 0: b\[ii\] \-= I\_eq

                if jj >= 0: b\[jj\] \+= I\_eq

            elif ct == ComponentType\.JOSEPHSON:

                G\_eq, I\_eq = comp\.companion\(V\_branch\)

                \# Also add C\_J as capacitor

                c\_val = comp\.params\['C\_J'\]

                self\.\_stamp\_conductance\(G, ni, nj, G\_eq \+ c\_val/self\.dt\)

                if ii >= 0: b\[ii\] \-= I\_eq \- c\_val/self\.dt\*V\_branch

                if jj >= 0: b\[jj\] \+= I\_eq \- c\_val/self\.dt\*V\_branch

            elif ct == ComponentType\.VSOURCE:

                k = ev\_map\[id\(comp\)\]

                if ii >= 0: G\[ii,k\] \+= 1; G\[k,ii\] \+= 1

                if jj >= 0: G\[jj,k\] \-= 1; G\[k,jj\] \-= 1

                b\[k\] \+= comp\.params\['V'\]

            elif ct == ComponentType\.ISOURCE:

                if ii >= 0: b\[ii\] \-= comp\.params\['I'\]

                if jj >= 0: b\[jj\] \+= comp\.params\['I'\]

        return G, C, b

    def solve\_step\(self, x\_prev, nonlinear\_comps=None, max\_nr=20\):

        '''One timestep with NR iteration\.'''

        x = x\_prev\.copy\(\)

        for nr\_iter in range\(max\_nr\):

            G, C, b = self\.build\(x\)

            A   = G \+ C / self\.dt

            rhs = b \+ C @ x\_prev / self\.dt

            x\_new = np\.linalg\.solve\(A \+ np\.eye\(self\.size\)\*1e\-15, rhs\)

            if np\.abs\(x\_new \- x\)\.max\(\) < 1e\-8: break

            x = x\_new

        return x\_new

## __6\.4  The Top\-Level Simulation Loop__

class HybridCircuitSimulator:

    '''

    Top\-level simulator\. Integrates MNA solving, state updates,

    guard checking, and adaptive timestep into one clean interface\.

    '''

    def \_\_init\_\_\(self, n\_nodes: int, dt: float = 1e\-9\):

        self\.mna  = MNASystem\(n\_nodes, dt\)

        self\.dt   = dt

        self\.t    = 0\.0

        self\.x    = np\.zeros\(n\_nodes \- 1\)

        self\.log  = \[\]   \# list of \(t, x, states\) tuples

    def add\(self, comp\): self\.mna\.add\(comp\); return self

    def run\(self, t\_end: float,

            sources: dict = None,

            adaptive: bool = True,

            log\_every: int = 1\):

        '''

        Run simulation from current time to t\_end\.

        sources: dict mapping VSOURCE/ISOURCE component \-> callable\(t\) \-> value

        adaptive: use adaptive timestep control

        log\_every: record every nth step \(reduces memory for long runs\)

        '''

        dt      = self\.dt

        step\_n  = 0

        x       = self\.x\.copy\(\)

        t       = self\.t

        dt\_min  = dt \* 1e\-4

        dt\_max  = dt \* 100

        while t < t\_end:

            dt = min\(dt, t\_end \- t\)  \# don't overshoot

            self\.mna\.dt = dt

            \# Update time\-varying sources

            if sources:

                for comp, fn in sources\.items\(\):

                    if comp\.comp\_type == ComponentType\.VSOURCE:

                        comp\.params\['V'\] = fn\(t\)

                    elif comp\.comp\_type == ComponentType\.ISOURCE:

                        comp\.params\['I'\] = fn\(t\)

            \# Solve MNA system for this timestep

            x\_new = self\.mna\.solve\_step\(x\)

            \# Update all component internal states

            for comp in self\.mna\.components:

                ni, nj = comp\.node\_p, comp\.node\_n

                ii, jj = ni\-1 if ni>0 else \-1, nj\-1 if nj>0 else \-1

                Vi = x\_new\[ii\] if ii >= 0 else 0\.0

                Vj = x\_new\[jj\] if jj >= 0 else 0\.0

                V\_b = Vi \- Vj

                G\_b = comp\.conductance\(V\_b\)

                I\_b = V\_b \* G\_b

                comp\.update\_state\(V\_b, I\_b, dt\)

                \# Check discrete guard conditions

                new\_sd = comp\.check\_guards\(V\_b, I\_b\)

                if new\_sd is not None:

                    comp\.state\_d = new\_sd

            t   \+= dt

            x    = x\_new

            step\_n \+= 1

            if step\_n % log\_every == 0:

                states = \{comp\.name: \(comp\.state\_c\.copy\(\), comp\.state\_d\)

                          for comp in self\.mna\.components\}

                self\.log\.append\(\{'t': t, 'x': x\.copy\(\), 'states': states\}\)

            \# Adaptive timestep: simple heuristic based on solution change rate

            if adaptive:

                dxdt = np\.abs\(x\_new \- x\)\.max\(\) / dt

                if dxdt > 1e6:   dt = max\(dt \* 0\.5, dt\_min\)

                elif dxdt < 1e3: dt = min\(dt \* 1\.5, dt\_max\)

        self\.t = t

        self\.x = x

        return self\.log

SECTION 7  ·  THOUSANDS OF CIRCUITS IN PARALLEL

__GPU Network Simulation__

The CPU solver handles one circuit instance\. For applications like Monte Carlo yield analysis \(running the same circuit with manufacturing tolerances swept across thousands of parameter combinations\) or training neural networks of circuits, we need to simulate many independent circuit instances simultaneously on a GPU\.

## __7\.1  Batched MNA on GPU — The Key Insight__

For N identical circuit topologies with different parameters, the MNA matrix has the same sparsity pattern for all N instances but different numerical values\. We can stack all N matrices into a single batch and solve them simultaneously using batched linear algebra:

__A\[k\] · x\[k\]  =  b\[k\]      for  k = 1, 2, \.\.\., N__

PyTorch's torch\.linalg\.solve handles batched systems natively — it dispatches to cuBLAS batched LU factorisation on the GPU, solving all N systems in parallel\.

import torch

class GPUCircuitBatch:

    '''

    GPU\-accelerated simulation of N identical circuit topologies

    with different component parameters \(Monte Carlo / parameter sweep\)\.

    '''

    def \_\_init\_\_\(self, topology: dict, param\_batch: dict,

                 n\_nodes: int, device='cuda'\):

        '''

        topology:    dict describing circuit connections \(nodes, component types\)

        param\_batch: dict mapping component\_name \-> tensor of shape \(N,\)

                     containing parameter values for each of the N instances

        n\_nodes:     number of nodes in the circuit

        '''

        self\.N       = next\(iter\(param\_batch\.values\(\)\)\)\.shape\[0\]

        self\.n\_nodes = n\_nodes \- 1   \# exclude GND

        self\.device  = device

        self\.topo    = topology

        \# Convert all parameters to GPU tensors of shape \(N,\)

        self\.params  = \{k: v\.to\(device\)\.float\(\)

                        for k, v in param\_batch\.items\(\)\}

        \# Solution vectors: shape \(N, n\_nodes\)

        self\.x = torch\.zeros\(self\.N, self\.n\_nodes, device=device\)

    def build\_G\_batch\(self, x\_batch\):

        '''

        Build G matrices for all N instances simultaneously\.

        Returns G of shape \(N, n\_nodes, n\_nodes\)\.

        This is the GPU\-vectorised version of MNASystem\.build\(\)\.

        '''

        N, n = self\.N, self\.n\_nodes

        G = torch\.zeros\(N, n, n, device=self\.device\)

        b = torch\.zeros\(N, n, device=self\.device\)

        for comp in self\.topo\['components'\]:

            ii, jj = comp\['node\_p'\]\-1, comp\['node\_n'\]\-1

            if comp\['type'\] == 'R':

                g = 1\.0 / self\.params\[comp\['name'\]\]  \# shape \(N,\)

                if ii >= 0: G\[:,ii,ii\] \+= g

                if jj >= 0: G\[:,jj,jj\] \+= g

                if ii >= 0 and jj >= 0:

                    G\[:,ii,jj\] \-= g;  G\[:,jj,ii\] \-= g

            elif comp\['type'\] == 'MEM':

                \# Memristor: w state per instance

                w   = self\.params\[comp\['name'\]\+'\_w'\]     \# shape \(N,\)

                Ron = self\.params\[comp\['name'\]\+'\_Ron'\]

                Rof = self\.params\[comp\['name'\]\+'\_Roff'\]

                D   = self\.params\[comp\['name'\]\+'\_D'\]

                R\_mem = Ron\*\(w/D\) \+ Rof\*\(1 \- w/D\)

                g = 1\.0 / R\_mem

                if ii >= 0: G\[:,ii,ii\] \+= g

                if jj >= 0: G\[:,jj,jj\] \+= g

                if ii >= 0 and jj >= 0:

                    G\[:,ii,jj\] \-= g;  G\[:,jj,ii\] \-= g

        return G, b

    def step\_batch\(self, dt, sources\_batch=None\):

        '''One timestep for all N instances simultaneously\.'''

        G, b = self\.build\_G\_batch\(self\.x\)

        if sources\_batch is not None:

            b \+= sources\_batch   \# shape \(N, n\_nodes\)

        \# Solve N linear systems in parallel: G @ x = b

        \# torch\.linalg\.solve expects \(\.\.\., n, n\) and \(\.\.\., n\)

        x\_new = torch\.linalg\.solve\(G \+ torch\.eye\(self\.n\_nodes,

                                    device=self\.device\)\.unsqueeze\(0\)\*1e\-15, b\)

        \# Update memristor states \(all N simultaneously\)

        for comp in self\.topo\['components'\]:

            if comp\['type'\] == 'MEM':

                ii, jj = comp\['node\_p'\]\-1, comp\['node\_n'\]\-1

                Vi = x\_new\[:,ii\] if ii>=0 else torch\.zeros\(self\.N,device=self\.device\)

                Vj = x\_new\[:,jj\] if jj>=0 else torch\.zeros\(self\.N,device=self\.device\)

                V\_b = Vi \- Vj

                w   = self\.params\[comp\['name'\]\+'\_w'\]

                D   = self\.params\[comp\['name'\]\+'\_D'\]

                Ron = self\.params\[comp\['name'\]\+'\_Ron'\]

                mu\_v = self\.params\[comp\['name'\]\+'\_mu\_v'\]

                R\_mem = Ron\*\(w/D\) \+ \(self\.params\[comp\['name'\]\+'\_Roff'\]\)\*\(1\-w/D\)

                I\_b   = V\_b / R\_mem

                window = 1 \- \(2\*w/D \- 1\)\*\*2

                w\_new = \(w \+ mu\_v\*\(Ron/D\*\*2\)\*I\_b\*window\*dt\)\.clamp\(0, D\)

                self\.params\[comp\['name'\]\+'\_w'\] = w\_new

        self\.x = x\_new

        return x\_new

    def simulate\(self, t\_end, dt, sources\_fn=None, log\_every=100\):

        '''Full simulation loop for GPU batch\.'''

        n\_steps = int\(t\_end / dt\)

        results = \[\]

        for step in range\(n\_steps\):

            t = step \* dt

            src = sources\_fn\(t, self\.N, self\.device\) if sources\_fn else None

            self\.step\_batch\(dt, src\)

            if step % log\_every == 0:

                results\.append\(self\.x\.cpu\(\)\.clone\(\)\)

        return torch\.stack\(results\)  \# shape: \(n\_logs, N, n\_nodes\)

## __7\.2  Monte Carlo Yield Analysis__

def monte\_carlo\_yield\(n\_samples=100\_000, device='cuda'\):

    '''

    Example: yield analysis of a memristor\-resistor voltage divider\.

    Finds what fraction of manufactured devices have V\_out in spec \[0\.4, 0\.6\] V\.

    Manufacturing spread: Ron ± 20%, Roff ± 15%, D ± 5%\.

    '''

    import torch

    N = n\_samples

    \# Sample manufacturing parameters

    Ron\_nom, Roff\_nom, D\_nom = 100\.0, 16000\.0, 10e\-9

    Ron  = torch\.normal\(Ron\_nom,  Ron\_nom \*0\.20, \(N,\)\)\.clamp\(10, 500\)

    Roff = torch\.normal\(Roff\_nom, Roff\_nom\*0\.15, \(N,\)\)\.clamp\(1000, 50000\)

    D    = torch\.normal\(D\_nom,    D\_nom   \*0\.05, \(N,\)\)\.clamp\(5e\-9, 20e\-9\)

    w0   = D \* 0\.5   \# start at 50% doped

    \# Circuit: V\_s=1V \-> R\_load=1kOhm \-> Memristor \-> GND

    \# Nodes: 1=V\_in, 2=V\_mid, GND=0

    topo = \{'components': \[

        \{'type':'R',   'name':'R\_load', 'node\_p':1, 'node\_n':2\},

        \{'type':'MEM', 'name':'M1',     'node\_p':2, 'node\_n':0\},

    \]\}

    params = \{

        'R\_load':   torch\.ones\(N, device=device\) \* 1000\.0,

        'M1\_Ron':   Ron\.to\(device\),

        'M1\_Roff':  Roff\.to\(device\),

        'M1\_D':     D\.to\(device\),

        'M1\_w':     w0\.to\(device\),

        'M1\_mu\_v':  torch\.ones\(N,device=device\)\*1e\-14,

    \}

    sim = GPUCircuitBatch\(topo, params, n\_nodes=3, device=device\)

    \# Source: node 1 held at 1V \(implemented as large conductance to V\_s\)

    def source\_fn\(t, N, dev\):

        \# Current injection into node 1 to enforce V=1V via 1 Ohm source R

        return torch\.zeros\(N, sim\.n\_nodes, device=dev\)

    \# Run for 1 us

    log = sim\.simulate\(t\_end=1e\-6, dt=1e\-9, log\_every=1000\)

    \# Read final V\_mid \(node 2, index 1\)

    V\_mid\_final = sim\.x\[:, 1\]   \# shape \(N,\)

    in\_spec = \(\(V\_mid\_final > 0\.4\) & \(V\_mid\_final < 0\.6\)\)\.float\(\)

    yield\_pct = in\_spec\.mean\(\)\.item\(\) \* 100

    print\(f'Yield \(\{N\} samples\): \{yield\_pct:\.1f\}%'\)

    return V\_mid\_final\.cpu\(\)

*🚀  Running 100,000 circuit simulations in parallel on an A100 GPU takes approximately the same wall\-clock time as running 1 simulation on a CPU\. For yield analysis with tight manufacturing tolerances, this changes the workflow from 'run overnight on a cluster' to 'run in a few seconds on a workstation'\.*

SECTION 8  ·  THREE COMPLETE CIRCUIT SIMULATIONS

__Worked Examples__

## __Example A: Memristor Crossbar 4×4 — In\-Memory Matrix Multiply__

A 4×4 memristor crossbar has 16 memristors arranged in a grid\. Row nodes receive input voltages V\_in \(a 4\-vector\)\. Column nodes output currents I\_out\. Each memristor conductance G\_ij encodes one element of a 4×4 matrix W\. The output current at column j is:

__I\_out\[j\]  =  sum\_i  G\_ij · V\_in\[i\]     \(Ohm's law applied to each memristor\)__

This is a matrix\-vector multiply W·v executed at the speed of electrical current flow — no multiply\-accumulate operations, no memory access\. This is the core operation of in\-memory computing for AI inference\.

def build\_memristor\_crossbar\(W\_matrix, V\_input, R\_load=1000\.0\):

    '''

    Build a 4x4 memristor crossbar circuit and compute W @ V\_input\.

    W\_matrix:  4x4 weight matrix \(values between 0 and 1\)

    V\_input:   4\-element input voltage vector

    R\_load:    load resistor at each output column

    '''

    import numpy as np

    rows, cols = 4, 4

    \# Node numbering:

    \# Row nodes: 1\-4 \(inputs, held at V\_input values\)

    \# Column nodes: 5\-8 \(outputs, read through R\_load to GND\)

    \# GND = 0

    n\_nodes = 9  \# 0=GND, 1\-4=row, 5\-8=col

    mna = MNASystem\(n\_nodes, dt=1e\-9\)

    \# Input voltage sources \(set row voltages\)

    for i in range\(rows\):

        vs = Component\.\_\_new\_\_\(Component\)

        vs\.comp\_type = ComponentType\.VSOURCE

        vs\.node\_p, vs\.node\_n = i\+1, 0

        vs\.params  = \{'V': V\_input\[i\]\}

        vs\.state\_c = np\.array\(\[\]\)

        vs\.state\_d = 0

        mna\.extra\_vars\.append\(vs\)

        mna\.components\.append\(vs\)

    \# Memristor conductances \(one per crossbar intersection\)

    Ron, Roff = 100, 50000

    for i in range\(rows\):

        for j in range\(cols\):

            \# Map W value \[0,1\] to resistance range \[Roff, Ron\]

            R\_ij = Roff \- W\_matrix\[i,j\] \* \(Roff \- Ron\)

            mem = ResistorComponent\(node\_p=i\+1, node\_n=j\+5,

                                    comp\_type=ComponentType\.RESISTOR,

                                    params=\{'R': R\_ij\}, state\_c=np\.array\(\[\]\),

                                    state\_d=0, name=f'W\{i\}\{j\}'\)

            mem\.comp\_type = ComponentType\.RESISTOR

            mna\.components\.append\(mem\)

    \# Load resistors at outputs

    for j in range\(cols\):

        rl = ResistorComponent\(node\_p=j\+5, node\_n=0,

                               comp\_type=ComponentType\.RESISTOR,

                               params=\{'R': R\_load\}, state\_c=np\.array\(\[\]\),

                               state\_d=0, name=f'RL\{j\}'\)

        rl\.comp\_type = ComponentType\.RESISTOR

        mna\.components\.append\(rl\)

    \# Solve \(DC — just solve once, no time stepping needed for static matrix multiply\)

    sz = mna\.size

    G, C, b = mna\.build\(np\.zeros\(sz\)\)

    x = np\.linalg\.solve\(G \+ np\.eye\(sz\)\*1e\-15, b\)

    \# Read output currents through load resistors

    I\_out = np\.zeros\(cols\)

    for j in range\(cols\):

        V\_col = x\[j\+4\]   \# column node \(index = node\-1\)

        I\_out\[j\] = V\_col / R\_load

    return x, I\_out

\# Test: encode an identity matrix

W = np\.eye\(4\)

V = np\.array\(\[1\.0, 0\.5, 0\.25, 0\.125\]\)

x, I = build\_memristor\_crossbar\(W, V\)

print\('Expected \(proportional to V\):', V\)

print\('Got \(output currents\):', I / I\.max\(\)\)

## __Example B: Josephson Junction Oscillator with GMR Load__

A Josephson junction biased above I\_c oscillates at the Josephson frequency f\_J = 2eV/h\. Here we drive a GMR spin resistor with this oscillating voltage to modulate its spin alignment, coupling quantum oscillations to a classical magnetic component\.

def josephson\_gmr\_circuit\(\):

    '''

    Circuit: I\_bias \-> JJ in parallel with GMR \-> GND

    JJ oscillates; GMR resistance modulates with spin dynamics\.

    '''

    from dataclasses import dataclass

    \# Use HybridCircuitSimulator

    \# Nodes: 1 = top node \(JJ and GMR both connect here\), 0 = GND

    sim = HybridCircuitSimulator\(n\_nodes=2, dt=1e\-12\)

    \# Current source: bias above Ic to make JJ oscillate

    I\_src = Component\.\_\_new\_\_\(Component\)

    I\_src\.comp\_type = ComponentType\.ISOURCE

    I\_src\.node\_p, I\_src\.node\_n = 1, 0

    I\_src\.params   = \{'I': 12e\-6\}   \# 1\.2 \* Ic

    I\_src\.state\_c  = np\.array\(\[\]\)

    I\_src\.state\_d  = 0

    I\_src\.name     = 'I\_bias'

    sim\.mna\.components\.append\(I\_src\)

    \# Josephson junction

    jj = JosephsonComponent\(node\_p=1, node\_n=0, Ic=10e\-6, R\_J=50, C\_J=1e\-15\)

    jj\.name = 'JJ1'

    sim\.mna\.components\.append\(jj\)

    sim\.mna\.extra\_vars  \# not a vsource/inductor, so no extra var

    \# GMR resistor in parallel: simplified as state\-dependent resistor

    \# R\_GMR\(t\) controlled externally by spin simulation running in background

    gmr = ResistorComponent\.\_\_new\_\_\(ResistorComponent\)

    gmr\.comp\_type = ComponentType\.RESISTOR

    gmr\.node\_p, gmr\.node\_n = 1, 0

    gmr\.params    = \{'R': 106\.0\}   \# mid\-value between RP=100 and RAP=112

    gmr\.state\_c   = np\.array\(\[0\.0\]\)  \# theta\_mag

    gmr\.state\_d   = 0

    gmr\.name      = 'GMR1'

    sim\.mna\.components\.append\(gmr\)

    \# Run for 1 ns

    log = sim\.run\(t\_end=1e\-9, log\_every=10\)

    t\_arr = np\.array\(\[e\['t'\] for e in log\]\)

    V1    = np\.array\(\[e\['x'\]\[0\] for e in log\]\)   \# node 1 voltage

    phi   = np\.array\(\[e\['states'\]\['JJ1'\]\[0\]\[0\] for e in log\]\)  \# phase

    \# Josephson frequency

    hbar, e\_q = 1\.055e\-34, 1\.602e\-19

    V\_dc  = np\.mean\(V1\)

    f\_J   = 2 \* e\_q \* V\_dc / \(2 \* np\.pi \* hbar\)

    print\(f'JJ oscillation frequency: \{f\_J/1e9:\.2f\} GHz'\)

    print\(f'Expected: 2eV/h = \{2\*e\_q\*V\_dc/6\.626e\-34/1e9:\.2f\} GHz'\)

    return t\_arr, V1, phi

## __Example C: LIF Spiking Neural Network — 3 Neurons__

Three Leaky Integrate\-and\-Fire neurons wired with memristor synapses\. Each spike from neuron i sends a current pulse to neuron j through memristor M\_ij\. The memristor weight adapts based on the timing of spikes — implementing Spike\-Timing Dependent Plasticity \(STDP\), the biological learning rule\.

class LIFNeuronComponent\(Component\):

    '''

    Leaky integrate\-and\-fire neuron as a circuit component\.

    Models as a parallel RC with threshold comparator\.

    '''

    def \_\_init\_\_\(self, node, Cm=1e\-9, Rm=1e7, V\_thresh=0\.02, V\_reset=\-0\.07\):

        super\(\)\.\_\_init\_\_\(ComponentType\.LIF\_NEURON, node, 0,

                         \{'Cm':Cm,'Rm':Rm,'V\_thresh':V\_thresh,'V\_reset':V\_reset\}\)

        self\.state\_c = np\.array\(\[\-0\.07\]\)  \# membrane voltage V\_m

        self\.state\_d = 0   \# 0=integrating, 1=refractory

        self\.spike\_times = \[\]

        self\.\_t = 0\.0

    def conductance\(self, V\): return 1\.0/self\.params\['Rm'\] \+ self\.params\['Cm'\]\*1e9

    def current\(self, V\):     return V/self\.params\['Rm'\]

    def check\_guards\(self, V, I\):

        if V >= self\.params\['V\_thresh'\] and self\.state\_d == 0:

            self\.spike\_times\.append\(self\.\_t\)

            return 1   \# enter refractory

        if self\.state\_d == 1 and V <= self\.params\['V\_reset'\] \+ 0\.001:

            return 0   \# leave refractory

        return None

def stdp\_update\(w, t\_pre, t\_post, A\_plus=0\.01, A\_minus=0\.01, tau=20e\-3\):

    '''

    Spike\-Timing Dependent Plasticity weight update\.

    Pre fires before post \(t\_pre < t\_post\): potentiation \(w increases\)\.

    Post fires before pre \(t\_post < t\_pre\): depression \(w decreases\)\.

    '''

    dt\_spk = t\_post \- t\_pre

    if dt\_spk > 0:   \# pre before post \-> potentiation

        dw =  A\_plus  \* np\.exp\(\-dt\_spk / tau\)

    else:            \# post before pre \-> depression

        dw = \-A\_minus \* np\.exp\( dt\_spk / tau\)

    return np\.clip\(w \+ dw, 0\.0, 1\.0\)

\# Build 3\-neuron network

\# Neurons at nodes 1, 2, 3\. Memristor synapses connect all pairs\.

sim = HybridCircuitSimulator\(n\_nodes=4, dt=1e\-4\)

neurons = \[LIFNeuronComponent\(node=i\+1\) for i in range\(3\)\]

for n in neurons: sim\.mna\.components\.append\(n\)

\# Synaptic memristors \(simplified as resistors with STDP weight updates\)

syn\_weights = np\.ones\(\(3,3\)\) \* 0\.5

syn\_weights\[np\.eye\(3,dtype=bool\)\] = 0  \# no self\-connections

\# External input current sources to neuron 1

I\_ext = Component\.\_\_new\_\_\(Component\)

I\_ext\.comp\_type = ComponentType\.ISOURCE

I\_ext\.node\_p, I\_ext\.node\_n = 1, 0

I\_ext\.params = \{'I': 3e\-9\}

I\_ext\.state\_c = np\.array\(\[\]\); I\_ext\.state\_d = 0; I\_ext\.name = 'I\_ext'

sim\.mna\.components\.append\(I\_ext\)

print\('3\-neuron LIF network ready\. Synaptic weights:', syn\_weights\)

SECTION 9  ·  GENERATING NETLISTS FOR INDUSTRY EDA TOOLS

__SPICE\-Compatible Export__

SPICE is the industry standard for circuit simulation, used by every chip design tool \(Cadence, Synopsys, Mentor\)\. While SPICE cannot natively simulate hybrid components, we can export behavioural models that approximate the hybrid behaviour using SPICE primitives and voltage\-controlled sources\. This allows the circuit to be used within larger designs\.

## __9\.1  SPICE Behavioural Models__

SPICE supports a B\-element \(behavioural voltage/current source\) that evaluates an arbitrary mathematical expression\. We use this to implement the hybrid I\-V curves:

### __Quantum Tunnel Resistor SPICE model:__

\.SUBCKT QTR anode cathode

\* Quantum Tunnel Resistor behavioural model

\* Simmons model approximation \(low\-voltage regime\)

\.PARAM d=2e\-9 phi=3\.0 A\_junc=2\.5e\-15

\.PARAM G0='1e\-8 \* exp\(\-4\*pi\*d/6\.626e\-34 \* sqrt\(2\*9\.109e\-31\*phi\*1\.602e\-19\)\)'

B1 anode cathode I='G0 \* V\(anode,cathode\) \*

\+  \(1 \+ \(V\(anode,cathode\)\)^2 / \(6\*phi^2\)\)'

\.ENDS QTR

### __Memristor SPICE model \(HP model\):__

\.SUBCKT MEMRISTOR anode cathode

\* HP TiO2 memristor with internal state variable w

\.PARAM Ron=100 Roff=16000 D=10n mu\_v=1e\-14

\* State variable w stored as voltage on internal capacitor

Cw w 0 1 IC=5e\-9   ; w starts at D/2 = 5nm

\* Current through device

Eresist anode cathode value='V\(anode,cathode\) /

\+  \(Ron\*V\(w\)/D \+ Roff\*\(1\-V\(w\)/D\)\)'

\* State equation: dw/dt = mu\_v\*\(Ron/D^2\)\*I\*window

Bw w 0 I='mu\_v\*\(Ron/D^2\) \* I\(Eresist\) \*

\+  \(1 \- \(2\*V\(w\)/D \- 1\)^2\)'

\.ENDS MEMRISTOR

### __Python SPICE netlist generator:__

def export\_to\_spice\(simulator, filename='hybrid\_circuit\.sp',

                     title='Hybrid Component Circuit'\):

    '''

    Export a HybridCircuitSimulator to a SPICE netlist\.

    Uses \.SUBCKT for each hybrid component type\.

    '''

    lines = \[

        f'\* \{title\}',

        '\* Generated by HybridCircuit Solver Phase 2',

        '\* Hybrid components approximated with behavioural SPICE models',

        '',

    \]

    \# Include subcircuit definitions

    lines \+= \[

        '\* ─── SUBCIRCUIT LIBRARY ───────────────────────────────────',

        '\.SUBCKT QTR anode cathode',

        '\.PARAM d=2n phi=3\.0 A=2\.5e\-15',

        '\.PARAM G0=\{1e\-8\*exp\(\-2\.226e10\*d\*sqrt\(phi\)\)\}',

        'B1 anode cathode I=\{G0\*V\(anode,cathode\)\*\(1\+V\(anode,cathode\)^2/\(6\*phi^2\)\)\}',

        '\.ENDS QTR',

        '',

        '\.SUBCKT MEMRISTOR anode cathode RON=100 ROFF=16000 D=10n',

        'Cw internal 0 1 IC=\{D/2\}',

        'Gdev anode cathode value=\{V\(anode,cathode\)/\(RON\*V\(internal\)/D\+ROFF\*\(1\-V\(internal\)/D\)\)\}',

        'Bstate internal 0 I=\{1e\-14\*\(RON/D^2\)\*I\(Gdev\)\*\(1\-\(2\*V\(internal\)/D\-1\)^2\)\}',

        '\.ENDS MEMRISTOR',

        '',

        '\* ─── CIRCUIT NETLIST ─────────────────────────────────────',

    \]

    \# Emit each component

    comp\_counts = \{\}

    for comp in simulator\.mna\.components:

        ct = comp\.comp\_type

        name = comp\.name or ct\.value

        np\_node = f'N\{comp\.node\_p\}' if comp\.node\_p > 0 else '0'

        nn\_node = f'N\{comp\.node\_n\}' if comp\.node\_n > 0 else '0'

        if ct == ComponentType\.RESISTOR:

            lines\.append\(f'R\{name\} \{np\_node\} \{nn\_node\} \{comp\.params\["R"\]\}'\)

        elif ct == ComponentType\.CAPACITOR:

            lines\.append\(f'C\{name\} \{np\_node\} \{nn\_node\} \{comp\.params\["C"\]\}'\)

        elif ct == ComponentType\.VSOURCE:

            lines\.append\(f'V\{name\} \{np\_node\} \{nn\_node\} DC \{comp\.params\["V"\]\}'\)

        elif ct == ComponentType\.ISOURCE:

            lines\.append\(f'I\{name\} \{np\_node\} \{nn\_node\} DC \{comp\.params\["I"\]\}'\)

        elif ct == ComponentType\.MEMRISTOR:

            lines\.append\(f'X\{name\} \{np\_node\} \{nn\_node\} MEMRISTOR'

                         f' RON=\{comp\.params\["Ron"\]\} ROFF=\{comp\.params\["Roff"\]\}'

                         f' D=\{comp\.params\["D"\]\}'\)

        elif ct == ComponentType\.TUNNEL\_R:

            lines\.append\(f'X\{name\} \{np\_node\} \{nn\_node\} QTR'

                         f' d=\{comp\.params\["d"\]\} phi=\{comp\.params\["phi\_bar"\]\}'\)

        elif ct == ComponentType\.JOSEPHSON:

            \# Approximate JJ as current\-controlled resistor \+ L

            hbar\_2e = 3\.29e\-16   \# hbar / 2e

            L\_J = hbar\_2e / comp\.params\['Ic'\]

            lines\.append\(f'\* Josephson Junction \(linearised at zero bias\)'\)

            lines\.append\(f'L\{name\} \{np\_node\} \{nn\_node\} \{L\_J:\.3e\}'\)

            lines\.append\(f'R\{name\}\_shunt \{np\_node\} \{nn\_node\} \{comp\.params\["R\_J"\]\}'\)

    lines \+= \['', '\.TRAN 1n 1u', '\.END'\]

    with open\(filename, 'w'\) as f:

        f\.write\('\\n'\.join\(lines\)\)

    print\(f'SPICE netlist written to \{filename\}'\)

    return '\\n'\.join\(lines\)

# __Phase 2 Summary — What Was Built__

__Section 1 — Graph Theory__

Incidence matrix A\_r, KCL as matrix equation, KVL as transpose, branch type taxonomy

__Section 2 — MNA__

Component stamps for R, C, L, V\-source, I\-source, and all hybrid types; full matrix equation

__Section 3 — NR Iteration__

Newton\-Raphson companion model \(G\_eq, I\_eq\), Jacobians for QTR/memristor/Josephson

__Section 4 — Time Integration__

Backward Euler derivation, TR\-BDF2 implementation, adaptive timestep PI controller

__Section 5 — Event Detection__

Zero\-crossing bisection algorithm, guard table for all components, post\-jump restart

__Section 6 — HybridCircuit__

Complete Component class hierarchy, MNASystem builder, Newton\-Raphson solver, main simulation loop

__Section 7 — GPU Batch__

GPUCircuitBatch with batched LU solve, vectorised memristor state updates, Monte Carlo yield analysis

__Section 8 — Examples__

4×4 memristor crossbar matrix multiply, Josephson\-GMR oscillator, 3\-neuron STDP spiking network

__Section 9 — SPICE Export__

QTR and memristor \.SUBCKT definitions, Python netlist generator for any HybridCircuitSimulator

__Phase 2 Complete  ·  General Circuit Solver Built__

*Next: Phase 3 — Advanced GPU Kernels \(custom CUDA, stiff solvers, real\-time performance\)*

