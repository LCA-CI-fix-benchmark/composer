# Copyright 2022 MosaicML Composer authors
# SPDX-License-Identifier: Apache-2.0

import pytest
from torch.utils.data import DataLoader
import pathlib

from composer.trainer import Trainer
from tests.common import RandomClassificationDataset, SimpleModel
from composer.loggers import LoggerDestination
from composer import State, Trainer


class FileUploaderTracker(LoggerDestination):

    def __init__(self) -> None:
        self.uploaded_files = []

    def upload_file(self, state: State, remote_file_name: str, file_path: pathlib.Path, *, overwrite: bool):
        del state, overwrite  # unused
        self.uploaded_files.append((remote_file_name, file_path))


@pytest.mark.parametrize('interval', ['1ba', '3ba'])
    # Construct the trainer and train
    trainer = Trainer(
        model=simple_model,
        loggers=[file_tracker_destination],
        callbacks=memory_snapshot,
        train_dataloader=DataLoader(RandomClassificationDataset()),
        max_duration='10ba',
    )
