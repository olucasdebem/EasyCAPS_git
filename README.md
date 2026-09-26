# EasyCAPS 🧬

**The EasyCAPS web tool enables restriction enzyme genotyping and donor DNA design for CRISPR/Cas9 genome editing**

🌐 **Access the web application:** [https://easycaps-app.onrender.com/](https://easycaps-app.onrender.com/)
📄 **Read the preprint:** [bioRxiv](https://doi.org/10.64898/2026.04.17.719238) 

---

## 📌 Overview

Tracking Single Nucleotide Polymorphisms (SNPs) following CRISPR-Cas9 genome editing is a critical yet often labor-intensive step in modern genetic research. Existing dCAPS primer design tools suffer from significant limitations, such as strict sequence length limits and rigid enzyme lists. 

**EasyCAPS** is an interactive, web-based bioinformatics tool developed to integrate genotyping and gene-editing planning. It streamlines molecular biology workflows by automating the identification of natural and derived restriction sites (CAPS and dCAPS). Furthermore, it assists in the rational design of donor sequences for CRISPR experiments, suggesting silent mutations to mask the Protospacer Adjacent Motif (PAM) while rigorously evaluating codon usage bias to maintain translational efficiency.

---

## ✨ Key Features

* **CAPS & dCAPS Identification:** Automatic identification of natural restriction sites (CAPS) and generation of derived sites (dCAPS) based on a dynamic, user-defined restriction enzyme library.
* **"Masking PAM" Module:** Designs synonymous mutations to mask the Cas9 recognition site, preventing re-cleavage of the newly edited allele and facilitating direct one-step editing.
* **Codon Usage Bias Analysis:** Evaluates all generated synonymous mutations against the target organism's codon usage table, calculating the fold-change between the original and new codon to prevent negative impacts on mRNA stability and translation speed.
* **Rational Donor Design:** Scans donor sequences to identify positions where single-nucleotide substitutions can create new restriction sites (Silent CAPS) for tracking, without altering the amino acid sequence.

---

## 🚀 How to Use

The EasyCAPS interface is designed for an intuitive, centralized workflow without navigating multiple pages. It consists of three logical modules:

1.  **CAPS / dCAPS Analysis:** Input the nucleotide sequences (up to 200 bp) of the two alleles to be compared (e.g., wild-type and mutant). For analyses involving coding regions, sequences must be in the correct reading frame (frame 0). Users can define the mismatch threshold for dCAPS primer design (0 to 3).
2.  **Enzyme Selection:** Search the library by enzyme name or recognition sequence. Users can scan all available enzymes or select a specific subset available in their laboratory.
3.  **CRISPR Parameters (Optional):** For silent mutation strategies, select the target organism (e.g., *S. cerevisiae*, *E. coli*, *H. sapiens*) to load the correct codon usage table. Input the PAM pattern (default NGG) and up to 10 gRNA sequences.

---

## 🛠️ Architecture and Technologies

The EasyCAPS computational pipeline was designed to process inputs sequentially through Data Preprocessing, Core CAPS/dCAPS Identification, Silent Mutation Engineering, and Output Rendering.

* **Backend:** Python 3.14.0 and Flask 3.1.0 microframework.
* **Templating & Security:** Jinja2 3.1.6 for server-side rendering and Bleach 6.2.0 for input sanitization against injection attacks.
* **Frontend:** Standard HTML5, CSS3, and JavaScript ensuring cross-browser compatibility.
* **Deployment:** The live web application is hosted on the Render cloud platform as a synchronized mirror of this repository.

---

## 📖 Citation

If you use EasyCAPS in your research, please cite our preprint:

> De Bem, L. S., Gross, J., & Jacobus, A. P. (2026). EasyCAPS: A web tool for restriction-based genotyping and rational CRISPR-Cas9 donor design. *bioRxiv*. [https://doi.org/10.64898/2026.04.17.719238](https://doi.org/10.64898/2026.04.17.719238) 

---

## 📜 License

The complete source code is open-source and freely accessible. The preprint is made available under a **CC-BY-NC-ND 4.0 International license**.

***

