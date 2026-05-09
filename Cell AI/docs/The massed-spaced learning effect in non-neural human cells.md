# The massed-spaced learning effect in non-neural human cells

> **Source paper.** N. V. Kukushkin, R. E. Carney, T. Tabassum, T. J. Carew. *Nature Communications* (2024) **15**:9635. <https://doi.org/10.1038/s41467-024-53922-x>. Open Access (CC BY-NC-ND 4.0). Converted from the original PDF — figures and supplementary panels are not embedded; refer to the published article for the figure plates.

---

## Abstract

The massed-spaced effect is a hallmark feature of memory formation. We now demonstrate this effect in two separate non-neural, immortalised cell lines stably expressing a short-lived luciferase reporter controlled by a CREB-dependent promoter. We emulate training using repeated pulses of forskolin and/or phorbol ester, and, as a proxy for memory, measure luciferase expression at various points after training. Four spaced pulses of either agonist elicit stronger and more sustained luciferase expression than a single "massed" pulse. Spaced pulses also result in stronger and more sustained activation of molecular factors critical for memory formation, ERK and CREB, and inhibition of ERK or CREB blocks the massed-spaced effect. Our findings show that canonical features of memory do not necessarily depend on neural circuitry, but can be embedded in the dynamics of signalling cascades conserved across different cell types.

---

## Introduction

Learning and memory in animals exhibit a peculiar feature known as the massed-spaced effect: training distributed across multiple sessions (spaced training) produces stronger memory than the same amount of training applied in a single episode (massed training). This effect is highly conserved across the animal kingdom and is observed at both behavioural and synaptic levels.

The massed-spaced effect, also known as the spacing effect and first documented by Hermann Ebbinghaus, is characterised by the existence of an optimal intertrial interval (ITI) between training sessions. Previous research has identified some molecular and cellular components that determine this optimal spacing. For instance, studies in *Drosophila* have shown that manipulating SHP2 expression in mushroom body neurons alters the optimal ITI for long-term memory (LTM) induction, correlating with changes in the activation of extracellularly regulated kinase (ERK). Similarly, our research in *Aplysia* has demonstrated a correlation between ERK phosphorylation timing and optimal spacing of training patterns.

While the spacing effect is typically associated with neural systems, we hypothesised that it might also be observable in non-neural cells, given that much of the molecular toolkit for memory formation is conserved across cell types. To test this hypothesis, we developed a non-neural reporter cell line to study the spacing effect. On the one hand, it provides exponentially greater experimental throughput than neural systems, accelerating the development of formal, predictive models of memory formation, and in the future, potentially creating new avenues for cognitive enhancement and treatment of cognitive disabilities. On the other hand, it enables the exploration of "cellular cognition" beyond neural systems.

Our study builds upon previous work on temporal pattern detection by individual neurons, including those expressing CRE reporters, the emergent properties of biological cascades in non-neuronal cells, including research on bistable switch-like behaviours in ERK signalling, and models of how different effects of massed vs. spaced stimulation could lead to different learning outcomes. What is distinct in our approach is the exposure of generic, non-neural cell cultures to fast, minute-scale temporal patterns generally believed to be the province of neurons.

---

## Results

### Design and calibration of a reporter cell line

We developed our reporter system from the human neuroblastoma cell line, SH-SY5Y. Our choice of input stimuli was motivated by our previous studies of spaced training in *Aplysia* neurons, which employed serotonin (5HT) as the memory-inducing stimulus. 5HT engages multiple conserved signalling cascades, and its effect on memory is known to rely on protein kinases A and C (PKA and PKC), which, in contrast to 5HT receptors, are common to all eukaryotic cells. We therefore applied activators of PKA and PKC to SH-SY5Y cells in place of 5HT. Forskolin, the activator of adenylate cyclase, was used to raise cellular levels of cyclic adenosine monophosphate (cAMP) and thus activate PKA. Tetradecanoyl phorbol acetate (TPA) was used as a direct activator of PKC, substituting for its endogenous second messenger diacylglycerol. Phorbol esters and cAMP have indeed been shown to substitute for 5HT in at least some forms of synaptic facilitation in *Aplysia*.

