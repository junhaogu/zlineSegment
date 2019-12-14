{"nbformat":4,"nbformat_minor":0,"metadata":{"colab":{"name":"UNet.py","provenance":[],"collapsed_sections":[]},"kernelspec":{"name":"python3","display_name":"Python 3"}},"cells":[{"cell_type":"code","metadata":{"id":"h3nqFYWGMH1T","colab_type":"code","colab":{}},"source":["from collections import OrderedDict\n","\n","import torch\n","import torch.nn as nn\n","\n","class unet(nn.Module):\n","\n","    def __init__(self, in_channels=3, out_channels=1, init_features=20,block=4):\n","        super(unet, self).__init__()\n","\n","        features = init_features\n","        self.encoder1 = UNet._block(in_channels, features, name=\"enc1\")\n","        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)\n","        self.encoder2 = UNet._block(features, features * 2, name=\"enc2\")\n","        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)\n","        self.encoder3 = UNet._block(features * 2, features * 4, name=\"enc3\")\n","        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)\n","        self.encoder4 = UNet._block(features * 4, features * 8, name=\"enc4\")\n","        self.pool4 = nn.MaxPool2d(kernel_size=2, stride=2)\n","        self.encoder5 = UNet._block(features * 8, features * 16, name=\"enc5\")\n","        self.pool5 = nn.MaxPool2d(kernel_size=2, stride=2)\n","        if block ==5:        \n","          self.bottleneck = UNet._block(features * 16, features * 32, name=\"bottleneck\")\n","        else:\n","          self.bottleneck = UNet._block(features * 8, features * 16, name=\"bottleneck\")\n","        \n","        self.upconv5 = nn.ConvTranspose2d(\n","            features * 32, features * 16, kernel_size=2, stride=2\n","        )\n","        self.decoder5 = UNet._block((features * 16) * 2, features * 16, name=\"dec5\")\n","        self.upconv4 = nn.ConvTranspose2d(\n","            features * 16, features * 8, kernel_size=2, stride=2\n","        )\n","        self.decoder4 = UNet._block((features * 8) * 2, features * 8, name=\"dec4\")\n","        self.upconv3 = nn.ConvTranspose2d(\n","            features * 8, features * 4, kernel_size=2, stride=2\n","        )\n","        self.decoder3 = UNet._block((features * 4) * 2, features * 4, name=\"dec3\")\n","        self.upconv2 = nn.ConvTranspose2d(\n","            features * 4, features * 2, kernel_size=2, stride=2\n","        )\n","        self.decoder2 = UNet._block((features * 2) * 2, features * 2, name=\"dec2\")\n","        self.upconv1 = nn.ConvTranspose2d(\n","            features * 2, features, kernel_size=2, stride=2\n","        )\n","        self.decoder1 = UNet._block(features * 2, features, name=\"dec1\")\n","\n","        self.conv = nn.Conv2d(\n","            in_channels=features, out_channels=out_channels, kernel_size=1\n","        )\n","\n","    def forward(self, x):\n","        enc1 = self.encoder1(x)\n","        enc2 = self.encoder2(self.pool1(enc1))\n","        enc3 = self.encoder3(self.pool2(enc2))\n","        enc4 = self.encoder4(self.pool3(enc3))\n","        if block==5:\n","          enc5 = self.encoder5(self.pool3(enc4))\n","          bottleneck = self.bottleneck(self.pool5(enc5))\n","          dec5 = self.upconv5(bottleneck)\n","          dec5 = torch.cat((dec5, enc5), dim=1)\n","          dec5 = self.decoder5(dec5)\n","          dec4 = self.upconv4(dec5)\n","        else:\n","          bottleneck = self.bottleneck(self.pool4(enc4))\n","          dec4=self.upconv4(bottleneck)\n","        dec4 = torch.cat((dec4, enc4), dim=1)\n","        dec4 = self.decoder4(dec4)\n","        dec3 = self.upconv3(dec4)\n","        dec3 = torch.cat((dec3, enc3), dim=1)\n","        dec3 = self.decoder3(dec3)\n","        dec2 = self.upconv2(dec3)\n","        dec2 = torch.cat((dec2, enc2), dim=1)\n","        dec2 = self.decoder2(dec2)\n","        dec1 = self.upconv1(dec2)\n","        dec1 = torch.cat((dec1, enc1), dim=1)\n","        dec1 = self.decoder1(dec1)\n","        return torch.sigmoid(self.conv(dec1))\n","\n","    @staticmethod\n","    def _block(in_channels, features, name):\n","        return nn.Sequential(\n","            OrderedDict(\n","                [\n","                    (\n","                        name + \"conv1\",\n","                        nn.Conv2d(\n","                            in_channels=in_channels,\n","                            out_channels=features,\n","                            kernel_size=3,\n","                            padding=1,\n","                            bias=False,\n","                        ),\n","                    ),\n","                    (name + \"norm1\", nn.BatchNorm2d(num_features=features)),\n","                    (name + \"relu1\", nn.ReLU(inplace=True)),\n","                    (\n","                        name + \"conv2\",\n","                        nn.Conv2d(\n","                            in_channels=features,\n","                            out_channels=features,\n","                            kernel_size=3,\n","                            padding=1,\n","                            bias=False,\n","                        ),\n","                    ),\n","                    (name + \"norm2\", nn.BatchNorm2d(num_features=features)),\n","                    (name + \"relu2\", nn.ReLU(inplace=True)),\n","                ]\n","            )\n","        )"],"execution_count":0,"outputs":[]}]}