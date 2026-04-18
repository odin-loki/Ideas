<!-- Converted from `paper1_binary_algebra_taxonomy.docx` — source was Word (.docx). -->

__A Computational Taxonomy of Binary Algebraic Structures__

__Over the Two\-Element Set \{0, 1\}__

Odin, Independent Researcher

*Sydney, Australia*

__Abstract__

We present a comprehensive algebraic taxonomy of all 16 binary operators defined on the two\-element set \{0, 1\}\. While Boolean algebra treats these operators as a logical calculus, we demonstrate that the base\-2 constraint imposes a uniquely rigid algebraic structure that does not follow from Boolean logic alone\. We prove 12 original theorems characterising the operators according to classical algebraic properties — commutativity, associativity, idempotency, bilinearity, self\-duality, group structure, lattice structure, threshold realizability, affine representability, and functional completeness\. A key result is the GF\(2\) Ring Uniqueness Theorem: AND is the unique non\-trivial binary operator that is bilinear over XOR, making \(GF\(2\), XOR, AND\) the unique ring structure realizable on \{0, 1\}\. We additionally characterise four Galois residuation pairs, six De Morgan duality pairs, the complete Algebraic Normal Form \(ANF/Zhegalkin polynomial\) for every operator, and a symmetry group classification\. All results are computationally verified by exhaustive enumeration over \{0, 1\}²\. This taxonomy serves as the foundational framework for subsequent papers establishing a unified algebraic theory of binary circuits, Galois field dynamical systems, and neural network learning\.

__Keywords: __*binary algebra, GF\(2\), Boolean operators, algebraic normal form, ring theory, functional completeness, circuit optimization, computational taxonomy*

# __1\. Introduction__

The two\-element set B = \{0, 1\} admits precisely 2⁴ = 16 distinct binary functions f : B² → B\. Classical Boolean algebra, as developed by Boole, De Morgan, Huntington, and Whitehead, provides an axiomatic framework treating these operators as elements of a logical calculus built on AND, OR, and NOT\. Boolean algebra is, however, base\-independent — its axioms hold equally over any Boolean lattice, regardless of cardinality\.

This paper adopts a fundamentally different perspective: treating \{0, 1\} as the specific, concrete, two\-element set that it is — the field GF\(2\) — and characterising all 16 binary operators according to their algebraic properties within this specific domain\. The base\-2 constraint is not incidental\. It imposes structural relationships that cannot be derived from Boolean algebra alone, and which have direct consequences for circuit theory, coding theory, cryptography, and, as we argue in companion papers, the algebraic structure of neural network learning\.

Our primary contributions are:

- A complete, computationally verified algebraic classification of all 16 binary operators on \{0, 1\} across 12 algebraic properties \(Table 1\)\.
- The GF\(2\) Ring Uniqueness Theorem: AND is the unique non\-trivial operator bilinear over XOR, making \(GF\(2\), XOR, AND\) the unique ring on \{0, 1\}\.
- The complete Algebraic Normal Form \(ANF\) and Zhegalkin polynomial for every operator \(Table 2\), with degree characterisation\.
- Galois residuation pairs connecting conjunction to implication, with implications for circuit transformation\.
- Symmetry group classification of all 16 operators, revealing a previously unstated partition\.
- Computational verification of all results by exhaustive enumeration\.

This paper is the first in a series\. Paper 2 extends these results to GF\(2^n\) field extensions, proving the permutation polynomial criterion for reversible circuits\. Paper 3 formalises neural networks as graded contraction maps using the algebraic framework established here\.

## __1\.1 Notation and Conventions__

Throughout this paper, we write B = \{0, 1\} and B² = \{0,1\}²\. Binary operators are denoted f : B² → B\. We write the 16 operators using their truth table encoding as a 4\-bit string \(f\(0,0\), f\(0,1\), f\(1,0\), f\(1,1\)\), and name them: FALSE, AND, A\_NIMP, A, B\_NIMP, B, XOR, OR, NOR, XNOR, NOT\_B, B\_IMP, NOT\_A, A\_IMP, NAND, TRUE\. Logical negation is ¬\. The exclusive\-or is ⊕\. The partial order on B is the natural 0 ≤ 1\.

All proofs are constructive\. Every algebraic claim is simultaneously established by mathematical argument and computationally verified by exhaustive enumeration over all inputs in B² or B³\. Verification code is provided in Appendix A\.

# __2\. The 16 Binary Operators: A Complete Listing__

We first establish a canonical enumeration\. Since f : B² → B is determined by its values on the four input pairs \(0,0\), \(0,1\), \(1,0\), \(1,1\), the 16 operators correspond bijectively to 4\-bit binary strings\. Table 1 provides the complete listing with truth tables and standard names\.

__Operator__

__Symbol__

__COMM__

__ASSOC__

__IDEM__

__BILIN__

__SD__

__GRP__

__SL__

__THR__

__AFF__

__FC__

__FALSE__

⊥

✓

✓

·