Our choice of experimental output was also based on the existing understanding of cell signalling in the service of memory formation. It is well known that memory induction in neurons is associated with the transcription of immediate-early genes (IEGs), a large network of early-response genes under the control of a cAMP response element (CRE) and the corresponding transcription factor, cAMP response element-binding protein 1 (CREB1). When CREB1 is phosphorylated by upstream signalling kinases, it drives expression of IEGs, which go on to modify the function of the neuron. Although many IEGs are relatively or completely specific to neurons (e.g. neurotransmitter-producing enzymes and synaptic vesicle proteins), CRE and CREB are conserved across cell types and regulate a diverse range of cellular responses to environmental stimuli. CREB1 is phosphorylated, directly and indirectly, by many key signalling enzymes including PKA, PKC, ERK, p38, Akt, CaMKII and CaMKIV, which in turn receive their inputs from a variety of receptors and second messengers, and in doing so, encode real-time cellular experience. CREB serves as an integrator of this experiential information that converts transient patterns of cell signalling into sustained cellular changes.

We therefore chose the expression of luciferase placed under the control of CRE as our proxy for cellular memory. To ensure that the readout represents immediate transcriptional activity rather than the accumulation of the protein product, we employed a short-lived variant of luciferase modified with a destabilising PEST sequence. A monoclonal cell line was derived from SH-SY5Y cells stably transfected with a CRE-dependent, PEST-modified luciferase, and termed **CRE-luc**.

To calibrate our system, we first measured the response of CRE-luc to forskolin and TPA. Cells were kept in serum-free media for 24 h prior to the start of the experiment. At t = 0, cells were perfused with media containing either of the two agonists in various concentrations, and responses were measured 4 h after the onset of the treatment. Drugs were applied either in a single 3-minute pulse followed by media washout, or continuously throughout the 4 h incubation. Both compounds elicited robust expression of luciferase at t = 4 h. Interestingly, the responses to TPA were roughly similar regardless of the length of treatment, whereas responses to forskolin differed more strongly between the single 3 min pulse and the continuous 4 h incubation, demonstrating higher sensitivity to the treatment duration.

For subsequent experiments, we selected concentrations of both forskolin and TPA that elicited minimal effect after a single pulse of each: forskolin was used at a concentration of **2 μM**, and TPA **2 nM**. This allowed for a greater dynamic ratio of luciferase induction in response to different numbers of pulses.

### Repetition boosts CRE-dependent transcription and slows its decay

To mimic our past studies, which employed 5HT acting through both the PKA and PKC signalling cascades as closely as possible, we employed a combination of forskolin and TPA delivered simultaneously. A single 3-min pulse of this drug combination produced robust luciferase expression 4 h after training. Four pulses of the same (ITI = 10 min) also induced luciferase expression, which was **~1.4-fold higher** (n = 3). By 24 h, however, luciferase expression induced by a single pulse was reduced, but remained relatively stable in cells that had received four pulses, eventually leading to a **2.8-fold difference** between conditions (n = 14). Similar effects were observed for both TPA and forskolin alone. The largest differences between the effects of a single pulse and repeated pulses (**29 %** vs **391 %** increase compared to untreated controls after 24 h, respectively) were observed for TPA. Notably, the length of TPA treatment had hardly any effect on luciferase expression. It appears that while PKA is more sensitive to the duration of stimulation, PKC is more sensitive to the number of events.

It is especially notable that the difference in the induction of luciferase by 1 versus 4 pulses of TPA or TPA+forskolin becomes greatly accentuated at 24 h, even though (i) stimulation in all cases ceases less than 1 h after the onset of the protocol, and (ii) at 4 h, the induction of luciferase is comparable. This result aligns well with the established dynamics of memory formation: repetition influences not only the immediate strength of memory, but the rate of forgetting, and so long-term memory differences between training protocols emerge over time. This phenomenon is most famously expressed in Ebbinghaus's forgetting curves, whose slopes change with every subsequent repetition of training. Our result also demonstrates the utility of the short-lived, PEST-tagged reporter construct, since without a destabilising sequence it may not have been possible to observe cellular forgetting.

### CRE-luc cells display the massed-spaced effect

