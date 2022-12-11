from PIL import Image
import requests

from transformers import CLIPProcessor, CLIPModel

def food_not_food(input_image):
    model = CLIPModel.from_pretrained("flax-community/clip-rsicd-v2")
    processor = CLIPProcessor.from_pretrained("flax-community/clip-rsicd-v2")

    labels = ["food", "not food"]
    inputs = processor(text=[f"a photo of a {l}" for l in labels], images=input_image, return_tensors="pt", padding=True)

    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image 
    prob = logits_per_image.softmax(dim=1).detach().cpu().numpy().argmax(axis=1)
    return labels[prob[0]]