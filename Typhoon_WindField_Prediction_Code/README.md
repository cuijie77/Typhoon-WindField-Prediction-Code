# 基于注意力机制与多分支特征融合的台风局地风场预测研究

This repository is the code-only public release for the master's thesis
**《基于注意力机制与多分支特征融合的台风局地风场预测研究》**. It contains the core
model, fixed-t0 processing logic, training/evaluation scripts, and code used to
reproduce Figures 1--5. It does **not** contain raw data, model weights,
prediction outputs, or other large artifacts.

## Task

Predict a local 31 x 31 two-component (u10/v10) wind field at 6 h, 12 h, or
24 h from four historical hourly patches. The corrected target is
`Y_H = W(t0 + H, C(t0))`: the future ERA5 wind field is sampled at the
initialization-time storm center, not the future storm center.

## Data sources

Users must obtain and prepare the data themselves, subject to their respective
licences and access policies:

- CMA best-track data
- ERA5 reanalysis u10/v10 wind fields
- FY-3E WindRAD products (for the study's satellite-data component)

No ERA5, CMA, FY-3E HDF, model checkpoint, prediction NPZ, or manuscript
result file is included in this repository.

## Environment

- Python 3.10
- PyTorch 2.0.1
- CUDA 11.8

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Install the CUDA-compatible PyTorch wheel appropriate for your operating system
and CUDA driver if the generic `pip` command does not provide it.

## Repository layout

- `models/`: CNN-LSTM, SE attention, MBFN, and full STL-Net.
- `data_processing/`: track cleaning, fixed-t0 patch construction, NPZ loading, and normalization.
- `train/`: training entry points for 6 h, 12 h, and 24 h.
- `evaluation/`: RMSE, MAE, WS-MAE/AWSE, and prediction-NPZ evaluation.
- `visualization/`: Figure 1--5 plotting scripts.
- `data/README.md`: expected user-prepared dataset format.

## Data preparation

Prepare the NPZ files described in [`data/README.md`](data/README.md). Training
requires `X` `(N, 4, 2, 31, 31)` and `Y` `(N, 2, 31, 31)`, with a fixed
2020--2021/train, 2022/validation, and 2023/test split. The Min--Max scaler is
fitted from `X_train` and `Y_train` only. Validation selects the checkpoint by
normalized MSE; the 2023 test split is evaluated only after training.

## Training

Run from the repository root so package imports resolve:

```bash
python -m train.train_6h --data-dir data/datasets --output-dir outputs --seed 0
python -m train.train_12h --data-dir data/datasets --output-dir outputs --seed 0
python -m train.train_24h --data-dir data/datasets --output-dir outputs --seed 0
```

Default protocol: MSE loss, Adam (`lr=1e-3`, `weight_decay=0`), batch size 64,
100 maximum epochs, ReduceLROnPlateau (factor 0.5, patience 5, min LR 1e-6),
and early stopping patience 15.

## Evaluation

Metrics are reported in m s^-1:

- RMSE: component-wise root mean squared error.
- MAE: component-wise mean absolute error.
- WS-MAE / AWSE: mean absolute error of wind-speed magnitude.

```bash
python -m evaluation.evaluate outputs/6h/seed_0/test_predictions.npz
```

## Figures

`visualization/` contains Figure 1--5 plotting scripts with relative paths.
They create outputs under `results/figures/`. Figures 1, 2, 3, and 5 use values
or schematic geometry defined in their scripts. Figure 4 intentionally requires
user-prepared seed-0 prediction files at `results/6h/test_predictions.npz`,
`results/12h/test_predictions.npz`, and `results/24h/test_predictions.npz`.
Those result arrays are not released.

## GitHub readiness

This folder contains code and documentation only. `.gitignore` excludes raw
data, processed NPZ/NPY files, outputs, checkpoints, caches, IDE files, and
other generated artifacts. It can be uploaded directly to GitHub after adding
any preferred licence, citation, and data-access statement.