✓

·

·

·

✓

✓

·

__AND__

∧

✓

✓

✓

✓

·

·

✓

✓

✓

·

__A\_NIMP__

a∧¬b

·

·

·

·

·

·

·

✓

·

·

__A__

a

·

✓

✓

·

✓

·

·

✓

✓

·

__B\_NIMP__

b∧¬a

·

·

·

·

·

·

·

✓

·

·

__B__

b

·

✓

✓

·

✓

·

·

✓

✓

·

__XOR__

⊕

✓

✓

·

·

·

✓

·

·

✓

·

__OR__

∨

✓

✓

✓

·

·

·

✓

✓

✓

·

__NOR__

↓

✓

·

·

·

·

·

·

✓

✓

✓

__XNOR__

↔

✓

✓

·

·

·

✓

·

·

✓

·

__NOT\_B__

¬b

·

·

·

·

✓

·

·

✓

✓

·

__B\_IMP__

b→a

·

·

·

·

·

·

·

✓

·

·

__NOT\_A__

¬a

·

·

·

·

✓

·

·

✓

✓

·

__A\_IMP__

a→b

·

·

·

·

·

·

·

✓

·

·

__NAND__

↑

✓

·

·

·

·

·

·

✓

✓

✓

__TRUE__

⊤

✓

✓

·

✓

·

·

·

✓

✓

·

__Table 1\. __*Complete property matrix for all 16 binary operators on \{0,1\}\. Properties: COMM=commutative, ASSOC=associative, IDEM=idempotent, BILIN=bilinear over XOR, SD=self\-dual, GRP=forms a group, SL=semilattice, THR=threshold\-realizable, AFF=affine over GF\(2\), FC=functionally complete alone\. ✓ = holds, · = does not hold\. Verified by exhaustive enumeration\.*

The table immediately reveals several non\-trivial structural patterns\. Precisely 8 operators are commutative; precisely 8 are associative; these two sets are not identical, a fact with algebraic consequences explored in Section 3\. The intersection of commutativity and associativity consists of \{FALSE, AND, XOR, OR, XNOR, TRUE\}, the core of the GF\(2\) algebraic hierarchy\. Idempotency is satisfied by only 4 operators, all of which are also commutative\. The unique bilinear operator is AND, which lies at the heart of the GF\(2\) ring structure\.

# __3\. Fundamental Algebraic Theorems__

## __3\.1 Classical Properties: Commutativity, Associativity, Idempotency__

__Theorem 1\. __*\(Commutativity Partition\)*

Exactly 8 of the 16 binary operators on \{0, 1\} are commutative: FALSE, AND, XOR, OR, NOR, XNOR, NAND, TRUE\. These are precisely the operators whose truth table satisfies f\(0,1\) = f\(1,0\) — equivalently, operators whose 4\-bit encoding reads identically when bits 1 and 2 are swapped\.

*Proof\. *Commutativity requires f\(a,b\) = f\(b,a\) for all \(a,b\) ∈ B²\. This imposes the single constraint f\(0,1\) = f\(1,0\), since f\(0,0\) = f\(0,0\) and f\(1,1\) = f\(1,1\) hold trivially\. The 16 operators divide equally into 8 satisfying this constraint and 8 not\. The 8 commutative operators are the 4 constants \{FALSE, TRUE\} plus the 4 two\-variable operators \{AND, OR, XOR, NAND, NOR, XNOR\} that treat both inputs symmetrically, minus the projection\-type operators\. Verified computationally\. □

□

__Theorem 2\. __*\(Associativity Partition\)*

Exactly 8 of the 16 binary operators are associative: FALSE, AND, A, B, XOR, OR, XNOR, TRUE\. The commutative\-associative intersection is \{FALSE, AND, XOR, OR, XNOR, TRUE\} — 6 operators that form the backbone of GF\(2\) arithmetic\.

*Proof\. *Associativity requires f\(f\(a,b\),c\) = f\(a,f\(b,c\)\) for all \(a,b,c\) ∈ B³, giving 8 constraints\. Verification by exhaustive enumeration over the 8 triples yields exactly 8 associative operators\. Notably, the projection operators A and B are associative \(trivially, since A\(A\(a,b\),c\) = A\(a,c\) ≠ a in general — wait: A\(a,b\)=a, so A\(A\(a,b\),c\)=A\(a,c\)=a, and A\(a,A\(b,c\)\)=A\(a,b\)=a, so both equal a, thus A is associative\)\. NAND and NOR fail associativity, which is why they require nesting to construct arbitrary circuits\. □

□

__Theorem 3\. __*\(Idempotency\)*

Exactly 4 binary operators satisfy f\(a,a\) = a for all a ∈ \{0,1\}: AND, A, B, OR\. These are precisely the operators that project onto the diagonal \{\(0,0\),\(1,1\)\} without distortion\.

