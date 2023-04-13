import torch
import pytorch_lightning as pl
import segmentation_models_pytorch as smp
from torchmetrics import JaccardIndex


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
        self.loss = torch.nn.BCEWithLogitsLoss()
        self.metric = JaccardIndex(task="binary", num_classes=2)


    def training_step(self, batch, batch_idx):
        x, y = batch
        y_pred = self.model(x)
        loss_value = self.loss(y_pred, y)
        self.log("train_loss", loss_value)

        return loss_value

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer

    def validation_step(self, batch, batch_idx):
        self.log("average_value", batch_idx+1)

        # this is the validation loop
        x, y = batch
        y_pred = self.model(x)
        val_loss = self.loss(y_pred, y)
        self.log("val_loss", val_loss)

    def test_step(self, batch, batch_idx):
        self.log("average_value", batch_idx + 1)

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
