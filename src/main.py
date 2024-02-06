import time
import cv2
import argparse
import supervision as sv
import numpy as np
from ultralytics import YOLO
import src.aws_send_photos as awssp

FPS = 20
frame_size = (360, 360)

image_folder = "./resimler/"
video_name = "./videolar/video.mp4"

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Person Detection")
    parser.add_argument(
        "--webcam-resolution", 
        default=[360, 360], 
        nargs=2, 
        type=int
    )
    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    model = YOLO("best.pt")

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    frame_count = 0
    time_start = time.time()

    while True:

        ret, frame = cap.read()

        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_yolov8(result)
        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _
            in detections
        ]
        frame = box_annotator.annotate(
            scene=frame, 
            detections=detections, 
            labels=labels
        )   

        # kameradan alınan her bir frame resimler klasörüne tek tek kayıt yapılır.
        if ret:
            cv2.imwrite("resimler/frame{}.jpg".format(frame_count), frame)
            frame_count += 1

        cv2.imshow("Person_Detection", frame)

        time_finish = time.time()

        if time_finish - time_start >= 10:
            cap.release()
            cv2.destroyAllWindows()
            awssp.images_sending_to_aws()
            break

        if (cv2.waitKey(30) == 27):
            cap.release()
            cv2.destroyAllWindows()
            awssp.images_sending_to_aws()
            break

if __name__ == "__main__":
    main()