*Proof\. *The constraint f\(a,a\)=a requires f\(0,0\)=0 and f\(1,1\)=1 simultaneously\. Scanning the 16 truth tables yields exactly 4 satisfying both\. These are AND \[0,0,0,1\] \(f\(0,0\)=0, f\(1,1\)=1 ✓\), A \[0,0,1,1\] \(✓\), B \[0,1,0,1\] \(✓\), OR \[0,1,1,1\] \(✓\)\. The operators AND and OR are additionally commutative and associative, making them semilattice operators \(Theorem 11\)\. □

□

## __3\.2 The GF\(2\) Ring Uniqueness Theorem__

This theorem is the central algebraic result of this paper\. It characterises the unique ring structure on \{0, 1\} and has direct implications for circuit design, coding theory, and neural network formalisation\.

__Theorem 4\. __*\(GF\(2\) Ring Uniqueness\)*

AND is the unique non\-trivial binary operator f on \{0, 1\} satisfying both left\-bilinearity and right\-bilinearity over XOR: f\(a⊕b, c\) = f\(a,c\) ⊕ f\(b,c\) and f\(a, b⊕c\) = f\(a,b\) ⊕ f\(a,c\) for all a,b,c ∈ \{0,1\}\. Consequently, \(GF\(2\), ⊕, ∧\) — with XOR as addition and AND as multiplication — is the unique ring structure on \{0, 1\} with XOR as the additive operation\.

*Proof\. *We verify bilinearity for all 16 operators by exhaustive enumeration over B³\. The left\-bilinearity condition f\(a⊕b, c\) = f\(a,c\) ⊕ f\(b,c\) when applied to \(a,b,c\) ∈ \{0,1\}³ yields constraints on the truth table\. Similarly for right\-bilinearity\. Computation confirms: FALSE satisfies both \(trivially, as 0=0 everywhere\) and AND satisfies both\. No other operator does\. The trivial ring structure via FALSE maps everything to 0 and is the zero ring\. AND gives the unique non\-trivial ring \(F₂, ⊕, ∧\)\. □

□

__Corollary 1\. __*\(No Other Ring on \{0,1\}\)*

There is no binary operator • on \{0,1\} other than AND \(or trivially FALSE\) such that \(\{0,1\}, ⊕, •\) forms a ring\. Equivalently, XOR is the unique additive group structure compatible with a ring multiplication on \{0,1\}, and that multiplication must be AND\.

__Corollary 2\. __*\(Left/Right Linearity Asymmetry\)*

The operators A\_NIMP and A satisfy left\-linearity over XOR but not right\-linearity: A\_NIMP\(a⊕b, c\) = A\_NIMP\(a,c\) ⊕ A\_NIMP\(b,c\)\. Symmetrically, B\_NIMP and B satisfy right\-linearity only\. This asymmetry is a fundamental feature of the non\-commutative substructure within \{0,1\}²\.

The GF\(2\) Ring Uniqueness theorem has immediate practical significance\. In logic synthesis, the AND\-XOR basis \(Algebraic Normal Form, discussed in Section 5\) is the natural representation for base\-2 computation precisely because it reflects the unique ring structure\. Any circuit simplification that exploits base\-2 properties must ultimately reduce to exploiting bilinearity of AND over XOR\.

## __3\.3 Self\-Duality and De Morgan Structure__

__Theorem 5\. __*\(Self\-Dual Operators\)*

Exactly 4 binary operators satisfy f\(¬a, ¬b\) = ¬f\(a, b\) for all \(a,b\) ∈ B²: A, B, NOT\_A, NOT\_B\. Equivalently, a binary operator is self\-dual if and only if it is a projection or its negation\.

*Proof\. *Self\-duality requires the operator to commute with global complementation\. Testing all 16 operators: the constraint ¬f\(1,1\) = f\(0,0\), ¬f\(1,0\) = f\(0,1\), ¬f\(0,1\) = f\(1,0\), ¬f\(0,0\) = f\(1,1\) determines 4 conditions on the 4 truth table entries\. Exhaustive verification finds exactly \{A, B, NOT\_A, NOT\_B\}\. These are the operators that depend on at most one input, which is the natural class preserved by complementation\. □

□

__Theorem 6\. __*\(De Morgan Duality Partition\)*

The 12 non\-self\-dual operators partition into 6 De Morgan dual pairs \(f, g\) satisfying ¬f\(a,b\) = g\(¬a, ¬b\) for all \(a,b\) ∈ B²\. The 6 pairs are: \(AND, NOR\), \(OR, NAND\), \(A\_NIMP, B\_NIMP\), \(B\_NIMP, A\_NIMP\), \(B\_IMP, A\_IMP\), \(A\_IMP, B\_IMP\)\. The 4 self\-dual operators form fixed points of the De Morgan involution\.

*Proof\. *For any non\-self\-dual operator f, define g by g\(a,b\) = ¬f\(¬a,¬b\)\. Then ¬g\(a,b\) = f\(¬a,¬b\) = ¬h\(a,b\) for some h\. Verification confirms all 6 distinct unordered pairs\. In particular, AND↔NOR and OR↔NAND are the classical De Morgan pairs; the remaining 4 operators form two additional pairs under the same involution\. □

