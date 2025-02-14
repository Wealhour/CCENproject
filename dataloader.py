from model_config import *
from natsort import natsorted
import tifffile as tiff
from torch.utils.data import Dataset as BaseDataset
import os, numpy as np, cv2
import torch ,  torch.nn.functional as F
import tensorflow as tf


IMG_SIZE = Infra_Config.SIZE
IMG_CHANNELS = Infra_Config.CHANNELS
CLASSES = Infra_Config.CLASSES


class Dataset(BaseDataset):
    
    def __init__(
            self, 
            images_dir, 
            masks_dir, 
            augmentation=None, 
            preprocessing=None,
    ):
        self.ids = natsorted(os.listdir(images_dir))
        self.mask_ids = natsorted(os.listdir(masks_dir))
        self.images_fps = [os.path.join(images_dir, image_id) for image_id in self.ids]
        self.masks_fps = [os.path.join(masks_dir, image_id) for image_id in self.mask_ids]
        
        self.augmentation = augmentation
        self.preprocessing = preprocessing
    
    def __getitem__(self, i):
        #i=1495
        # Read in TIFF image tile
        img = tiff.imread(self.images_fps[i])
        # Extract B, G, R bands, leaving out NIR.
        img = img[:,:,0:3]
        # Convert from BGR to RGB
        img = cv2.cvtColor(img, 4)
        # Apply minimum-maximum normalization.
        img = cv2.normalize(img, dst=None, alpha=0, beta=65535,norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_16U)
        # Ensure image tiles are 256x256 pixels
        image = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        #print('no.',self.masks_fps[i])
        # Read in TIFF mask tile
        mask = tiff.imread(self.masks_fps[i])
    
        #print("mask0",np.nonzero(mask))
        #print("mask1",mask[:,1][50:200])
        #print("mask2",mask[:,2][100:150])
        #print("mask3",mask[:,:,3][100:150, 100:150])
        
        # Ensure image tiles are 256x256 pixels. Interpolation argument must be set to nearest-neighbor
        # to preserve ground truth.
        mask = cv2.resize(mask, (IMG_SIZE, IMG_SIZE), interpolation = cv2.INTER_NEAREST)
       # print("mask",mask.shape)
        
        # Remove white pixels
        mask[mask==255] = 0
        # # Merge building subclasses into one class
        mask[mask==0] = 0
        mask[mask==1] = 1
        mask[mask==2] = 2
        mask[mask==3] = 3
        # # Reassign pixel values because we merged 4 classes into 1
        # mask[mask==5] = 2
        # mask[mask==6] = 3
        # mask[mask==7] = 4
        # mask[mask==8] = 5
        # mask[mask==9] = 6
        
        # One-hot encode masks for multi-class segmentation
        # (10 infrastructure classes, or 7 if we merge building classes)
        #label = torch.tensor([0,1,2,3])
        #mask = F.one_hot(label, num_classes=CLASSES).float()

       
        onehot_mask = tf.one_hot(mask, CLASSES, axis = 0)
        mask = np.stack(onehot_mask, axis=-1).astype('float')
      
        # Apply augmentations
        if self.augmentation:
            sample = self.augmentation(image=image, mask=mask)
            image, mask = sample['image'], sample['mask']
        
        # Apply preprocessing
        if self.preprocessing:
            sample = self.preprocessing(image=image, mask=mask)
            image, mask = sample['image'], sample['mask']
            
        return image, mask
        
    def __len__(self):
        return len(self.ids)
    
    print(torch.cuda.is_available())
    print(torch.version.cuda)


    
def get_training_augmentation():
    train_transform = Infra_Config.AUGMENTATIONS
    return albu.Compose(train_transform)

def to_tensor(x, **kwargs):
    #print(x.shape)
    return x.transpose(2, 0, 1).astype('float32')



def get_preprocessing(preprocessing_fn):
    """Construct preprocessing transform
    
    Args:
        preprocessing_fn (callable): data normalization function 
            (can be specific for each pretrained neural network)
    Return:
        transform: albumentations.Compose
    
    """
    
    _transform = [
        albu.Lambda(image=preprocessing_fn),
        albu.Lambda(image=to_tensor, mask=to_tensor),
        
    ]
    return albu.Compose(_transform)



    