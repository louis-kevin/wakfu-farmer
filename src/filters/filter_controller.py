import io
import json
import os

import cv2
import numpy as np

from src.filters.edge_filter import EdgeFilter
from src.filters.hsv_filter import HsvFilter


class FilterController:
    TRACKBAR_WINDOW = "Trackbars"

    @staticmethod
    def save(path, name):
        hsv = FilterController.get_hsv_filter_from_controls()
        edge = FilterController.get_edge_filter_from_controls()
        data = {'hsv': hsv.to_data(), 'edge': edge.to_data()}
        with io.open(path + '/' + name + '.json', 'w', encoding='utf8') as outfile:
            json_str = json.dumps(data,
                                  indent=4, sort_keys=True,
                                  separators=(',', ': '), ensure_ascii=False)
            outfile.write(json_str)
        print('Filter Saved')

    # create gui window with controls for adjusting arguments in real-time
    @staticmethod
    def init_control_gui(filter_data=None):
        hsv = HsvFilter()
        edge = EdgeFilter()

        if filter_data is not None:
            hsv = filter_data.hsv
            edge = filter_data.edge

        cv2.namedWindow(FilterController.TRACKBAR_WINDOW, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(FilterController.TRACKBAR_WINDOW, 350, 70)

        # required callback. we'll be using getTrackbarPos() to do lookups
        # instead of using the callback.
        def nothing(position):
            pass

        # create trackbars for bracketing.
        # OpenCV scale for HSV is H: 0-179, S: 0-255, V: 0-255
        cv2.createTrackbar('HMin', FilterController.TRACKBAR_WINDOW, 0, 179, nothing)
        cv2.createTrackbar('HMax', FilterController.TRACKBAR_WINDOW, 0, 179, nothing)
        cv2.createTrackbar('SMin', FilterController.TRACKBAR_WINDOW, 0, 255, nothing)
        cv2.createTrackbar('SMax', FilterController.TRACKBAR_WINDOW, 0, 255, nothing)
        cv2.createTrackbar('VMin', FilterController.TRACKBAR_WINDOW, 0, 255, nothing)
        cv2.createTrackbar('VMax', FilterController.TRACKBAR_WINDOW, 0, 255, nothing)
        # Set default value for Max HSV trackbars
        cv2.setTrackbarPos('HMax', FilterController.TRACKBAR_WINDOW, hsv.hMax)
        cv2.setTrackbarPos('SMax', FilterController.TRACKBAR_WINDOW, hsv.sMax)
        cv2.setTrackbarPos('VMax', FilterController.TRACKBAR_WINDOW, hsv.vMax)
        cv2.setTrackbarPos('HMin', FilterController.TRACKBAR_WINDOW, hsv.hMin)
        cv2.setTrackbarPos('SMin', FilterController.TRACKBAR_WINDOW, hsv.sMin)
        cv2.setTrackbarPos('VMin', FilterController.TRACKBAR_WINDOW, hsv.vMin)

        # trackbars for increasing/decreasing saturation and value
        cv2.createTrackbar('SAdd', FilterController.TRACKBAR_WINDOW, 0, 255, nothing)
        cv2.createTrackbar('SSub', FilterController.TRACKBAR_WINDOW, 0, 255, nothing)
        cv2.createTrackbar('VAdd', FilterController.TRACKBAR_WINDOW, 0, 255, nothing)
        cv2.createTrackbar('VSub', FilterController.TRACKBAR_WINDOW, 0, 255, nothing)

        cv2.setTrackbarPos('SAdd', FilterController.TRACKBAR_WINDOW, hsv.sAdd)
        cv2.setTrackbarPos('SSub', FilterController.TRACKBAR_WINDOW, hsv.sSub)
        cv2.setTrackbarPos('VAdd', FilterController.TRACKBAR_WINDOW, hsv.vAdd)
        cv2.setTrackbarPos('VSub', FilterController.TRACKBAR_WINDOW, hsv.vSub)

        # trackbars for edge creation
        cv2.createTrackbar('KernelSize', FilterController.TRACKBAR_WINDOW, 1, 30, nothing)
        cv2.createTrackbar('ErodeIter', FilterController.TRACKBAR_WINDOW, 1, 5, nothing)
        cv2.createTrackbar('DilateIter', FilterController.TRACKBAR_WINDOW, 1, 5, nothing)
        cv2.createTrackbar('Canny1', FilterController.TRACKBAR_WINDOW, 0, 200, nothing)
        cv2.createTrackbar('Canny2', FilterController.TRACKBAR_WINDOW, 0, 500, nothing)
        cv2.createTrackbar('HasEdge', FilterController.TRACKBAR_WINDOW, 0, 1, nothing)
        # Set default value for Canny trackbars
        cv2.setTrackbarPos('KernelSize', FilterController.TRACKBAR_WINDOW, edge.kernelSize)
        cv2.setTrackbarPos('Canny1', FilterController.TRACKBAR_WINDOW, edge.canny1)
        cv2.setTrackbarPos('Canny2', FilterController.TRACKBAR_WINDOW, edge.canny2)
        cv2.setTrackbarPos('ErodeIter', FilterController.TRACKBAR_WINDOW, edge.erodeIter)
        cv2.setTrackbarPos('DilateIter', FilterController.TRACKBAR_WINDOW, edge.dilateIter)
        cv2.setTrackbarPos('HasEdge', FilterController.TRACKBAR_WINDOW, 1 if edge.hasEdge else 0)

    # returns an HSV filter object based on the control GUI values
    @staticmethod
    def get_hsv_filter_from_controls():
        # Get current positions of all trackbars
        hsv_filter = HsvFilter()
        hsv_filter.hMin = cv2.getTrackbarPos('HMin', FilterController.TRACKBAR_WINDOW)
        hsv_filter.sMin = cv2.getTrackbarPos('SMin', FilterController.TRACKBAR_WINDOW)
        hsv_filter.vMin = cv2.getTrackbarPos('VMin', FilterController.TRACKBAR_WINDOW)
        hsv_filter.hMax = cv2.getTrackbarPos('HMax', FilterController.TRACKBAR_WINDOW)
        hsv_filter.sMax = cv2.getTrackbarPos('SMax', FilterController.TRACKBAR_WINDOW)
        hsv_filter.vMax = cv2.getTrackbarPos('VMax', FilterController.TRACKBAR_WINDOW)
        hsv_filter.sAdd = cv2.getTrackbarPos('SAdd', FilterController.TRACKBAR_WINDOW)
        hsv_filter.sSub = cv2.getTrackbarPos('SSub', FilterController.TRACKBAR_WINDOW)
        hsv_filter.vAdd = cv2.getTrackbarPos('VAdd', FilterController.TRACKBAR_WINDOW)
        hsv_filter.vSub = cv2.getTrackbarPos('VSub', FilterController.TRACKBAR_WINDOW)
        return hsv_filter

        # returns a Canny edge filter object based on the control GUI values

    @staticmethod
    def get_edge_filter_from_controls():
        # Get current positions of all trackbars
        edge_filter = EdgeFilter()
        edge_filter.kernelSize = cv2.getTrackbarPos('KernelSize', FilterController.TRACKBAR_WINDOW)
        edge_filter.erodeIter = cv2.getTrackbarPos('ErodeIter', FilterController.TRACKBAR_WINDOW)
        edge_filter.dilateIter = cv2.getTrackbarPos('DilateIter', FilterController.TRACKBAR_WINDOW)
        edge_filter.canny1 = cv2.getTrackbarPos('Canny1', FilterController.TRACKBAR_WINDOW)
        edge_filter.canny2 = cv2.getTrackbarPos('Canny2', FilterController.TRACKBAR_WINDOW)
        edge_filter.hasEdge = True if cv2.getTrackbarPos('HasEdge', FilterController.TRACKBAR_WINDOW) == 1 else False

        return edge_filter
