import time
import cv2
import argparse
import supervision as sv
import numpy as np
from ultralytics import YOLO
# import aws_send_photos as awssp

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

    model = YOLO("yolov8n.pt")

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    frame_count = 0
    time_start = time.time()

    while True:

        ret, frame = cap.read()

        result = model(frame)[0]

# for i in range(detection_count):
#             cls = int(result.boxes.cls[i].item())
#             name = result.names[cls]
#             confidence = float(result.boxes.conf[i].item())
#             bounding_box = result.boxes.xyxy[i].cpu().numpy()




        detection_count = result.boxes.shape[0]
        for i in range(detection_count):
            cls = int(result.boxes.cls[i].item())
            # print(cls)
        

        if result:
            
            boxes = result[0].boxes.xyxy.tolist()
            for box in boxes:
                xyxy = box
                x1 = int(xyxy[0])
                y1 = int(xyxy[1])
                x2 = int(xyxy[2])
                y2 = int(xyxy[3])

                cropped_image = frame[y1:y1+y2, x1:x1+x2]

                cv2.imwrite("human_img/frame{}.jpg".format(frame_count), cropped_image)
        
        else:
            print("Liste bos")

        # print(model.model.names)

        try:
            if model.model.names[67] == "cell phone":
                cell_phone_boxes = result[0].boxes.xyxy.tolist()
                print("cell", cell_phone_boxes)
                for box in cell_phone_boxes:
                    xyxy = box
                    x1 = int(xyxy[0])
                    y1 = int(xyxy[1])
                    x2 = int(xyxy[2])
                    y2 = int(xyxy[3])

                    cropped_image = frame[y1:y1+y2, x1:x1+x2]

                    cv2.imwrite("error_images/frame{}.jpg".format(frame_count), cropped_image)
                print("bla1")
                # cv2.imwrite("error_images/error_frame{}.jpg".format(frame_count), )
                print("blaa")
            else:print("esitligi dogru gir cano")
        except Exception as e:
            print(e)

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

        # cv2.imshow("Person_Detection", frame)

        time_finish = time.time()

        if time_finish - time_start >= 5:
            cap.release()
            cv2.destroyAllWindows()
            # awssp.images_sending_to_aws()
            break

        if (cv2.waitKey(30) == 27):
            cap.release()
            cv2.destroyAllWindows()
            # awssp.images_sending_to_aws()
            break

if __name__ == "__main__":
    main()
