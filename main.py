import time
from PIL import Image

import numpy as np
from torch.autograd import Variable
from torchvision.models import squeezenet1_1
from torchvision.transforms import Normalize, Compose, RandomSizedCrop, RandomHorizontalFlip, ToTensor

model = squeezenet1_1(pretrained=True)
model.eval()

transform = Compose([
    RandomSizedCrop(224),
    RandomHorizontalFlip(),
    ToTensor(),
    Normalize(mean=[0.485, 0.456, 0.406],
              std=[0.229, 0.224, 0.225]),
])


pil_image = Image.open('cat.jpg')

inferences = []
predictions = []

for i in range(1, 1000):
    prediction_meter = time.time()
    image = transform(pil_image)
    image.unsqueeze_(0)

    image_tensor = Variable(image)

    inference_meter = time.time()
    output = model(image_tensor)
    finish_time = time.time()

    inferences.append(finish_time - inference_meter)
    predictions.append(finish_time - prediction_meter)

inferences = np.asarray(inferences)
predictions = np.asarray(predictions)

print("Model: {}".format('Squeezenet'))
print("Inference")
print("=======================")
print("mean: {}, std: {}".format(inferences.mean(), inferences.std()))

print("Prediction")
print("=======================")
print("mean: {}, std: {}".format(predictions.mean(), predictions.std()))