Cells were treated with either a single 3-min pulse of the TPA+forskolin combination, or either drug by itself; four pulses, spaced either **10, 20 or 30 min** apart; or a single quadruple **12-min** pulse representing the massed condition. Expression of luciferase was measured 24 h after treatment. In all cases, expression of luciferase induced by spaced pulses was significantly greater than by the massed treatment. For TPA+forskolin and TPA alone, the optimal ITI was **10 min**, and the induction of luciferase diminished with more time between pulses. For forskolin alone, the difference between ITIs was less pronounced, with **20 min** being optimal. This suggests that PKA and PKC are "tuned" to distinct ITIs, meaning that responses to neuromodulators such as 5HT may in fact be an interactive summation of these overlapping timelines.

In our previous studies in *Aplysia*, we observed that two events spaced 45 min had the same effect on long-term memory as four events spaced 15 min — in other words, only two events, and their temporal spacing, were critical for the induction of sensitisation memory in that system. Although the precise mechanisms for this temporal specificity remain unknown, we tested whether CRE-luc cells also responded to the overall duration of the training protocol, rather than repetition of the training pulses, by including in our experiments two-pulse protocols that matched the timing of the first and last pulse in the four-pulse TPA treatment protocols. These two-pulse protocols, however, did not induce sustained luciferase expression, indicating that **repetition of > 2 training pulses is critical for the effect**.

### Massed-spaced effect correlates with CREB and ERK activation

To further characterise the massed-spaced effect in CRE-luc cells, we studied the effect of various TPA treatment protocols (1×, 4×, and massed) on the phosphorylation of CREB and ERK, an important node of cellular signalling known to act upstream of CREB and to integrate transient events in the service of long-term memory formation, including signals from PKA and PKC. Cells were lysed immediately after the end of the training protocol. Western blot showed robust phosphorylation of ERK after all treatments, and CREB after the 4× and massed treatments. However, both types of phosphorylation were significantly stronger in cells treated with 4 spaced pulses compared to the massed paradigm. We therefore observed the massed-spaced effect at the level of post-translational modifications immediately after the treatment protocol. We conclude that the temporal discrimination between the spaced and massed paradigms occurs at least in part upstream of ERK activation. Notably, when cells were lysed 1, 2, or 4 h after the treatment protocol, the differences in effects between paradigms gradually waned, but by 24 h were once again readily apparent.

At rest, ERK is localised to the cytosol. Upon its phosphorylation, ERK translocates to the nucleus, where it exhibits its principal downstream effects such as the activation of transcription factors including CREB. To examine whether the spaced and massed paradigms lead to differential translocation of ERK to the nucleus, we studied the localisation of total ERK and P-ERK by immunofluorescence immediately after treatment with TPA. We did observe a significantly greater nuclear : cytosolic ratio of P-ERK immediately after spaced training compared to massed training. The same trend was observed for total ERK. Overall, both phosphorylation and nuclear translocation of ERK differentially respond to massed and spaced treatments with TPA, indicating that the temporal pattern of stimulation is decoded at least in part either by ERK itself, or upstream of this kinase.

### Massed-spaced effect is blocked by ERK and CREB inhibition

To examine the role of ERK and CREB in mediating the massed-spaced effect, we employed **U0126**, the inhibitor of ERK phosphorylation, and **666-15**, the inhibitor of CREB transcriptional activity. Cells were preincubated with either inhibitor 10 min prior to the start of the training period. Drugs were maintained in the culture media throughout the training period and washed out either 1 h after the end of training (+1 h) or 24 h later upon sample collection (+24 h). Luciferase expression was measured at the 24 h time point by Western blot, together with total / phospho-ERK and CREB, with histone H3 used as loading control.

**U0126 (10 μM)** significantly reduced luciferase expression 24 h after 4×TPA treatment when the inhibitor was washed out 1 h after training. **666-15 (1 μM)** also significantly reduced luciferase expression 24 h after 4×TPA treatment, both when the drug was washed out 1 h after training, and when maintained for 24 h. Both treatments were sufficient to bring the ratio of luciferase induction by 4×TPA and massed protocols close to 1, completely blocking the spacing effect.

The sustained, interdependent activity of both ERK and CREB is required for the long-term induction of CRE-luc, and specifically by spaced training.

### Massed-spaced effect is replicated in HEK293 cells

