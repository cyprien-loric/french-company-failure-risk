# Company insolvency risk prediction (France)

Predicting which French companies are most likely to go through a collective judicial procedure (receivership or liquidation), using open public data.

Portfolio project: a full pipeline on real data, from raw files to a trained model.

## Data

Two public sources, joined on the SIREN (the 9-digit company ID):

- **BODACC** : publishes judicial procedures. Used to build the target: a company is labelled as "defaulting" if it appears there with a judgment between 2019 and 2026.
- **Sirene (INSEE)** : the registry of all French companies (creation date, sector, legal form, size). Used as the features.

The raw data is not included. Run the scripts in `src/` to download it.

## How it works

Three notebooks, run in order:

1. `01_ETL` — load, clean and join the two sources into one dataset.
2. `02_EDA` — explore the data (age, sector, legal form, size).
3. `03_Modélisation` — train and compare three models, then analyse the best one.

The final dataset has ~16.9M companies, 2.66 % of them defaulting. This imbalance is handled with class weights. The judgment date and nature are excluded from the features, since they only exist after a default (to avoid data leakage ).

## Results

Logistic regression : AUC 0.86, recall 0.82, F1 0.18  
Random Forest : AUC 0.81, recall 0.40, F1 0.27  
XGBoost : AUC 0.91, recall 0.86, F1 0.19

XGBoost is kept. It catches 86 % of the companies that actually default, with a precision of 11 %: the model flags a lot of companies on purpose, because in credit risk a missed default costs more than a false alarm. It works as a prioritisation tool, not a final decision.

## Run it

```bash
pip install -r requirements.txt
```

1. Run the scripts in `src/` to download the data into `Data/raw/`.
2. Run the ETL notebook to build the final dataset.
3. Run the EDA and modelling notebooks.

## Limitations

- The model only uses structural data (sector, age, size, legal form), 
  not financial ratios, so it scores company profiles, not individual situations.
- The dataset mostly contains active companies and those with a court 
  procedure. Companies that closed without going through court are 
  underrepresented (survivorship bias).
- It was trained and tested on the same time period (2019–2026), not on 
  a train/test split by year, so the metrics are likely optimistic.
  
## Next steps

- Add INPI financial ratios (the main lever for improvement).
- Calibrate the probabilities and tune the decision threshold.
- Build a small dashboard to explore the scores.

## Author

Cyprien Loric — [github.com/Cyprien-Loric](https://github.com/Cyprien-Loric)