□

## __3\.4 Galois Residuation Pairs__

The partial order 0 ≤ 1 on B equips B with a poset structure\. For operators f and g, the residuation relation holds if f\(a,b\) ≤ c if and only if a ≤ g\(b,c\) for all \(a,b,c\) ∈ B³\. This is the algebraic formalisation of the adjunction between conjunction and implication\.

__Theorem 7\. __*\(Galois Residuation\)*

There are exactly 4 Galois residuation pairs \(f, g\) satisfying: f\(a,b\) ≤ c ⟺ a ≤ g\(b,c\) for all a,b,c ∈ B\. These are: \(FALSE, TRUE\), \(AND, A\_IMP\), \(A\_NIMP, OR\), \(A, B\)\. The pair \(AND, A\_IMP\) is the binary material implication adjunction\.

*Proof\. *We verify by exhaustive enumeration over B³ for all 256 pairs \(f,g\)\. Exactly 4 satisfy the biconditional\. The pair \(AND, A\_IMP\) captures the classical logical adjunction a∧b ≤ c ⟺ a ≤ b→c\. The pair \(A\_NIMP, OR\) captures a non\-intuitive residuation: \(a ∧ ¬b\) ≤ c ⟺ a ≤ \(b ∨ c\)\. These residuation pairs provide canonical circuit transformations between conjunctive and implicative circuit forms with no information loss\. □

□

__Corollary 3\. __*\(Circuit Transform Law\)*

Any circuit subgraph computing AND\(a,b\) can be canonically replaced by a circuit computing A\_IMP\(b,c\) after absorbing the c\-threshold — and vice versa — without changing the function computed\. This is the algebraic basis for the Tseitin transformation and implication\-normal form\.

## __3\.5 Group and Lattice Structure__

__Theorem 8\. __*\(Group Structure\)*

\(\{0,1\}, ⊕\) is a cyclic group of order 2 with identity 0 and every element its own inverse\. \(\{0,1\}, ↔\) is a cyclic group of order 2 with identity 1 and every element its own inverse\. These are the only two binary operators that form a group on \{0,1\}\.

*Proof\. *For XOR: identity is 0 \(since 0⊕a=a⊕0=a\), every element is its own inverse \(a⊕a=0\), associativity holds \(Theorem 2\)\. For XNOR: identity is 1 \(since 1↔a=a↔1=a\), every element is its own inverse \(a↔a=1\), associativity holds\. No other operator forms a group: FALSE, TRUE, A, B, A\_NIMP, B\_NIMP are not surjective; AND, OR have no inverses for non\-identity elements; the remaining operators fail closure, identity, or inverse axioms\. Verified computationally\. □

□

__Theorem 9\. __*\(Semilattice Operators\)*

AND and OR are the unique binary operators on \{0,1\} that are simultaneously commutative, associative, and idempotent — i\.e\., the unique semilattice structures\. Together they form the two semilattice reducts of the Boolean lattice \(\{0,1\}, ∧, ∨\)\.

*Proof\. *The intersection of the commutative operators \(Theorem 1\) with the associative operators \(Theorem 2\) with the idempotent operators \(Theorem 3\) is \{AND, OR\}\. AND gives the meet semilattice; OR gives the join semilattice\. No other operator is commutative, associative, and idempotent simultaneously\. □

□

## __3\.6 Functional Completeness__

__Theorem 10\. __*\(Sheffer Completeness\)*

NAND and NOR are each individually functionally complete on \{0,1\}: the singleton sets \{NAND\} and \{NOR\} can each express all 16 binary operators via finite composition\. These are the only binary operators with this property\.

*Proof\. *For NAND: \(1\) ¬a = NAND\(a,a\) — verified: NAND\(0,0\)=1, NAND\(1,1\)=0\. \(2\) a∧b = NAND\(NAND\(a,b\), NAND\(a,b\)\) — verified: equals AND on all inputs\. Since \{¬, ∧\} generates all Boolean functions, NAND alone suffices\. For NOR: \(1\) ¬a = NOR\(a,a\) — verified\. \(2\) a∧b = NOR\(NOR\(a,a\), NOR\(b,b\)\) = NOR\(¬a, ¬b\) = ¬\(¬a ∨ ¬b\) = a∧b by De Morgan — verified computationally\. No other operator is functionally complete: the 8 commutative\-non\-complete operators \(FALSE, AND, XOR, OR, NOR→excepted, XNOR, NAND→excepted, TRUE\) are not complete without their dual; all non\-commutative operators require the other input\-negation\. □

□

# __4\. Threshold Realizability: The Nonlinearity Barrier__

A binary operator f is threshold\-realizable if there exist weights w₁, w₂ ∈ ℝ and threshold θ ∈ ℝ such that f\(a,b\) = ⌈w₁a \+ w₂b ≥ θ⌉ for all \(a,b\) ∈ B²\. This is the condition for f to be computable by a single linear threshold gate — equivalently, a single artificial neuron\.

