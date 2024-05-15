import numpy as np
import cv2
import time
import glob
from scipy.optimize import fsolve
from Steering_Controller import Controller
import matplotlib.pyplot as plt

def cut(image, pixels):
    
    
    # Cut the lower 50 pixels of the image
    height = image.shape[0]
    width = image.shape[1]
    width = 400
    cut_image = image[:, :width]
    
    return cut_image

def canny(inpImage):
    # Convert image to grayscale, apply threshold, blur & extract edges
    gray = cv2.cvtColor(inpImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(3, 3), 0)
    canny = cv2.Canny(blur, 40, 60)
    return canny

# Another edge detector
def sobel_binary(img, sobel_kernel=7, mag_thresh=(3, 255), s_thresh=(170, 255)):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    gray = hls[:, :, 1]
    s_channel = hls[:, :, 2]
    # Binary matrixes creation
    sobel_binary = np.zeros(shape=gray.shape, dtype=bool)
    s_binary = sobel_binary
    combined_binary = s_binary.astype(np.float32)
    # Sobel Transform
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = 0 
    #cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    sobel_abs = np.abs(sobelx**2 + sobely**2)
    sobel_abs = np.uint8(255 * sobel_abs / np.max(sobel_abs))
    sobel_binary[(sobel_abs > mag_thresh[0]) & (sobel_abs <= mag_thresh[1])] = 1
    # Threshold color channel
    s_binary[(s_channel >= s_thresh[0]) & (s_channel <= s_thresh[1])] = 1
    # Combine the two binary thresholds
    combined_binary[(s_binary == 1) | (sobel_binary == 1)] = 1
    combined_binary = np.uint8(255 * combined_binary / np.max(combined_binary))
    return combined_binary

# Cut parts of the image where we do not expect the road
def region_of_interest(img):
    mask = np.zeros_like(img)
    height, width = img.shape[:2]  # Get the height and width of the input image
    bottom = height
    bl = [int(width * 0.1), bottom]  # Bottom left point
    tl = [int(width * 0.45), int(height * 0.6)]  # Top left point
    tr = [int(width * 0.55), int(height * 0.6)]  # Top right point
    br = [int(width), bottom]  # Bottom right point
    points = np.array([bl, tl, tr, br], dtype=np.int32)
    cv2.fillPoly(mask, [points], 255)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def warp(img, src, dst):
    src = np.float32([src])
    dst = np.float32([dst])
    M = cv2.getPerspectiveTransform(src, dst)

    # Apply the transformation to get the bird's-eye view
    birds_eye_view = cv2.warpPerspective(img, M, (530, 600))
    return birds_eye_view

def sliding_windown(img_w):

    histogram = np.sum(img_w[int(img_w.shape[0] / 2):, :], axis=0)
    # Create an output image to draw on and visualize the result
    out_img = np.dstack((img_w, img_w, img_w)) * 255
    # Find the peak of the left and right halves of the histogram
    # These will be the starting point for the left and right lines
    midpoint = np.int32(histogram.shape[0] / 2)
    leftx_base = np.argmax(histogram[:midpoint])
    rightx_base = np.argmax(histogram[midpoint:]) + midpoint

    # Choose the number of sliding windows
    nwindows = 9
    # Set height of windows
    window_height = np.int32(img_w.shape[0] / nwindows)
    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = img_w.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
    # Current positions to be updated for each window
    leftx_current = leftx_base
    rightx_current = rightx_base
    # Set the width of the windows +/- margin
    margin = 100
    # Set minimum number of pixels found to recenter window
    minpix = 50
    # Create empty lists to receive left and right lane pixel indices
    left_lane_inds = []
    right_lane_inds = []

    # Step through the windows one by one
    for window in range(nwindows):
        # Identify window boundaries in x and y (and right and left)
        win_y_low = img_w.shape[0] - (window + 1) * window_height
        win_y_high = img_w.shape[0] - window * window_height
        win_xleft_low = leftx_current - margin
        win_xleft_high = leftx_current + margin
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin
        # Draw the windows on the visualization image
        cv2.rectangle(out_img, (win_xleft_low, win_y_low), (win_xleft_high, win_y_high), (0, 255, 0), 2)
        cv2.rectangle(out_img, (win_xright_low, win_y_low), (win_xright_high, win_y_high), (0, 255, 0), 2)
        # Identify the nonzero pixels in x and y within the window
        good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) & (
            nonzerox < win_xleft_high)).nonzero()[0]
        good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) & (
            nonzerox < win_xright_high)).nonzero()[0]
        # Append these indices to the lists
        left_lane_inds.append(good_left_inds)
        right_lane_inds.append(good_right_inds)
        # If you found > minpix pixels, recenter next window on their mean position
        if len(good_left_inds) > minpix:
            leftx_current = np.int32(np.mean(nonzerox[good_left_inds]))
        if len(good_right_inds) > minpix:
            rightx_current = np.int32(np.mean(nonzerox[good_right_inds]))

    # Concatenate the arrays of indices
    left_lane_inds = np.concatenate(left_lane_inds)
    right_lane_inds = np.concatenate(right_lane_inds)

    # Check if lane pixels were found
    if len(left_lane_inds) == 0 or len(right_lane_inds) == 0:
        raise ValueError("Failed to detect lane lines")

    # Extract left and right line pixel positions
    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds]
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]

    # Fit a third order polynomial to each
    left_fit = np.polyfit(lefty, leftx, 3)
    right_fit = np.polyfit(righty, rightx, 3)

    return left_fit, right_fit

