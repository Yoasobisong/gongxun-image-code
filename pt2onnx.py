from ultralytics import YOLO
model = YOLO('./mat_pt/mat.pt') 
result = model.export(format='onnx')