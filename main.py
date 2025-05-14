import keyboard  
from camera_stream import CameraStream  
from motor_control import MotorControl  
from audio_input import AudioInput 

def main():
    print(f"Starting Pet Feeder System")

    # 모듈 초기화
    camera = CameraStream()
    motor = MotorControl()
    audio = AudioInput() 

    # 모터 2의 회전 상태 추적
    motor2_running = False  # 모터 2가 현재 회전 중인지 여부
    motor2_direction = None # 모터 2의 현재 회전 방향
    motor2_speed = 50  # 기본 속도 50%

    try:
        # 카메라 스트리밍 시작 (백그라운드 스레드)
        camera.start_stream()  # 스트리밍을 별도 스레드에서 실행
        print(f"Camera streaming started in background")

        # 키보드 입력 처리 루프
        while True:
            # 위쪽 방향키: 모터 1 CW 1회전
            if keyboard.is_pressed('up'):
                motor.rotate_motor(1, 512, "CW", speed=50)  # 모터 1을 512 스텝 CW 회전, 속도 50%
                print(f"Up arrow pressed: Motor 1 CW")
                while keyboard.is_pressed('up'):
                    pass  # 키 뗄 때까지 대기, 반복 실행 방지

            # 왼쪽 방향키: 모터 2 CCW 연속 회전
            elif keyboard.is_pressed('left'):
                if not motor2_running:  # 모터 2가 아직 회전 중이 아니면 시작
                    print(f"Left arrow pressed: Motor 2 CCW continuous, speed: {motor2_speed}%")
                    motor2_running = True
                    motor2_direction = "CCW"
                    motor.rotate_motor(2, 0, motor2_direction, speed=motor2_speed, continuous=True)  # 연속 회전 시작

            # 오른쪽 방향키: 모터 2 CW 연속 회전
            elif keyboard.is_pressed('right'):
                if not motor2_running:  # 모터 2가 아직 회전 중이 아니면 시작
                    print(f"Right arrow pressed: Motor 2 CW continuous, speed: {motor2_speed}%")
                    motor2_running = True
                    motor2_direction = "CW"
                    motor.rotate_motor(2, 0, motor2_direction, speed=motor2_speed, continuous=True)  # 연속 회전 시작

            # 속도 증가/감소: '+'와 '-' 키
            elif keyboard.is_pressed('+'):
                motor2_speed = min(100, motor2_speed + 10)
                print(f"Speed increased to {motor2_speed}%")
                if motor2_running:
                    motor.rotate_motor(2, 0, motor2_direction, speed=motor2_speed, continuous=True)
                while keyboard.is_pressed('+'):
                    pass

            elif keyboard.is_pressed('-'):
                motor2_speed = max(0, motor2_speed - 10)
                print(f"Speed decreased to {motor2_speed}%")
                if motor2_running:
                    motor.rotate_motor(2, 0, motor2_direction, speed=motor2_speed, continuous=True)
                while keyboard.is_pressed('-'):
                    pass

            # 'm' 키: 마이크 입력 토글
            elif keyboard.is_pressed('m'):
                if not audio.listening:
                    audio.start_listening()  # 오디오 입력 시작 별도 스레드에서 실행
                    print(f"Audio listening started in background")
                else:
                    audio.stop_listening()  # 마이크 입력 중지
                    print(f"Audio stop")
                while keyboard.is_pressed('m'):
                    pass  # 키 뗄 때까지 대기, 반복 토글 방지

            # 키 뗌 감지: 모터 2 정지
            if motor2_running and not (keyboard.is_pressed('left') or keyboard.is_pressed('right')):
                motor.stop_motor(2)  # 모터 2 정지
                motor2_running = False  # 회전 상태 갱신
                motor2_direction = None  # 방향 초기화

            # 'q' 키: 프로그램 종료
            if keyboard.is_pressed('q'):
                print(f"Quitting...")
                break

    except KeyboardInterrupt:  # Ctrl+C로 강제 종료 시 처리
        print(f"Shutting down...") 

    finally: # 리소스 정리
        camera.close()  
        audio.close()  
        motor.cleanup()

if __name__ == "__main__":
    main()