def fit_from_lines(left_fit, right_fit, img_w):
    nonzero = img_w.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
    margin = 100
    left_lane_inds = ((nonzerox > (left_fit[0] * (nonzeroy ** 3) + left_fit[1] * (nonzeroy**2) + left_fit[2] * nonzeroy + left_fit[3] - margin)) & (
    nonzerox < (left_fit[0] * (nonzeroy ** 3) + left_fit[1] * (nonzeroy**2) + left_fit[2] * nonzeroy + left_fit[3] - margin)))
    right_lane_inds = (
    (nonzerox > (right_fit[0] * (nonzeroy ** 3) + right_fit[1] * (nonzeroy**2) + right_fit[2] * nonzeroy + right_fit[3] - margin)) & (
    nonzerox < (right_fit[0] * (nonzeroy ** 3) + right_fit[1] * (nonzeroy**2) + right_fit[2] * nonzeroy + right_fit[3] - margin)))

    # Again, extract left and right line pixel positions
    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds]
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]
    # Fit a third order polynomial to each
    left_fit = np.polyfit(lefty, leftx, 3)
    right_fit = np.polyfit(righty, rightx, 3)
    

    return left_fit, right_fit

def draw_lines(img_w, left_fit, right_fit, center_fit):
    # Create an image to draw the lines on
    warp_zero = np.zeros_like(img_w).astype(np.uint8)
    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

    ploty = np.linspace(0, img_w.shape[0] - 1, img_w.shape[0])
    left_fitx = left_fit[0] * ploty ** 3 + left_fit[1] * ploty ** 2 + left_fit[2] * ploty + left_fit[3]
    right_fitx = right_fit[0] * ploty ** 3 + right_fit[1] * ploty ** 2 + right_fit[2] * ploty + right_fit[3]
    center_fitx = center_fit[0] * ploty ** 3 + center_fit[1] * ploty ** 2 + center_fit[2] * ploty + center_fit[3]

    # Ensure left_fitx and right_fitx have the same length
    min_len = min(len(left_fitx), len(right_fitx), len(center_fitx))
    left_fitx = left_fitx[:min_len]
    right_fitx = right_fitx[:min_len]
    center_fitx = center_fitx[:min_len]

    # Create arrays of points for left and right lines
    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_center = np.array([np.transpose(np.vstack([center_fitx, ploty]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    
    # Concatenate the arrays along the second dimension
    pts = np.hstack((pts_left[0], pts_right[0]))

    # Convert the points to int32
    pts = pts.reshape((-1, 1, 2)).astype(np.int32)

    # Draw the lane onto the warped blank image
    cv2.fillPoly(color_warp, [pts], (0, 255, 0))

    # Plot the lines on the bird's eye view image
    cv2.polylines(img_w, np.int_([pts_right]), isClosed=False, color=(255, 0, 0), thickness=5)
    cv2.polylines(img_w, np.int_([pts_left]), isClosed=False, color=(255, 255, 0), thickness=5)
    cv2.polylines(img_w, np.int_([pts_center]), isClosed=False, color=(255, 0, 0), thickness=5)

    return img_w

def draw_lines_extended(original_img, left_fit, right_fit, center_fit, scale_factor):
    # Get the dimensions of the original image
    height, width = original_img.shape[:2]

    # Define the size of the extended image
    new_height = height + scale_factor
    new_width = width

    # Create a larger canvas filled with black
    larger_canvas = np.zeros((new_height, new_width), dtype=np.uint8)


    # Define y-range for extrapolation based on the original image height
    ploty = np.linspace(0, new_height - 1, new_height)

    # Extrapolate lines along the height direction
    left_fitx = left_fit[0] * ploty ** 3 + left_fit[1] * ploty ** 2 + left_fit[2] * ploty + left_fit[3]
    right_fitx = right_fit[0] * ploty ** 3 + right_fit[1] * ploty ** 2 + right_fit[2] * ploty + right_fit[3]
    center_fitx = center_fit[0] * ploty ** 3 + center_fit[1] * ploty ** 2 + center_fit[2] * ploty + center_fit[3]

    # Ensure left_fitx, right_fitx, and center_fitx have the same length
    min_len = min(len(left_fitx), len(right_fitx), len(center_fitx))
    left_fitx = left_fitx[:min_len]
    right_fitx = right_fitx[:min_len]
    center_fitx = center_fitx[:min_len]

    # Create arrays of points for left, right, and center lines
    pts_left = np.array([np.vstack([left_fitx, ploty]).T])
    pts_right = np.array([np.vstack([right_fitx, ploty]).T])
    pts_center = np.array([np.vstack([center_fitx, ploty]).T])

    # Draw the lines onto the larger canvas
    cv2.polylines(larger_canvas, np.int32([pts_left]), isClosed=False, color=125, thickness=5)
    cv2.polylines(larger_canvas, np.int32([pts_right]), isClosed=False, color=125, thickness=5)
    cv2.polylines(larger_canvas, np.int32([pts_center]), isClosed=False, color=125, thickness=5)

    # Copy the original image onto the larger canvas
    larger_canvas[:height, :] = original_img

    return larger_canvas


def find_center_point(left_fit, right_fit, img_height):
    # Calculate x values for left and right lines at the middle of the image
    midpoint_y = 720
    left_midpoint_x = left_fit[0] * midpoint_y ** 3 + left_fit[1] * midpoint_y ** 2 + left_fit[2] * midpoint_y + left_fit[3]
    right_midpoint_x = right_fit[0] * midpoint_y ** 3 + right_fit[1] * midpoint_y ** 2 + right_fit[2] * midpoint_y + right_fit[3]

    # Calculate the average of the midpoint x coordinates
    center_x = (left_midpoint_x + right_midpoint_x) // 2

    # Return the center point coordinates
    return center_x, midpoint_y

def distance(point, center_fit):
    # Define the circle equation parameters
    ya, xa = point

    intersection_x = center_fit[0] * 720**3 + center_fit[1] * 720**2 + center_fit[2] * 720 + center_fit[3]
    #print('inter',intersection_x)
    #print('intersection_x =', intersection_x )
    
    # Calculate the distance between the given point and the intersection point
    distance = (intersection_x - 530/2)
    
    
    return distance

# Pipeline
angle_values = []
#time_stamps = []
font = cv2.FONT_HERSHEY_SIMPLEX
smoothed_angle = 0
MOV_AVG_LENGTH = 4
mov_avg_left = []
mov_avg_right = []

#cap = cv2.VideoCapture("C:\\Users\\Jandl\\Downloads\\project_video (1).mp4")
cap = cv2.VideoCapture("C:\\Users\\Jandl\\Downloads\\HD1080_Standing_Lines.avi") # front camera capture

#dt = time.time()


# PID settings
#dt = 0
#start_time = time.time()

c = Controller()

while(True):
    #current_time = time.time()
    car_angle = 90 # Import current angle from car
    car_angle = car_angle - 90
    car_angle = np.deg2rad(car_angle)


    #dt = float(round(current_time - start_time, 2))
    
    #start_time = current_time  # Update start time for the next iteration

    ret, frame = cap.read()
    if ret is True: 
        image = cv2.resize(frame,(800,600),interpolation=cv2.INTER_AREA)
    else:
        print("Getting no frames")
        break
    #-------------------------Color & Gradient Threshold------------------------ 
    image = cut(image, 50)
    image = cv2.resize(image,(800,600),interpolation=cv2.INTER_AREA)
    height = image.shape[0]
    width = image.shape[1]
    edges1 = canny(image)
    edges2=sobel_binary(image)
    
    A = cv2.addWeighted(edges2,0.6,edges1,0.4,0)
    BW1 = cv2.bitwise_and(A, edges2)
    #img_b = region_of_interest(BW1)
    img_b = BW1
    # source and destiantion points for the wrap
    src = np.array([[253, 272],[573, 272],[1233, 540], [-407, 540]])
    dst = np.float32([[0, 0], [530, 0], [530, 600], [0, 600]])

    
    bev = warp(img_b, src, dst) # Changes to birds eye view
    bevo = warp(image, src, dst)
    #---------------------------------- Line detection ---------------------------------------
    mov_length = 4
    
    height = bev.shape[0]
    width = bev.shape[1]

    try:
        # If lines are detected close to where expected
        left_fit, right_fit = fit_from_lines(bev, left_fit, right_fit, bev)
        if len(mov_avg_left) < mov_length:
            mov_avg_left.append(left_fit)
            mov_avg_right.append(right_fit)
        else:
            mov_avg_left.pop(0)
            mov_avg_right.pop(0)
            mov_avg_left.append(left_fit)
            mov_avg_right.append(right_fit)
        
    except Exception:
        # If line are not detected close to the previous instance
        left_fit, right_fit = sliding_windown(bev)
        if len(mov_avg_left) == 0:
            mov_avg_left = [left_fit]
            mov_avg_right = [right_fit]
        elif len(mov_avg_left) < mov_length:
            mov_avg_left.append(left_fit)
            mov_avg_right.append(right_fit)
        else:
            mov_avg_left.pop(0)
            mov_avg_right.pop(0)
            mov_avg_left.append(left_fit)
            mov_avg_right.append(right_fit)

    # Calculate the moving average of the last 3 fits for both left and right lanes
    left_fit = np.mean(mov_avg_left, axis=0)
    right_fit = np.mean(mov_avg_right, axis=0)

    #print(mov_avg_left)
    center_fit = (left_fit + right_fit) / 2

    distance_ahead = 3
    pom = (distance_ahead-2)*height/10
    alpha = np.arctan(2*center_fit[1]*(height-pom)+3*((height-pom)**2 *center_fit[0]) + center_fit[2]) # Angle between road and car
     
    # Draw the lines
    final = draw_lines(bev, left_fit, right_fit, center_fit) 
    result = draw_lines_extended(bev, left_fit, right_fit, center_fit, 120)
    height = result.shape[0]
    width = result.shape[1]
    #print(width, height)
    

    # Inside your main loop after detecting lines and drawing them
    center_x, center_y = find_center_point(left_fit, right_fit, 600)

    dist = distance([width/2,720], center_fit) # Distance in pixels [x, y] is position of car

    # Plot the center point on the bird's eye view image
    cv2.circle(result, (int(center_x), int(center_y)), 10, (255, 255, 0), -1)  # Draw center point as a circle
    cv2.circle(result, (265, 720), 15, (150, 100, 0), -1)  # Draw center point as a circle
    point = int(center_fit[0] * height**3 + center_fit[1] * height**2 + center_fit[2] * height + center_fit[3])
    point2 = int(center_fit[0] * pom**3 + center_fit[1] * pom**2 + center_fit[2]  * pom + center_fit[3])
    #print(point)
    cv2.circle(result, (point, 720), 10, (255, 255, 255), -1)  # Draw center point as a circle
    cv2.circle(result, (point2, 530), 5, (255, 255, 0), -1)  # Draw center point as a circle
 

    result = cv2.resize(result, (530,600))
    
    # Info for final
    lateral_error = dist/60
    polynomial = center_fit
    angle = alpha - car_angle
    

    # Controller usage
    ff = c.feedforward(polynomial)
    fb = c.feedback(angle, lateral_error)
    angle = ff + fb
    angle = np.rad2deg(angle)
    angle = angle  - car_angle
    angle = int(angle  + 90) #conversion this will be returned
    print(angle)
    
    #ff = np.rad2deg(ff)
    #fb = np.rad2deg(fb)

    # Show the updated bird's eye view image
    #cv2.imshow('final', final)
    #---------------------------------- Display ---------------------------------------
    #cv2.imshow('Front_view', image)
    #cv2.imshow('added', A)
    #cv2.imshow('BW1', BW1)
    #cv2.imshow('ROIb', img_b)
    #cv2.imshow('bev', bev)
    #angle_values.append(angle)
    #time_stamps.append(current_time)
    #cv2.imshow('result', result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break