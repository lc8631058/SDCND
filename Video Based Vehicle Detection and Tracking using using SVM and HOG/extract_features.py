import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.feature import hog

def draw_boxes(img, bboxes, color=(0, 0, 255), thickness=6):
    # Add bounding boxes in this format, these are just example:
    # bboxes = [((100, 100), (200, 200)), ((300, 300), (400, 400))]
    # make a copy of the image 
    copy = np.copy(img)
    # draw each bounding box on your copy image
    for ii in range(len(bboxes)):
        cv2.rectangle(copy, bboxes[ii][0], bboxes[ii][1], color, thickness)
    # return the image copy with boxes drawn 
    return copy

def color_hist(img, nbins=32, bins_range=(0, 256)):
    # Computer the histogram of the RGB channels separately
    r_hist = np.histogram(img[:, :, 0], bins=nbins, range=bins_range)
    g_hist = np.histogram(img[:, :, 1], bins=nbins, range=bins_range)
    b_hist = np.histogram(img[:, :, 2], bins=nbins, range=bins_range)
    # Generating bin centers
    bin_edges = r_hist[1]
        # 将数组错开相加除以2
    bin_centers = (bin_edges[0:len(bin_edges)-1] + bin_edges[1:])/2
    # Concatenate the histograms into a single vector
    hist_features = np.concatenate((r_hist[0], g_hist[0], b_hist[0]))
    # Returen the individual histograms, bin_centers and feature vector 
    return bin_centers, hist_features

def bin_spatial(img, size=(32, 32)):

    features = np.resize(img, size).ravel()
    # Return the feature vector
    return features

# def data_look(car_list, notcar_list):
#     data_dict = {}
#     # Define a key in data_dict "n_cars" and store the number of car images
#     data_dict["n_cars"] = len(car_list)
#     # Define a key "n_notcars" and store the number of notcar images
#     data_dict["n_notcars"] = len(notcar_list)
#     # Read in a test image, either car or notcar
#     img = mpimg.imread(car_list[0])
#     # Define a key "image_shape" and store the test image shape 3-tuple
#     data_dict["image_shape"] = img.shape
#     # Define a key "data_type" and store the data type of the test image.
#     data_dict["data_type"] = img.dtype
#     # Return data_dict
#     return data_dict

def get_hog_features(img, orient, pix_per_cell, cell_per_block, 
                     vis=True, feature_vec=True):
    # Define a function to return HOG features and visualization
    # Call with two outputs if vis==True
    if vis == True:
        features, hog_image = hog(img, orientations=orient, 
                                  pixels_per_cell=(pix_per_cell, pix_per_cell),
                                  cells_per_block=(cell_per_block, cell_per_block),
                                  block_norm= 'L2-Hys',
                                  transform_sqrt=False, 
                                  visualise=vis, feature_vector=feature_vec)
        return features, hog_image
    # Otherwise call with one output
    else:      
        features = hog(img, orientations=orient, 
                       pixels_per_cell=(pix_per_cell, pix_per_cell),
                       cells_per_block=(cell_per_block, cell_per_block),
                       block_norm= 'L2-Hys',
                       transform_sqrt=False, 
                       visualise=vis, feature_vector=feature_vec)
        return features

# def extract_features(imgs, cspace='RGB', spatial_size=(32, 32),
#                         hist_bins=32, hist_range=(0, 256)):
#     # Define a function to extract features from a list of images
#     # Have this function call bin_spatial() and color_hist()
#     # Create a list to append feature vectors to
#     features = []
#     # Iterate through the list of images
#     for img_path in imgs:
#         # Read in each one by one
#         img = mpimg.imread(img_path)
#         # apply color conversion if other than 'RGB'
#         if cspace != 'RGB':
#             if cspace =='HSV':
#                 feature_image = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
#             elif cspace =='LUV':
#                 feature_image = cv2.cvtColor(img, cv2.COLOR_RGB2LUV)
#             elif cspace =='HLS':
#                 feature_image = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
#             elif cspace =='YUV':
#                 feature_image = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
#             elif cspace =='YCrCb':
#                 feature_image = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
#         else: 
#             feature_image = np.copy(img)
#         # Apply bin_spatial() to get spatial color features
#         spatial_features = bin_spatial(feature_image, size=spatial_size)
#         # Apply color_hist() to get color histogram features
#         bin_centers, hist_features = color_hist(feature_image, nbins=hist_bins, bins_range=hist_range)
#         # Append the new feature vector to the features list
#         features.append(np.concatenate((spatial_features, hist_features)))
#     # Return list of feature vectors
#     return features