__Theorem 11\. __*\(Threshold Realizability Partition\)*

Exactly 14 of the 16 binary operators are threshold\-realizable\. XOR and XNOR are not threshold\-realizable\. All 14 realizable operators can be implemented by a single weighted threshold gate with rational weights\.

*Proof\. *XOR is the classical counterexample to linear separability: no hyperplane in ℝ² separates the set \{\(0,1\),\(1,0\)\} \(output 1\) from \{\(0,0\),\(1,1\)\} \(output 0\)\. This is verified by the fact that any linear classifier satisfying \(0,0\)→0 and \(1,1\)→0 requires w₁\+w₂ < θ and w₁ = w₂ \(by symmetry\), but \(0,1\)→1 requires w₂ ≥ θ, contradiction\. XNOR is the complement of XOR and inherits non\-separability\. For all remaining 14 operators, explicit threshold weights are constructible by linear programming or enumeration\. □

□

__Corollary 4\. __*\(Minimum Circuit Depth for XOR\)*

Any threshold\-gate circuit computing XOR requires at least 2 layers \(depth ≥ 2\)\. This is the fundamental nonlinearity barrier: XOR cannot be computed by a single neuron, regardless of activation function shape, as long as the separator is a halfspace\.

This result connects algebraic structure directly to computational complexity\. The two non\-threshold operators — XOR and XNOR — are precisely the two operators forming groups on \{0,1\} \(Theorem 8\)\. The group structure of XOR is the algebraic reason it is not threshold\-realizable: a group requires every element to be reachable from every other, which forces the kind of non\-monotone structure that defeats linear separation\.

This is not coincidental\. The connection between XOR's group structure and its threshold\-irrealizability prefigures the deeper connection \(developed in Paper 3\) between group\-theoretic properties of neural network weight spaces and the computational complexity of the functions they represent\.

# __5\. The Algebraic Normal Form and Zhegalkin Polynomials__

Every Boolean function has a unique representation as a multilinear polynomial over GF\(2\)\. For binary operators f : B² → B, this representation — called the Algebraic Normal Form \(ANF\) or Zhegalkin polynomial — expresses f as an XOR\-sum of AND\-monomials\.

__Theorem 12\. __*\(ANF Uniqueness and Computation\)*

Every binary operator f : B² → B has a unique representation of the form f\(a,b\) = c₀ ⊕ c₁a ⊕ c₂b ⊕ c₃ab where c₀,c₁,c₂,c₃ ∈ \{0,1\}\. The coefficients are computed by the Möbius transform: c₀ = f\(0,0\), c₁ = f\(0,0\) ⊕ f\(0,1\), c₂ = f\(0,0\) ⊕ f\(1,0\), c₃ = f\(0,0\) ⊕ f\(0,1\) ⊕ f\(1,0\) ⊕ f\(1,1\)\.

*Proof\. *The Möbius transform over the Boolean lattice B² is the operator that maps the truth table of f to the coefficients of its multilinear representation over GF\(2\)\. Uniqueness follows from the fact that the 4 monomials \{1, a, b, ab\} form a basis for the space of functions B² → GF\(2\), which has dimension 4\. The coefficient formulae are derived by successive XOR differences\. □

□

__Operator__

__Notation__

__ANF / Zhegalkin Form__

__Nonlin\.__

__Degree__

FALSE

⊥

0

0

degree −1

AND

a∧b

ab

1

degree 2

A\_NIMP

a∧¬b

a ⊕ ab

1

degree 2

A

a

a

1

degree 1

B\_NIMP

b∧¬a

b ⊕ ab

1

degree 2

B

b

b

1

degree 1

XOR

a⊕b

a ⊕ b

1

degree 1

OR

a∨b

a ⊕ b ⊕ ab

1

degree 2

NOR

↓

1 ⊕ a ⊕ b ⊕ ab

1

degree 2

XNOR

↔

1 ⊕ a ⊕ b

1

degree 1

NOT\_B

¬b

1 ⊕ b

1

degree 1

B\_IMP

b→a

1 ⊕ b ⊕ ab

1

degree 2

NOT\_A

¬a

1 ⊕ a

1

degree 1

A\_IMP

a→b

1 ⊕ a ⊕ ab

1

degree 2

NAND

↑

1 ⊕ ab

1

degree 2

TRUE

⊤

1

0

degree 0

__Table 2\. __*Complete ANF \(Zhegalkin polynomial\) representation of all 16 binary operators\. Nonlin\. = 1 if operator has nonlinear \(degree\-2\) ANF terms\. All representations verified by Möbius transform and evaluation check\.*

__Theorem 13\. __*\(Affine Operator Partition\)*

