import torch
import os
from torchvision.io import read_image
from monai.data import ArrayDataset
import random as rnd


    
# Distribution decides how many patches are used for training and how many are used for validation.
def partition_patches(type: str, distribution: int = 0.75):
    types = ["train", "test"]
    if type not in types:
        raise ValueError("Invalid sim type. Expected one of: %s" % types)
    
    label_dir = 'Labels/'
    train_dir = 'Patches/'
    path_dir = 'train_patches' if type == "train" else 'test_patches'
    
    def add(obj):
        obj["imgs"].append(read_image(os.path.join(path_dir, train_dir, 'patch_' + str(count) + '.png')))
        obj["labels"].append(read_image(os.path.join(path_dir, label_dir, 'labels_' + str(count) + '.png')))
    
    dir_path = os.path.join(path_dir, label_dir)
    count = 0
    training = {
        "imgs": [],
    "labels" : []}
    test = {
        "imgs": [],
    "labels" : []}
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            if rnd.random() < distribution:
                add(training)
            else:
                add(test)
        count += 1
            
    return ArrayDataset(img=training["imgs"],labels=training["labels"]), ArrayDataset(img=test["imgs"], labels=test["labels"])