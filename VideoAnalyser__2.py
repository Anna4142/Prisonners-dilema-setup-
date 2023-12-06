from vimba import *
from vidgear.gears import WriteGear
import time
import cv2
import numpy as np


class Video_Analyzer:
    def __init__(self):
        self.video_file_loc = 'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/event_based_conditiong/video/1472/28_09_23_01_down.avi'
        self.regions = self.define_regions()
        self.thresholds = self.define_thresholds()

    def define_regions(self):
        # Define the regions of interest (ROI) for the mouse
        regions = {
            'r1': [(90, 610), (160, 710)],
            'r2': [(255, 610), (325, 700)],
            'r3': [(410, 610), (480, 700)],
            'r4': [(90, 270), (160, 350)],
            'r5': [(230, 260), (290, 340)],
            'r6': [(400, 260), (480, 340)],
            'experimenter_start_zone':[(x1,y1),(x2,y2)]
        }
        return regions

    def define_thresholds(self):
        # Define the thresholds for each region
        thresholds = {
            'r1': 90000,
            'r2': 90000,
            'r3': 90000,
            'r4': 90000,
            'r5': 90000,
            'r6': 90000,
            'experimenter_start_zone': 9000,#whatever it maybe
        }
        return thresholds

    def check_zones(self, frame):
        # Initialize an empty list to hold zone activation status
        zone_activation = [0] * 6  # [0, 0, 0, 0, 0, 0]

        for idx, region_key in enumerate(self.regions):
            (y1, x1), (y2, x2) = self.regions[region_key]
            sum_of_pixels = np.sum(frame[y1:y2, x1:x2])

            # If the sum of pixels exceeds the threshold, set the corresponding index to 1
            if sum_of_pixels <= self.thresholds[region_key]:
                zone_activation[idx] = 1
        print("in check zones", zone_activation)
        return zone_activation

    def stream_and_process(self):
        with Vimba.get_instance() as vimba:
            cams = vimba.get_all_cameras()
            with cams[0] as cam:
                for feature in cam.get_all_features():
                    try:
                        value = feature.get()
                    except:
                        (AttributeError, VimbaFeatureError)
                        value = None
                    cam.Height.set(1216)
                    cam.Width.set(1936)
                    cam.BinningHorizontal = 4
                    cam.BinningVertical = 4
                    cam.AcquisitionFrameRateEnable.set("True")

                    formats = cam.get_pixel_formats()
                    print(f"Feature name: {feature.get_name()}")
                    print(f"Display name: {feature.get_display_name()}")
                    if not value == None:
                        if not feature.get_unit() == '':
                            print(f"Unit: {feature.get_unit()}", end=' ')
                            print(f"value={value}")
                        else:
                            print(f"Not set")
                            print("--------------------------------------------")
                    opencv_formats = intersect_pixel_formats(formats, OPENCV_PIXEL_FORMATS)
                    cam.set_pixel_format(opencv_formats[0])
                    cam.AcquisitionMode = 'Continuous'
                    cam.ExposureTime.set(10000)

                while True:
                    frame = cam.get_frame().as_opencv_image()
                    frame = cv2.resize(frame, (960, 540))
                    self.zone_activations = self.check_zones(frame)
                    self.exp_zone= self.check_experimenter_zone(frame)
                    cv2.imshow('Frame', frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cam.stop_streaming()

    def check_experimenter_zone(self, frame):
        # Check the experimenter zone
        (y1, x1), (y2, x2) = self.regions['experimenter_zone']
        sum_of_pixels = np.sum(frame[y1:y2, x1:x2])

        # Return True if the sum of pixels in the experimenter zone is below the threshold
        return sum_of_pixels <= self.thresholds['experimenter_zone']
    def get_zone_activations(self):
        # Return the latest zone activations
        return self.zone_activations
    def get_exp_zone_activations(self):
        # Return the latest zone activations
        return self.exp_zone