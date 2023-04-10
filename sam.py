import numpy as np
import torch
from typing import List, Tuple

from segment_anything import sam_model_registry, SamPredictor


class SAM:
    def __init__(self, model: str) -> None:
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = "./model/sam_" + model + ".pth"
        
        self.sam = sam_model_registry[model](checkpoint=self.model)
        self.sam.to(device=self.device)
        self.predictor = SamPredictor(self.sam)
        
        self.input_point = np.empty((0, 2))
        self.input_label = np.array([1])
        self.img = None
        self.mask = None

    def set_image(self, img: np.ndarray) -> None:
        self.img = img
        self.predictor.set_image(img)

    def get_mask(self, input_point: List[Tuple[int, int]]) -> np.ndarray:
        self.input_point = np.array(input_point)

        masks, scores, _ = self.predictor.predict(
            point_coords=self.input_point,
            point_labels=self.input_label,
            multimask_output=True,
        )

        self.mask = sorted(zip(masks, scores), key=lambda x: x[1])[-1][0].astype(np.uint8)
        torch.cuda.empty_cache()

    def mask_for_sd(self) -> np.ndarray:
        return self.mask*255
    
    def mask_to_show(self) -> np.ndarray:
        masked_img = self.img.copy()
        color_mask = np.random.random((1, 3)).tolist()[0]
        for i in range(3):
            masked_img[:,:,i] = np.where(self.mask == 1, 
                                         masked_img[:,:,i] * (1 - 0.35) + 0.35 * color_mask[i] * 255, 
                                         masked_img[:,:,i])
   
        return masked_img