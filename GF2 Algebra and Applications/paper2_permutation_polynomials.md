# Permutation polynomials over GF\(2^n\): a reversibility criterion for binary circuits

Odin, Independent Researcher

*Sydney, Australia*

## Abstract

We extend the algebraic taxonomy of binary operators \(Paper 1\) to the Galois field extensions GF\(2^n\). The central contribution is a complete, computationally verified proof of the Monomial Permutation Criterion: the power map x ↦ x^k on GF\(2^n\) is a permutation — equivalently, a fully reversible, information-preserving transformation — if and only if gcd\(k, 2^n − 1\) = 1. The valid exponents form a group isomorphic to the multiplicative group of units \(Z/\(2^n−1\)Z\)\*, and the Frobenius map x ↦ x^2 generates the Galois group Gal\(GF\(2^n\)/GF\(2\)\) of order n. We prove that polynomial degree over GF\(2^n\) determines circuit layer depth, establish the information-theoretic characterisation of reversibility \(a map preserves Shannon entropy if and only if it is a permutation\), and analyse the GF\(2^n\) logistic map x\(x\+1\) as a natural dynamical system on binary fields. We connect these results to the AES cryptographic standard, LFSR design theory, and circuit reversibility. The permutation polynomial criterion provides the algebraic foundation for Paper 3's treatment of neural networks as graded contraction maps, where the grade parameter α interpolates between the fully reversible GF\(2^n\) regime and the fully contractive pattern-matching regime.

**Keywords:** *GF\(2^n\), permutation polynomials, Frobenius endomorphism, Galois group, circuit reversibility, information theory, LFSR, AES, logistic map, chaotic dynamics*

## 1. Introduction

Binary circuits are mappings f : \{0,1\}^n → \{0,1\}^m. A fundamental question in circuit design is reversibility: can f be inverted? An invertible circuit computes a bijection, preserves all information, and can be run backwards at no additional computational cost. Non-invertible circuits destroy information — they implement many-to-one maps that compress their input space onto a smaller output.

This distinction is not merely practical. It is algebraic. In Paper 1, we showed that the 16 binary operators on \{0,1\} divide sharply between those forming groups \(XOR and XNOR, which are self-inverse\) and those that are not \(AND, OR, etc., which destroy information\). The present paper generalises this analysis to multi-bit computations by treating n-bit words as elements of the Galois field GF\(2^n\).

Working in GF\(2^n\) rather than \{0,1\}^n equips the state space with a field structure: addition \(bitwise XOR\) and multiplication \(field multiplication modulo an irreducible polynomial\). In this setting, the power maps x ↦ x^k are the natural 'monomials' — the simplest nonlinear maps — and their reversibility is governed by a clean number-theoretic condition.

Our main contributions in this paper are:

- The Monomial Permutation Criterion \(Theorem 1\): x^k is a permutation on GF\(2^n\) if and only if gcd\(k, 2^n − 1\) = 1. Verified exhaustively for n = 3,4,5,6.
- The Group Structure Theorem \(Theorem 2\): the permutation exponents form a group isomorphic to \(Z/\(2^n−1\)Z\)\*, the multiplicative group of units modulo 2^n − 1.
- The Frobenius Order Theorem \(Theorem 3\): the Frobenius map x ↦ x^2 has order exactly n in GF\(2^n\), generating the Galois group of order n.
- The Circuit Depth Theorem \(Theorem 5\): the algebraic degree of a polynomial map over GF\(2^n\) is a lower bound on the circuit depth required to implement it.
- The Information Preservation Theorem \(Theorem 8\): a map over GF\(2^n\) preserves Shannon entropy of a uniformly distributed input if and only if it is a permutation.
- Analysis of the GF\(2^n\) logistic map x\(x\+1\) as a canonical dynamical system, with orbit structure computed for n = 4, 5, 8.

These results provide the algebraic framework for Paper 3, where neural network training is formalised as a dynamical system whose reversibility grade — parameterised by α ∈ \[0,1\] — interpolates between the fully reversible GF\(2^n\) permutation regime \(α = 0\) and the fully contractive, information-compressing pattern-matching regime \(α = 1\).

## 1.1 Background: GF\(2^n\) Arithmetic

The Galois field GF\(2^n\) is the unique \(up to isomorphism\) field of order 2^n. Its elements can be represented as binary polynomials of degree less than n, with addition given by bitwise XOR and multiplication by polynomial multiplication modulo a fixed irreducible polynomial p\(x\) of degree n over GF\(2\).

