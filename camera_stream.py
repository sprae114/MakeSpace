from picamera import PiCamera  
import cv2  # OpenCV
import threading  # 스트리밍을 백그라운드에서 실행
from config import CAMERA_RESOLUTION, CAMERA_FRAMERATE

class CameraStream:
    def __init__(self):
        self.camera = PiCamera()  # 카메라 객체 생성
        self.camera.resolution = CAMERA_RESOLUTION  
        self.camera.framerate = CAMERA_FRAMERATE 
        self.streaming = False  # 스트리밍 상태 플래그
        self.thread = None  # 스트리밍 스레드 객체

    def start_stream(self): # 실시간 스트리밍 시작
        if not self.streaming:
            self.streaming = True  # 스트리밍 상태 활성화
            self.thread = threading.Thread(target=self._stream, daemon=True) # 스트리밍을 별도 스레드에서 실행
            self.thread.start()

    def _stream(self): # 실제 스트리밍 로직
        # capture_continuous()로 연속 프레임 캡처, OpenCV로 표시
        try:
            for frame in self.camera.capture_continuous():
                if not self.streaming:
                    break  # 스트리밍 종료 신호 시 루프 탈출
                cv2.imshow("Pet Feeder Camera", frame)
                cv2.waitKey(1)
        finally:   # 스트리밍 종료 시 정리
            self.camera.close()  # 카메라 리소스 해제
            cv2.destroyAllWindows()  # OpenCV 창 닫기

    def stop_stream(self): # 스트리밍 종료
        self.streaming = False  # 스트리밍 상태 비활성화
        if self.thread:
            self.thread.join()  # 스레드 종료 대기

    def close(self):  # 카메라 리소스 정리
        self.stop_stream()
        if self.camera:
            self.camera.close()