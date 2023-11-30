from vimba import *
from vidgear.gears import WriteGear
import time
import cv2
import numpy as np

class Video_Analyzer:
    def __init__(self,vimba_instance):
        self.vimba = vimba_instance
        self.video_file_loc = 'C:/Users/EngelHardBlab.MEDICINE/Desktop/experimentfolder/event_based_conditiong/video/1472/28_09_23_01_down.avi'
        self.regions = self.define_regions()
        self.thresholds = self.define_thresholds()
        # Initialize the Vimba SDK and get a camera instance

        with Vimba.get_instance() as vimba:

            cams = vimba.get_all_cameras()
            if not cams:
                raise ValueError("No cameras found")
            with cams[0] as cam:
                self.cam = cams[0]
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


    def define_regions(self):
        # Define the regions of interest (ROI) for the mouse
        regions = {
             'r1': [(500, 310), (535, 380)],#bottom right
            'r2': [(500, 110), (535, 180)],#top right
            'r3': [(455, 310), (490, 380)],#bottom left

            'r4': [(455, 110), (490, 180)],#top left

            'r5': [(590, 220), (660, 280)],#center right
            'r6': [(330, 220), (400, 280)],#center left
        }
        return regions

    def draw_regions(self, frame):
        for region_key in self.regions:
            top_left, bottom_right = self.regions[region_key]
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)  # Green rectangle
        return frame
    def define_thresholds(self):
        # Define the thresholds for each region
        thresholds = {
            'r1': 90000,
            'r2': 90000,
            'r3': 90000,
            'r4': 90000,
            'r5': 90000,
            'r6': 90000,
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
        #print("in check zones", zone_activation)
        return zone_activation

    def format_time(self,seconds):
        # Helper function to format seconds into H:M:S format
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "{:02d}:{:02d}:{:02d}".format(int(h), int(m), int(s))
    def process_single_frame(self):
        with self.vimba:
            # Now, access the camera
            with self.cam:
                frame = self.cam.get_frame().as_opencv_image()


                zone_activations = self.check_zones(frame)


                return  zone_activations

    def get_zone_activations(self):
        # Return the latest zone activations
        return self.zone_activations

#analyzer = VideoAnalyzer()
#analyzer.stream_and_process()