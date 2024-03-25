# Given a frame returns area
# input [object name, coordinates]
def Calculate_area(object):
    area = None

    if object[0]=='traffic light':
        area = (object[3]-object[1])*(object[4]-object[2])/(0.3*0.1)

    elif object[0]=='speed sign':
        area = ((object[3]-object[1])*(object[4]-object[2])/(0.6*0.6))

    elif object[0]=='zebra crossing':
        area = ((object[3]-object[1])*(object[4]-object[2])/(2*3))

    else:
        print('other object detected') #debugging statement

    #print(area, object[0])
    return [area, object[0]] #return

########################################################################
#
# Copyright (c) 2022, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################

"""
    This sample demonstrates how to capture a live 3D point cloud   
    with the ZED SDK and display the result in an OpenGL window.    
"""

import sys
import ogl_viewer.viewer as gl
import pyzed.sl as sl
import argparse



########################################################################
#
# Copyright (c) 2022, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################

import pyzed.sl as sl
import math
import numpy as np
import sys
import math

# def calculate_distance(x1, x2, y1, y2, point_cloud):
def calculate_value(original_value, fraction, max_value):
    scaled_value = original_value * (fraction / max_value)
    result = original_value - scaled_value
    return result
def main():
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.NEURAL  # Use ULTRA depth mode
    init_params.coordinate_units = sl.UNIT.METER  # Use meter units (for depth measurements)
    # runtime_parameters = sl.RuntimeParameters()
    # runtime_parameters.sensing_mode = sl.SENSING_MODE.FILL


    # Open the camera
    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:  # Ensure the camera has opened succesfully
        print("Camera Open : " + repr(status) + ". Exit program.")
        exit()

    # Create and set RuntimeParameters after opening the camera
    runtime_parameters = sl.RuntimeParameters()


    image = sl.Mat()
    depth = sl.Mat()
    point_cloud = sl.Mat()

    # mirror_ref = sl.Transform()
    # mirror_ref.set_translation(sl.Translation(2.75, 4.0, 0))

    x1, y1 = 50, 50
    x2, y2 = 400, 350

    num_rows = 10
    num_columns = 10

    res = sl.Resolution()
    res.width = 720
    res.height = 404

    camera_model = zed.get_camera_information().camera_model
    # Create OpenGL viewer
    viewer = gl.GLViewer()
    viewer.init(1, sys.argv, camera_model, res)

    points = np.zeros((num_rows, num_columns))

    while viewer.is_available():
        # A new image is available if grab() returns SUCCESS
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # Retrieve left image
            zed.retrieve_image(image, sl.VIEW.LEFT)

            # Retrieve depth map. Depth is aligned on the left image
            zed.retrieve_measure(depth, sl.MEASURE.DEPTH)
            # Retrieve colored point cloud. Point cloud is aligned on the left image.
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)

            # print(zed.get_camera_information().camera_model)
            # Get and print distance value in mm at the center of the image
            # We measure the distance camera - object using Euclidean distance

            for i in range(num_rows):
                for j in range(num_columns):
                    x = x2 - (round(calculate_value(x2 - x1, i, num_rows)) + x1) + x1
                    y = y2 - (round(calculate_value(y2 - y1, j, num_columns)) + y1) + y1
                    # points[i, j] = point_cloud.get_value(x, y)
                    err, point_cloud_value = point_cloud.get_value(x, y)
                    # print(points)
                    if math.isfinite(point_cloud_value[2]):
                        distance = math.sqrt(point_cloud_value[0] * point_cloud_value[0] +
                                             point_cloud_value[1] * point_cloud_value[1] +
                                             point_cloud_value[2] * point_cloud_value[2])
                        points[i, j] = distance
                        print(points)

                    else:
                        print(f"ERROR: The distance can not be computed at {{{x};{y}}}")
            viewer.updateData(point_cloud)






    # Close the camera
    zed.close()


if __name__ == "__main__":
    main()