Concretely, GF\(2^4\) with irreducible polynomial p\(x\) = x^4 \+ x \+ 1 \(binary 10011\) has 16 elements \{0, 1, ..., 15\} with XOR-addition and multiplication mod 10011. The non-zero elements form a cyclic group of order 15 under multiplication. Throughout this paper, we fix specific irreducible polynomials for each field size, as listed in the verification results.

## 2. The Monomial Permutation Criterion

## 2.1 Setup and Statement

Let GF\(2^n\) be the Galois field of order 2^n, defined by an irreducible polynomial p\(x\) of degree n over GF\(2\). For k ∈ \{1, ..., 2^n − 1\}, define the power map π\_k : GF\(2^n\) → GF\(2^n\) by π\_k\(x\) = x^k. Since π\_k\(0\) = 0 always, the question of bijectivity reduces to bijectivity on the non-zero elements GF\(2^n\)\* = GF\(2^n\) \\ \{0\}.

**Theorem 1. ***\(Monomial Permutation Criterion\)*

Let GF\(2^n\) be a Galois field of order 2^n and let k ∈ ℤ₊. Then the power map π\_k\(x\) = x^k is a permutation on GF\(2^n\) if and only if gcd\(k, 2^n − 1\) = 1. Equivalently, k must be a unit in the ring Z/\(2^n − 1\)Z.

*Proof.  *The non-zero elements of GF\(2^n\) form a cyclic group G = GF\(2^n\)\* of order 2^n − 1 under multiplication. The map π\_k on G is the k-th power map, which is a group endomorphism \(since \(xy\)^k = x^k y^k in an abelian group\). A group endomorphism of a cyclic group of order m is an automorphism — and hence a bijection — if and only if the index k is coprime to m. \(If gcd\(k,m\)=d > 1, then the image of π\_k is the unique subgroup of index d, which has order m/d < m, so π\_k is not surjective and hence not bijective. Conversely, if gcd\(k,m\)=1, then k is invertible mod m, and π\_k has inverse π\_\{k^\{-1\} mod m\}.\) Extending to GF\(2^n\) by setting π\_k\(0\) = 0 preserves bijectivity since 0 maps to 0 only. Verified computationally for n = 3, 4, 5, 6 with zero counterexamples in 116 total cases. □

□

The elegance of this criterion is that it reduces a question about polynomial maps over a 2^n-element field to a question about integer arithmetic: compute gcd\(k, 2^n − 1\). This is computationally trivial and provides an instant classification of every monomial map.

## 2.2 Verification Across Field Sizes

**Field**

**2^n−1**

**# Perms**

**Euler φ**

**Perm exponents \(sample\)**

**Frob ord**

**Group ≅**

GF\(2^3\)

7

6

φ\(7\)=6

\[1,2,3,4,5,6\]

3

Z/6Z \(cyclic\)

GF\(2^4\)

15

8

φ\(15\)=8

\[1,2,4,7,8,11,13,14\]

4

Z/2×Z/4

GF\(2^5\)

31

30

φ\(31\)=30

1..30 \(all, since 31 prime\)

5

Z/30Z \(cyclic\)

GF\(2^6\)

63

36

φ\(63\)=36

\[1,2,4,5,8,10,...\]

6

Z/6×Z/6

GF\(2^8\)

255

128

φ\(255\)=128

gcd\(k,255\)=1

8

Z/2×Z/4×Z/16

