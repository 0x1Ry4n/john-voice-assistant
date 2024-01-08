import cv2
import webbrowser

class QRCodeScanner:
    @staticmethod
    def scan(): 
        cap = cv2.VideoCapture(0) 
        detector = cv2.QRCodeDetector()

        while True: 
            _, img = cap.read()
            decoded_info, _, _ = detector.detectAndDecode(img) 

            if decoded_info: 
                data = str(decoded_info) 
                break
            
            cv2.imshow("QRCode Scanner", img)     
            
            if cv2.waitKey(1) == ord("q"): 
                break
            
        webbrowser.open(data) 
        cap.release() 
        cv2.destroyAllWindows()
        
        return data

