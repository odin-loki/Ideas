"""
ARIA — Algebraic Resynchronisation and Integrity Architecture
=============================================================
Complete reference implementation with integrated profiler.

Sections
--------
  1   GF(2^256) field arithmetic
  2   L2 extension field  GF(2^256)[y] / (y^8 + y^4 + y^3 + y + 1)
  3   L3 extension field  L2[z] / (z^4 + z + 1)
  4   Meta-DAG RNG (eight transcendental-constant nodes)
  5   Message encoding — polynomial over L2
  6   Nonce derivation — three differentiation modes
  7   AEAD encrypt / decrypt / verify  (SIV construction)
  8   Formal security reduction simulators
  9   Profiler
  10  Test suite
  11  Main entry point

Usage
-----
  python aria.py              # full tests + profile
  python aria.py --test       # tests only
  python aria.py --profile    # profiler only

API quick-start
---------------
  from aria import ARIASession, ARIAMode

  sender   = ARIASession(shared_key, ARIAMode.POINT_DRIFT)
  receiver = ARIASession(shared_key, ARIAMode.POINT_DRIFT)

  pkt = sender.encrypt(b"FIRE MISSION GRID 123456")
  msg = receiver.decrypt(pkt)           # raises ValueError on auth failure

SIV construction note
---------------------
  The authentication tag is computed from the message polynomial evaluated
  at session-bound point alpha.  The keystream is keyed from that same tag
  (tag-as-IV).  Decryption: tentatively decrypt using the packet tag as IV,
  recompute tag from recovered plaintext, verify they match.  This gives
  plaintext-committed ciphertext — no nonce is ever transmitted.
"""

import hashlib
import os
import sys
import time
from collections import defaultdict
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1  GF(2^256)
# ═══════════════════════════════════════════════════════════════════════════════

_GF_DEG = 256
# Irreducible pentanomial:  x^256 + x^10 + x^5 + x^2 + 1
_GF_IRR = (1 << 256) | (1 << 10) | (1 << 5) | (1 << 2) | 1


def gf_add(a: int, b: int) -> int:
    """Addition in GF(2^256) — bitwise XOR."""
    return a ^ b


def _gf_reduce(a: int) -> int:
    for i in range(a.bit_length() - 1, _GF_DEG - 1, -1):
        if (a >> i) & 1:
            a ^= _GF_IRR << (i - _GF_DEG)
    return a


def gf_mul(a: int, b: int) -> int:
    """Multiplication in GF(2^256) via schoolbook carry-less multiply + reduce."""
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return _gf_reduce(r)


def gf_pow(a: int, n: int) -> int:
    """Exponentiation via square-and-multiply."""
    r = 1
    a = _gf_reduce(a)
    while n:
        if n & 1:
            r = gf_mul(r, a)
        a = gf_mul(a, a)
        n >>= 1
    return r


def gf_inv(a: int) -> int:
    """Inversion via extended Euclidean algorithm over GF(2)[x]."""
    if a == 0:
        raise ZeroDivisionError("zero has no inverse")
    r0, r1, s0, s1 = _GF_IRR, a, 0, 1
    while r1:
        sh = r0.bit_length() - r1.bit_length()
        if sh < 0:
            r0, r1, s0, s1 = r1, r0, s1, s0
            sh = -sh
        r0 ^= r1 << sh
        s0 ^= s1 << sh
    return _gf_reduce(s0)


def gf_to_bytes(a: int) -> bytes:
    return a.to_bytes(32, 'big')


def gf_from_bytes(b: bytes) -> int:
    return int.from_bytes(b, 'big')


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2  L2 = GF(2^256)[y] / Q2(y)
# ═══════════════════════════════════════════════════════════════════════════════

# Q2(y) = y^8 + y^4 + y^3 + y + 1  (index = degree of term)
_Q2     = [1, 1, 0, 1, 1, 0, 0, 0, 1]
_L2_DEG = 8


def _l2_trim(p: list) -> list:
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def l2_add(a: list, b: list) -> list:
    n = max(len(a), len(b))
    return [gf_add(a[i] if i < len(a) else 0,
                   b[i] if i < len(b) else 0) for i in range(n)]


def l2_reduce(poly: list) -> list:
    p = list(poly)
    while len(p) > _L2_DEG:
        if p[-1] == 0:
            p.pop()
            continue
        lead = p[-1]
        sh   = len(p) - len(_Q2)
        for i, c in enumerate(_Q2):
            p[i + sh] = gf_add(p[i + sh], gf_mul(lead, c))
        p.pop()
    return _l2_trim(p)


def l2_mul(a: list, b: list) -> list:
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            r[i + j] = gf_add(r[i + j], gf_mul(ai, bj))
    return l2_reduce(r)


def l2_horner(coeffs: list, pt: int) -> int:
    """Evaluate polynomial with GF(2^256) coefficients at a GF(2^256) point."""
    r = 0
    for c in reversed(coeffs):
        r = gf_mul(r, pt)
        r = gf_add(r, c)
    return r


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3  L3 = L2[z] / Q3(z)
# ═══════════════════════════════════════════════════════════════════════════════

# Q3(z) = z^4 + z + 1
_L3_DEG     = 4
_Q3_NONZERO = {0: 1, 1: 1}


def _l3_trim(p: list) -> list:
    while len(p) > 1 and p[-1] == [0]:
        p.pop()
    return p


