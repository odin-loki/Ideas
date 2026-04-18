# ARIA Encryption Algorithm — Full Write-Up of ARIA Block Cipher

> **🔐 Overview**: Full write-up of **ARIA** — the Korean block cipher — as paper plus implementable spec.

---

## 🔐 Overview

**ARIA Encryption Algorithm** provides a comprehensive analysis of the ARIA block cipher, a 128-bit block cipher developed by Korea University and NIST. This work includes both research paper and implementable specification, making ARIA accessible for analysis and implementation.

### Key Features

- **128-bit Block Size**: Standard block cipher block size
- **128/192/256-bit Keys**: Multiple key length options
- **14 Rounds**: Balanced round structure
- **Korean National Standard**: Developed for Korean use, submitted to NESSIE

---

## 📄 Core Documents

| Document | Description |
|----------|-------|
| [`ARIA_Research_Paper.md`](ARIA_Research_Paper.md) | Comprehensive research paper on ARIA structure and properties |
| [`ARIA_Specification.md`](ARIA_Specification.md) | Implementable specification with detailed algorithm description |
| [`aria.py`](aria.py) | Python implementation for analysis and testing |

---

## 🔬 ARIA Structure

### Key Expansion

- **128-bit Key**: Uses 11 round keys
- **192-bit Key**: Uses 12 round keys
- **256-bit Key**: Uses 13 round keys

### Round Function

Each round consists of:
- **SubBytes**: Non-linear substitution using S-box
- **ShiftRows**: Byte permutation
- **MixColumns**: Linear diffusion across columns
- **AddRoundKey**: Key addition

### Final Round

The final round omits MixColumns for a cleaner structure.

---

## 📊 Security Analysis

| Property | Value | Notes |
|--|--|--|
| **Key Size** | 128/192/256 bits | Multiple key lengths |
| **Block Size** | 128 bits | Standard block size |
| **Rounds** | 14 rounds | Standard configuration |
| **SPN Structure** | Substitution-Permutation Network | Standard modern cipher structure |
| **S-Box** | 128-bit S-box | Derived from AES S-box |

---

## 🔗 Related Work

This work connects to:
- **Asset Tracking Algorithm** — ARIA-INTEL fusion of asset tracking
- **Break AES** — AES cryptanalysis approaches
- **Compression Algorithms** — Information compression and cryptography
- **GF2 Algebra** — Algebraic structures underlying block ciphers
- **Cypha** — Signal processing and pattern matching

---

## 📖 See Also

- [`EDITORIAL_ROADMAP.md`](../EDITORIAL_ROADMAP.md) — editorial standards and batch history
- [`EDITORIAL_STYLE.md`](../docs/EDITORIAL_STYLE.md) — house style guide
- [`Asset Tracking Algorithm/`](../Asset%20Tracking%20Algorithm/) — asset tracking
- [`Break AES/`](../Break%20AES/) — AES cryptanalysis
- [`Compression Algorithms/`](../Compression%20Algorithms/) — information compression

---

## 🛡️ About This Project

This project provides **educational analysis of the ARIA cipher**. The goal is to:
- Understand the structure and properties of ARIA
- Enable implementation and analysis
- Compare with other block ciphers
- Contribute to cryptographic research

**Note**: ARIA is a standard algorithm for general use. This documentation is for educational purposes.

---

## 💡 Key Takeaways

1. **ARIA is sound**: ARIA passed NIST's round-robin evaluation
2. **Simple structure**: Substitution-permutation network with standard operations
3. **Efficient**: Performs well on various platforms
4. **Well-analysed**: Extensive cryptanalysis confirms security

[← Back to main README](../README.md)