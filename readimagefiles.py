{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "readimagefiles",
      "provenance": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/junhaogu/zlineSegment/blob/master/readimagefiles.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "l_QCWjcc04pw",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "import glob\n",
        "import torch\n",
        "import os\n",
        "from PIL import Image\n",
        "from matplotlib import pyplot as plt\n",
        "import torchvision.transforms as transforms\n",
        "import numpy as np\n",
        "def read_single_cell_image(image_data_path, mask_data_path):\n",
        "  data_path=os.path.join(image_data_path, '*.tif')\n",
        "  data_path1=os.path.join(mask_data_path, '*.tif')\n",
        "  files=glob.glob(data_path)\n",
        "  files1=glob.glob(data_path1)\n",
        "  files.sort()\n",
        "  files1.sort()\n",
        "  sample_data = torch.zeros([1,3,256,512]).type(torch.FloatTensor)\n",
        "  temp=torch.zeros([1,3,256,512]).type(torch.FloatTensor)\n",
        "  counter=0\n",
        "  for f1 in files:\n",
        "    img=Image.open(f1)\n",
        "    img=img-np.mean(img)\n",
        "    imgTensor=transforms.ToTensor()(img).type(torch.FloatTensor)\n",
        "    temp=torch.cat((temp, imgTensor[None,:,:,:]),0) \n",
        "    counter +=1 \n",
        "    if counter%100==0:\n",
        "      print(counter) \n",
        "    if temp.shape[0]>17:\n",
        "      sample_data=torch.cat((sample_data,temp[1:,:,:,:]),0)\n",
        "      temp = torch.zeros([1,3,256,512]).type(torch.FloatTensor)\n",
        "  sample_data=sample_data[1:,:,:,:]\n",
        "  \n",
        "\n",
        "  mask = torch.zeros([1,1,256,512]).type(torch.float)\n",
        "  temp = torch.zeros([1,1,256,512]).type(torch.float)\n",
        "  for f1 in files1:\n",
        "    img=Image.open(f1)\n",
        "    img=img.convert('1')\n",
        "    imgTensor=transforms.ToTensor()(img).type(torch.float)\n",
        "    for i in range(17):\n",
        "      temp=torch.cat((temp,imgTensor[None,:,:,:]),0)\n",
        "      counter +=1\n",
        "    \n",
        "    mask=torch.cat((mask,temp[1:,:,:,:]),0)\n",
        "    temp = torch.zeros([1,1,256,512]).type(torch.float)\n",
        "    if counter%100==0:\n",
        "      print(counter)\n",
        "  mask=mask[1:,:,:,:]\n",
        "  \n",
        "  plt.imshow(mask[0][0,:,:])\n",
        "  plt.imshow(sample_data[0][0,:,:])\n",
        "  return sample_data, mask"
      ],
      "execution_count": 0,
      "outputs": []
    }
  ]
}