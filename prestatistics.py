from model_config import *
import matplotlib.pyplot as plt
import matplotlib
from sklearn.metrics import *
from torch.utils.data import DataLoader
from dataloader import *
from tqdm import tqdm
import itertools
from matplotlib.colors import ListedColormap

x_train_dir = Infra_Config.IMG_DIR + '/x_train1'
y_train_dir = Infra_Config.IMG_DIR + '/y_train1'
train_dataset = Dataset(
    x_train_dir,
    y_train_dir,
    #augmentation=get_training_augmentation(),
    augmentation=None,
    preprocessing=get_preprocessing(Infra_Config.PREPROCESS)
)
train_loader = DataLoader(train_dataset, batch_size=Infra_Config.TRAIN_BATCH_SIZE, shuffle=True, num_workers=0)
# Evaluation and Visualization

# load best saved checkpoint

device = torch.device(Infra_Config.DEVICE)
best_model = torch.load(Infra_Config.WEIGHT_PATH)
best_model.to(device)

# Create test dataset for model evaluation and prediction visualization

x_test_dir = Infra_Config.IMG_DIR + '/x_test1'
y_test_dir = Infra_Config.IMG_DIR + '/y_test1'

test_dataset = Dataset(
    x_test_dir, 
    y_test_dir, 
    preprocessing=get_preprocessing(Infra_Config.PREPROCESS),
)

test_dataloader = DataLoader(test_dataset)

train_dataset_vis = Dataset(
    x_train_dir,
    y_train_dir
)

# Evaluate model on test dataset

test_epoch = smp.utils.train.ValidEpoch(
    model=best_model,
    loss=Infra_Config.LOSS,
    metrics=Infra_Config.METRICS,
    device=Infra_Config.DEVICE,
)

logs = test_epoch.run(train_loader)

# Create function to visualize predictions


def visualize(**images):
    """Plot images in one row."""
    n = len(images)
    plt.figure(figsize=(16, 5))
    cmap = ListedColormap(['black', 'green', 'red','yellow'])
    norm = plt.Normalize(vmin=0, vmax=3)

    for i, (name, image) in enumerate(images.items()):
        plt.subplot(1, n, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.title(' '.join(name.split('_')).title())
        plt.imshow(image,cmap=cmap,norm=norm)
    #plt.show()


# Visualize predictions on test dataset.


# for i, id_ in tqdm(enumerate(train_dataset), total=len(train_dataset)):
    
#     image_vis = train_dataset_vis[i][0].astype('float')
#     image_vis = image_vis/65535
#     image, gt_mask = train_dataset[i]
        
#     gt_mask = gt_mask.squeeze()
    
#     x_tensor = torch.from_numpy(image).to('cuda').unsqueeze(0)
#     pr_mask = best_model.predict(x_tensor)
#     pr_mask = (pr_mask.squeeze().cpu().numpy().round())

#     predicted_mask = np.moveaxis(pr_mask, 0, 2)

    # visualize(
    #    image=image_vis,
    #    ground_truth_mask=np.argmax(np.moveaxis(gt_mask, 0, 2), axis=2),
    #    predicted_mask=np.argmax(predicted_mask, axis=2)
    #    )

    # name = Infra_Config.TEST_OUTPUT_DIR + '/test_preds/' + str(i) + '.png'
    # plt.savefig(name)


# Run inference on test images and store the predictions and labels <br>
# in arrays to construct confusion matrix.


labels = np.empty([688, Infra_Config.CLASSES, Infra_Config.SIZE, Infra_Config.SIZE])
preds = np.empty([688, Infra_Config.CLASSES, Infra_Config.SIZE, Infra_Config.SIZE])
for i, id_ in tqdm(enumerate(train_dataset), total = len(train_dataset)):
    
    image, gt_mask = train_dataset[i]
    
    gt_mask = gt_mask.squeeze()
    labels[i] = gt_mask
    
    x_tensor = torch.from_numpy(image).to(Infra_Config.DEVICE).unsqueeze(0)
    pr_mask = best_model.predict(x_tensor)
    pr_mask = (pr_mask.squeeze().cpu().numpy().round())
    preds[i] = pr_mask


# Prepare prediction and label arrays for confusion matrix by deriving the predicted class for each sample and
# flattening the arrays

preds_max = np.argmax(preds, 1)
preds_max_f = preds_max.flatten()
labels_max = np.argmax(labels, 1)
labels_max_f = labels_max.flatten()

# Construct confusion matrix and calculate classification metrics with sklearn

# cm = confusion_matrix(labels_max_f, preds_max_f)
report = classification_report(labels_max_f, preds_max_f)
print(report)

# # Define function to plot confusion matrix 

# classes = ['Background', 'Road', 'Residents', 'Public']


# def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
#     matplotlib.use('Agg')
#     if normalize:
#         cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
#         print("Normalized confusion matrix")
#     else:
#         print('Confusion matrix')
#     print(cm)
    
#     plt.imshow(cm, interpolation='nearest', cmap=cmap)
#     plt.title(title)
#     tick_marks = np.arange(len(classes))
#     plt.xticks(tick_marks, classes, rotation=45)
#     plt.yticks(tick_marks, classes)
#     fmt = '.2f' if normalize else 'd'
#     thresh = cm.max() / 2.
#     for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
#         plt.text(j, i, format(cm[i, j], fmt), horizontalalignment="center", color="white" if cm[i, j] > thresh else "black")
#     plt.tight_layout()
#     plt.ylabel('True label')
#     plt.xlabel('Predicted label')
#     plt.savefig(Infra_Config.TEST_OUTPUT_DIR + '/confusion_matrix' + '.png', #dpi = 1000#
#                 dpi=500, bbox_inches = "tight")


# # Plot confusion matrix
# plt.figure(figsize=(4, 4))
# plot_confusion_matrix(cm, classes)