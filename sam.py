import numpy as np
import cv2
import torch

from segment_anything import sam_model_registry, SamPredictor


class SAM:
    def __init__(self) -> None:
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = "./model/sam_vit_l_0b3195.pth"
        
        self.sam = sam_model_registry["vit_l"](checkpoint=self.model)
        self.sam.to(device=self.device)
        self.predictor = SamPredictor(self.sam)
        
        self.input_point = np.empty((0, 2))
        self.input_label = np.array([1])
        self.img = None
        self.mask = None

    def set_image(self, img: np.ndarray) -> None:
        self.img = img
        self.predictor.set_image(img)

    def get_mask(self, input_point: np.ndarray) -> np.ndarray:
        self.input_point = input_point

        masks, scores, _ = self.predictor.predict(
            point_coords=input_point,
            point_labels=self.input_label,
            multimask_output=True,
        )

        self.mask = sorted(zip(masks, scores), key=lambda x: x[1])[-1][0]
    
    def mask_for_sd(self) -> np.ndarray:
        h, w = self.mask.shape[-2:]
        return self.mask.reshape(h, w, 1) * np.ones(3).reshape(1, 1, -1)
    
    def mask_to_show(self) -> np.ndarray:
        masked_img = self.img.copy()
        color_mask = np.random.random((1, 3)).tolist()[0]
        for i in range(3):
            masked_img[:,:,i] = np.where(self.mask == 1, 
                                         masked_img[:,:,i] * (1 - 0.35) + 0.35 * color_mask[i] * 255, 
                                         masked_img[:,:,i])
   
        return masked_img