To verify that the effects described above were not due to neuron-like properties of neuroblastoma cells, we tested our findings in a different human cell line completely abstracted from the nervous system — **HEK293 cells** derived from embryonic kidney. We generated a stable monoclonal cell line based on HEK293, expressing the same CRE-luc construct used throughout this study. When subjected to TPA treatments (1×, 4×, and massed), these cells showed significantly stronger induction of luciferase at 24 h after the 4× spaced treatment compared to the other two paradigms. When HEK293 cells were treated in the same way and lysed immediately after treatment, the 4×TPA-treated cells also showed the expected disproportionate elevation in the P-ERK / total ERK and P-CREB / total CREB ratios compared to cells treated with massed TPA. Overall, HEK293 cells demonstrated a strong spacing effect, further generalising our results.

---

## Discussion

We have observed, in two separate non-neural CRE reporter cell lines, persistent (>24 h) transcriptional responses that discriminated between minute-scale time patterns of stimulation with activators of PKA and PKC. We showed that these responses depended on both the number of training pulses, and their precise temporal spacing, and that these factors determined not only the amplitude of the response but also the rate of its decay, demonstrating hallmark features of memory. These results show that behaviourally relevant features of cognition, such as the spacing effect and the forgetting curve, can be studied in dividing, non-neural cells. Our work therefore extends the concept of "cellular cognition" beyond neural systems, acknowledging that all cells must extract salient patterns from environmental signals and convert them into stable, longer-term responses.

Several cell signalling components have been previously implicated in such persistent, memory-like cellular responses and are likely to play a role in the effects observed here. The activity of PKA can become persistent through the degradation of the enzyme's regulatory subunit. PKC has multiple known mechanisms of persistence, including membrane insertion, proteolytic cleavage, and de novo synthesis of an atypical, constitutively active form of PKC termed PKM. In the nervous system, these two kinases couple a large variety of neuromodulatory receptors (e.g. 5HT receptors, metabotropic glutamate receptors, muscarinic acetylcholine receptors, dopamine receptors, and β-adrenergic receptors) to the activation of ERK, whose persistence can be maintained through a number of mechanisms, including positive feedback at the cascade level, and a distributed mechanism of phosphorylation / dephosphorylation. The transcriptional activity of CREB can also be persistently maintained. Known mechanisms include (i) a positive feedback loop involving the CREB-dependent production of a CREB-activating secreted messenger such as BDNF; (ii) the degradation of transcriptional repressor ATF4/CREB2, known to depend on its phosphorylation of PKA; and (iii) the stabilisation of CREB output through CREB regulated transcription coactivator 1 (CRTC1), which can sustain CREB-dependent transcription independently of CREB phosphorylation. All these mechanisms are likely to be highly integrated.

Our reporter system presents an opportunity to unravel the precise temporal relationships between the components of this complex, dynamic signalling network underlying learning and memory. An experimental throughput required to generate formal, mathematical models of cell signalling in memory formation is nearly impossible to attain using neural systems, including cultures of primary or iPSC-derived neurons. Our system, however, is infinitely scalable and could potentially be automated. This now enables us to pursue formalised molecular models of memory formation, with potential applications in cognitive enhancement and treatment of cognitive disabilities.

---

## Methods (summary)

### Reagents

Forskolin was from Amsbio. TPA was from CST. 666-15 was from Tocris Bioscience. Other reagents were from Sigma unless indicated otherwise.

### Cell culture and treatments

Cell lines were acquired from ATCC (SH-SY5Y: CRL-2266; HEK-293: CRL-1573). Cells were maintained in standard growth media according to ATCC recommendations. For experiments, cells were seeded in 6-well plates at `0.3 × 10⁶` cells per well. 24 h before treatment, media were changed to serum-free. Treatments were performed using gentle perfusion with a needleless syringe / vacuum manifold to minimise mechanical disruption and maintain stable temperature and pH. Drugs were dissolved in DMSO as 1000× stocks and diluted in serum-free media to a final DMSO concentration of `0.1 %` (referred to as "Vehicle"), applied in precisely timed pulses, and washed out with vehicle-containing media.

### Stable transfection

To generate the CRE-luc reporter cell lines, SH-SY5Y or HEK293 cells were transfected with `pGL4.29[luc2P/CRE/Hygro]` vector (Promega) using Lipofectamine 3000. Stable transfectants were selected using `200 μg/ml` hygromycin. Monoclonal lines were isolated using the "scratch-and-sniff" method and tested for luciferase induction in response to forskolin treatment.

### Western blot

