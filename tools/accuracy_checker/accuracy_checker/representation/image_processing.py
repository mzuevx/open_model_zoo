"""
Copyright (c) 2018-2021 Intel Corporation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from enum import Enum
import numpy as np

from .base_representation import BaseRepresentation
from ..data_readers import BaseReader


class GTLoader(Enum):
    PILLOW = 0
    OPENCV = 1
    DICOM = 2
    RAWPY = 3


class ImageProcessingRepresentation(BaseRepresentation):
    pass


class ImageProcessingAnnotation(ImageProcessingRepresentation):
    LOADERS = {
        GTLoader.PILLOW: 'pillow_imread',
        GTLoader.OPENCV: 'opencv_imread',
        GTLoader.DICOM: 'dicom_reader',
        GTLoader.RAWPY: 'rawpy'
    }

    def __init__(self, identifier, path_to_gt, gt_loader=GTLoader.PILLOW):
        """
        Args:
            identifier: object identifier (e.g. image name).
            path_to_gt: path where gt image should be loaded from. The path is relative to data source.
            gt_loader: back-end, used to load segmentation masks.
        """

        super().__init__(identifier)
        self._image_path = path_to_gt
        self._gt_loader = self.LOADERS.get(gt_loader)
        self._value = None

    @property
    def value(self):
        if self._value is None:
            data_source = self.metadata.get('additional_data_source')
            if not data_source:
                data_source = self.metadata['data_source']
            loader = BaseReader.provide(self._gt_loader, data_source)
            gt = loader.read(self._image_path)
            return gt.astype(np.uint8) if self._gt_loader not in ['dicom_reader', 'rawpy'] else gt
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class ImageProcessingPrediction(ImageProcessingRepresentation):
    def __init__(self, identifiers, prediction):
        """
        Args:
            identifiers: object identifier (e.g. image name).
            prediction: array with shape (height, width) contained result image.
        """

        super().__init__(identifiers)
        self.value = prediction