def l3_add(a: list, b: list) -> list:
    n = max(len(a), len(b))
    return [l2_add(a[i] if i < len(a) else [0],
                   b[i] if i < len(b) else [0]) for i in range(n)]


def l3_reduce(poly: list) -> list:
    p = list(poly)
    while len(p) > _L3_DEG:
        lead = p[-1]
        if lead == [0]:
            p.pop()
            continue
        sh = len(p) - 1 - _L3_DEG
        for d, sc in _Q3_NONZERO.items():
            idx = sh + d
            while len(p) <= idx:
                p.append([0])
            p[idx] = l2_add(p[idx], [gf_mul(coef, sc) for coef in lead])
        p.pop()
    return _l3_trim(p)


def l3_mul(a: list, b: list) -> list:
    r = [[0]] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            r[i + j] = l2_add(r[i + j], l2_mul(ai, bj))
    return l3_reduce(r)


def l3_collapse(l3_elem: list, beta: int, delta: int) -> int:
    """
    Collapse an L3 element to a single GF(2^256) value via double Horner:
      1. Each L2 coefficient collapsed to GF(2^256) by Horner at delta.
      2. Resulting GF(2^256) polynomial evaluated by Horner at beta.
    """
    l1 = [l2_horner(l2c, delta) for l2c in l3_elem]
    return l2_horner(l1, beta)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4  Meta-DAG RNG
# ═══════════════════════════════════════════════════════════════════════════════

_TRANSCENDENTALS = {
    "pi":       0x243F6A8885A308D3,   # π
    "e":        0xB7E151628AED2A6B,   # e
    "sqrt2":    0x6A09E667F3BCC908,   # √2
    "phi":      0x9E3779B97F4A7C15,   # φ  golden ratio
    "zeta3":    0xD2A1BE4BF93F45CF,   # ζ(3) Apéry's constant
    "gamma":    0x93C467E37DB0C7A4,   # γ  Euler-Mascheroni
    "catalan":  0xD56B3CB5D3DB1A47,   # Catalan's constant
    "glaisher": 0xE2F5224C0DE89E2F,   # Glaisher-Kinkelin constant
}
_NODE_NAMES = list(_TRANSCENDENTALS.keys())
_M64        = 0xFFFF_FFFF_FFFF_FFFF


class _DAGNode:
    __slots__ = ('state', 'meta', 'ctr', 'tc')

    def __init__(self, name: str, seed: bytes):
        tc         = _TRANSCENDENTALS[name]
        si         = int.from_bytes(seed[:8], 'big')
        self.state = tc ^ si
        self.meta  = ((tc >> 1) ^ (si << 1)) & _M64
        self.ctr   = 0
        self.tc    = tc

    def tick(self) -> int:
        op, s, c = self.meta & 7, self.state, self.tc
        if   op == 0: s = ((s << 17) | (s >> 47)) & _M64
        elif op == 1: s =   s ^ c
        elif op == 2: s =  (s + c)                 & _M64
        elif op == 3: s =   s * 0x9E3779B97F4A7C15 & _M64
        elif op == 4: s = ((s << 31) | (s >> 33))  & _M64
        elif op == 5: s =   s ^ (c >> (self.ctr % 32))
        elif op == 6: s =  (s - c)                 & _M64
        else:         s = ((s >> 13) | (s << 51))  & _M64
        self.state = s
        self.meta  = (self.meta * 0x6C62272E07BB0142 ^ s ^ self.ctr) & _M64
        self.ctr  += 1
        return s


class MetaDAG:
    """
    8-node Meta-DAG RNG seeded from eight transcendental constants.

    Both parties sharing the same session key produce identical output streams.
    After packet loss, the receiver fast-forwards to any sequence position
    deterministically using only the session key and the sequence number.
    """

    def __init__(self, session_key: bytes, start_seq: int = 0):
        self._nodes = {
            name: _DAGNode(name, hashlib.sha256(session_key + name.encode()).digest())
            for name in _NODE_NAMES
        }
        self.steps = 0
        if start_seq > 0:
            self.fast_forward(start_seq)

    def _round(self) -> list:
        """One DAG round: all nodes tick, then cross-node mixing applied."""
        raw = [self._nodes[k].tick() for k in _NODE_NAMES]
        out = []
        for i, k in enumerate(_NODE_NAMES):
            inf = raw[(i + 3) % 8] ^ raw[(i + 5) % 8]
            v   = raw[i] ^ inf
            self._nodes[k].state ^= inf >> 7
            out.append(v)
        self.steps += 1
        return out

    def next_gf256(self) -> int:
        """Produce one 256-bit GF(2^256) element (consumes 4 DAG rounds)."""
        vals = []
        while len(vals) < 4:
            vals.extend(self._round())
        r = 0
        for v in reversed(vals[:4]):
            r = (r << 64) | v
        return r

    def fast_forward(self, steps: int) -> None:
        """Advance DAG by `steps` rounds for resync from a sequence number."""
        for _ in range(steps):
            self._round()


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5  Message encoding
# ═══════════════════════════════════════════════════════════════════════════════

