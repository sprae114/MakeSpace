from camera_stream import CameraStream
from motor_control import MotorControl
from audio_input import AudioInput
from keyboard_handler import KeyboardHandler
import keyboard

def main():
    print(f"Starting Pet Feeder System")

    # 모듈 초기화
    camera = CameraStream()
    motor = MotorControl()
    audio = AudioInput()
    handler = KeyboardHandler(motor, audio)

    try:
        # 카메라 스트리밍 시작 (백그라운드 스레드)
        camera.start_stream()
        print(f"Camera streaming started in background")

        # 키보드 이벤트 리스너 설정 (인터럽트 방식)
        handler.setup_event_listeners()

        # 키보드 이벤트를 기다리며 루프 유지
        keyboard.wait()

    except KeyboardInterrupt:  # Ctrl+C로 강제 종료 시 처리
        print(f"Shutting down...")

    finally:  # 리소스 정리
        camera.close()
        audio.close()
        motor.cleanup()

if __name__ == "__main__":
    main()