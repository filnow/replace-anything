import numpy as np
import torch

from diffusers import StableDiffusionInpaintPipeline


class SD:
    def __init__(self) -> None:
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = "runwayml/stable-diffusion-inpainting"
        self.sd = StableDiffusionInpaintPipeline.from_pretrained(self.model, torch_dtype=torch.float16)
        self.sd = self.sd.to(self.device)

    def generate_for_mask(self, 
                          img: np.ndarray, 
                          mask: np.ndarray, 
                          prompt: str) -> np.ndarray:
        
        image = self.sd(prompt=prompt, 
                        image=img, 
                        mask_image=mask).images[0]
        torch.cuda.empty_cache()
        return image
