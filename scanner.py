import cv2
from pyzbar.pyzbar import decode

def scan_barcode():
    cap = cv2.VideoCapture(0)
    code = None
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            for b in decode(frame):
                code = b.data.decode("utf-8").strip()
                break
            if code:
                break
            cv2.imshow("Scan (press Q to cancel)", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
    return code