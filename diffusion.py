import numpy as np
from diffusers import StableDiffusionInpaintPipeline

class SD:
    def __init__(self) -> None:
        self.model = "runwayml/stable-diffusion-inpainting"
        self.sd = StableDiffusionInpaintPipeline.from_pretrained(self.model)

    def generate_for_mask(self, 
                          img: np.ndarray, 
                          mask: np.ndarray, 
                          prompt: str) -> np.ndarray:
        
        image = self.sd(prompt=prompt, 
                        image=img, 
                        mask_image=mask).images[0]
        return image