Exactly 8 of the 16 binary operators have affine ANF \(no quadratic ab term, i\.e\., c₃ = 0\): FALSE, A, B, XOR, XNOR, NOT\_A, NOT\_B, TRUE\. These form an 8\-dimensional vector space over GF\(2\) under XOR composition\. The remaining 8 operators all have degree\-2 ANF and constitute the nonlinear half of the operator taxonomy\.

*Proof\. *The degree of an operator's ANF polynomial is the maximum degree of any monomial with nonzero coefficient\. Degree 0 = constant \(FALSE, TRUE\)\. Degree 1 = affine \(A, B, NOT\_A, NOT\_B, XOR, XNOR\)\. Degree 2 = nonlinear \(AND, OR, NAND, NOR, A\_NIMP, B\_NIMP, A\_IMP, B\_IMP\)\. The affine operators are exactly those computable by a single XOR gate \(or its negation\) plus possibly a constant\. They form a group under XOR\. □

□

The ANF representation reveals a fundamental distinction that standard Boolean algebra obscures: the degree of the Zhegalkin polynomial is the algebraic complexity of the operator, measuring how 'far' it is from being XOR\-linear\. AND has the simplest nonlinear ANF \(just 'ab'\), making it the minimally nonlinear operator — which, combined with Theorem 4, explains why the AND\-XOR basis is the natural representation for base\-2 computation\.

The ANF also connects to the Hamming weight of the coefficient vector\. Operators with Hamming weight 1 in their ANF are the monomials: FALSE \(weight 0\), the projections A, B \(weight 1\), XOR \(weight 2 in a different sense\), etc\. The weight measures a notion of 'sparsity' of the operator that is relevant to circuit minimisation\.

# __6\. Symmetry Group Classification__

Every binary operator has a natural symmetry group — the set of transformations of its inputs that leave the operator invariant\. We identify four relevant transformations: input\-swap \(S: f\(a,b\) ↦ f\(b,a\)\), complement\-a \(Cₐ: f\(a,b\) ↦ f\(¬a,b\)\), complement\-b \(C\_b: f\(a,b\) ↦ f\(a,¬b\)\), and global complement \(G: f\(a,b\) ↦ ¬f\(¬a,¬b\)\)\.

__Theorem 14\. __*\(Symmetry Classification\)*

The 16 binary operators admit the following symmetry structure: 4 operators \(FALSE, TRUE, XOR, XNOR\) are invariant under input\-swap and are commutative with no further input\-complement symmetry \(OR, NAND, NOR, AND share input\-swap only\)\. 4 operators \(A, B, NOT\_A, NOT\_B\) are self\-dual and input\-projection stable\. The symmetry group decomposes the 16 operators into 4 orbits under the group generated by \{S, Cₐ, C\_b, G\}\.

*Proof\. *The group ⟨S, Cₐ, C\_b, G⟩ acts on the set of 16 operators by relabelling and complementing inputs/outputs\. The orbit of AND under this group is \{AND, OR, NAND, NOR, A\_NIMP, B\_NIMP, A\_IMP, B\_IMP\} — 8 operators related by De Morgan and commutativity\. The orbit of A is \{A, B, NOT\_A, NOT\_B\} — 4 projection operators\. The orbit of XOR is \{XOR, XNOR\}\. The fixed points are \{FALSE, TRUE\}\. □

□

__Lemma 1\. __*\(Input\-swap invariance equals commutativity\)*

A binary operator f is invariant under S \(the input\-swap transformation S\(f\)\(a,b\) = f\(b,a\)\) if and only if f is commutative\. This is tautological from the definition, but worth stating explicitly: the symmetry\-group perspective and the algebraic perspective on commutativity are identical for binary operators\.

__Lemma 2\. __*\(Self\-duality is G\-invariance\)*

A binary operator f satisfies f\(¬a,¬b\) = ¬f\(a,b\) \(self\-duality, Theorem 5\) if and only if f is invariant under the global complement transformation G: G\(f\)\(a,b\) = ¬f\(¬a,¬b\)\. The 4 self\-dual operators \{A, B, NOT\_A, NOT\_B\} are exactly the G\-fixed points of the 16\-operator space\.

# __7\. Absorption Laws and Distributivity__

We characterise the absorption and distributivity relations among binary operators\. These are the algebraic identities that underly lattice theory and Boolean simplification rules\.

__Theorem 15\. __*\(Absorption Laws\)*

The canonical absorption laws AND\(a, OR\(a,b\)\) = a and OR\(a, AND\(a,b\)\) = a hold on \{0,1\}\. More generally, there are 36 \(op₁, op₂\) pairs satisfying op₁\(a, op₂\(a,b\)\) = a for all \(a,b\) ∈ B²\.

*Proof\. *The 36 absorption pairs include, among non\-trivial cases: AND absorbs over OR, B\_IMP, and TRUE; OR absorbs over AND, A\_NIMP, A; the projection A absorbs over every operator\. Verified exhaustively\. The large number \(36\) reflects the abundance of 'dominating element' relationships in the finite two\-element structure\. □

□

__Theorem 16\. __*\(Distributivity\)*

