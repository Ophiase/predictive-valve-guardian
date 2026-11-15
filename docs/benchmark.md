# Benchmark

Repeated stratified 5-fold cross-validation, three repeats, over every cycle;
mean ± standard deviation across the 15 folds. Written by `just benchmark`.

| Representation | Columns | Model | F1 | ROC AUC | Brier | |
| --- | --- | --- | --- | --- | --- | --- |
| statistics to signal + 20 fourier | 54 | logistic regression | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0004 ± 0.0001 | **deployed** |
| raw | 6600 | random forest | 1.0000 ± 0.0000 | 1.0000 ± 0.0000 | 0.0008 ± 0.0002 |  |
| statistics to slope + 20 fourier | 68 | logistic regression | 0.9996 ± 0.0009 | 1.0000 ± 0.0000 | 0.0004 ± 0.0005 |  |
| raw | 6600 | xgboost | 0.9996 ± 0.0009 | 0.9996 ± 0.0009 | 0.0005 ± 0.0009 |  |
| statistics to curvature + 20 fourier | 82 | logistic regression | 0.9994 ± 0.0010 | 0.9991 ± 0.0018 | 0.0009 ± 0.0009 |  |
| raw | 6600 | logistic regression | 0.9991 ± 0.0014 | 0.9999 ± 0.0002 | 0.0008 ± 0.0011 |  |
| statistics to signal + 20 fourier | 54 | xgboost | 0.9987 ± 0.0020 | 1.0000 ± 0.0001 | 0.0012 ± 0.0017 |  |
| statistics to slope + 20 fourier | 68 | xgboost | 0.9984 ± 0.0019 | 1.0000 ± 0.0000 | 0.0013 ± 0.0016 |  |
| statistics to signal + 20 fourier | 54 | random forest | 0.9982 ± 0.0027 | 1.0000 ± 0.0000 | 0.0014 ± 0.0012 |  |
| statistics to curvature + 20 fourier | 82 | xgboost | 0.9981 ± 0.0020 | 1.0000 ± 0.0000 | 0.0013 ± 0.0015 |  |
| statistics to slope + 20 fourier | 68 | random forest | 0.9979 ± 0.0026 | 1.0000 ± 0.0000 | 0.0015 ± 0.0012 |  |
| statistics to curvature + 20 fourier | 82 | random forest | 0.9976 ± 0.0028 | 1.0000 ± 0.0000 | 0.0015 ± 0.0011 |  |
| statistics to slope | 28 | random forest | 0.9948 ± 0.0033 | 0.9999 ± 0.0001 | 0.0073 ± 0.0016 |  |
| statistics to curvature | 42 | random forest | 0.9941 ± 0.0041 | 0.9999 ± 0.0002 | 0.0078 ± 0.0017 |  |
| statistics to signal | 14 | random forest | 0.9934 ± 0.0034 | 0.9997 ± 0.0003 | 0.0099 ± 0.0019 |  |
| statistics to curvature | 42 | xgboost | 0.9932 ± 0.0038 | 0.9999 ± 0.0002 | 0.0051 ± 0.0028 |  |
| statistics to slope | 28 | xgboost | 0.9919 ± 0.0052 | 0.9998 ± 0.0002 | 0.0059 ± 0.0033 |  |
| statistics to signal | 14 | xgboost | 0.9913 ± 0.0032 | 0.9997 ± 0.0003 | 0.0065 ± 0.0025 |  |
| statistics to curvature | 42 | logistic regression | 0.9911 ± 0.0055 | 0.9974 ± 0.0026 | 0.0091 ± 0.0034 |  |
| statistics to slope | 28 | logistic regression | 0.9903 ± 0.0038 | 0.9966 ± 0.0027 | 0.0111 ± 0.0031 |  |
| statistics to signal | 14 | logistic regression | 0.9124 ± 0.0104 | 0.9619 ± 0.0056 | 0.0905 ± 0.0051 |  |
