import parse_openpose_json
import numpy as np

import prepocessing
import matplotlib.pyplot as plt
import normalising
import affine_transformation
import pose_match
import pose_comparison


json_data_path = 'data/json_data/'
images_data_path = 'data/image_data/'

json_data_path = 'data/json_data/'
images_data_path = 'data/image_data/'

model = "foto1"
input = "kleuter8"
model_json = json_data_path + model + '.json'
input_json = json_data_path + input + '_keypoints.json'

model_image = images_data_path + model + '.jpg'
input_image = images_data_path + input + '.jpg'

# model_features = parse_openpose_json.parse_JSON_single_person(model_json)
# input_features = parse_openpose_json.parse_JSON_single_person(input_json)
model_features = parse_openpose_json.parse_JSON_single_person('data/json_data/foto1.json')
input_features = parse_openpose_json.parse_JSON_single_person('data/json_data/model1.json')



match_result = pose_match.single_person(model_features, input_features, True)
model_features = parse_openpose_json.parse_JSON_single_person(model_json)
input_features = parse_openpose_json.parse_JSON_single_person(input_json)
pose_match.plot_single_person(model_features, input_features, model_image, input_image)

#plt.show()