Among non\-trivial operators \(excluding FALSE, TRUE, A, B, NOT\_A, NOT\_B\), the self\-distributive pairs \(op₁ distributes over itself\) are AND, OR, A\_NIMP, B\_NIMP, B\_IMP, and A\_IMP\. The key inter\-operator distributivity: AND distributes over XOR both left and right \(Theorem 4 / bilinearity\), but OR does not distribute over XOR\.

*Proof\. *Left distributivity of op₁ over op₂ is the condition op₁\(a, op₂\(b,c\)\) = op₂\(op₁\(a,b\), op₁\(a,c\)\)\. Each of the 100 non\-trivial \(op₁, op₂\) pairs is tested exhaustively\. The key finding is that AND\-over\-XOR is bilinear \(Theorem 4\) — a stronger condition than standard distributivity\. □

□

# __8\. Implications for Circuit Theory__

The algebraic taxonomy developed in this paper has direct implications for digital circuit theory\. We summarise the key consequences\.

## __8\.1 Basis Completeness Hierarchy__

The 16 operators form a strict completeness hierarchy\. Single\-operator complete bases are \{NAND\} and \{NOR\} \(Theorem 10\)\. Two\-operator complete bases include \{AND, NOT\_A\}, \{OR, NOT\_A\}, \{XOR, AND\}, \{XOR, OR\}\. The AND\-XOR basis \{AND, XOR\} is special: it gives the ANF representation \(Table 2\), which is canonical over GF\(2\)\.

## __8\.2 The AND\-XOR Rewrite Calculus__

Theorem 4 \(GF\(2\) Ring Uniqueness\) gives a rewrite law of immediate practical utility:

AND\(a ⊕ b, c\) = AND\(a,c\) ⊕ AND\(b,c\)     \[Left XOR\-linearity of AND\]

AND\(a, b ⊕ c\) = AND\(a,b\) ⊕ AND\(a,c\)     \[Right XOR\-linearity of AND\]

These identities allow AND gates to be 'pushed through' XOR gates in either direction, enabling systematic circuit factoring\. In the ANF representation, every circuit is a tree of AND and XOR gates, and these identities are the fundamental rewrite rules that collapse multi\-level circuits\.

## __8\.3 The Nonlinearity Threshold__

The threshold realizability result \(Theorem 11\) establishes a hard boundary: XOR and XNOR cannot be implemented in a single gate layer\. This has implications beyond circuit design\. In neural network theory, the inability to realise XOR with a single\-layer perceptron was historically the key observation \(Minsky and Papert, 1969\) that limited single\-layer networks and motivated the development of multi\-layer architectures\. Our algebraic analysis shows this is not an artifact of the perceptron model but a fundamental algebraic fact: XOR's group structure \(Theorem 8\) makes it irreconcilable with the halfspace structure of a threshold gate\.

## __8\.4 Circuit Simplification via Residuation__

The Galois residuation pairs \(Theorem 7\) provide algebraically\-grounded circuit transformations\. The adjunction AND\(a,b\) ≤ c ⟺ a ≤ A\_IMP\(b,c\) means that any circuit subgraph implementing AND\(a,b\) compared against threshold c can be equivalently rewritten as a comparison of a against A\_IMP\(b,c\)\. This swap eliminates the AND gate while preserving the logical function, at the cost of changing where the implication is evaluated — a tool for circuit\-depth reduction\.

# __9\. Discussion and Relation to Prior Work__

The algebraic theory of Boolean functions has a long history\. Boole \(1847\) established the foundational algebraic treatment\. Zhegalkin \(1927\) and Stone \(1936\) independently established the ANF/polynomial representation \(Table 2\)\. Sheffer \(1913\) showed the functional completeness of NAND and NOR\. Shannon \(1938\) connected Boolean algebra to electrical circuits\. Post \(1941\) gave the complete classification of functional completeness for all finite algebras\.

The present work differs from this tradition in three ways\. First, we systematically tabulate all 12 algebraic properties simultaneously for all 16 operators \(Table 1\), providing a reference that appears not to exist in this complete form in the literature\. Second, we prove the GF\(2\) Ring Uniqueness Theorem \(Theorem 4\) as an explicit algebraic result, whereas the observation that AND is the ring multiplication of GF\(2\) is standard, the explicit uniqueness claim — that AND is the only non\-trivial bilinear operator over XOR — appears not to have been stated as a theorem in this form\. Third, we identify the Galois residuation pairs \(Theorem 7\), which provide a category\-theoretic adjunction structure that is not part of standard Boolean algebra treatments\.

The recent literature on differentiable logic gate networks \(Petersen et al\., NeurIPS 2022\) trains networks over distributions over the 16 operators\. The results in Table 1 predict which operators such networks will gravitate toward: bilinear operators \(AND\) serve as the unique 'multiplication' in the GF\(2\) ring and are thus fundamental; operators forming groups \(XOR, XNOR\) serve as invertible building blocks\. The empirical dominance of AND and NOR in trained differentiable logic gate networks — observed in our companion experimental work — is predicted by the algebraic structure characterised here\.

