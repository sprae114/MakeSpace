import RPi.GPIO as GPIO  # 라즈베리 파이 GPIO 제어
import time  # 스텝 딜레이를 위한 시간 제어
from config import MOTOR1_PINS, MOTOR2_PINS, STEP_DELAY, STEPS_PER_REVOLUTION 

class MotorControl:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # BCM 모드: GPIO 번호를 BCM 핀 번호로 사용
        self.motors = [MOTOR1_PINS, MOTOR2_PINS]  # 모터 1, 2의 핀 리스트
        self.pwm_freq = 100  # PWM 주파수 100Hz
        self.pwm = {}  # 각 모터의 PWM 객체 저장
        for pins in self.motors:
            GPIO.setup(pins, GPIO.OUT)  # 각 모터의 4개 핀을 출력 모드로 설정
            # 첫 번째 핀에 PWM 설정
            self.pwm[pins[0]] = GPIO.PWM(pins[0], self.pwm_freq)
            self.pwm[pins[0]].start(0)  # 초기 듀티 사이클 0%

        # 4상 스텝모터 시퀀스 (8스텝, 풀 스텝 모드) 
        self.step_sequence = [ 
            [1, 0, 0, 1],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1]
        ]

    # motor_id: 1(모터 1) 또는 2(모터 2)
    # steps: 회전할 스텝 수 (continuous=True면 무시)
    # direction: "CW" (시계 방향) 또는 "CCW" (반시계 방향)
    # speed: PWM 듀티 사이클 (0~100%)
    # continuous: True면 연속 회전
    def rotate_motor(self, motor_id, steps, direction, speed=100, continuous=False): # 모터 회전 제어
        pins = self.motors[motor_id - 1]  # 선택한 모터의 GPIO 핀 리스트
        sequence = self.step_sequence if direction == "CW" else list(reversed(self.step_sequence))  # 방향에 따라 시퀀스 설정

        # PWM 듀티 사이클 설정
        self.pwm[pins[0]].ChangeDutyCycle(speed)

        if continuous: # 연속 회전: 단일 시퀀스 사이클 실행 후 반환
            for step in sequence:
                for pin, state in zip(pins, step):
                    GPIO.output(pin, state)  # 핀에 HIGH/LOW 출력
                time.sleep(STEP_DELAY) # 스텝 간 딜레이
            return  
        
        else:  # 고정 스텝 회전: 지정된 스텝 수만큼 실행
            for _ in range(steps):
                for step in sequence:
                    for pin, state in zip(pins, step):
                        GPIO.output(pin, state)  # 핀 상태 설정
                    time.sleep(STEP_DELAY)  # 스텝 간 딜레이

        print(f"Motor {motor_id} rotated {'continuously' if continuous else steps} steps, direction: {direction}, speed: {speed}%")

    def stop_motor(self, motor_id): # 모터 정지
        pins = self.motors[motor_id - 1]
        self.pwm[pins[0]].ChangeDutyCycle(0)  # PWM 정지
        for pin in pins:
            GPIO.output(pin, 0) 
        print(f"Motor {motor_id} stopped")

    def cleanup(self): # GPIO 리소스 정리
        for pwm in self.pwm.values():
            pwm.stop()  # PWM 객체 정리
        GPIO.cleanup()