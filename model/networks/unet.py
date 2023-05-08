import torch
import pytorch_lightning as pl
import segmentation_models_pytorch as smp
import torch.nn.functional as F

from torchmetrics import JaccardIndex
from torchmetrics.classification import BinaryJaccardIndex

from segmentation_models_pytorch.utils.metrics import IoU





# TODO:: add tests
# TODO:: add linkers
class Model(pl.LightningModule):
    def __init__(self):
        super().__init__()
        self.save_hyperparameters()
        self.model = smp.Unet(
            encoder_name='resnet50',
            encoder_weights='imagenet',
            in_channels=1,
            classes=1,
        )
        # self.loss = torch.nn.BCEWithLogitsLoss()
        # self.metric = BinaryJaccardIndex()

        self.loss = self.bce_dice_loss
        self.metric = IoU()

    def bce_dice_loss(self, y_pred, y_true, eps=1e-7):
        # BCE Loss
        bce_loss = F.binary_cross_entropy_with_logits(y_pred, y_true)

        # Dice Loss
        y_pred = torch.sigmoid(y_pred)
        intersection = torch.sum(y_pred * y_true)
        union = torch.sum(y_pred) + torch.sum(y_true) + eps
        dice_loss = 1 - (2 * intersection + eps) / union

        # Конечная функция потерь
        loss = bce_loss + dice_loss

        return loss


    def training_step(self, batch, batch_idx):
        x, y = batch
        y_pred = self.model(x)
        loss_value = self.loss(y_pred, y)
        self.log("train_loss", loss_value)

        # print(y.shape)
        # print(y[0, 0, 0, 0:10])
        # print(y_pred[0, 0, 0, 0:10])

        return loss_value

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer

    def validation_step(self, batch, batch_idx):

        # this is the validation loop
        x, y = batch
        y_pred = self.model(x)
        val_loss = self.loss(y_pred, y)
        self.log("val_loss", val_loss)
        iou = self.metric(y_pred, y)
        self.log('IOU_val', iou)

    def test_step(self, batch, batch_idx):

        x, y = batch
        y_pred = self.model(x)
        iou = self.metric(y_pred, y)
        self.log('IOU', iou)

    def forward(self, x):
        y_pred = self.model(x)
        y_pred = torch.sigmoid(y_pred)
        return y_pred

    def predict_step(self, batch, batch_idx):
        x, y = batch
        y_pred = self.model(x)
        y_pred = torch.sigmoid(y_pred)
        return y_pred

# model = MyLightningModule.load_from_checkpoint("/path/to/checkpoint.ckpt")
# model.eval()
