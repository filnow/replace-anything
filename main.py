import cv2
import numpy as np
from segment_anything import sam_model_registry, SamPredictor
import matplotlib.pyplot as plt

def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)
    
def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)   
    
def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))    

def click_event(event, x, y, flags, params):
   if event == cv2.EVENT_LBUTTONDOWN:
      input_point.append(np.array([[x,y]]))
      print(f'({x},{y})')

model = "./model/sam_vit_h_4b8939.pth"

img = cv2.imread("./images//dog.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

input_point = []
input_label = np.array([1])

cv2.namedWindow('Point Coordinates')
cv2.setMouseCallback('Point Coordinates', click_event)

while input_point == []:
   cv2.imshow('Point Coordinates',img)
   k = cv2.waitKey(1) & 0xFF
   if k == 27:
      break
cv2.destroyAllWindows()

sam = sam_model_registry["default"](checkpoint=model)
predictor = SamPredictor(sam)
predictor.set_image(img)

masks, scores, logits = predictor.predict(
    point_coords=input_point[0],
    point_labels=input_label,
    multimask_output=True,
)

mask = sorted(zip(masks, scores), key=lambda x: x[1])

plt.figure(figsize=(10,10))
plt.imshow(img)
show_mask(np.array(mask[-1][0]), plt.gca())
show_points(input_point[0], input_label, plt.gca())
plt.axis('off')
plt.show()  