# About

Project for the [conference](https://amu.edu.pl/wiadomosci/events/dzien-kol-naukowych) of scientific circles held at UAM.

The website allows segmentation of objects by clicking on the desired thing in the photo and replacing it with any other object through the appropriate prompt using inpainting.

Segmentation is done using [SAM](https://github.com/facebookresearch/segment-anything), inpating is done using [Diffusers](https://github.com/huggingface/diffusers).

# Installation 

Firstly you need to download a SAM model and requirements.
That can be done with setup.sh script.

```bash

git clone https://github.com/filnow/replace-anything.git
cd replace-anything
chmod +x setup.sh
./setup.sh {MODEL_NAME}

```
where {MODEL_NAME} should be replaced with one of the following options:

* vit_h: download the Huge model (2,4GB).

* vit_l: download the Large model (1,2GB).

* vit_b: download the Big model (358MB).

For example, to download the Large model, you would run:

```bash

./setup.sh vit_l

```

After first prompt the Stable Diffusion will download automatically (about 10GB) and then you good to go.

Despite our limitations in hardware it takes abour 2s for a segmentation and 6s for inpainting for vit_l on GPU with 6GB of memory and CUDA environment.

# Results

* TODO: add results


