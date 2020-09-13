# food-recognition-challenge-mmdetection-baseline
![AIcrowd-Logo](https://raw.githubusercontent.com/AIcrowd/AIcrowd/master/app/assets/images/misc/aicrowd-horizontal.png)

# Problem Statement

The goal of this challenge is to train models which can look at images of food items and detect the individual food items present in them.
We provide a novel dataset of food images collected using the MyFoodRepo project where numerous volunteer Swiss users provide images of their daily food intake. The images have been hand labelled by a group of experts to map the individual food items to an ontology of Swiss Food items.

This is an evolving dataset, where we will release more data as the dataset grows in size.

![image1](https://i.imgur.com/zS2Nbf0.png)

# Baseline
Detectron2 is an object detection/Instance segmentation library based on PyTorch, developed by Facebook, with a large Model Zoo with many customised models that can be plugged and tested. You can read more about it at: [Detectron2 github](https://github.com/facebookresearch/detectron2)

# Dataset
The Dataset can be downloaded from the main [challenge page](https://www.aicrowd.com/challenges/food-recognition-challenge) 

This will be the ideal directory structure that you can follow. The Detectron2 starter kit follows this structure as well.

```bash
|-- data/
|   |-- train/
|   |   |-- images (has all the images for training)
|   |   |__ annotation.json : Annotation of the data in MS COCO format
|   |   |__ annotation-small.json : Smaller version of the previous dataset
|   |-- val/
|   |   |-- images (has all the images for training)
|   |   |__ annotation.json : Annotation of the data in MS COCO format
|   |   |__ annotation-small.json : Smaller version of the previous dataset
|   |-- train.zip (zip that you downloaded)
|   |-- val.zip (zip that you downloaded)

```

# Submission Instructions

This challenge is a codebase submission challenge. Participants are supposed to create a repository which consists of the model, a script which has a function which can take inference, and a dockerfile which can help us in creating a container with the necessary libraries that are required to execute your code.

To submit to the challenge you'll need to ensure you've set up an appropriate repository structure, create a private git repository at https://gitlab.aicrowd.com with the contents of your submission, and push a git tag corresponding to the version of your repository you'd like to submit.

The Detectron2 starter kit notebook has all the information that you need in making a submissionn if you are using detectron2 to build your model.

## Repository Structure
We have created this sample submission repository which you can use as reference. We will be cloning this repository and make changes to it and then make a submission. (Refer to the notebook)

#### aicrowd.json
Each repository should have a aicrowd.json file with the following fields:

```
{
    "challenge_id" : "aicrowd-food-recognition-challenge",
    "grader_id": "aicrowd-food-recognition-challenge",
    "authors" : ["aicrowd-user"],
    "description" : "Food Recognition Challenge Submission",
    "license" : "MIT",
    "gpu": true
}
```
This file is used to identify your submission as a part of the Food Recognition Challenge.  You must use the `challenge_id` and `grader_id` specified above in the submission. The `gpu` key in the `aicrowd.json` lets your specify if your submission requires a GPU or not. In which case, a NVIDIA-K80 will be made available to your submission when evaluation the submission.

#### Submission environment configuration
You can specify the software runtime of your code by modifying the included [Dockerfile](Dockerfile). 

#### Code Entrypoint
The evaluator will use `/home/aicrowd/run.sh` as the entrypoint. Please remember to have a `run.sh` at the root which can instantiate any necessary environment variables and execute your code. This repository includes a sample `run.sh` file.

### Local Debug

If you wish to locally debug your submission repo, then you will have to build the docker image using `docker build .` (make sure you are inside your repo).
Then you will need to run the container in interactive mode `docker run -it <Docker image id>`

Now you can check if all the dependencies are available. Feel free to edit the Dockerfile in order to add more libraries for your use.

### Submitting 
To make a submission, you will have to create a private repository on [https://gitlab.aicrowd.com](https://gitlab.aicrowd.com).

You will have to add your SSH Keys to your GitLab account by following the instructions [here](https://docs.gitlab.com/ee/gitlab-basics/create-your-ssh-keys.html).
If you do not have SSH Keys, you will first need to [generate one](https://docs.gitlab.com/ee/ssh/README.html#generating-a-new-ssh-key-pair).

Then you can create a submission by making a *tag push* to your repository, adding the correct git remote and pushing to the remote:

You now should be able to see the details of your submission at : 
[gitlab.aicrowd.com/<YOUR_AICROWD_USER_NAME>/food-challenge-pytorch-baseline/issues](gitlab.aicrowd.com/<YOUR_AICROWD_USER_NAME>/food_recognition_detectron2_baseline/issues)


Note : If the contents of your repository (latest commit hash) does not change, then pushing a new tag will not trigger a new evaluation.


**Best of Luck**


## Credits
* Parts of the documentation for this baseline was taken from : https://gitlab.aicrowd.com/nikhil_rayaprolu/food-round2/blob/master/README.md
* and the baseline is built using Detectron2 : https://github.com/facebookresearch/detectron2

# Author   
**[Naveen Narayanan](naveen@ext.aicrowd.com)**
