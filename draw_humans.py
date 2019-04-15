import numpy as np
from enum import Enum
import cv2
import parse_openpose_json
import matplotlib.pyplot as plt


def test():
    json_data_path = 'data/json_data/'
    images_data_path = 'data/image_data/'
    model = "foto1"
    input = "kleuter2"
    model_json = json_data_path + model + '.json'
    input_json = json_data_path + input + '_keypoints.json'

    model_image = images_data_path + model + '.jpg'
    input_image = images_data_path + input + '.jpg'

    model_features = parse_openpose_json.parse_JSON_multi_person(model_json)
    assert type(model_features) is list
    img = draw_humans(model_image, model_features, True)
    plt.figure()
    plt.imshow(img)#.astype(np.uint8)
    plt.show()



#class CocoPart(Enum):
class CocoPart():
    # Nose = 0
    # Neck = 1
    # RShoulder = 2
    # RElbow = 3
    # RWrist = 4
    # LShoulder = 5
    # LElbow = 6
    # LWrist = 7
    # RHip = 8
    # RKnee = 9
    # RAnkle = 10
    # LHip = 11
    # LKnee = 12
    # LAnkle = 13
    # REye = 14
    # LEye = 15
    # REar = 16
    # LEar = 17
    # Background = 18
    Nose = 0
    LEye = 1
    REye = 2
    LEar = 3
    REar = 4
    LShoulder = 5
    RShoulder = 6
    LElbow = 7
    RElbow = 8
    LWrist = 9
    RWrist = 10
    LHip = 11
    RHip = 12
    LKnee = 13
    RKnee = 14
    LAnkle = 15 
    RAnkle = 16
    #Neck = 17
    Background = 17

CocoColors = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0], [85, 255, 0], [0, 255, 0],
              [0, 255, 85], [0, 255, 170], [0, 255, 255], [0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255],
              [170, 0, 255], [255, 0, 255], [255, 0, 170]]

# CocoColors = [[1, 0, 0], [1, 0.33333, 0], [1, 0.666666, 0], [1, 1, 0], [0.666666, 1, 0], [0.33333, 1, 0], [0, 1, 0],
#               [0, 1, 0.33333], [0, 1, 0.666666], [0, 1, 1], [0, 0.666666, 1], [0, 0.33333, 1], [0, 0, 1], [0.33333, 0, 1],
#               [0.666666, 0, 1], [1, 0, 1], [1, 0, 0.666666]]

CocoPairs = [
    (0,1),(1,3),(0,2),(2,4),(0,11),(0,12),(11,13),(13,15),(12,14),(14,16),(5,6),(5,7),(7,9),(6,8),(8,10)

]   # = 19
CocoPairsRender = CocoPairs[:-2]

thickness = 4

# source: https://github.com/ildoonet/tf-pose-estimation/blob/master/src/estimator.py
def draw_humans(npimg, humans, imgcopy=False):
    #npimg = plt.imread(img_path)
    if imgcopy:
        npimg = np.copy(npimg)
    #image_h, image_w = npimg.shape[:2]
    centers = {}

    # if is type list => openpose.json van multiple persons
    if type(humans) is list:
        for human in humans:

            # draw point
            for i in range(CocoPart.Background):

                body_part = human[i]

                if body_part[0] == 0 and body_part[1] ==0:
                    continue
                print("laaaaaaaaaaaaaaaaa")
                center = (int(body_part[0]), int(body_part[1]))
                centers[i] = center
                cv2.circle(npimg, center, thickness, CocoColors[i], thickness=thickness, lineType=8, shift=0)

            #draw line
            for pair_order, pair in enumerate(CocoPairsRender):
                # if pair[0] not in human.body_parts.keys() or pair[1] not in human.body_parts.keys():
                #     continue

                # npimg = cv2.line(npimg, centers[pair[0]], centers[pair[1]], common.CocoColors[pair_order], 3)
                print("##############################")
                print(centers[pair[0]], centers[pair[1]], CocoColors[pair_order])
                cv2.line(npimg, centers[pair[0]], centers[pair[1]], CocoColors[pair_order], thickness=thickness)


        return npimg
    else: # single-person pose  (no list, but plain np.array)
        # draw point
        for i in range(CocoPart.Background):

            body_part = humans[i]

            if body_part[0] == 0 and body_part[1] == 0:
                continue

            center = (int(body_part[0]), int(body_part[1]))
            centers[i] = center

            vers = 7
            #cv2.rectangle(npimg, (center[0]-vers,center[1]-vers), (center[0]+vers,center[1]+vers) ,CocoColors[i], thickness=cv2.FILLED)
            cv2.circle(npimg, center, thickness + 1, CocoColors[i], thickness=thickness + 2, lineType=8, shift=0)

        # draw line
        for pair_order, pair in enumerate(CocoPairsRender):
            if pair[0] not in centers.keys() or pair[1] not in centers.keys():
                continue

            # npimg = cv2.line(npimg, centers[pair[0]], centers[pair[1]], common.CocoColors[pair_order], 3)
            cv2.line(npimg, centers[pair[0]], centers[pair[1]], CocoColors[pair_order], thickness = thickness-1)


    return npimg

def draw_square(npimg, features):
    centers = {}

    # draw point
    for i in range(CocoPart.Background):

        body_part = features[i]

        if body_part[0] == 0 and body_part[1] == 0:
            continue

        center = (int(body_part[0]), int(body_part[1]))
        centers[i] = center

        vers = 7

        cv2.rectangle(npimg, (center[0] - vers, center[1] - vers), (center[0] + vers, center[1] + vers),
                      color=[abs(CocoColors[i][0]-255),abs(CocoColors[i][1]-255),abs(CocoColors[i][2]-255)], thickness=3)


        # cv2.circle(npimg, center, thickness + 1, color=[255, 0, 170], thickness=thickness + 2, lineType=8, shift=0)

        # cv2.rectangle(npimg, (center[0] - vers, center[1] - vers), (center[0] + vers, center[1] + vers),
        #               color=[255, 0, 170], thickness=3)



    return npimg


