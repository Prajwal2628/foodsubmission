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
reverse_id_mapping = {0: 50,
 1: 387,
 2: 578,
 3: 630,
 4: 633,
 5: 727,
 6: 732,
 7: 1004,
 8: 1007,
 9: 1009,
 10: 1010,
 11: 1013,
 12: 1014,
 13: 1019,
 14: 1022,
 15: 1024,
 16: 1026,
 17: 1032,
 18: 1033,
 19: 1038,
 20: 1040,
 21: 1050,
 22: 1054,
 23: 1055,
 24: 1056,
 25: 1058,
 26: 1060,
 27: 1061,
 28: 1065,
 29: 1068,
 30: 1069,
 31: 1070,
 32: 1074,
 33: 1075,
 34: 1078,
 35: 1082,
 36: 1084,
 37: 1085,
 38: 1089,
 39: 1092,
 40: 1094,
 41: 1098,
 42: 1102,
 43: 1107,
 44: 1108,
 45: 1113,
 46: 1116,
 47: 1119,
 48: 1123,
 49: 1124,
 50: 1126,
 51: 1138,
 52: 1143,
 53: 1144,
 54: 1150,
 55: 1151,
 56: 1152,
 57: 1153,
 58: 1154,
 59: 1156,
 60: 1157,
 61: 1162,
 62: 1163,
 63: 1166,
 64: 1169,
 65: 1170,
 66: 1176,
 67: 1180,
 68: 1181,
 69: 1184,
 70: 1186,
 71: 1187,
 72: 1190,
 73: 1191,
 74: 1198,
 75: 1199,
 76: 1200,
 77: 1203,
 78: 1209,
 79: 1210,
 80: 1212,
 81: 1213,
 82: 1214,
 83: 1215,
 84: 1220,
 85: 1221,
 86: 1223,
 87: 1228,
 88: 1229,
 89: 1237,
 90: 1249,
 91: 1264,
 92: 1280,
 93: 1294,
 94: 1300,
 95: 1307,
 96: 1308,
 97: 1310,
 98: 1311,
 99: 1321,
 100: 1323,
 101: 1327,
 102: 1328,
 103: 1348,
 104: 1352,
 105: 1371,
 106: 1376,
 107: 1383,
 108: 1384,
 109: 1402,
 110: 1422,
 111: 1453,
 112: 1455,
 113: 1463,
 114: 1467,
 115: 1468,
 116: 1469,
 117: 1478,
 118: 1482,
 119: 1483,
 120: 1487,
 121: 1490,
 122: 1494,
 123: 1496,
 124: 1505,
 125: 1506,
 126: 1513,
 127: 1520,
 128: 1522,
 129: 1523,
 130: 1533,
 131: 1536,
 132: 1538,
 133: 1545,
 134: 1547,
 135: 1551,
 136: 1554,
 137: 1556,
 138: 1557,
 139: 1560,
 140: 1561,
 141: 1565,
 142: 1566,
 143: 1568,
 144: 1569,
 145: 1580,
 146: 1587,
 147: 1588,
 148: 1607,
 149: 1614,
 150: 1620,
 151: 1627,
 152: 1670,
 153: 1724,
 154: 1727,
 155: 1728,
 156: 1730,
 157: 1731,
 158: 1748,
 159: 1788,
 160: 1789,
 161: 1793,
 162: 1794,
 163: 1831,
 164: 1853,
 165: 1856,
 166: 1879,
 167: 1889,
 168: 1893,
 169: 1915,
 170: 1916,
 171: 1919,
 172: 1924,
 173: 1942,
 174: 1948,
 175: 1956,
 176: 1967,
 177: 1980,
 178: 1985,
 179: 1986,
 180: 2022,
 181: 2053,
 182: 2073,
 183: 2099,
 184: 2103,
 185: 2131,
 186: 2132,
 187: 2134,
 188: 2172,
 189: 2237,
 190: 2254,
 191: 2269,
 192: 2278,
 193: 2303,
 194: 2320,
 195: 2350,
 196: 2362,
 197: 2376,
 198: 2388,
 199: 2413,
 200: 2446,
 201: 2454,
 202: 2470,
 203: 2495,
 204: 2498,
 205: 2501,
 206: 2504,
 207: 2512,
 208: 2521,
 209: 2524,
 210: 2530,
 211: 2534,
 212: 2543,
 213: 2555,
 214: 2562,
 215: 2578,
 216: 2580,
 217: 2616,
 218: 2618,
 219: 2620,
 220: 2634,
 221: 2711,
 222: 2714,
 223: 2728,
 224: 2729,
 225: 2730,
 226: 2734,
 227: 2736,
 228: 2738,
 229: 2741,
 230: 2742,
 231: 2743,
 232: 2747,
 233: 2749,
 234: 2750,
 235: 2807,
 236: 2836,
 237: 2841,
 238: 2873,
 239: 2895,
 240: 2898,
 241: 2905,
 242: 2920,
 243: 2923,
 244: 2930,
 245: 2934,
 246: 2935,
 247: 2939,
 248: 2944,
 249: 2949,
 250: 2952,
 251: 2954,
 252: 2961,
 253: 2964,
 254: 2967,
 255: 2970,
 256: 2973,
 257: 3042,
 258: 3080,
 259: 3100,
 260: 3115,
 261: 3220,
 262: 3221,
 263: 3249,
 264: 3262,
 265: 3306,
 266: 3308,
 267: 3332,
 268: 3358,
 269: 3532,
 270: 3630,
 271: 5641,
 272: 6404}




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