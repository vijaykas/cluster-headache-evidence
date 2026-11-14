# Cluster headache evidence log

A running, machine-readable record of what has been tried in cluster headache and what happened. As of 2026-11-12.

**Conventions.** Add rows; don't overwrite them. When a finding is superseded, mark it in place rather than deleting it — the history is part of the record. Every row carries a source.

- `type`: acute | bridge | preventive | mechanism | genetics | device | circadian | computational
- `population`: ECH = episodic, CCH = chronic, mixed = both
- `design`: RCT | crossover-RCT | open-label | registry | GWAS | provocation | dose-controlled-RCT | case-series | case-report | lab | survey | in-silico
- `result`: positive | negative | mixed | n/a
- `strength`: high | moderate | low | very-low | mechanistic

Rows marked `[Analysis N]` are computed in this repository; see `analyses.md` for their methods.

```csv
year,intervention_or_topic,type,population,design,n,primary_outcome,result_numbers,result,strength,source
2009,High-flow oxygen 100% 12 L/min,acute,mixed,crossover-RCT,76,pain-free/adequate relief at 15 min,78% vs 20% air,positive,high,https://journalclub.wustl.edu/2009/12/14/high-flow-oxygen-for-treatment-of-cluster-headache-a-randomized-trial/
1991,Sumatriptan 6 mg SC,acute,mixed,RCT,,improved at 15 min,~74%,positive,high,https://www.aafp.org/pubs/afp/issues/2010/0801/p284.pdf
2019,nVNS gammaCore (ACT1+ACT2 pooled),acute,ECH,RCT,225,pain-free at 15 min,ECH 24% vs 7% sham; CCH 7% vs 11%,mixed,moderate,https://pubmed.ncbi.nlm.nih.gov/31246132/
2022,Intranasal ketamine,acute,CCH,open-label,20,50% pain reduction at 15 min,missed at 15 min; -59% at 30 min,mixed,low,https://www.moreblossom.com/papers/intranasal-ketamine-for-acute-cluster-headache-attacks-results-from-a-proof-of-c
2018,SPG stimulation (Pathway CH-2),device,CCH,RCT-sham,93,relief at 15 min in >=50% of attacks,63% vs 29%,positive,moderate,https://community.the-hospitalist.org/content/device-impresses-chronic-cluster-headache-attacks
2021,Prednisone 100 mg taper 17 days,bridge,ECH,RCT,116,attacks in week 1,attack-free day 7 35% vs 7%; ~25% fewer attacks,positive,moderate,https://epub.ub.uni-muenchen.de/100899/
2011,Suboccipital cortivazol x3,bridge,mixed,RCT,43,responders,95% vs 55%,positive,moderate,https://www.mdedge9-ma1.mdedge.com/node/48649/path_term/51946
2025,GON methylprednisolone 80 mg + verapamil,bridge,ECH,RCT,,verapamil use over 12 weeks,no reduction,negative,moderate,https://doi.org/10.1177/03331024251370324
2019,Galcanezumab 300 mg,preventive,ECH,RCT,106,weekly attacks wk1-3,-8.7 vs -5.2; 50% responders 71% vs 53%,positive,moderate,https://pubmed.ncbi.nlm.nih.gov/31291515/
2020,Galcanezumab,preventive,CCH,RCT,,weekly attacks wk1-12,missed primary endpoint,negative,moderate,https://journals.sagepub.com/doi/pdf/10.1177/0333102420905321
2023,Galcanezumab started in pre-cluster period (Hong),preventive,ECH,case-series,2,bout course,cluster periods ended without typical attacks 10-60 days after,positive,very-low,https://thejournalofheadacheandpain.biomedcentral.com/counter/pdf/10.1186/s10194-023-01661-7.pdf
2018,Fremanezumab,preventive,CCH,RCT,,monthly attacks 12 wk,stopped for futility,negative,moderate,https://www.biocentury.com/article/296157/teva-discontinues-chronic-cluster-headache-trial-of-fremanezumab
2019,Fremanezumab,preventive,ECH,RCT,169,weekly attacks 4 wk,stopped for futility,negative,moderate,https://clinicaltrials.gov/study/NCT02945046
2025,Eptinezumab 400 mg IV (ALLEVIATE),preventive,ECH,RCT,231,weekly attacks wk1-2,-4.0 vs -4.6 (p=0.50); 50% responders 51% vs 37%,negative,moderate,https://pubmed.ncbi.nlm.nih.gov/40388178/
2025,Eptinezumab 400 mg IV q12w (CHRONICLE),preventive,CCH,open-label,131,safety,well tolerated; attacks fell (no control),n/a,low,https://researchprofiles.ku.dk/da/publications/long-term-safety-tolerability-and-efficacy-of-eptinezumab-in-chro/
2025,Erenumab 280 then 140 mg (CHERUB01),preventive,CCH,RCT,81,weekly attacks wk5-6,-7.3 vs -5.9; 50% responders 31.7% vs 45.0%,negative,moderate,https://pubmed.ncbi.nlm.nih.gov/40526384/
2026,Rimegepant 150 mg (Mayo pilot),acute+preventive,mixed,open-label,13,weekly attack frequency,-4.0 attacks/wk; 2/13 pain-free at 15 min,n/a,very-low,https://index.mirasmart.com/AAN2026/PDFfiles/AAN2026-003556.html
2011,Frovatriptan 5 mg short-term prophylaxis (Pageler),preventive,ECH,RCT,11,attack frequency,stopped at 11/80 for infeasibility; not significant,n/a,very-low,https://pubmed.ncbi.nlm.nih.gov/21198573/
2001,Olanzapine abortive (Rozen),acute,mixed,open-label,5,pain reduction,>=80% reduction in 4/5; ~20 min,positive,very-low,https://pubmed.ncbi.nlm.nih.gov/11576207/
1980,Chlorpromazine 75-700 mg/day (Caviness),preventive,mixed,open-label,13,headache relief,full relief in 12/13 (93%),positive,very-low,https://pubmed.ncbi.nlm.nih.gov/7390793/
2006,Clozapine-responsive cluster headache,preventive,mixed,case-report,1,headache,CH resolved alongside schizophrenia treatment,n/a,very-low,https://pubmed.ncbi.nlm.nih.gov/16804270/
2022,Psilocybin low-dose 3-dose course (Yale pilot),preventive,mixed,RCT,14,weekly attacks,~30% reduction; not significant; d=1.25 in chronic; no correlation with psychedelic intensity,mixed,low,https://unlimitedsciences.org/wp-content/uploads/2024/02/Exploratory_investigation_of_a_patient_i.pdf
2024,Psilocybin second course (Yale blinded extension),preventive,mixed,open-label-extension,10,weekly attacks 3 wk,18.4 -> 9.8/wk (p=0.013),positive,low,https://pubmed.ncbi.nlm.nih.gov/38581739/
2024,Psilocybin 3 doses (Madsen Copenhagen),preventive,CCH,open-label,10,attack frequency,-31%; 1 remission 21 wk; hypothalamic FC R=-0.81,positive,low,https://pubmed.ncbi.nlm.nih.gov/38238974/
2025,Psilocybin effect vs acute psychedelic intensity (pooled 3 trials),mechanism,mixed,secondary-analysis,34,correlation of 5D-ASC with headache change,p=0.453 (no relationship),n/a,low,https://index.mirasmart.com/AAN2025/PDFfiles/AAN2025-003327.html
2006,Psilocybin/LSD self-report (Sewell),preventive,mixed,survey,53,self-reported efficacy,22/53 (42%) benefit at subhallucinogenic doses,n/a,very-low,https://moreblossom.com/papers/response-of-cluster-headache-to-psilocybin-and-lsd
2023,2-Br-LSD (BOL-148) receptor profile,mechanism,n/a,lab,,receptor activity,5-HT2A partial agonist (Emax ~60%); 5-HT2B antagonist; pan 5-HT1 agonist,n/a,mechanistic,https://pmc.ncbi.nlm.nih.gov/articles/PMC10112881/
2026,BOL-148 (NYPRG-101) Phase 1/2,preventive,mixed,planned-RCT,,safety then efficacy,enrollment Q4 2026; Phase 1 data Q2 2027,n/a,very-low,https://www.biospace.com/press-releases/ceruvia-raises-8-million-to-complete-integrated-phase-1-2-trial-of-proprietary-non-hallucinogenic-lsd-analog-for-cluster-headache
2026,Psilocybin PEACE pilot (Australia),preventive,mixed,planned-RCT,,attack prevention,funded,n/a,n/a,https://www.georgeinstitute.org/news-and-media/news/hope-for-cluster-headache-community-as-psilocybin-trial-funded
2024,Lu AG09222 anti-PACAP (HOPE) - MIGRAINE not CH,preventive,migraine,RCT,237,monthly migraine days,-6.2 vs -4.2,positive,mechanistic,https://www.binasss.sa.cr/set24/42.pdf
2021,Vitamin D3 + multivitamin,preventive,mixed,RCT,27,weekly attacks,terminated; no results,n/a,n/a,https://www.centerwatch.com/clinical-trials/listings/NCT04570475/high-dose-vitamin-d-plus-multivitamin-in-the-prevention-of-cluster-headache
1996,Melatonin 10 mg evening (Leone),preventive,mixed,RCT,20,attack frequency 2 wk,5/10 responders vs 0/10 placebo; chronic did not respond,positive,low,https://www.curehunter.com/public/pubmed8933994.do
2016,Ramelteon (Imai),preventive,ECH,case-report,1,nocturnal attacks,nocturnal attacks stopped; early-morning persisted,n/a,very-low,https://pubmed.ncbi.nlm.nih.gov/27062025/
2027,Light therapy glasses (LUMIAVFc NCT06540651),preventive,CCH,RCT,48,median weekly attacks,recruiting; completion 2027-05,n/a,n/a,https://clinicaltrials.gov/study/NCT06540651
2017,Clomiphene (Nobre),preventive,mixed,case-series,15,remission,chronicity interrupted in all; pain-free mean 15 days,positive,very-low,https://www.thieme-connect.de/products/ejournals/abstract/10.1590/0004-282X20170119
2015,Clomiphene (Rozen),preventive,CCH,case-report,1,remission,pain-free 3.5 y; relapse; re-response,positive,very-low,https://zendy.io/title/10.1111/head.12491
2023,CPAP vs sham CPAP,preventive,CCH,crossover-RCT,25,weekly attacks,no difference (p=0.904),negative,moderate,https://hdl.handle.net/11250/3081075
2021,Occipital nerve stimulation (ICON),device,CCH,dose-controlled-RCT,131,weekly attacks wk21-24,100%: 17.6->9.5; 30%: 15.0->6.75; no group difference,mixed,moderate,https://medicaldialogues.in/neurology-neurosurgery/news/occipital-nerve-stimulation-decreases-attack-frequency-of-intractable-chronic-cluster-headache-lancet-79747
2026,ONSS occipital field stimulator,device,CCH,first-in-human,,safety and frequency,recruiting; completion 2027-07,n/a,n/a,https://clinicaltrials.gov/study/NCT07677137
2018,CGRP infusion provocation,mechanism,mixed,provocation,32,attack induction,ECH-active 8/9; CCH 7/14; remission 0,n/a,mechanistic,https://pmc.ncbi.nlm.nih.gov/articles/PMC6233850
2020,PACAP38 vs VIP infusion provocation,mechanism,mixed,provocation,44,attack induction,ECH-active PACAP 6/14 VIP 5/14; CCH 7/15 each; remission 0,n/a,mechanistic,https://pubmed.ncbi.nlm.nih.gov/31816859/
2022,Plasma CGRP/mast cell during PACAP/VIP attacks,mechanism,mixed,provocation,44,plasma markers,no change in CGRP tryptase histamine,n/a,mechanistic,https://research.regionh.dk/da/publications/pacap38-and-vip-induced-cluster-headache-attacks-are-not-associat/
2024,Levcromakalim (KATP opener) provocation,mechanism,mixed,provocation,41,attack induction,ECH-active 6/10 vs 1/10 placebo; CCH 5/17 vs 0; remission 1/15,n/a,mechanistic,https://pubmed.ncbi.nlm.nih.gov/38127692/
2009,Oxygen mechanism in rat TAC model (Akerman),mechanism,n/a,lab,,trigeminal/parasympathetic activity,acts on parasympathetic/facial projections not trigeminal afferents,n/a,mechanistic,https://pubmed.ncbi.nlm.nih.gov/19719541/
2023,Oxygen vs air on provoked autonomic reflex (healthy),mechanism,healthy,crossover-RCT,21,lacrimation,no effect,negative,mechanistic,https://fis.uke.de/portal/en/publications/oxygen-inhalation-has-no-effect-on-provoked-cranial-autonomic-symptoms-using-kinetic-oscillation-stimulation-in-healthy-volunteers(881d5f04-59a1-40dc-a842-59007784032e).html
2023,Circadian meta-analysis (Benkli/Burish),circadian,mixed,meta-analysis,4953 attacks,circadian pattern,71% circadian; peak 21:00-03:00; spring/autumn; low melatonin high cortisol; CLOCK & REV-ERBa; 5/9 risk genes clock-controlled,n/a,moderate,https://pubmed.ncbi.nlm.nih.gov/36967359/
2021,Verapamil circadian effects in mice/cells,circadian,n/a,lab,,clock period/genes,period shortening; clock gene changes in hypothalamus and trigeminal ganglion,n/a,mechanistic,https://pubmed.ncbi.nlm.nih.gov/33829951/
2022,Verapamil/lithium/prednisone vs anterior hypothalamic clock genes (mice),circadian,n/a,lab,,clock gene expression,no change in Clock Bmal1 Cry Per,negative,mechanistic,https://flore.unifi.it/retrieve/e398c381-ad35-179a-e053-3705fe0a4cff/2022%20-Cephalalgia%20Cluster-Clock.pdf
2008,5-HT7 knockout mouse circadian responses (Gardani),circadian,n/a,lab,,phase resetting,non-photic (8-OH-DPAT) response eliminated; altered light response at CT22,n/a,mechanistic,https://pubmed.ncbi.nlm.nih.gov/18065150/
2015,5-HT7 blockade and circadian phase shifts (Shelton),circadian,n/a,lab,,phase shift to light and 8-OH-DPAT,JNJ-18038683 blunted light-induced phase delay; abolished phase advance; blocked non-photic advance,n/a,mechanistic,https://pmc.ncbi.nlm.nih.gov/articles/PMC4295543/
2002,Frovatriptan receptor function (Comer),mechanism,n/a,lab,,5-HT7 functional activity,moderately potent FULL AGONIST at 5-HT7,n/a,mechanistic,https://pubmed.ncbi.nlm.nih.gov/12028320/
2002,5-HT7 and cranial vasodilation (Terron),mechanism,n/a,lab,,cranial vascular tone,5-HT7 mediates carotid/cranial vasodilation; mRNA high in cranial vessels; proposed for migraine prophylaxis,n/a,mechanistic,https://pubmed.ncbi.nlm.nih.gov/11937086/
2014,5-HT7 antagonist and meningeal artery flow (Wang),mechanism,n/a,lab,,middle meningeal artery flow,agonist AS-19 increased flow; antagonist SB269970 reduced it,n/a,mechanistic,https://pubmed.ncbi.nlm.nih.gov/24584680/
2026,Prejunctional 5-HT7 and CGRP release (Terol-Ubeda),mechanism,n/a,lab,,CGRPergic vasodepressor responses,5-HT7 agonist AS-19 INHIBITED perivascular sensory CGRP release in both sexes,n/a,mechanistic,https://pubmed.ncbi.nlm.nih.gov/42131800/
2025,5-HT7 antagonists and neurotrophins (Lee),mechanism,n/a,lab,,visceral nociception,5-HT7 antagonists cut NGF/BDNF overproduction and mucosal neurite outgrowth; analgesic,n/a,mechanistic,https://pubmed.ncbi.nlm.nih.gov/40757652/
2012,JNJ-18038683 selective 5-HT7 antagonist - MDD not CH,mechanism,MDD,RCT,225,MADRS change,failed vs placebo (study lacked assay sensitivity); tolerated; REM latency prolonged in healthy volunteers,negative,mechanistic,https://pubmed.ncbi.nlm.nih.gov/22570363/
2024,JNJ-18038683 - bipolar cognition not CH,mechanism,bipolar,RCT,60,neurocognitive battery,no difference vs placebo; tolerated,negative,mechanistic,https://pubmed.ncbi.nlm.nih.gov/39250138/
2023,GWAS meta-analysis (Winsvold),genetics,mixed,GWAS,4777,risk loci,8 loci; SNP heritability 14.5%; MR smoking causal,n/a,moderate,https://pmc.ncbi.nlm.nih.gov/articles/PMC10952302/
2021,GWAS (O'Connor),genetics,mixed,GWAS,1443,risk loci,loci on chr 1 2 6; immune pathways,n/a,moderate,https://pubmed.ncbi.nlm.nih.gov/34184781/
2026,[Analysis 1] Trial landscape (ClinicalTrials.gov),computational,mixed,in-silico,94 trials,approach coverage,CGRP 1740/6105 enrolled; 0 trials melatonin-type/lithium/hormones/pre-bout/genotype-guided/anti-PACAP,n/a,moderate,this repository
2026,[Analysis 2] Risk-gene tissue enrichment (GTEx),computational,mixed,in-silico,16 genes,tissue enrichment vs 10k random sets,tibial artery p<0.0001 FDR 0.005; coronary FDR 0.008; aorta FDR 0.021; hypothalamus p=0.91; 13/16 genes up in artery,n/a,moderate,this repository
2026,[Analysis 3] Receptor signature (ChEMBL),computational,mixed,in-silico,8 drugs + 4225 approved,shared potent targets,5-HT7/5-HT6/5-HT2A bound by all 4 lasting-effect drugs not triptans; frovatriptan only triptan with 5-HT7 (pChEMBL 7.44); DIRECTION SUPERSEDED BY ANALYSIS 6,n/a,low,this repository
2026,[Analysis 5] Risk-variant eQTLs (GTEx),computational,mixed,in-silico,13 variants,eQTL direction for risk allele,LRP1 up in artery (p=9e-21); UFL1 up in tibial artery (p=1e-9); PLCE1 DOWN in artery/nerve/skin (both variants ~1e-6); CAPN2 down; no hypothalamus eQTL,n/a,moderate,this repository
2026,[Analysis 5] Drug-target tissue expression (GTEx),computational,n/a,in-silico,18 genes,artery vs hypothalamus specificity,artery-enriched: HTR1B CACNA1C CALCRL RAMP1 NR3C1 VIPR2 KCNJ8 ABCC9; hypothalamus-enriched: ADCYAP1R1 (PAC1) ABCC8; HTR7 both,n/a,low,this repository
2026,[Analysis 6] 5-HT7 functional direction (IUPHAR/GtoPdb via PubChem),computational,mixed,in-silico,57 ligands,direction and potency at 5-HT7,all 4 lasting-effect drugs are ANTAGONISTS; frovatriptan is a FULL AGONIST; lasting-effect pKi 7.67 vs acute-only triptan 6.65 (~11x); exact permutation p=0.067 (most extreme of 15 orderings),n/a,low,this repository
2026,[Analysis 6] HTR7 dual-tissue specificity (GTEx),computational,n/a,in-silico,514 background genes,joint artery+hypothalamus specificity,HTR7 artery z=+1.84 hypothalamus z=+2.26; rank 1/514 on the joint score (0/514 higher); HTR2A 2nd; PLCE1/LRP1/FHL5 artery-only (hypothalamus -0.57/-0.71/-0.54),n/a,low,this repository
2026,[Analysis 6] 5-HT7 literature gap (PubMed),computational,mixed,in-silico,n/a,co-mention counts,0 papers pair 5-HT7 with cluster headache; 23 papers 5-HT7 x circadian phase shift vs 6 for 5-HT2A; 0 CH papers for lurasidone/risperidone/ziprasidone/vortioxetine/metergoline/ritanserin,n/a,moderate,this repository
2026,[Analysis 6] Selective 5-HT7 antagonists in human trials (ClinicalTrials.gov),computational,n/a,in-silico,15 compounds,human trial record,only JNJ-18038683 has reached humans (3 trials; Phase 2 complete in MDD and bipolar); SB269970/LP-211/DR-4004/SB-258719/SB-656104 preclinical only,n/a,moderate,this repository
2026,[Analysis 7] Who runs CH trials (ClinicalTrials.gov),computational,n/a,in-silico,129 studies,investigators and sponsors,UTHealth Houston and Leiden UMC lead 5 each then a long tail; top sites Houston/Danish Headache Center/Lariboisiere/Frankfurt/Ghent/Leiden,n/a,moderate,this repository
2026,[Analysis 7] CH vs 5-HT7 literatures (PubMed),computational,n/a,in-silico,980 + 71 papers,author overlap,the two literatures barely overlap; 14 author names appear in both,n/a,low,this repository
2026,[Analysis 8] NIH funding for CH (RePORTER),computational,n/a,in-silico,173 projects,phrase-filtered grant count,39 mention CH; 6 have it in the title; 5 of those are one Michigan project 1997-2000; 1 current (NINDS R61 UTHealth Houston Burish/Yoo),n/a,moderate,this repository
2026,[Analysis 8] European CH funding (OpenAIRE),computational,n/a,in-silico,3 projects,non-US grants,Aarhus/Novo Nordisk Foundation TENS trial; Capital Region of Denmark/Lundbeck Foundation PACAP38; EU grant to a Dutch neuromodulation company,n/a,low,this repository
2026,[Analysis 8] Commercial sponsors (ClinicalTrials.gov),computational,n/a,in-silico,50 studies / 28 orgs,industry activity,large pharma exited after CGRP (Lilly 2016 Teva 2017 Novartis 2016 Lundbeck 2021); remaining activity is almost entirely neurostimulation devices,n/a,moderate,this repository
```