Cells were lysed in RIPA buffer with protease and phosphatase inhibitors (Roche). Western blotting was performed using standard protocols. Primary antibodies used: anti-P-ERK (CST #9101, polyclonal, 1:1000), anti-ERK (CST #4696, L34F12, 1:1000), anti-P-CREB (CST #9198, 87G3, 1:1000), anti-CREB (CST #9104, 86B10, 1:1000), anti-firefly luciferase (Invitrogen PA5-32209, polyclonal, 1:1000), anti-β-actin (CST #3700, 8H10D10, 1:5000), anti-H3 histone (CST #4499, D1H2, 1:10 000). LiCor IRDye secondary antibodies were used at 1:10 000 dilution.

### Luciferase assay

Luciferase activity was measured using the Luciferase Assay System (Promega) according to the manufacturer's instructions. Luminescence was measured using a Spectramax ID3 plate reader, and data collected using SoftMax Pro 7.1 software.

### Immunofluorescence

Cells grown on laminin-coated coverslips were fixed with 4 % formaldehyde, blocked, and incubated with primary antibodies (anti-P-ERK, CST #9101, 1:1000; anti-total ERK, CST #4696, 1:1000) overnight at 4 °C. Secondary antibodies (AlexaFluor 488 and 555, Thermo Fisher, 1:1000) were applied for 2 h at room temperature. Coverslips were mounted using ProLong Gold with DAPI (Thermo Fisher) and imaged using a Leica SP8 confocal system.

### Statistics and reproducibility

GraphPad Prism 10.3 was used for statistical analysis. Data are presented as log of the ratio of the effect in the treated sample to that in untreated controls. Normal distribution was verified using the Kolmogorov–Smirnov test, and paired parametric statistics used throughout. No data were excluded from analysis.

---

## Acknowledgements

This work was supported by NIH grant no. **1R01MH120300-01A1** (T.J.C.). The authors thank Anastasiya Susha for technical assistance and the lab of Dr. Stanislav Shvartsman (Princeton University) for helpful discussions of the earlier version of this manuscript.

## Author contributions

N.V.K. conceived the project and designed all experiments. N.V.K., R.E.C. and T.T. performed the experiments and analysed data. N.V.K., R.E.C., T.T. and T.J.C. interpreted the data. N.V.K. wrote the manuscript. T.J.C. edited the manuscript.

## Competing interests

The authors declare no competing interests.

## Citation

> Kukushkin, N. V., Carney, R. E., Tabassum, T., & Carew, T. J. (2024). The massed-spaced learning effect in non-neural human cells. *Nature Communications*, **15**, 9635. <https://doi.org/10.1038/s41467-024-53922-x>

## Licence

This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Licence (CC BY-NC-ND 4.0). View the licence at <https://creativecommons.org/licenses/by-nc-nd/4.0/>.

---

## Selected references (full list in the original article)

1. Cattaneo, V., San Martin, A., Lew, S. E., Gelb, B. D. & Pagani, M. R. *Neurobiol. Learn. Mem.* **172**, 107233 (2020).
2. Michael, D. et al. *Proc. Natl Acad. Sci. USA* **95**, 1864–1869 (1998).
3. Carpenter, S. K., Cepeda, N. J., Rohrer, D., Kang, S. H. K. & Pashler, H. *Educ. Psychol. Rev.* **24**, 369–378 (2012).
4. Ebbinghaus, H. *Memory: A contribution to experimental psychology* (Dover, 1964).
5. Pagani, M. R., Oishi, K., Gelb, B. D. & Zhong, Y. *Cell* **139**, 186–198 (2009).
6. Kukushkin, N. V., Tabassum, T. & Carew, T. J. *Proc. Natl. Acad. Sci.* **119**, e2210478119 (2022).
7. Smolen, P., Zhang, Y. & Byrne, J. H. *Nat. Rev. Neurosci.* **17**, 77–88 (2016).
8. Sun, W. et al. *Nature* **627**, 374–381 (2024).
9. Yin, J. C. P. & Tully, T. *Curr. Opin. Neurobiol.* **6**, 264–268 (1996).
10. Zhang, Y. et al. *Nat. Neurosci.* **15**, 294–297 (2011).

(Full reference list: see the original article at <https://doi.org/10.1038/s41467-024-53922-x>.)
