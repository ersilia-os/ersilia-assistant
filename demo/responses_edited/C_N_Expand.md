
### Understanding Your Query

- You have **manually curated** the literature to identify **natural products** that inhibit **SARS-CoV-1** and/or **SARS-CoV-2**.
- You would like to explore the **chemical space** around these identified natural products.
- Your goal is likely to understand the **structural features** and potential **modifications** that could enhance or alter the activity of these compounds against SARS-CoV-1 and/or SARS-CoV-2.

---

### Recommended Models for Exploration

#### Model: **eos8fth**

- **URL**: [eos8fth GitHub Repository](https://github.com/ersilia-os/eos8fth)
- **Title**: SARS-CoV-2 Antiviral Prediction: REDIAL-2020
- **Why Use It?**
  - Specifically designed to predict the activity of small molecules against **SARS-CoV-2**.
  - Trained on a large dataset of **high-throughput screening data**.
  - Uses an **ensemble learning approach** and diverse descriptor types to identify potential analogs or derivatives.
  - **How to Use**: Input the chemical structures of your curated natural products into the **REDIAL-2020 web application** to:
    - Generate predictions of activity against SARS-CoV-2.
    - Explore the surrounding chemical space for potential leads.

---

#### Model: **eos4cxk**

- **URL**: [eos4cxk GitHub Repository](https://github.com/ersilia-os/eos4cxk)
- **Title**: SARS-CoV-2 Antiviral Screening with ImageMol
- **Why Use It?**
  - **ImageMol** is a self-supervised deep learning framework that captures structural information from molecular images.
  - Useful for understanding the **chemical properties** and relationships of natural products.
  - Excels in predicting molecular properties and drug targets, including those relevant to **COVID-19**.
  - **How to Use**: Employ ImageMol to process your dataset and identify potential leads.

---

### Suggested Recipe for Running the Models

Ensure your dataset is stored in a file named **`input.csv`** with a column called **`smiles`** containing the SMILES strings of the molecules.

#### Commands for Model eos8fth:
```bash
ersilia fetch eos8fth
ersilia serve eos8fth
ersilia run -i input.csv -o output_eos8fth.csv
```

#### Commands for Model eos4cxk:
```bash
ersilia fetch eos4cxk
ersilia serve eos4cxk
ersilia run -i input.csv -o output_eos4cxk.csv
```

---

### Next Steps

By leveraging these models, you can systematically explore the chemical space of your curated natural products and identify promising candidates for further investigation.
