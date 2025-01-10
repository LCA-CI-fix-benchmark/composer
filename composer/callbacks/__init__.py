import importlib

# Copyright 2022 MosaicML Composer authors
# SPDX-License-Identifier: Apache-2.0

"""Callbacks that run at each training loop :class:`.Event`.

Each callback inherits from the :class:`.Callback` base class. See detailed description and
examples for writing your own callbacks at the :class:`.Callback` base class.
"""

# Import all callback classes
module = importlib.import_module(__name__)
__all__ = [name for name in dir(module) if name[0] != '_']

# Export all callback classes
from composer.callbacks.activation_monitor import ActivationMonitor
from composer.callbacks.checkpoint_saver import CheckpointSaver
from composer.callbacks.early_stopper import EarlyStopper
from composer.callbacks.export_for_inference import ExportForInferenceCallback
from composer.callbacks.free_outputs import FreeOutputs
from composer.callbacks.generate import Generate
from composer.callbacks.health_checker import HealthChecker
from composer.callbacks.image_visualizer import ImageVisualizer
from composer.callbacks.lr_monitor import LRMonitor
from composer.callbacks.memory_monitor import MemoryMonitor
from composer.callbacks.mlperf import MLPerfCallback
from composer.callbacks.nan_monitor import NaNMonitor
from composer.callbacks.optimizer_monitor import OptimizerMonitor
from composer.callbacks.runtime_estimator import RuntimeEstimator
from composer.callbacks.speed_monitor import SpeedMonitor
from composer.callbacks.system_metrics_monitor import SystemMetricsMonitor
from composer.callbacks.threshold_stopper import ThresholdStopper
from composer.callbacks.memory_snapshot import MemorySnapshot

__all__ = [
    'HealthChecker',
    'RuntimeEstimator',
    'SystemMetricsMonitor',
    'Generate',
    'FreeOutputs',
    'MemorySnapshot',
]

# Order the imports to match the __all__ list
from composer.callbacks.activation_monitor import ActivationMonitor
from composer.callbacks.optimizer_monitor import OptimizerMonitor
from composer.callbacks.lr_monitor import LRMonitor
from composer.callbacks.memory_monitor import MemoryMonitor
from composer.callbacks.nan_monitor import NaNMonitor
from composer.callbacks.speed_monitor import SpeedMonitor
from composer.callbacks.checkpoint_saver import CheckpointSaver
from composer.callbacks.mlperf import MLPerfCallback
from composer.callbacks.early_stopper import EarlyStopper
from composer.callbacks.export_for_inference import ExportForInferenceCallback