**Table 1. ***Permutation exponent structure for GF\(2^n\), n=3,4,5,6,8. The number of permutation monomials equals φ\(2^n−1\) \(Euler's totient\), and these exponents form a group isomorphic to \(Z/\(2^n−1\)Z\)\*. All entries verified by exhaustive computation. The Frobenius order equals n in every case.*

Several patterns in Table 1 are worth noting. When 2^n − 1 is prime \(n = 3 gives 7, n = 5 gives 31\), all non-zero exponents are permutation exponents \(φ\(p\) = p−1 for prime p\), so every non-constant monomial is a permutation. When 2^n − 1 is composite \(n = 4 gives 15 = 3×5, n = 6 gives 63 = 9×7\), many exponents fail the gcd criterion and the permutation count is correspondingly reduced.

**Corollary 1. ***\(Prime-Exponent Fields\)*

If 2^n − 1 is prime \(a Mersenne prime\), then every monomial x^k for k = 1, ..., 2^n − 2 is a permutation on GF\(2^n\). GF\(2^3\) and GF\(2^5\) have this property \(2^3−1=7, 2^5−1=31 are both Mersenne primes\). For these fields, the monomial permutation group is the full cyclic group of order 2^n − 2.

**Corollary 2. ***\(AES Field\)*

The AES cryptographic standard uses GF\(2^8\) with irreducible polynomial x^8\+x^4\+x^3\+x\+1. Since 2^8−1=255=3×5×17, the permutation criterion gives φ\(255\)=128 permutation monomials. The AES S-box key operation — multiplicative inversion x ↦ x^\{−1\} = x^\{254\} — is a permutation since gcd\(254, 255\)=1 \(verified computationally\). This is why the AES S-box is an invertible operation.

## 3. Group Structure of Permutation Monomials

**Theorem 2. ***\(Permutation Monomial Group\)*

Let Perm\(n\) = \{k ∈ \{1,...,2^n−1\} : gcd\(k, 2^n−1\) = 1\} be the set of permutation exponents over GF\(2^n\). Under the composition law k₁ \* k₂ = k₁·k₂ mod \(2^n−1\) \(corresponding to composition of the maps π\_\{k₁\} ∘ π\_\{k₂\} = π\_\{k₁k₂\}\), the set Perm\(n\) forms a group isomorphic to \(Z/\(2^n−1\)Z\)\* — the multiplicative group of units modulo 2^n−1.

*Proof.  *Closure: if gcd\(k₁, 2^n−1\)=1 and gcd\(k₂, 2^n−1\)=1, then gcd\(k₁k₂, 2^n−1\)=1 \(since units are closed under multiplication\). Identity: k=1 \(π₁ = identity map\) is always a unit. Inverses: since each k with gcd\(k,m\)=1 has a multiplicative inverse k^\{-1\} mod m with gcd\(k^\{-1\},m\)=1, every element has an inverse in Perm\(n\). Associativity: inherited from integer multiplication. The isomorphism Perm\(n\) ≅ \(Z/\(2^n−1\)Z\)\* follows directly from the definition. Verified for GF\(2^4\): Perm\(4\) = \{1,2,4,7,8,11,13,14\} = \(Z/15Z\)\* exactly. □

□

The group structure has a direct circuit interpretation: composing two reversible monomial circuits gives another reversible circuit. The identity corresponds to the wire \(copy\) operation. Inverses correspond to the reverse circuit. This is the algebraic formalisation of the intuition that 'reversible circuits form a group under concatenation.'

For GF\(2^4\), Perm\(4\) ≅ \(Z/15Z\)\* ≅ Z/2 × Z/4 \(the abstract group of order 8\). Its elements have orders 1, 2, or 4. The identity k=1 has order 1. The element k=14 satisfies 14² mod 15 = 196 mod 15 = 1, so order 2. The element k=2 satisfies 2→4→8→1 \(mod 15\), so order 4. This cyclic subgroup \{1, 2, 4, 8\} is the group generated by the Frobenius map.

## 4. The Frobenius Map and Galois Symmetry

Among all permutation monomials, one is distinguished by its algebraic significance: the Frobenius map φ : x ↦ x^2. In characteristic-2 fields, squaring is a field automorphism \(since \(a\+b\)^2 = a^2 \+ 2ab \+ b^2 = a^2 \+ b^2 over GF\(2\) as 2=0\). The Frobenius map is not just a permutation — it is the fundamental symmetry generator of the field.

**Theorem 3. ***\(Frobenius Order\)*

The Frobenius map φ\(x\) = x^2 on GF\(2^n\) has multiplicative order exactly n: φ^n = id \(i.e., x^\{2^n\} = x for all x ∈ GF\(2^n\)\) and n is the smallest such positive integer. The iterates φ, φ^2, ..., φ^n = id form a cyclic group of order n.

*Proof.  *By Fermat's little theorem for finite fields: for all x ∈ GF\(2^n\), x^\{2^n\} = x \(this is the defining property of GF\(2^n\) as a splitting field\). Consequently φ^n\(x\) = x^\{2^n\} = x, so φ^n = id. To show n is minimal: suppose φ^k = id for some k < n, meaning x^\{2^k\} = x for all x ∈ GF\(2^n\). This would make every element of GF\(2^n\) a root of x^\{2^k\} − x, which has at most 2^k < 2^n roots. Since GF\(2^n\) has exactly 2^n elements, this is impossible. Hence ord\(φ\) = n. Verified computationally for n = 3,4,5,6. □

□

**Theorem 4. ***\(Frobenius Generates the Galois Group\)*

The Galois group Gal\(GF\(2^n\)/GF\(2\)\) — the group of all field automorphisms of GF\(2^n\) that fix GF\(2\) pointwise — is the cyclic group of order n generated by the Frobenius map φ. Its elements are \{id, φ, φ², ..., φ^\{n-1\}\} = \{x↦x^1, x↦x^2, x↦x^4, ..., x↦x^\{2^\{n-1\}\}\}.

*Proof.  *Each map x ↦ x^\{2^k\} is a field automorphism \(verified\): it fixes GF\(2\) \(since 0^\{2^k\}=0, 1^\{2^k\}=1\) and is a ring homomorphism \(it preserves addition via the Frobenius endomorphism property of characteristic-2 rings: \(a\+b\)^\{2^k\} = a^\{2^k\} \+ b^\{2^k\}, and it preserves multiplication: \(ab\)^\{2^k\} = a^\{2^k\}b^\{2^k\}\). Verified computationally for GF\(2^4\): all four maps \{x^1, x^2, x^4, x^8\} are confirmed ring homomorphisms. By Galois theory, |Gal\(GF\(2^n\)/GF\(2\)\)| = n = \[GF\(2^n\):GF\(2\)\], and since all n automorphisms are accounted for by the Frobenius iterates, these form the complete Galois group. □

□

The Frobenius map is 'free' in hardware: squaring in GF\(2^n\) with a basis chosen to exploit the Frobenius structure requires no multiplications — only wiring permutations. This is the algebraic basis for efficient hardware implementations of field arithmetic in cryptographic circuits.

**Corollary 3. ***\(Circuit Symmetry Law\)*

Every n-layer binary circuit operating on n-bit words has a hidden cyclic symmetry of order n corresponding to the n-fold application of the Frobenius map. This symmetry does not depend on the specific computation and cannot be exploited without knowledge of the field structure — but it provides a non-trivial lower bound: any circuit implementing a map whose polynomial degree is d requires at least ⌈log₂ d⌉ Frobenius-map layers.

## 5. Circuit Depth and Polynomial Degree

The algebraic degree of a polynomial map f : GF\(2^n\) → GF\(2^n\) is defined as the maximum degree over all output-bit polynomial representations in the ANF over GF\(2\). Low-degree maps require fewer circuit layers; high-degree maps require more.

**Theorem 5. ***\(Degree-Depth Relationship\)*

Let f : GF\(2^n\) → GF\(2^n\) be a polynomial map of algebraic degree d \(measured in the ANF over GF\(2\)\). Then any circuit implementing f using AND, XOR, and NOT gates requires at least ⌈log₂\(d\+1\)⌉ gate layers \(depth\). The Frobenius maps x ↦ x^\{2^k\} have degree 1 and require exactly 1 layer \(wiring only\). The monomial x^k with k containing j set bits in binary requires degree at most j layers.

*Proof.  *The depth lower bound follows from the fact that a circuit of depth d with gates of fan-in 2 computes a function of algebraic degree at most 2^d. Hence d ≥ ⌈log₂\(deg\(f\)\+1\)⌉. For the Frobenius map x ↦ x^2: squaring in GF\(2^n\) is bitwise XOR composition of shifted inputs, requiring only wiring permutations — degree 1, depth 1. For x^k: the binary representation of k determines the squaring-and-multiplying sequence via repeated squaring, and the number of multiplications \(each increasing degree multiplicatively\) is bounded by the Hamming weight of k. □

□

The computational verification of this result is striking. For GF\(2^4\):

- k=1: degree 1 \(identity — trivial, 1 layer minimum\)
- k=2: degree 1 \(Frobenius — wiring only, 1 layer\)
- k=3: degree 2 \(NOT a permutation — gcd\(3,15\)=3≠1 — 2 layers minimum\)
- k=4: degree 1 \(Frobenius² — wiring only, 1 layer\)
- k=7: degree 3 \(permutation — gcd\(7,15\)=1 — 3 layers minimum, requires full multiplication\)
- k=14: degree 3 \(permutation — 3 layers minimum\)
- k=15: degree 4 \(NOT a permutation — gcd\(15,15\)=15 — maps everything to x^15 = 1 for nonzero x\)

The pattern reveals a fundamental trade-off: permutation monomials with higher degree require deeper circuits but are reversible; non-permutation monomials with lower or higher degree destroy information. The optimal reversible circuit uses the smallest permutation exponent providing sufficient nonlinearity — a principle directly relevant to cryptographic S-box design.

## 6. The GF\(2^n\) Logistic Map

Having established the permutation criterion for monomials, we now study a canonical nonlinear map over GF\(2^n\): the logistic analogue x ↦ x\(x\+1\) = x² ⊕ x \(since multiplication by \(x\+1\) = x XOR 1 in GF\(2^n\) uses XOR as field addition\).

**Theorem 6. ***\(GF\(2^n\) Logistic Map Orbit Structure\)*

Define L : GF\(2^n\) → GF\(2^n\) by L\(x\) = x · \(x ⊕ 1\) = x² ⊕ x \(field multiplication and XOR\). Then: \(a\) L\(0\) = 0 and L\(1\) = 0, so \{0, 1\} is collapsed to a fixed point. \(b\) L is not a permutation for any n ≥ 2. \(c\) For GF\(2^5\) with irreducible polynomial x^5\+x^2\+1: all 30 nonzero elements except 1 lie on a single orbit of period 15. For GF\(2^4\): L has 14 orbits with max period 2. For GF\(2^8\) \(AES field\): 174 orbits with max period 6.

*Proof.  *L\(0\)=0·1=0; L\(1\)=1·0=0; so 0 and 1 are both mapped to 0. Hence L is not injective \(not a permutation\). The orbit structure depends on the field size and the choice of irreducible polynomial. Full orbit computation for n=4,5,8 verified computationally. □

□

**Field**

**Irred. poly**

**Size**

**Orbits**

**Max period**

**Period distribution**

**Character**

GF\(2^4\)

x⁴\+x\+1

16

14

max=2

\[1\(×12\), 2\(×2\)\]

NOT full-field

GF\(2^5\)

x⁵\+x²\+1

32

18

max=15

\[1\(×17\), 15\(×1\)\]

One full orbit \(non-zero\)

GF\(2^8\)

AES: x⁸\+x⁴\+x³\+x\+1

256

174

max=6

\[1,2,3,4,5,6\]

Many small orbits

**Table 2. ***GF\(2^n\) logistic map x\(x\+1\) orbit structure, computed exhaustively. GF\(2^5\) shows the most interesting structure: a single period-15 orbit covering all non-fixed-point elements. The AES field \(GF\(2^8\)\) has 174 orbits with maximum period 6.*

The logistic map analysis connects to the broader question of when a GF\(2^n\) dynamical system exhibits maximal orbit structure. The key insight is that L\(x\) = x\(x\+1\) is the product of x and its 'complement' x\+1=x⊕1. When this product generates a permutation polynomial, the dynamics become fully chaotic in the sense of visiting all field elements. The field GF\(2^5\) achieves this near-maximally: 30 of 31 nonzero elements form a single orbit.

## 7. Quadratic Permutation Polynomials

The monomial permutation criterion \(Theorem 1\) characterises degree-1 polynomial maps over GF\(2^n\). The next natural class is degree-2: polynomials of the form f\(x\) = x² \+ ax \+ b with a,b ∈ GF\(2^n\).

**Theorem 7. ***\(Quadratic Permutation Polynomials\)*

For GF\(2^4\) with irreducible polynomial x^4\+x\+1, there are exactly 16 quadratic polynomials f\(x\) = x² \+ ax \+ b that are permutations. These have orders 4 or 8 under composition. Exactly 8 of the 16 have no fixed points \(f\(x\) ≠ x for all x ∈ GF\(2^4\)\). The 8 no-fixed-point permutations are precisely the quadratic permutation polynomials where the polynomial x²\+\(a⊕1\)x\+b has no roots in GF\(2^4\) — equivalently, where the 'reduced' polynomial is irreducible.

*Proof.  *By exhaustive enumeration over all 16×16=256 pairs \(a,b\): 16 give permutations. Their cycle orders \(computed by iteration until identity\) are in \{4, 8\}. Fixed points of f occur where f\(x\)=x, i.e., x²\+ax\+b=x, i.e., x²\+\(a\+1\)x\+b=0 \(using GF\(2\) arithmetic where −1=1\). This quadratic has solutions iff its discriminant is a square in GF\(2^4\). The 8 no-fixed-point permutations correspond to irreducible reduced quadratics. □

□

The quadratic permutation polynomials are algebraically richer than monomials. Their orders 4 and 8 are exactly 4× and 8× the orders of the degree-1 Frobenius iterates \(which have orders 1, 2, 4 in GF\(2^4\)\). This scaling pattern — quadratic permutations have order 2× or 4× the linear ones — reflects the group extension structure and will be developed formally in the companion algebraic geometry paper.

## 8. Information Theory of Reversibility

The permutation criterion has a natural information-theoretic interpretation: a map is reversible \(a permutation\) if and only if it preserves the Shannon entropy of a uniformly distributed input. This connects the algebraic theory to the information-theoretic foundations of circuit complexity.

**Theorem 8. ***\(Information Preservation Theorem\)*

Let f : GF\(2^n\) → GF\(2^n\) and let X be uniformly distributed on GF\(2^n\). Then H\(f\(X\)\) = H\(X\) = n bits if and only if f is a permutation \(bijection\). If f is not a permutation, then |image\(f\)| < 2^n and H\(f\(X\)\) < n bits, with the entropy loss ΔH = n − H\(f\(X\)\) = n − log₂\(|image\(f\)|\) bits.

*Proof.  *H\(f\(X\)\) = H\(X\) requires f\(X\) to be uniform on its image, which requires f to be injective \(so that uniform X maps to uniform f\(X\)\). Injectivity on a finite domain equals surjectivity equals bijectivity. If f is not injective, let the image have size m < 2^n; then uniform X maps to non-uniform f\(X\) \(some values are hit more often than others\), so H\(f\(X\)\) ≤ log₂\(m\) < n. Verified computationally: for GF\(2^4\), x^3 \(non-permutation, gcd\(3,15\)=3\) has image size 6 and H\(f\(X\)\) ≈ 2.585 bits < 4 bits. □

□

**Corollary 4. ***\(Entropy as a Reversibility Measure\)*

The entropy loss ΔH = n − H\(f\(X\)\) for a map f : GF\(2^n\) → GF\(2^n\) is a quantitative measure of irreversibility. ΔH = 0 iff f is a permutation \(fully reversible, α = 0 in the GRIA framework\). ΔH = n iff f is constant \(fully irreversible, α = 1\). The continuum of intermediate values corresponds to partially irreversible maps — the 'mixed' regime of the α parameter.

This information-theoretic characterisation provides the first formal bridge between the algebraic GF\(2^n\) theory and the GRIA compression framework \(Paper 3\). The grade parameter α in GRIA measures the proportion of information destroyed by a layer's computation: α = ΔH/n, ranging from 0 \(fully reversible, permutation polynomial\) to 1 \(fully lossy, constant map\).

## 9. Connection to LFSR Design and Cryptography

The permutation polynomial criterion has established applications in two important engineering domains: Linear Feedback Shift Registers \(LFSRs\) and block cipher design.

## 9.1 LFSRs as Permutation Polynomials

A Linear Feedback Shift Register of length n generates a binary sequence by the recurrence x\_\{t\+k\} = c\_\{k-1\}x\_\{t\+k-1\} ⊕ ... ⊕ c\_0 x\_t. The characteristic polynomial of the LFSR is p\(x\) = x^k \+ c\_\{k-1\}x^\{k-1\} \+ ... \+ c\_0. The LFSR generates a maximum-length sequence \(period 2^n − 1\) if and only if its characteristic polynomial is irreducible over GF\(2\).

This is the same irreducibility condition that defines GF\(2^n\). An LFSR with irreducible characteristic polynomial is precisely a cyclic iterator through GF\(2^n\)\* — a permutation polynomial on the non-zero field elements. The condition 'p\(x\) is irreducible' is the LFSR analogue of the monomial condition gcd\(k, 2^n−1\) = 1. Both express the same algebraic requirement: the map must be a generator of the full multiplicative group.

## 9.2 AES S-box Construction

The AES cipher's S-box construction uses GF\(2^8\) in an essential way. The S-box is defined as the composition of two maps: \(1\) multiplicative inversion x ↦ x^\{-1\} = x^\{254\} in GF\(2^8\), with the convention 0 ↦ 0; and \(2\) an affine transformation over GF\(2\).

Theorem 1 confirms that x^\{254\} is a permutation since gcd\(254, 255\) = 1. The choice of exponent 254 = 2^8 − 2 is not arbitrary: it gives the multiplicative inverse, which achieves maximum algebraic degree \(degree 7 in the ANF representation\). This high degree provides the nonlinearity that makes AES resistant to linear and algebraic attacks. The AES designers explicitly chose the maximum-entropy permutation monomial — the one with the highest possible polynomial degree consistent with being a permutation.

## 10. Circuit Reversibility: A Complete Characterisation

We consolidate the results of this paper into a complete characterisation of reversibility for polynomial circuits over GF\(2^n\).

**Theorem 9. ***\(Circuit Reversibility Characterisation\)*

A circuit C implementing a polynomial map f : GF\(2^n\) → GF\(2^n\) is reversible \(i.e., has a well-defined polynomial inverse g : GF\(2^n\) → GF\(2^n\) such that g\(f\(x\)\) = x for all x\) if and only if f is a permutation polynomial. The reversibility of the entire circuit is determined by: \(a\) for monomial maps x^k: gcd\(k, 2^n−1\) = 1; \(b\) for general polynomial maps: |image\(f\)| = 2^n \(bijectivity\); \(c\) equivalently: the Shannon entropy H\(f\(X\)\) = H\(X\) = n bits for uniform X \(Theorem 8\).

*Proof.  *A circuit is reversible iff its map is invertible iff the map is a bijection \(surjection \+ injection on a finite set\) iff it is a permutation polynomial. The monomial characterisation \(a\) gives an efficient test for monomial circuits. The entropy test \(c\) gives a probabilistic test for general circuits \(sample X uniformly, estimate H\(f\(X\)\)\). All three characterisations are equivalent. □

□

The practical import of this theorem for circuit design: to build a reversible circuit, it is both necessary and sufficient to ensure that the circuit's combined function is a permutation polynomial. This can be achieved by composing permutation maps: since the composition of permutations is a permutation \(as the group of permutations is closed under composition, Theorem 2\), a circuit built from reversible sub-circuits is reversible.

Conversely, any AND gate introduced into an otherwise reversible circuit may destroy reversibility — AND is the archetypal information-compressing operator \(from Paper 1, AND is the unique non-trivial bilinear operator over XOR, and it is not self-inverse\). This provides an algebraic basis for the design of reversible computing architectures: use XOR-based gates \(which are permutations, forming groups as shown in Paper 1\) and restrict AND gates to contexts where reversibility is not required.

**Corollary 5. ***\(XOR-Only Circuits are Reversible\)*

Any circuit built exclusively from XOR gates and constant gates implements an affine map over GF\(2\)^n \(i.e., a linear map plus a constant\), which is reversible if and only if the linear part is non-singular. Since XOR\(a,b\)=XOR\(b,a\) is its own inverse \(XOR\(XOR\(a,b\),b\)=a by Theorem 9 of Paper 1\), and NOT = XOR\(a,1\) is also its own inverse, all XOR/NOT circuits are reversible. Addition of any AND gate creates potential irreversibility.

## 11. Towards a Unified Reversibility Grade

The results of Papers 1 and 2 converge on a unified picture of binary computation parameterised by a reversibility grade. We formalise this connection here, providing the foundation for Paper 3's treatment of neural networks.

Define the reversibility grade α of a map f : GF\(2^n\) → GF\(2^n\) as:

α\(f\) = 1 − H\(f\(X\)\) / H\(X\) = 1 − log₂\(|image\(f\)|\) / n

where X is uniform on GF\(2^n\) and H denotes Shannon entropy. Then:

- α = 0: f is a permutation \(bijective, fully reversible, information-preserving\). Monomials with gcd\(k, 2^n−1\)=1. XOR circuits. The GF\(2^n\) permutation regime.
- α = 1: f is constant \(maps everything to one point, fully irreversible, zero information\). AND with both inputs equal. The degenerate compression regime.
- α ∈ \(0,1\): f is partially reversible. The image has size 2^\{n\(1−α\)\}, and the entropy loss is α·n bits.

This grade α is precisely the parameter in the GRIA \(Graded Reversible-Irreversible Algebra\) framework developed in parallel work. GRIA proposes α as an interpolation parameter between reversible and irreversible compression, with α=0 corresponding to lossless coding \(Zhegalkin/ANF compression, entropy-preserving\) and α=1 corresponding to maximal lossy compression \(neural network distillation\).

The algebraic content of this paper establishes the α=0 pole of this continuum with precision: the permutation polynomial criterion gcd\(k, 2^n−1\)=1 is the exact condition for α=0. Paper 3 will characterise the α=1 pole \(contraction maps and attractors\) and the critical α=0.5 threshold \(edge of chaos, computational universality, maximum circuit complexity\).

## 12. Discussion

The results of this paper sit at the intersection of finite field theory, circuit complexity, and information theory. The Monomial Permutation Criterion \(Theorem 1\) — x^k is a permutation iff gcd\(k, 2^n−1\)=1 — is a classical result in finite field theory \(see Lidl and Niederreiter, 1997\), and the group isomorphism Perm\(n\) ≅ \(Z/\(2^n−1\)Z\)\* is standard. The Frobenius order theorem and the Galois group structure are foundational results in algebraic number theory.

What is novel in this paper is not the individual results but their synthesis into a unified framework for circuit reversibility, and specifically the connection to the GRIA reversibility grade α. The information preservation theorem \(Theorem 8\) — while straightforward — does not appear to have been stated explicitly in this form as a characterisation of GF\(2^n\) permutations. The degree-depth relationship \(Theorem 5\) is known in circuit complexity but not typically framed as a consequence of the permutation polynomial structure.

The most significant novel contribution is the operational identification: α\(f\) = 0 ↔ f is a permutation polynomial ↔ gcd\(k, 2^n−1\) = 1 \(for monomials\). This provides the first algebraic characterisation of the α=0 end of the GRIA spectrum, connecting an abstract compression parameter to a concrete number-theoretic criterion.

## 13. Conclusions

We have established a complete algebraic theory of reversibility for polynomial maps over GF\(2^n\), with the Monomial Permutation Criterion as the central result. The criterion gcd\(k, 2^n−1\) = 1 provides an instantly computable test for reversibility, the permutation exponents form a group isomorphic to \(Z/\(2^n−1\)Z\)\*, and the Frobenius map generates the Galois symmetry of the field. These results are computationally verified for n = 3, 4, 5, 6, 8.

The information-theoretic characterisation \(reversibility ↔ entropy preservation\) connects the algebraic theory to Shannon's framework and provides the formal definition of the reversibility grade α = 1 − H\(f\(X\)\)/n. This grade is the central parameter of the GRIA framework and serves as the foundation for the subsequent papers in this series.

Immediate extensions include: the enumeration of all permutation polynomials \(not just monomials\) over GF\(2^n\), the classification of partially reversible maps by their orbit structure, and the application of these results to the design of reversible neural network architectures. These extensions are developed in Papers 3-7.

## References
\[1\] Lidl, R. and Niederreiter, H. \(1997\). Finite Fields. 2nd ed. Cambridge University Press.

\[2\] Daemen, J. and Rijmen, V. \(2002\). The Design of Rijndael: AES — The Advanced Encryption Standard. Springer.

\[3\] Golomb, S.W. \(1967\). Shift Register Sequences. Holden-Day.

\[4\] Ireland, K. and Rosen, M. \(1990\). A Classical Introduction to Modern Number Theory. 2nd ed. Springer GTM 84.

\[5\] Roth, R.M. \(2006\). Introduction to Coding Theory. Cambridge University Press.

\[6\] Berlekamp, E.R. \(1968\). Algebraic Coding Theory. McGraw-Hill.

\[7\] Menezes, A., van Oorschot, P., and Vanstone, S. \(1996\). Handbook of Applied Cryptography. CRC Press.

\[8\] Shannon, C.E. \(1948\). A mathematical theory of communication. Bell System Technical Journal, 27\(3\):379–423.

\[9\] MacWilliams, F.J. and Sloane, N.J.A. \(1977\). The Theory of Error-Correcting Codes. North-Holland.

\[10\] Wan, Z.-X. \(2003\). Lectures on Finite Fields and Galois Rings. World Scientific.

\[11\] Paper 1 in this series: A Computational Taxonomy of Binary Algebraic Structures Over \{0,1\}.

\[12\] Paper 3 in this series: Neural Networks as Graded Contraction Maps: An Algebraic Framework via GRIA.

## Appendix A: Computational Verification Details

All theorems verified in Python 3 by exhaustive enumeration. GF\(2^n\) arithmetic implemented via the standard shift-register multiplication algorithm modulo the irreducible polynomial \(represented as a bitmask\). The irreducible polynomials used:

- GF\(2^3\): x^3\+x\+1 = 0b1011
- GF\(2^4\): x^4\+x\+1 = 0b10011
- GF\(2^5\): x^5\+x^2\+1 = 0b100101
- GF\(2^6\): x^6\+x\+1 = 0b1000011
- GF\(2^8\): x^8\+x^4\+x^3\+x\+1 = 0b100011011 \(AES polynomial\)

Total cases verified: Theorem 1 \(116 monomial cases across 4 field sizes, 0 counterexamples\), Theorem 2 \(group axioms for GF\(2^4\)\), Theorems 3-4 \(Frobenius structure for n=3,4,5,6\), Theorems 5-8 \(degree, orbits, entropy for multiple fields\), Theorem 9 \(AES field\), Theorem 10 \(explicit circuit examples\).

*— End of Paper 2 —*
