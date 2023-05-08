import pytorch_lightning as pl
import yaml

from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from pytorch_lightning.loggers import WandbLogger
from torch.utils.data import DataLoader

from dataset.ct_segmentation_dataset import LungDataset
from networks.unet import Model

'''
Wand: 1. Добавить логирование промежуточных картинок
2. Добавить логирование метрик на валидации
3. Добавить логирование артефактов, такие как модель

Для логирование датасетов использовать специальную приблуду DNV (я не помню точно)
'''


def run():
    with open('config/standard.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    train_path = config['train']
    batch_size = int(config['batch_size'])
    train_ds = LungDataset(train_path)
    train_loader = DataLoader(train_ds, batch_size=batch_size)

    val_path = config['val']
    val_ds = LungDataset(val_path)
    val_loader = DataLoader(val_ds, batch_size=batch_size)

    test_path = config['test']
    test_ds = LungDataset(test_path)
    test_loader = DataLoader(test_ds, batch_size=batch_size)

    print(len(train_loader), len(val_loader), len(test_loader))
    model = Model()

    checkpoint_callback = ModelCheckpoint(dirpath=config['checkpoint_dir'],
                                          save_top_k=5,
                                          monitor="val_loss",
                                          filename="{epoch:02d}-{val_loss:.2f}")

    early_stop_callback = EarlyStopping(monitor="val_loss",
                                        mode="min",
                                        patience=7,
                                        verbose=True)

    logger = WandbLogger(log_model=True,
                         name=config['name'],
                         save_dir='../../../AppData/Local/Temp')

    trainer = pl.Trainer(
        deterministic=True,
        accelerator='gpu',
        log_every_n_steps=1000,
        max_epochs=config['epochs'],
        check_val_every_n_epoch=3,
        logger=logger,
        callbacks=[
            early_stop_callback,
            checkpoint_callback, # checkpoint_callback.best_model_path
        ],
        default_root_dir='../../logs',
    )

    trainer.fit(model=model, train_dataloaders=train_loader, val_dataloaders=val_loader)
    trainer.test(model, dataloaders=test_loader)

if __name__ == '__main__':
    # run()

    model = Model.load_from_checkpoint("../logs/unet/epoch=17-val_loss=1.00.ckpt")
    model.eval()


    with open('config/standard.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    trainer = pl.Trainer(
        deterministic=True,
        accelerator='gpu',
        log_every_n_steps=1000,
        max_epochs=config['epochs'],
        check_val_every_n_epoch=3,
        default_root_dir='../../logs',
    )
    test_path = config['test']
    test_ds = LungDataset(test_path)
    test_loader = DataLoader(test_ds, batch_size=10)
    trainer.test(model, dataloaders=test_loader)
    a, b = next(iter(test_loader))
    print(a.shape)
    y_pred = model(a)
    print(y_pred.shape)
    x = y_pred[5]
    x = x.permute(1, 2, 0)
    x = x.detach().numpy()
    import matplotlib.pyplot as plt
    plt.imshow(x[:, :, 0]) # поставить порог 0,5
    plt.show()
    x = b[5]
    x = x.permute(1, 2, 0)
    x = x.detach().numpy()
    plt.imshow(x[:, :, 0])
    plt.show()

