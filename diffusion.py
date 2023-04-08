import numpy as np
import requests
import torch
from io import BytesIO
from PIL import Image

from diffusers import StableDiffusionInpaintPipeline


# def download_image(url):
#     response = requests.get(url)
#     return Image.open(BytesIO(response.content)).convert("RGB")
#
# device = 'cuda' if torch.cuda.is_available() else 'cpu'
#
# img_url = "https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo.png"
# mask_url = "https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo_mask.png"
#
# #
# init_image = download_image(img_url).resize((512, 512))
# mask_image = download_image(mask_url).resize((512, 512))

#
# pipe = StableDiffusionInpaintPipeline.from_pretrained(
#     "runwayml/stable-diffusion-inpainting", torch_dtype=torch.float16
# )
# pipe = pipe.to(device)
#
# prompt = "A yellow cat sitting on a park bench"
# image = pipe(prompt=prompt, image=init_image, mask_image=mask_image).images[0]
#
# Image.Image.show(image)

class SD:
    def __init__(self) -> None:
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = "runwayml/stable-diffusion-inpainting"

        self.sd = StableDiffusionInpaintPipeline.from_pretrained(self.model, torch_dtype=torch.float16)
        self.sd = self.sd.to(self.device)

        self.prompt = None
        self.img = None
        self.mask = None

    def generate_for_mask(self, img: np.ndarray, mask: np.ndarray, prompt: str) -> np.ndarray:
        self.img = img
        self.mask = mask
        self.prompt = prompt
        image = self.sd(prompt=self.prompt, image=self.img, mask_image=self.mask).images[0]
        print(image)
        torch.cuda.empty_cache()
        return image
