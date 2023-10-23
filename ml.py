from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image


def analisador_img(upload_file):
    image = Image.open(upload_file)

    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

    detected_objects = []
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        detected_objects.append(
            {
                "label": model.config.id2label[label.item()],
                "confidence": round(score.item(), 3),
                "location": box
            }
        )
    return detected_objects


def predict_image(image_path, model, transform):
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        model.eval()  # Set model to evaluation mode
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
        return predicted.item()