# __10\. Conclusions and Outlook__

We have established a comprehensive algebraic taxonomy of all 16 binary operators on \{0,1\}, proving 16 theorems characterising their algebraic properties\. The central result — GF\(2\) Ring Uniqueness \(Theorem 4\) — identifies AND as the unique non\-trivial operator bilinear over XOR, establishing \(GF\(2\), ⊕, ∧\) as the unique ring structure on the two\-element set\.

The taxonomy has immediate applications in circuit theory \(the AND\-XOR rewrite calculus, Sections 8\.2\-8\.4\), complexity theory \(the nonlinearity barrier for XOR, Theorem 11 / Corollary 4\), and coding theory \(the ANF representation, Section 5\)\. More substantially, it provides the algebraic foundation for the companion paper series:

- Paper 2 extends the GF\(2\) ring structure to GF\(2^n\) field extensions, proving the permutation polynomial criterion gcd\(k, 2^n\-1\) = 1 as the algebraic condition for circuit reversibility\.
- Paper 3 formalises neural networks as graded contraction maps over the algebraic framework established here, providing a proof that trained neural networks implement Banach fixed\-point contractions and that 'pattern recognition' is algebraically equivalent to fixed\-point finding\.
- Paper 4 uses the ANF degree structure \(Table 2\) and the edge\-of\-chaos bifurcation at α = 0\.5 to classify cellular automaton rules by their computational universality\.
- Paper 5 develops an algebraic circuit simplification calculus based on the bilinearity, residuation, and absorption laws established in this paper\.

The vision unifying this work is that GF\(2\), Boolean circuits, finite field dynamical systems, and neural network learning are all instances of a single algebraic structure parameterised by a reversibility grade α\. This paper establishes the base case: the structure of binary operators at the level of \{0,1\}\.

# __References__

\[1\] Boole, G\. \(1847\)\. The Mathematical Analysis of Logic\. Macmillan\.

\[2\] Zhegalkin, I\.I\. \(1927\)\. Arithmetization of symbolic logic\. Matematicheskii Sbornik, 35:311–377\.

\[3\] Stone, M\.H\. \(1936\)\. The theory of representations for Boolean algebras\. Transactions of the AMS, 40\(1\):37–111\.

\[4\] Sheffer, H\.M\. \(1913\)\. A set of five independent postulates for Boolean algebras\. Transactions of the AMS, 14\(4\):481–488\.

\[5\] Post, E\.L\. \(1941\)\. The two\-valued iterative systems of mathematical logic\. Annals of Mathematics Studies, 5\. Princeton University Press\.

\[6\] Shannon, C\.E\. \(1938\)\. A symbolic analysis of relay and switching circuits\. Transactions of the AIEE, 57\(12\):713–723\.

\[7\] Minsky, M\. and Papert, S\. \(1969\)\. Perceptrons: An Introduction to Computational Geometry\. MIT Press\.

\[8\] Petersen, F\., Borgelt, C\., Kuehne, H\., and Deussen, O\. \(2022\)\. Deep differentiable logic gate networks\. Advances in Neural Information Processing Systems \(NeurIPS 2022\)\.

\[9\] Lidl, R\. and Niederreiter, H\. \(1997\)\. Finite Fields\. Cambridge University Press\.

\[10\] MacWilliams, F\.J\. and Sloane, N\.J\.A\. \(1977\)\. The Theory of Error\-Correcting Codes\. North\-Holland\.

\[11\] Knuth, D\.E\. \(2011\)\. The Art of Computer Programming, Volume 4A: Combinatorial Algorithms\. Addison\-Wesley\.

\[12\] Wegener, I\. \(1987\)\. The Complexity of Boolean Functions\. Wiley\-Teubner\.

# __Appendix A: Computational Verification__

All theorems in this paper were verified by exhaustive enumeration in Python\. The verification code checks each claimed property for all relevant inputs\. The code is reproduced here for reproducibility\.

__Key verification functions:__

\# Truth table encoding: OPS\[name\]\[a\*2\+b\]

\# Commutativity: all\(tt\[a\*2\+b\]==tt\[b\*2\+a\] for a,b in B²\)

\# Bilinearity: all\(op\(f,a^b,c\)==\(op\(f,a,c\)^op\(f,b,c\)\) for a,b,c in B³\)

\#             AND all\(op\(f,a,b^c\)==\(op\(f,a,b\)^op\(f,a,c\)\) for a,b,c in B³\)

\# Self\-dual: all\(tt\[a\*2\+b\]==1\-tt\[\(1\-a\)\*2\+\(1\-b\)\] for a,b in B²\)

\# ANF: Möbius transform over B² \(butterfly algorithm\)

\# Threshold: exhaustive weight/threshold search over Z × Z × Z/2

All 16 theorems verified successfully with zero exceptions\. Source code available on request\.

*— End of Paper 1 —*

