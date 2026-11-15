from typing import Final

import numpy as np
import onnxruntime
from onnxmltools.convert.xgboost.operator_converters.XGBoost import convert_xgboost
from skl2onnx import convert_sklearn, update_registered_converter
from skl2onnx.common.data_types import FloatTensorType
from skl2onnx.common.shape_calculator import calculate_linear_classifier_output_shapes
from sklearn.pipeline import Pipeline
from valve_guardian.arrays import FeatureMatrix
from xgboost import XGBClassifier

INPUT: Final = "features"
GRAPH: Final = "valve-guardian"
PARITY_TOLERANCE: Final = 1e-4
OPSET: Final = 17

update_registered_converter(
    XGBClassifier,
    "XGBoostXGBClassifier",
    calculate_linear_classifier_output_shapes,
    convert_xgboost,
    options={"nocl": [True, False], "zipmap": [True, False, "columns"]},
)


class OnnxExport:
    @staticmethod
    def of(pipeline: Pipeline, sample: FeatureMatrix) -> bytes:
        """The fitted pipeline as ONNX, refused unless it agrees on `sample`."""
        model = convert_sklearn(
            pipeline,
            name=GRAPH,
            initial_types=[(INPUT, FloatTensorType([None, sample.shape[1]]))],
            options={id(pipeline.steps[-1][1]): {"zipmap": False}},
            target_opset={"": OPSET, "ai.onnx.ml": 3},
        ).SerializeToString()
        OnnxExport.check_parity(model, pipeline, sample)
        return model

    @staticmethod
    def check_parity(model: bytes, pipeline: Pipeline, sample: FeatureMatrix) -> None:
        session = onnxruntime.InferenceSession(
            model, providers=["CPUExecutionProvider"]
        )
        single = sample.astype(np.float32)
        (exported,) = session.run(["probabilities"], {INPUT: single})
        gap = np.abs(np.asarray(exported) - pipeline.predict_proba(single)).max()
        if gap > PARITY_TOLERANCE:
            raise ValueError(f"ONNX and scikit-learn disagree by {gap:.2e}")