## GWAS loci and prioritized genes (Winsvold 2023)

```csv
locus,lead_variant,risk_allele,odds_ratio,prioritized_genes,eqtl_effect_of_risk_allele_GTEx_v8,notes
DUSP10,rs17011182,G,1.38,DUSP10,up RP11-815M8.1 lncRNA (lung; tibial nerve),MAPK (p38/JNK) phosphatase; inflammation
MERTK,rs13399108,G,1.41,MERTK;TMEM87B;FBLN7;SLC20A1,up MERTK (pancreas; tibial nerve); down TMEM87B (aorta; fibroblasts),efferocytosis
FTCDNL1,rs6714578,A,1.53,SATB2,down SATB2 (skin),neurodevelopment; strongest signal
FHL5,rs9486725,T,1.29,UFL1;FHL5;KLHL32;NDUFAF4,up UFL1 (tibial artery strongest),vascular smooth muscle; migraine locus
WNT2,rs2402176,C,1.20,CFTR;CAPZA2;ST7,none,unclear
PLCE1,rs57866767 / rs2274224 (missense),T / G,1.18,PLCE1,DOWN PLCE1 (tibial artery; nerve; skin); down NOC3L,risk allele lowers PLCE1
LRP1,rs11172113,T,1.18,LRP1,up LRP1 (tibial artery p=9e-21; aorta),migraine locus
CAPN2,rs10916600 (trans-ancestry),T,,CAPN2,down CAPN2 (fibroblasts; pituitary; adrenal; arteries),calpain-2
```

**Note on HTR7 and the genetics.** HTR7 sits at chr10:90,740,823–90,857,698, about 3.4 Mb from the PLCE1 lead variant at chr10:94,263,320. That is well outside a cis-eQTL window, so HTR7 is **not** a cluster headache genetic hit. The 5-HT7 hypothesis in `hypotheses.md` rests on convergent pharmacology and tissue expression, not on genetics, and should not be described otherwise.

## Gaps in this record

- Unregistered and non-English trials are missing; coverage is registry-based.
- Several older sources are secondary (news or society write-ups) rather than the primary paper. Replacing those with primary citations is a standing task.
- Effect sizes are recorded as reported, without re-analysis or risk-of-bias assessment.
- The funding picture is NIH-centred; European national funders and private foundations are partly captured, UK funding not at all.
