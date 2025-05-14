import pyaudio  # 오디오 입력 처리 라이브러리
import threading  # 비동기 입력 처리를 위한 스레딩

class AudioInput:
    def __init__(self):
        self.p = None  # PyAudio 객체, 초기화 지연
        self.stream = None  # 오디오 스트림, 초기화 지연
        self.listening = False  # 오디오 입력 처리 상태 플래그
        self.thread = None  # 오디오 입력 스레드 객체

    def start_listening(self): # 오디오 입력 처리 시작
        if not self.listening:
            self.p = pyaudio.PyAudio()  
            self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
            self.listening = True 
            self.thread = threading.Thread(target=self._listen, daemon=True)
            self.thread.start()
            print(f"Audio listening started in background")

    def _listen(self): # 실제 오디오 입력 처리 로직
        try:
            while self.listening:
            
                data = self.stream.read(1024, exception_on_overflow=False)
                print(f"Audio input detected!")  # 입력 감지 로그
        
        except Exception as e:  # 에러 처리
            print(f"Audio input error: {e}")

        finally:   # 스레드 종료 시 정리  
            if self.stream:
                self.stream.stop_stream()  # 스트림 중지
                self.stream.close()  # 스트림 닫기
            if self.p:
                self.p.terminate()  # PyAudio 객체 종료
            self.stream = None
            self.p = None
            self.listening = False  # 상태 갱신

    def stop_listening(self):  # 오디오 입력 처리 종료
        if self.listening:
            self.listening = False  
            if self.thread:
                self.thread.join()  
            print(f"Audio listening stopped")

    def close(self): # 마이크 리소스 정리
        self.stop_listening()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.p:
            self.p.terminate()
        self.stream = None
        self.p = None