# def slide_window(img, x_start_stop=[None, None], y_start_stop=[None, None], 
#                     xy_window=(64, 64), xy_overlap=(0.5, 0.5)):
#     imshape = img.shape
#     # If x and/or y start/stop positions not defined, set to image size
#     if x_start_stop[0] == None:
#         x_start_stop[0] = 0
#     if x_start_stop[1] == None:
#         x_start_stop[1] = imshape[1]
#     if y_start_stop[0] == None:
#         y_start_stop[0] = 0
#     if y_start_stop[1] == None:
#         y_start_stop[1] = imshape[0]
#     # Compute the span of the region to be searched
#     span_x = x_start_stop[1] - x_start_stop[0]   
#     span_y = y_start_stop[1] - y_start_stop[0]   
#     # Compute the number of pixels per step in x/y
#     pixs_per_step_x = np.int(xy_window[0] * (1-xy_overlap[0]))
#     pixs_per_step_y = np.int(xy_window[1] * (1-xy_overlap[1]))
#     # Compute the number of windows in x/y
#         # overlapped partition
#     buffer_x = np.int(xy_window[0] * xy_overlap[0])
#     buffer_y = np.int(xy_window[1] * xy_overlap[1])
#     windows_num_x = np.int(span_x - buffer_x)//pixs_per_step_x
#     windows_num_y = np.int(span_y - buffer_y)//pixs_per_step_y
#     # Initialize a list to append window positions to
#     window_list = []
#     # Loop through finding x and y window positions
#     #     Note: you could vectorize this step, but in practice
#     #     you'll be considering windows one by one with your
#     #     classifier, so looping makes sense
#     for x in range(windows_num_x):
#         for y in range(windows_num_y):
#             # Calculate each window position
#             start_x = x*pixs_per_step_x + x_start_stop[0]
#             end_x = start_x + xy_window[0]
#             start_y = y*pixs_per_step_y + y_start_stop[0]
#             end_y = start_y + xy_window[1]
#             # Append window position to list
#             window_list.append(((start_x, start_y), (end_x, end_y)))
#     # Return the list of windows
#     return window_list

def extract_single_img_features(img, color_space='RGB', spatial_size=(32, 32),
                                hist_bins=32, hist_range=(0,256), orient=9, pix_per_cell=8,
                                cell_per_block=2, hog_channel=0, spatial_feature=True,
                                hist_feature=True, hog_feature=True):
    #1) Define an empty list to receive features
    img_features = []
    #2) Apply color conversion if other than 'RGB'
    if color_space != 'RGB':
        if color_space == 'HSV':
            feature_image = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        elif color_space == 'LUV':
            feature_image = cv2.cvtColor(img, cv2.COLOR_RGB2LUV)
        elif color_space == 'HLS':
            feature_image = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
        elif color_space == 'YUV':
            feature_image = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
        elif color_space == 'YCrCb':
            feature_image = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
    else: 
        feature_image = np.copy(img)      
    #3) Compute spatial features if flag is set to True
    if spatial_feature:
        spatial_features = bin_spatial(feature_image, size=spatial_size)
        #4) Append features to list
        img_features.append(spatial_features)
    #5) Compute histogram features if flag is True
    if hist_feature:
        bin_centers, hist_features = color_hist(feature_image, nbins=hist_bins, bins_range=hist_range)
        #6) Append features to list
        img_features.append(hist_features)
    #7) Compute HOG features if flag is set
    if hog_feature:
        if hog_channel == 'ALL':
            hog_features = []
            for channel in range(feature_image.shape[2]):
                hog_features.extend(get_hog_features(feature_image[:,:,channel], orient, pix_per_cell, cell_per_block, 
                                 vis=False, feature_vec=True))
        else:
            hog_features = get_hog_features(feature_image[:,:,hog_channel], orient, pix_per_cell, cell_per_block, 
                                 vis=False, feature_vec=True)
        #8) Append features to list
        img_features.append(hog_features)

    return np.concatenate(img_features)

