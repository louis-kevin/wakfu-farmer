import json
import os

import cv2
import numpy as np

from src.filters.edge_filter import EdgeFilter
from src.filters.filter_controller import FilterController
from src.filters.hsv_filter import HsvFilter


class FilterApplier:
    def __init__(self, name, path, hsv=None, edge=None, from_control=True):
        self.name = name
        self.path = path
        self.hsv = hsv
        self.edge = edge
        self.from_control = from_control

    def apply(self, img):
        hsv = self.hsv
        edge = self.edge
        if self.from_control:
            hsv = None
            edge = None
        img = FilterApplier.apply_hsv_filter(img, hsv)
        img = FilterApplier.apply_edge_filter(img, edge)
        return img

    @staticmethod
    def load_filter(path, name, from_control=True):
        filter_applier = FilterApplier(name, path, hsv=HsvFilter(), edge=EdgeFilter(), from_control=from_control)
        file = path + '/' + name + '.json'
        if not os.path.exists(file):
            return filter_applier

        with open(file) as data_file:
            data_loaded = json.load(data_file)
            if 'hsv' in data_loaded:
                filter_applier.hsv = HsvFilter.from_data(data_loaded['hsv'])
            if 'edge' in data_loaded:
                filter_applier.edge = EdgeFilter.from_data(data_loaded['edge'])

            return filter_applier

    # given an image and an HSV filter, apply the filter and return the resulting image.
    # if a filter is not supplied, the control GUI trackbars will be used
    @staticmethod
    def apply_hsv_filter(original_image, hsv_filter=None):
        # convert image to HSV
        hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

        # if we haven't been given a defined filter, use the filter values from the GUI
        if not hsv_filter:
            hsv_filter = FilterController.get_hsv_filter_from_controls()

        # add/subtract saturation and value
        h, s, v = cv2.split(hsv)
        s = FilterApplier.shift_channel(s, hsv_filter.sAdd)
        s = FilterApplier.shift_channel(s, -hsv_filter.sSub)
        v = FilterApplier.shift_channel(v, hsv_filter.vAdd)
        v = FilterApplier.shift_channel(v, -hsv_filter.vSub)
        hsv = cv2.merge([h, s, v])

        # Set minimum and maximum HSV values to display
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
        # Apply the thresholds
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(hsv, hsv, mask=mask)

        # convert back to BGR for imshow() to display it properly
        img = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

        return img

    # given an image and a Canny edge filter, apply the filter and return the resulting image.
    # if a filter is not supplied, the control GUI trackbars will be used
    @staticmethod
    def apply_edge_filter(original_image, edge_filter=None):
        # if we haven't been given a defined filter, use the filter values from the GUI
        if not edge_filter:
            edge_filter = FilterController.get_edge_filter_from_controls()

        if not edge_filter.hasEdge:
            return original_image

        kernel = np.ones((edge_filter.kernelSize, edge_filter.kernelSize), np.uint8)
        eroded_image = cv2.erode(original_image, kernel, iterations=edge_filter.erodeIter)
        dilated_image = cv2.dilate(eroded_image, kernel, iterations=edge_filter.dilateIter)

        # canny edge detection
        result = cv2.Canny(dilated_image, edge_filter.canny1, edge_filter.canny2)

        # convert single channel image back to BGR
        img = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

        return img

    # apply adjustments to an HSV channel
    # https://stackoverflow.com/questions/49697363/shifting-hsv-pixel-values-in-python-using-numpy
    @staticmethod
    def shift_channel(c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c
