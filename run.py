import random
import json
import numpy as np
import argparse
import base64
import glob
import os
import traceback
from PIL import Image
import aicrowd_helpers
import gc

import torch, torchvision
import detectron2
import cv2
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.structures import Boxes, BoxMode 
import pycocotools.mask as mask_util


"""
Expected ENVIRONMENT Variables

* AICROWD_TEST_IMAGES_PATH : abs path to  folder containing all the test images
* AICROWD_PREDICTIONS_OUTPUT_PATH : path where you are supposed to write the output predictions.json
"""
#S
# Configuration Variables

threshold = 0.4
model_path = "./model_final.pth"
cpu_device = torch.device("cpu")

with open('/home/aicrowd/reverse_id_mapping_file.json') as f:
	reverse_id_mapping = json.load(f)


def gather_input_output_path():
    test_images_path = os.getenv("AICROWD_TEST_IMAGES_PATH", False)
    assert test_images_path != False, "Please provide the path to the test images using the environment variable : AICROWD_TEST_IMAGES_PATH"

    predictions_output_path = os.getenv("AICROWD_PREDICTIONS_OUTPUT_PATH", False)
    assert predictions_output_path != False, "Please provide the output path (for writing the predictions.json) using the environment variable : AICROWD_PREDICTIONS_OUTPUT_PATH"

    return test_images_path, predictions_output_path

def instances_to_coco_json(instances, img_id):
    num_instance = len(instances)
    if num_instance == 0:
        return []

    boxes = instances.pred_boxes.tensor.numpy()
    boxes = BoxMode.convert(boxes, BoxMode.XYXY_ABS, BoxMode.XYWH_ABS)
    boxes = boxes.tolist()
    scores = instances.scores.tolist()
    classes = instances.pred_classes.tolist()

    has_mask = instances.has("pred_masks")
    if has_mask:
        rles = [
            mask_util.encode(np.array(mask[:, :, None], order="F", dtype="uint8"))[0]
            for mask in instances.pred_masks
        ]
        for rle in rles:
            rle["counts"] = rle["counts"].decode("utf-8")

    results = []
    for k in range(num_instance):
        result = {
            "image_id": img_id,
            "category_id": classes[k],
            "bbox": boxes[k],
            "score": scores[k],
        }
        if has_mask:
            result["segmentation"] = rles[k]
    
        results.append(result)
    return results


def run():
	########################################################################
	# Register Prediction Start
	########################################################################
	aicrowd_helpers.execution_start()

	########################################################################
	# Gather Input and Output paths from environment variables
	########################################################################
	test_images_path, predictions_output_path = gather_input_output_path()

	########################################################################
	# Generate Predictions
	########################################################################
	cfg = get_cfg()
	cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
	cfg.MODEL.WEIGHTS = model_path
	cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold   # set the testing threshold for this model
	cfg.MODEL.ROI_HEADS.NUM_CLASSES = 273
	#cfg.MODEL.DEVICE = "cpu"
	predictor = DefaultPredictor(cfg)
	results = []
	del cfg
	for i in os.listdir(test_images_path):
		img_path =test_images_path + "/" +str(i)
		im = cv2.imread(img_path)
		outputs = predictor(im)
		instances = outputs["instances"].to(cpu_device)
		fname = int(i.split('.')[0])
		result = instances_to_coco_json(instances,fname)
		if(len(result)!=0):
			for ele in result:
				matchId = ele['category_id']
				ele['category_id'] = reverse_id_mapping[matchId]
				results.append(ele)    
			aicrowd_helpers.execution_progress({
				"image_ids" : [fname]
			})





	# Write output
	fp = open(predictions_output_path, "w")
	fp.write(json.dumps(results))
	fp.close()
	########################################################################
	# Register Prediction Complete
	########################################################################
	aicrowd_helpers.execution_success({
	"predictions_output_path" : predictions_output_path
	})

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        error = traceback.format_exc()
        print(error)
        aicrowd_helpers.execution_error(error)