# def search_windows(img, windows, clf, scaler, )
def convert_color(img, conv='RGB2YCrCb'):
    if conv == 'RGB2YCrCb':
        return cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
    if conv == 'RGB2HSV':
        return cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    if conv == 'RGB2LUV':
        return cv2.cvtColor(img, cv2.COLOR_RGB2LUV)
    if conv == 'RGB2HLS':
        return cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    if conv == 'RGB2YUV':
        return cv2.cvtColor(img, cv2.COLOR_RGB2YUV)

def add_heat(heatmap, bbox_list):
    # Iterate through list of bboxes
    heat = np.copy(heatmap)
    for box in bbox_list:
        # Add += 1 for all pixels inside each bbox
        # Assuming each "box" takes the form ((x1, y1), (x2, y2))
        heat[box[0][1]:box[1][1], box[0][0]:box[1][0]] += 1

    # Return updated heatmap
    return heat

def apply_threshold(heatmap, threshold=2):
    # Zero out pixels below the threshold
    thresholded_map = np.copy(heatmap)
    thresholded_map[thresholded_map <= threshold] = 0
    # Return thresholded map
    return thresholded_map

def find_cars(img, ystart, ystop, scale, predictor, X_scaler, conv='RGB2HSV', orient=9, 
              pix_per_cell=8, cell_per_block=2, spatial_size=(32,32), hist_bins=32, hist_range=(0,256), window=64, 
              spatial_feature=True, hist_feature=True, hog_feature=True):
    '''
    ystart, ystop: start and stop positions in vertical axis
    scale: adjust the size of searching windows
    '''
    # a single function that can extract features using hog sub-sampling and make predictions
    img = img.astype(np.float32)/255

    img_tosearch = img[ystart:ystop,:,:]
    ctrans_tosearch = convert_color(img_tosearch, conv=conv)

    if scale != 1:
        # 若scale大于1，ctrans_tosearch会比原图小，在小图里搜索相当于window变大了
        # 若scale小于1，等于在大图上搜索，window变小了
        # 在最后一部画图时，给检测出的的坐标乘以scale，
        # 就相当于坐标位置在缩小或放大前的原图中没有变化过，
        # 只需要加上y轴的迁移即可
        imshape = ctrans_tosearch.shape
        ctrans_tosearch = cv2.resize(ctrans_tosearch, (np.int(imshape[1]/scale), np.int(imshape[0]/scale)))

    ch1 = ctrans_tosearch[:,:,0]
    ch2 = ctrans_tosearch[:,:,1]
    ch3 = ctrans_tosearch[:,:,2]

    # Define blocks and steps
    # 因为一个轴里面包含的blocks，所涉及的step为1个cell，所以一个轴有
    # 几个cells基本就能确定有几个blcoks
    nxblocks = (ch1.shape[1] // pix_per_cell) - cell_per_block + 1
    nyblocks = (ch1.shape[0] // pix_per_cell) - cell_per_block + 1 
    nfeatures_per_block = orient*cell_per_block**2
    
    # number of blocks per window
    nblocks_per_window = (window // pix_per_cell) - cell_per_block + 1
    cells_per_step = 2 # how many cells to step
    nx_steps = (nxblocks - nblocks_per_window) // cells_per_step + 1
    ny_steps = (nyblocks - nblocks_per_window) // cells_per_step + 1

    # Compute individual channel HOG features for the entire image
    # feature_vec = False means output the features without flatten
    # Its shape should be (n_blocks_row, n_blocks_col, n_cells_row, n_cells_col, n_orient) 
    hog1 = get_hog_features(ch1, orient, pix_per_cell, cell_per_block, 
                            vis=False, feature_vec=False)
    hog2 = get_hog_features(ch2, orient, pix_per_cell, cell_per_block, 
                            vis=False, feature_vec=False)
    hog3 = get_hog_features(ch3, orient, pix_per_cell, cell_per_block, 
                            vis=False, feature_vec=False)
    bbox_list = []
    for xb in range(nx_steps):
        for yb in range(ny_steps):
            # all_features = []
            # 一个step有多少cells就代表跳过了多少个重叠的blocks
            ypos = yb*cells_per_step
            xpos = xb*cells_per_step
            # Extract HOG for this patch
            hog_patch_ch1 = hog1[ypos:ypos+nblocks_per_window, xpos:xpos+nblocks_per_window].ravel()
            hog_patch_ch2 = hog2[ypos:ypos+nblocks_per_window, xpos:xpos+nblocks_per_window].ravel()
            hog_patch_ch3 = hog3[ypos:ypos+nblocks_per_window, xpos:xpos+nblocks_per_window].ravel()
            hog_features = np.hstack((hog_patch_ch1, hog_patch_ch2, hog_patch_ch3))
            # all_features.append(hog_features)
            # 左上角的坐标 left-top
            xleft = xpos*pix_per_cell
            ytop = ypos*pix_per_cell

            # Extract the image patch 提取每一块以提取其他features
            subimg = cv2.resize((ctrans_tosearch[ytop:ytop+window, xleft:xleft+window]), (64, 64))
            
            # Get color features
            
            spatial_features = bin_spatial(subimg, size=spatial_size)
            # all_features.append(spatial_features)
            # if hist_feature:
            bin_centers, hist_features = color_hist(subimg, nbins=hist_bins, bins_range=hist_range)
            # all_features.append(hist_features)

            # Scale features and make a prediction
            all_features = np.reshape(np.hstack((spatial_features, hist_features, hog_features)).ravel(), [1, -1])
            # all_features = np.reshape(np.concatenate(all_features), [1, -1])
            scaled_features = X_scaler.transform(all_features)

            pred = predictor.predict(scaled_features)

            if np.int(pred) == 1:
                xbox_left = np.int(xleft*scale)
                ybox_top = np.int(ytop*scale)
                scaled_win = np.int(window*scale)
                box = ((xbox_left, ybox_top+ystart),(xbox_left+scaled_win, ybox_top+scaled_win+ystart))
                bbox_list.append(box)
                # cv2.rectangle(draw_img, box[0], box[1], (0,0,255), 6)
                # heatmap[box[0][1]:box[1][1], box[0][0]:box[1][0]] += 1

    return bbox_list

def draw_labeled_bboxes(img, labels):
    # After find cars, use this function to draw labeled boxes to image
    # Iterate through all detected cars
    draw_img = np.copy(img)
    colors = [(0,0,256), (256,0,0), (256,256,256), (256,0,256), (0,256,0), (256,256,0), (0,256,256)]
    for car_number in range(1, labels[1]+1):
        # Find pixels with each car_number label value
        nonzero = (labels[0] == car_number).nonzero()
        # Identify x and y values of those pixels
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        # Define a bounding box based on min/max x and y
        bbox = ((np.min(nonzerox), np.min(nonzeroy)), (np.max(nonzerox), np.max(nonzeroy)))
        # Draw the box on the image
        cv2.rectangle(draw_img, bbox[0], bbox[1], colors[(car_number-1)%7], 6)
    # Return the image
    return draw_img


