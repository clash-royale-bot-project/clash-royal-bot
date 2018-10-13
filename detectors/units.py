import cv2 as cv
import numpy as np

# Initialize the parameters
from utils import copy_image_to_np_array

confThreshold = 0.5  # Confidence threshold
nmsThreshold = 0.4  # Non-maximum suppression threshold
inpWidth = 576  # Width of network's input image
inpHeight = 576  # Height of network's input image

classesFile = "/Users/tolsi/Documents/clash_royale_bot/bot/bot/model/model.names"

# Load names of classes
def loadUnitsNNClasses():
    classes = None
    with open(classesFile, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')
    return classes

# Give the configuration and weight files for the model and load the network using them.
# modelConfiguration = "model/v2/yolov3_tiny.cfg"
# modelWeights = "model/v2/yolov3_tiny_185400.weights"
modelConfiguration = "/Users/tolsi/Documents/clash_royale_bot/bot/bot/model/yolov3-tiny_1.cfg"
modelWeights = "/Users/tolsi/Documents/clash_royale_bot/bot/bot/model/yolov3-tiny_1.backup"

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# Draw the predicted bounding box
def drawPred(frame, classes, classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)

    label = '%.2f' % conf

    # Get the label for the class name and its confidence
    if classes:
        assert (classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    # Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.rectangle(frame, (left, top - round(1.5 * labelSize[1])), (left + round(1.5 * labelSize[0]), top + baseLine),
                 (255, 255, 255), cv.FILLED)
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)


# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs, shift):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIds = []
    confidences = []
    boxes = []
    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left + shift[0], top + shift[1], width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    predictions = []
    for i in indices:
        i = i[0]
        predictions.append((boxes[i], classIds[i], confidences[i]))

    return predictions

detect_field_area = (50, 70, 435, 600)

# param - image
def predict_units(screen):
    frame = copy_image_to_np_array(screen.crop(detect_field_area))

    # Create a 4D blob from a frame.
    blob = cv.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)

    # Sets the input to the network
    net.setInput(blob)

    # Runs the forward pass to get output of the output layers
    outs = net.forward(getOutputsNames(net))

    # Remove the bounding boxes with low confidence and shift the predictions
    predictions = postprocess(frame, outs, detect_field_area)

    return predictions

# param - np array
def draw_predictions(frame, classes, predictions):
    for box, classId, confidence in predictions:
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(frame, classes, classId, confidence, left, top, left + width, top + height)

    # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
    t, _ = net.getPerfProfile()
    cv.putText(frame, 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency()), (0, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