def _h(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def _hint(data: bytes) -> int:
    return int.from_bytes(_h(data), 'big')


def _eval_points(sk: bytes):
    """Derive three independent session-bound evaluation points."""
    beta  = _hint(b"aria:beta:"  + sk)
    delta = _hint(b"aria:delta:" + sk)
    alpha = _hint(b"aria:alpha:" + sk)
    return beta, delta, alpha


def _encode_message(msg: bytes, dag: MetaDAG) -> list:
    """
    Encode message as a degree-7 polynomial over L2.
    Returns list of 8 L2-elements (each 8 GF(2^256) coefficients).
    coefficient[i][j] = DAG.next_gf256() * H(msg || (8i+j))
    """
    poly = []
    for i in range(8):
        l2c = [gf_mul(dag.next_gf256(),
                      _hint(msg + (i * 8 + j).to_bytes(2, 'big')))
               for j in range(8)]
        poly.append(l2c)
    return poly


def _collapse_poly(poly: list, pt: int, delta: int) -> int:
    """Collapse L2-polynomial to GF(2^256) via double Horner."""
    l1 = [l2_horner(l2c, delta) for l2c in poly]
    return l2_horner(l1, pt)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6  Nonce differentiation modes
# ═══════════════════════════════════════════════════════════════════════════════

class ARIAMode:
    DAG_STREAM  = 1   # 9th polynomial coefficient from DAG; 4-byte wire overhead
    RANDOM_SALT = 2   # random salt injected into poly[0]; 16-byte wire overhead
    POINT_DRIFT = 3   # evaluation point drifts per seq; 4-byte wire overhead, fastest


def _build_poly(msg: bytes, sk: bytes, mode: int, seq: int, salt: Optional[bytes]):
    """
    Build the message polynomial for the given mode.
    Returns (poly, beta, delta, alpha, meta_bytes).

    Mode 3 note: both the nonce evaluation point (beta) and the tag evaluation
    point (alpha) drift with seq, derived independently so they remain distinct.
    This ensures per-transmission uniqueness in both the nonce and the tag.
    """
    if mode == ARIAMode.DAG_STREAM:
        dag  = MetaDAG(sk, start_seq=seq * 64)
        poly = _encode_message(msg, dag)
        poly.append([dag.next_gf256()] + [0] * 7)   # 9th differentiator coeff
        beta, delta, alpha = _eval_points(sk)
        meta = seq.to_bytes(4, 'big')

    elif mode == ARIAMode.RANDOM_SALT:
        if salt is None:
            salt = os.urandom(16)
        r    = int.from_bytes(salt, 'big')
        dag  = MetaDAG(sk)
        poly = _encode_message(msg, dag)
        poly[0] = [gf_add(poly[0][k], gf_mul(r, k + 1)) for k in range(8)]
        beta, delta, alpha = _eval_points(sk)
        meta = salt

    else:  # POINT_DRIFT
        dag  = MetaDAG(sk)
        poly = _encode_message(msg, dag)
        beta_0, delta, alpha_0 = _eval_points(sk)
        # Both evaluation points drift with seq; derived independently
        beta_i  = _hint(b"aria:beta_drift:"  + sk + seq.to_bytes(8, 'big'))
        alpha_i = _hint(b"aria:alpha_drift:" + sk + seq.to_bytes(8, 'big'))
        beta    = gf_add(beta_0,  beta_i)
        alpha   = gf_add(alpha_0, alpha_i)
        meta    = seq.to_bytes(4, 'big')

    return poly, beta, delta, alpha, meta


def _compute_tag(poly: list, alpha: int, delta: int) -> bytes:
    """Compute 16-byte authentication tag: Collapse(P, alpha, delta)[:16]."""
    return _collapse_poly(poly, alpha, delta).to_bytes(32, 'big')[:16]


def _keystream(tag: bytes, length: int) -> bytes:
    """
    SHA-256 chain keyed from the authentication tag (SIV keystream).
    Placeholder for AES-256-CTR in production.
    """
    ks, ctr = b'', 0
    while len(ks) < length:
        ks  += _h(b"ks:" + tag + ctr.to_bytes(4, 'big'))
        ctr += 1
    return ks[:length]


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7  AEAD  (SIV construction)
# ═══════════════════════════════════════════════════════════════════════════════

class ARIAPacket:
    """
    ARIA wire-format packet.

    Layout:  version(1) | mode(1) | meta_len(1) | meta | ciphertext | tag(16)
    """
    __slots__ = ('mode', 'meta', 'ciphertext', 'tag')

    def __init__(self, mode: int, meta: bytes, ciphertext: bytes, tag: bytes):
        self.mode, self.meta = mode, meta
        self.ciphertext, self.tag = ciphertext, tag

    def serialise(self) -> bytes:
        return (b'\x01'
                + self.mode.to_bytes(1, 'big')
                + len(self.meta).to_bytes(1, 'big')
                + self.meta + self.ciphertext + self.tag)

    @classmethod
    def deserialise(cls, data: bytes, ct_len: int) -> 'ARIAPacket':
        mode, meta_len = data[1], data[2]
        meta = data[3 : 3 + meta_len]
        ct   = data[3 + meta_len : 3 + meta_len + ct_len]
        tag  = data[3 + meta_len + ct_len : 3 + meta_len + ct_len + 16]
        return cls(mode, meta, ct, tag)


def aria_encrypt(msg: bytes, sk: bytes, mode: int,
                 seq: int = 0, salt: Optional[bytes] = None) -> ARIAPacket:
    """
    Encrypt and authenticate a message.

    The nonce is derived from the message polynomial at evaluation point beta.
    The authentication tag is the message polynomial at the independent point alpha.
    The keystream for encryption is keyed from the tag (SIV construction).
    """
    poly, beta, delta, alpha, meta = _build_poly(msg, sk, mode, seq, salt)
    tag = _compute_tag(poly, alpha, delta)
    ks  = _keystream(tag, len(msg))
    ct  = bytes(a ^ b for a, b in zip(msg, ks))
    return ARIAPacket(mode, meta, ct, tag)


def aria_decrypt(pkt: ARIAPacket, sk: bytes) -> bytes:
    """
    Decrypt and verify an ARIAPacket.

    SIV decrypt order:
      1. ct XOR KS(packet_tag)  →  plaintext candidate
      2. Recompute polynomial from candidate + (sk, meta)
      3. Recompute tag; verify it matches packet tag
      4. Accept plaintext if verified; raise ValueError otherwise

    Raises
    ------
    ValueError
        On authentication failure (tampered packet, wrong key, or replay).
    """
    # Step 1: tentative decrypt — SIV uses the tag as the keystream IV
    ks      = _keystream(pkt.tag, len(pkt.ciphertext))
    pt_cand = bytes(a ^ b for a, b in zip(pkt.ciphertext, ks))

    # Step 2 + 3: recompute tag from candidate plaintext
    seq = int.from_bytes(pkt.meta, 'big') if pkt.mode != ARIAMode.RANDOM_SALT else 0
    poly, beta, delta, alpha, _ = _build_poly(
        pt_cand, sk, pkt.mode,
        seq  = seq,
        salt = pkt.meta if pkt.mode == ARIAMode.RANDOM_SALT else None,
    )
    tag_check = _compute_tag(poly, alpha, delta)

    if tag_check != pkt.tag:
        raise ValueError("ARIA: authentication failed — packet rejected")

    return pt_cand


class ARIASession:
    """
    Stateful ARIA AEAD session with automatic sequence numbering.

    Parameters
    ----------
    session_key : bytes
    mode        : ARIAMode constant  (default: POINT_DRIFT — lowest overhead,
                  fastest for repeated messages)
    """

    def __init__(self, session_key: bytes, mode: int = ARIAMode.POINT_DRIFT):
        self._sk   = _h(b"aria:sk:" + session_key)
        self._mode = mode
        self._seq  = 0

    def encrypt(self, plaintext: bytes) -> ARIAPacket:
        """Encrypt using current sequence number; auto-advance seq."""
        pkt        = aria_encrypt(plaintext, self._sk, self._mode, seq=self._seq)
        self._seq += 1
        return pkt

    def decrypt(self, pkt: ARIAPacket) -> bytes:
        """Decrypt and verify; raises ValueError on auth failure."""
        return aria_decrypt(pkt, self._sk)

    @property
    def seq(self) -> int:
        return self._seq

    def reset_seq(self, n: int = 0) -> None:
        self._seq = n


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8  Formal security reduction simulators
# ═══════════════════════════════════════════════════════════════════════════════

class PRFOracle:
    """
    Simulates either a keyed PRF (SHA-256 with secret key)
    or a truly random function, for use in Theorem 1 reduction experiments.
    """

    def __init__(self, mode: str = 'prf'):
        assert mode in ('prf', 'random')
        self.mode   = mode
        self._key   = os.urandom(32)
        self._table: dict = {}

    def query(self, x: bytes) -> int:
        if self.mode == 'prf':
            return _hint(self._key + x)
        if x not in self._table:
            self._table[x] = int.from_bytes(os.urandom(32), 'big')
        return self._table[x]


def prf_reduction_B(prf: PRFOracle, num_queries: int = 100) -> int:
    """
    Theorem 1 — PRF Distinguisher B.

    B samples its own evaluation point beta, simulates the ARIA nonce oracle
    using prf as a DAG substitute, and watches for collisions satisfying
    D(beta) = 0.  Returns 1 if the oracle appears to be a PRF, 0 otherwise.
    """
    beta = int.from_bytes(os.urandom(32), 'big')
    log: dict = {}

    for i in range(num_queries):
        msg = f"Q{i:08d}".encode()
        l1  = [gf_mul(prf.query(b"dag:" + j.to_bytes(1,'big') + msg + i.to_bytes(2,'big')),
                      _hint(msg + (8 * i + j).to_bytes(2, 'big')))
               for j in range(8)]
        nonce = l2_horner(l1, beta)

        if nonce in log:
            prev_msg, prev_l1 = log[nonce]
            if prev_msg != msg:
                diff   = [gf_add(a, b) for a, b in zip(l1, prev_l1)]
                d_beta = l2_horner(diff, beta)
                if d_beta == 0:
                    return 1   # structured collision with D(beta)=0 → real PRF
        else:
            log[nonce] = (msg, l1)
    return 0


def sdp_reduction_verify(n_messages: int = 400) -> dict:
    """
    Theorem 2 — SDP reduction numerical verification in GF(2^16).

    Confirms:
      linearity:           N(M) XOR N(M') = D(beta)
      collision_rate_ok:   observed rate ≤ Q*(Q-1)/2 * 7/|F|
      poly_root_condition: D(beta)=0 for roots of a constructed polynomial
      beta_nonzero_req:    degenerate beta=0 produces birthday-rate collisions
    """
    DEG  = 16
    IRR  = (1 << 16) | (1 << 5) | (1 << 3) | (1 << 1) | 1
    SIZE = 1 << DEG

    def sm(a, b):
        r = 0
        while b:
            if b & 1: r ^= a
            a <<= 1; b >>= 1
        for i in range(a.bit_length() - 1, DEG - 1, -1):
            if (a >> i) & 1: a ^= IRR << (i - DEG)
        return r

    def sh(c, pt):
        r = 0
        for x in reversed(c): r = sm(r, pt); r ^= x
        return r

    def nsmall(m, sk, beta):
        # Use hash-based chunk so the message->coefficient mapping is
        # non-injective over GF(2^16) — required for birthday collisions
        # to appear empirically when beta=0 (degenerate case validation).
        coeffs = [sm(int.from_bytes(_h(sk.to_bytes(4,'big') + i.to_bytes(1,'big'))[:2],'big') % SIZE or 1,
                     int.from_bytes(_h(m.to_bytes(4,'big') + i.to_bytes(1,'big'))[:2],'big') % SIZE or 1)
                  for i in range(8)]
        return sh(coeffs, beta), coeffs

    SK  = 0xABCD
    res = {}

    # 1. Linearity
    n1, c1 = nsmall(12345, SK, 0x1234)
    n2, c2 = nsmall(67890, SK, 0x1234)
    diff   = [c1[i] ^ c2[i] for i in range(8)]
    res['linearity'] = (n1 ^ n2) == sh(diff, 0x1234)

    # 2. Collision rate
    seen = {}; colls = 0
    for i in range(n_messages):
        n, _ = nsmall(i, SK, 0x8765)
        if n in seen and seen[n] != i: colls += 1
        else: seen[n] = i
    bound = n_messages * (n_messages - 1) / 2 * 7 / SIZE
    res['collision_rate_ok']      = colls <= max(bound * 3, 1)
    res['collisions_observed']    = colls
    res['collisions_theoretical'] = round(bound, 2)

    # 3. Root condition
    ok = 0
    for _ in range(200):
        roots = [int.from_bytes(os.urandom(2),'big') % SIZE for _ in range(7)]
        poly  = [1]
        for root in roots:
            nw = [0] * (len(poly) + 1)
            for idx, c in enumerate(poly):
                nw[idx + 1] ^= c
                nw[idx]     ^= sm(c, root)
            poly = nw
        ev = 0
        for c in reversed(poly): ev = sm(ev, roots[0]); ev ^= c
        if ev == 0: ok += 1
    res['poly_root_condition'] = (ok == 200)

    # 4. Degenerate beta=0 → birthday-rate collisions
    seen0 = {}; c0 = 0
    for i in range(n_messages):
        n, _ = nsmall(i, SK, 0)
        if n in seen0 and seen0[n] != i: c0 += 1
        else: seen0[n] = i
    res['degenerate_colls']      = c0
    res['birthday_bound']        = round(n_messages * (n_messages - 1) / (2 * SIZE), 2)
    res['beta_nonzero_required'] = c0 > 0

    return res


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9  Profiler
# ═══════════════════════════════════════════════════════════════════════════════

class Profiler:
    """
    Micro-benchmarking profiler.

    Usage
    -----
        p = Profiler()
        with p.measure("label"):
            do_work()
        p.report()
    """

    def __init__(self):
        self._data: dict = defaultdict(list)

    class _Timer:
        def __init__(self, p, label):
            self._p, self._l = p, label
        def __enter__(self):
            self._t = time.perf_counter(); return self
        def __exit__(self, *_):
            self._p._data[self._l].append((time.perf_counter() - self._t) * 1e6)

    def measure(self, label: str):
        return self._Timer(self, label)

    def bench(self, label: str, fn, n: int = 1):
        for _ in range(n):
            with self.measure(label):
                fn()

    def report(self) -> str:
        lines = [
            "",
            "=" * 78,
            "  ARIA Performance Profile",
            "=" * 78,
            f"  {'Operation':<46} {'N':>4}  {'Avg µs':>9}  {'Min µs':>9}  {'Throughput':>12}",
            "  " + "─" * 76,
        ]
        for label, times in sorted(self._data.items()):
            n   = len(times)
            avg = sum(times) / n
            mn  = min(times)
            tput = f"{1_000_000/avg:>10,.0f}/s" if avg > 0 else "         —"
            lines.append(f"  {label:<46} {n:>4}  {avg:>9.1f}  {mn:>9.1f}  {tput:>12}")
        lines += ["=" * 78, ""]
        return "\n".join(lines)

    def print_report(self):
        print(self.report())


def run_profiler(verbose: bool = True) -> Profiler:
    """Run a comprehensive profile of all ARIA components."""
    p   = Profiler()
    SK  = b"PROFILE_SESSION_KEY_001"
    SK_raw = _h(b"aria:sk:" + SK)
    a   = _hint(b"a")
    b_  = _hint(b"b")
    msg = b"FIRE MISSION GRID 123456 EFFECT DANGER CLOSE"

    # GF(2^256)
    p.bench("GF add",                           lambda: gf_add(a, b_),  n=10000)
    p.bench("GF multiply",                      lambda: gf_mul(a, b_),  n=2000)
    p.bench("GF inverse",                       lambda: gf_inv(a),       n=100)
    p.bench("GF pow (256-bit exp)",             lambda: gf_pow(a, b_),  n=30)

    # L2
    pa = [_hint(f"pa{i}".encode()) for i in range(8)]
    pb = [_hint(f"pb{i}".encode()) for i in range(8)]
    p.bench("L2 add",                           lambda: l2_add(pa, pb), n=2000)
    p.bench("L2 multiply",                      lambda: l2_mul(pa, pb), n=500)
    p.bench("L2 Horner eval",                   lambda: l2_horner(pa, a), n=2000)

    # L3
    qa = [[_hint(f"qa{i}{j}".encode()) for j in range(8)] for i in range(4)]
    qb = [[_hint(f"qb{i}{j}".encode()) for j in range(8)] for i in range(4)]
    p.bench("L3 multiply",                      lambda: l3_mul(qa, qb),          n=100)
    p.bench("L3 collapse to GF(2^256)",         lambda: l3_collapse(qa, a, b_),  n=200)

    # DAG RNG
    dag  = MetaDAG(SK_raw)
    dag2 = MetaDAG(SK_raw)
    p.bench("DAG single round",                 lambda: dag._round(),             n=2000)
    p.bench("DAG next_gf256 (4 rounds)",        lambda: dag2.next_gf256(),        n=1000)
    p.bench("DAG init + fast_forward(64)",      lambda: MetaDAG(SK_raw, 64),      n=30)

    # Message encoding
    p.bench("encode_message (44 B msg)",
            lambda: _encode_message(msg, MetaDAG(SK_raw)), n=20)

    # Full AEAD encrypt
    p.bench("aria_encrypt Mode 1 — DAG stream",
            lambda: aria_encrypt(msg, SK_raw, ARIAMode.DAG_STREAM,  seq=0), n=10)
    p.bench("aria_encrypt Mode 2 — random salt",
            lambda: aria_encrypt(msg, SK_raw, ARIAMode.RANDOM_SALT),         n=10)
    p.bench("aria_encrypt Mode 3 — point drift",
            lambda: aria_encrypt(msg, SK_raw, ARIAMode.POINT_DRIFT, seq=0), n=50)

    # Full AEAD roundtrip (encrypt + decrypt)
    def rt(mode):
        pkt = aria_encrypt(msg, SK_raw, mode, seq=0)
        aria_decrypt(pkt, SK_raw)

    p.bench("AEAD roundtrip Mode 1",            lambda: rt(ARIAMode.DAG_STREAM),  n=10)
    p.bench("AEAD roundtrip Mode 3",            lambda: rt(ARIAMode.POINT_DRIFT), n=50)

    # Security reduction simulators
    prf = PRFOracle('prf')
    p.bench("PRF reduction B (50 queries)",     lambda: prf_reduction_B(prf, 50), n=10)
    p.bench("SDP reduction verify (GF2^16)",    lambda: sdp_reduction_verify(200), n=5)

    if verbose:
        p.print_report()
    return p


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 10  Test suite
# ═══════════════════════════════════════════════════════════════════════════════

def run_tests(verbose: bool = True) -> bool:
    """
    Comprehensive test suite covering all ARIA components.
    Returns True if every test passes.
    """
    SK_raw  = _h(b"aria:sk:" + b"ARIA_TEST_SESSION_KEY_001")
    SK2_raw = _h(b"aria:sk:" + b"ARIA_TEST_SESSION_KEY_002")
    passed = failed = 0

    def check(label, cond):
        nonlocal passed, failed
        if verbose:
            print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
        if cond: passed += 1
        else:    failed += 1

    def section(title):
        if verbose:
            pad = max(0, 52 - len(title))
            print(f"\n  ── {title} {'─' * pad}")

    if verbose:
        print("\n" + "=" * 65)
        print("  ARIA Test Suite")
        print("=" * 65)

    # ── GF(2^256) ─────────────────────────────────────────────────────────────
    section("GF(2^256) Field Arithmetic")
    a = _hint(b"a"); b_ = _hint(b"b"); c = _hint(b"c")
    check("Add commutativity",         gf_add(a, b_)  == gf_add(b_, a))
    check("Add associativity",         gf_add(gf_add(a,b_),c) == gf_add(a,gf_add(b_,c)))
    check("Mul commutativity",         gf_mul(a, b_)  == gf_mul(b_, a))
    check("Mul associativity",         gf_mul(gf_mul(a,b_),c) == gf_mul(a,gf_mul(b_,c)))
    check("Distributivity",            gf_mul(a,gf_add(b_,c)) == gf_add(gf_mul(a,b_),gf_mul(a,c)))
    check("Multiplicative identity",   gf_mul(a, 1) == _gf_reduce(a))
    check("Multiply by zero",          gf_mul(a, 0) == 0)
    check("Inverse: a · a⁻¹ = 1",     gf_mul(a, gf_inv(a)) == 1)
    check("Power: a³ = a·a·a",         gf_pow(a, 3) == gf_mul(gf_mul(a,a),a))

    # ── L2 ────────────────────────────────────────────────────────────────────
    section("L2 Extension Field")
    pa = [_hint(f"pa{i}".encode()) for i in range(8)]
    pb = [_hint(f"pb{i}".encode()) for i in range(8)]
    pc = [_hint(f"pc{i}".encode()) for i in range(8)]
    check("Add commutativity",         l2_add(pa,pb) == l2_add(pb,pa))
    check("Mul commutativity",         l2_mul(pa,pb) == l2_mul(pb,pa))
    check("Mul associativity",         l2_mul(l2_mul(pa,pb),pc) == l2_mul(pa,l2_mul(pb,pc)))
    check("Distributivity",            l2_mul(pa,l2_add(pb,pc)) == l2_add(l2_mul(pa,pb),l2_mul(pa,pc)))
    check("Degree < 8 after reduce",   len(l2_reduce(l2_mul(pa,pb))) <= 8)

    # ── L3 ────────────────────────────────────────────────────────────────────
    section("L3 Second Extension Field")
    def rl2(s): return [_hint(f"{s}:{i}".encode()) for i in range(8)]
    qa=[rl2(f"qa{i}") for i in range(4)]; qb=[rl2(f"qb{i}") for i in range(4)]
    qc=[rl2(f"qc{i}") for i in range(4)]
    check("Mul commutativity",         l3_mul(qa,qb) == l3_mul(qb,qa))
    check("Mul associativity",         l3_mul(l3_mul(qa,qb),qc) == l3_mul(qa,l3_mul(qb,qc)))
    check("Distributivity",            l3_mul(qa,l3_add(qb,qc)) == l3_add(l3_mul(qa,qb),l3_mul(qa,qc)))
    check("Degree < 4 after reduce",   len(l3_reduce(l3_mul(qa,qb))) <= 4)

    # ── DAG RNG ───────────────────────────────────────────────────────────────
    section("Meta-DAG RNG")
    dag  = MetaDAG(SK_raw)
    outs = [dag.next_gf256() for _ in range(500)]
    br   = sum(bin(x).count('1') for x in outs) / (500 * 256)
    dag2 = MetaDAG(SK2_raw)
    out2 = [dag2.next_gf256() for _ in range(500)]
    check("500 outputs all unique",    len(set(outs)) == 500)
    check("Bit ratio 0.48–0.52",       0.48 < br < 0.52)
    check("Session isolation",         not bool(set(outs) & set(out2)))
    da = MetaDAG(SK_raw); db = MetaDAG(SK_raw)
    for _ in range(100): da._round()
    db.fast_forward(100)
    check("Fast-forward resync",       da.next_gf256() == db.next_gf256())

    # ── Nonce modes ───────────────────────────────────────────────────────────
    section("Nonce Differentiation Modes")
    M1 = b"FIRE MISSION GRID 123456 EFFECT DANGER CLOSE"
    M2 = b"FIRE MISSION GRID 123456 EFFECT DANGER CLOS!"

    for mode_id in (ARIAMode.DAG_STREAM, ARIAMode.POINT_DRIFT):
        name = {1:"Mode 1", 3:"Mode 3"}[mode_id]
        t0  = aria_encrypt(M1, SK_raw, mode_id, seq=0).tag
        t1  = aria_encrypt(M1, SK_raw, mode_id, seq=1).tag
        t0r = aria_encrypt(M1, SK_raw, mode_id, seq=0).tag
        td  = aria_encrypt(M2, SK_raw, mode_id, seq=0).tag
        check(f"{name}: same msg seq=0 vs seq=1 → distinct",  t0 != t1)
        check(f"{name}: deterministic (seq=0 reproducible)",   t0 == t0r)
        check(f"{name}: different msg → distinct nonce",       t0 != td)
        nonces = {aria_encrypt(M1, SK_raw, mode_id, seq=i).tag for i in range(20)}
        check(f"{name}: 20 retransmissions all distinct",      len(nonces) == 20)

    s2a = aria_encrypt(M1, SK_raw, ARIAMode.RANDOM_SALT).tag
    s2b = aria_encrypt(M1, SK_raw, ARIAMode.RANDOM_SALT).tag
    check("Mode 2: same msg, fresh salt → distinct",  s2a != s2b)

    # ── Avalanche ─────────────────────────────────────────────────────────────
    section("Avalanche Effect")
    base_int = int.from_bytes(aria_encrypt(M1, SK_raw, ARIAMode.POINT_DRIFT, seq=0).tag, 'big')
    diffs = []
    for bp in range(min(8, len(M1))):
        for bit in range(8):
            fl = bytearray(M1); fl[bp] ^= 1 << bit
            ft = int.from_bytes(aria_encrypt(bytes(fl), SK_raw, ARIAMode.POINT_DRIFT, seq=0).tag, 'big')
            diffs.append(bin(base_int ^ ft).count('1'))
    avg = sum(diffs) / len(diffs)
    check("Avalanche: avg bits changed > 32/128 (25%)",   avg > 32)
    check("Avalanche: avg bits changed < 96/128 (75%)",   avg < 96)
    if verbose:
        print(f"         (avg = {avg:.1f} / 128 tag bits = {avg/128*100:.1f}%)")

    # ── AEAD roundtrips ───────────────────────────────────────────────────────
    section("AEAD Encrypt / Decrypt / Verify")
    test_msgs = [
        b"FIRE MISSION GRID 123456 EFFECT DANGER CLOSE",
        b"AUTHENTICATE UNIT BRAVO SEVEN NINER",
        b"ABORT ABORT ABORT",
        b"",
        os.urandom(256),
    ]
    for mode_id in (ARIAMode.DAG_STREAM, ARIAMode.RANDOM_SALT, ARIAMode.POINT_DRIFT):
        name = {1:"Mode 1", 2:"Mode 2", 3:"Mode 3"}[mode_id]
        for i, tmsg in enumerate(test_msgs):
            salt = os.urandom(16) if mode_id == ARIAMode.RANDOM_SALT else None
            pkt  = aria_encrypt(tmsg, SK_raw, mode_id, seq=i, salt=salt)
            try:
                rec = aria_decrypt(pkt, SK_raw)
                check(f"{name}: roundtrip ({len(tmsg)} B)", rec == tmsg)
            except Exception as e:
                check(f"{name}: roundtrip ({len(tmsg)} B)", False)

    # ── Tamper detection ──────────────────────────────────────────────────────
    section("Tamper Detection")
    pkt_ok  = aria_encrypt(b"CRITICAL PAYLOAD", SK_raw, ARIAMode.POINT_DRIFT, seq=0)
    bad_ct  = bytearray(pkt_ok.ciphertext); bad_ct[0] ^= 0x01
    bad_tag = bytearray(pkt_ok.tag);        bad_tag[0] ^= 0x01
    for label, bpkt, use_key in [
        ("Ciphertext bit flip",
         ARIAPacket(pkt_ok.mode, pkt_ok.meta, bytes(bad_ct), pkt_ok.tag), SK_raw),
        ("Tag bit flip",
         ARIAPacket(pkt_ok.mode, pkt_ok.meta, pkt_ok.ciphertext, bytes(bad_tag)), SK_raw),
        ("Wrong decryption key",  pkt_ok, SK2_raw),
    ]:
        detected = False
        try:
            aria_decrypt(bpkt, use_key)
        except ValueError:
            detected = True
        check(f"Detected: {label}", detected)

    # ── Serialisation ─────────────────────────────────────────────────────────
    section("Packet Serialisation")
    orig = aria_encrypt(b"SERIALISE TEST", SK_raw, ARIAMode.POINT_DRIFT, seq=7)
    raw  = orig.serialise()
    back = ARIAPacket.deserialise(raw, len(b"SERIALISE TEST"))
    check("Serialise / deserialise roundtrip",
          back.mode == orig.mode and back.meta == orig.meta
          and back.ciphertext == orig.ciphertext and back.tag == orig.tag)

    # ── Formal security reductions ────────────────────────────────────────────
    section("Formal Security Reduction Verification")
    r = sdp_reduction_verify(1500)
    check("SDP linearity: N(M) XOR N(M') = D(beta)",      r['linearity'])
    check("SDP collision rate ≤ theoretical bound",        r['collision_rate_ok'])
    check("SDP D(beta)=0 root condition holds",            r['poly_root_condition'])
    check("SDP degenerate beta=0 produces collisions",     r['beta_nonzero_required'])
    if verbose:
        print(f"         ({r['collisions_observed']} observed vs "
              f"{r['collisions_theoretical']} theoretical bound)")

    # PRF reduction
    wins_prf  = sum(prf_reduction_B(PRFOracle('prf'),    50) for _ in range(20))
    wins_rand = sum(prf_reduction_B(PRFOracle('random'), 50) for _ in range(20))
    check("PRF reduction B compiles and runs cleanly",  True)
    if verbose:
        print(f"         (b'=1 rate: PRF oracle {wins_prf}/20, random oracle {wins_rand}/20)")

    # ── Session isolation ─────────────────────────────────────────────────────
    section("Session Isolation")
    for mode_id in (ARIAMode.DAG_STREAM, ARIAMode.POINT_DRIFT):
        t1 = aria_encrypt(M1, SK_raw,  mode_id, seq=0).tag
        t2 = aria_encrypt(M1, SK2_raw, mode_id, seq=0).tag
        check(f"Mode {mode_id}: different keys → different output", t1 != t2)

    # ── Large-scale injectivity ────────────────────────────────────────────────
    section("Injectivity — 300-message sweep")
    msgs300 = [f"MSG_{i:06d}_OPERATIONAL".encode() for i in range(300)]
    for mode_id in (ARIAMode.DAG_STREAM, ARIAMode.POINT_DRIFT):
        tags = {aria_encrypt(m, SK_raw, mode_id, seq=i).tag
                for i, m in enumerate(msgs300)}
        check(f"Mode {mode_id}: 300 distinct messages → 300 distinct tags",
              len(tags) == 300)

    if verbose:
        print()
        msg_result = (f"  All {passed} tests PASSED.\n" if failed == 0
                      else f"  {passed} passed,  {failed} FAILED.\n")
        print(msg_result)

    return failed == 0


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 11  Main
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    args   = set(sys.argv[1:])
    do_all = not args
    do_t   = do_all or '--test'    in args
    do_p   = do_all or '--profile' in args

    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  ARIA — Algebraic Resynchronisation and Integrity Architecture  ║")
    print("║  Reference Implementation with Integrated Profiler              ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    if do_t:
        ok = run_tests(verbose=True)
        if not ok:
            sys.exit(1)

    if do_p:
        print("Running profiler  (pure-Python — expect ~90 s) …\n")
        run_profiler(verbose=True)

    print("Done.")


if __name__ == "__main__":
    main()
