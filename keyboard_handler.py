import keyboard

class KeyboardHandler:
    def __init__(self, motor, audio):
        self.motor = motor
        self.audio = audio
        self.motor2_running = False  # 모터 2가 현재 회전 중인지 여부
        self.motor2_direction = None  # 모터 2의 현재 회전 방향
        self.motor2_speed = 50  # 기본 속도 50%

    def setup_event_listeners(self):
        # 키보드 이벤트 바인딩
        keyboard.on_press_key('up', self.on_up)
        keyboard.on_press_key('left', self.on_left)
        keyboard.on_press_key('right', self.on_right)
        keyboard.on_press_key('+', self.on_plus)
        keyboard.on_press_key('-', self.on_minus)
        keyboard.on_press_key('m', self.on_m)
        keyboard.on_press_key('q', self.on_q)
        keyboard.on_release(self.on_key_release)

    def on_up(self, e):
        # 위쪽 방향키: 모터 1 CW 1회전
        self.motor.rotate_motor(1, 512, "CW", speed=50)
        print("Up arrow pressed: Motor 1 CW")

    def on_left(self, e):
        # 왼쪽 방향키: 모터 2 CCW 연속 회전
        if not self.motor2_running:
            self.motor2_running = True
            self.motor2_direction = "CCW"
            self.motor.rotate_motor(2, 0, "CCW", speed=self.motor2_speed, continuous=True)
            print("Left arrow pressed: Motor 2 CCW continuous")

    def on_right(self, e):
        # 오른쪽 방향키: 모터 2 CW 연속 회전
        if not self.motor2_running:
            self.motor2_running = True
            self.motor2_direction = "CW"
            self.motor.rotate_motor(2, 0, "CW", speed=self.motor2_speed, continuous=True)
            print("Right arrow pressed: Motor 2 CW continuous")

    def on_plus(self, e):
        # '+' 키: 속도 증가
        self.motor2_speed = min(100, self.motor2_speed + 10)
        print(f"Speed increased to {self.motor2_speed}%")
        if self.motor2_running:
            self.motor.rotate_motor(2, 0, self.motor2_direction, speed=self.motor2_speed, continuous=True)

    def on_minus(self, e):
        # '-' 키: 속도 감소
        self.motor2_speed = max(0, self.motor2_speed - 10)
        print(f"Speed decreased to {self.motor2_speed}%")
        if self.motor2_running:
            self.motor.rotate_motor(2, 0, self.motor2_direction, speed=self.motor2_speed, continuous=True)

    def on_m(self, e):
        # 'm' 키: 마이크 입력 토글
        if not self.audio.listening:
            self.audio.start_listening()  # 오디오 입력 시작 (별도 스레드)
            print("Audio listening started in background")
        else:
            self.audio.stop_listening()
            print("Audio stop")

    def on_q(self, e):
        # 'q' 키: 프로그램 종료
        print("Quitting...")
        exit(0)

    def on_key_release(self, e):
        # 모터 2가 회전 중이고 방향키가 떼어진 경우 정지
        if e.name in ['left', 'right'] and self.motor2_running:
            self.motor.stop_motor(2)
            self.motor2_running = False
            self.motor2_direction = None
            print("Motor 2 stopped")