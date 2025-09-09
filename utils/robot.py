import math
import pygame
from utils.fsm import State, Event, transition

class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.state = State.FORWARD
        self.event = Event.NONE_ON_LINE
        self.speed = 1.2
        self.theta = 0  

    def get_sensors(self):
        offset = 15
        side = 20

        front_x = self.x + math.cos(self.theta) * offset
        front_y = self.y + math.sin(self.theta) * offset

        left_angle = self.theta - math.pi / 6
        right_angle = self.theta + math.pi / 6

        left_sensor = (
            int(front_x + math.cos(left_angle) * side),
            int(front_y + math.sin(left_angle) * side),
        )
        right_sensor = (
            int(front_x + math.cos(right_angle) * side),
            int(front_y + math.sin(right_angle) * side),
        )
        return left_sensor, right_sensor

    def update_state(self, left_on_line, right_on_line):
        # tentukan event
        if left_on_line and right_on_line:
            event = Event.BOTH_ON_LINE
        elif left_on_line:
            event = Event.LEFT_ON_LINE
        elif right_on_line:
            event = Event.RIGHT_ON_LINE
        else:
            event = Event.NONE_ON_LINE

        self.event = event
        
        self.state = transition(self.state, event)

    def move(self):
        if self.state == State.FORWARD:
            self.x += math.cos(self.theta) * self.speed
            self.y += math.sin(self.theta) * self.speed
        elif self.state == State.TURN_LEFT:
            self.theta -= 0.05
            self.x += math.cos(self.theta) * self.speed
            self.y += math.sin(self.theta) * self.speed
        elif self.state == State.TURN_RIGHT:
            self.theta += 0.05
            self.x += math.cos(self.theta) * self.speed
            self.y += math.sin(self.theta) * self.speed

    def draw(self, screen):
        # body
        pygame.draw.circle(screen, (0, 180, 255), (int(self.x), int(self.y)), self.radius)

        # arah depan
        front_x = self.x + math.cos(self.theta) * (self.radius + 15)
        front_y = self.y + math.sin(self.theta) * (self.radius + 15)
        pygame.draw.line(screen, (50, 50, 50), (self.x, self.y), (front_x, front_y), 3)

        # sensor
        left, right = self.get_sensors()
        pygame.draw.circle(screen, (255, 50, 50), left, 6)   # kiri
        pygame.draw.circle(screen, (50, 255, 50), right, 6)  # kanan

        # roda kiri & kanan
        wheel_offset = self.radius - 4
        wheel_length = 15
        wheel_width = 6
        perp_angle = self.theta + math.pi / 2

        left_wheel_center = (
            int(self.x + math.cos(perp_angle) * wheel_offset),
            int(self.y + math.sin(perp_angle) * wheel_offset)
        )
        
        right_wheel_center = (
            int(self.x - math.cos(perp_angle) * wheel_offset),
            int(self.y - math.sin(perp_angle) * wheel_offset)
        )

        left_surf = pygame.Surface((wheel_length, wheel_width), pygame.SRCALPHA)
        right_surf = pygame.Surface((wheel_length, wheel_width), pygame.SRCALPHA)
        pygame.draw.rect(left_surf, (0, 0, 0), (0, 0, wheel_length, wheel_width))
        pygame.draw.rect(right_surf, (0, 0, 0), (0, 0, wheel_length, wheel_width))

        left_rot = pygame.transform.rotate(left_surf, -math.degrees(self.theta))
        right_rot = pygame.transform.rotate(right_surf, -math.degrees(self.theta))

        screen.blit(left_rot, left_rot.get_rect(center=left_wheel_center))
        screen.blit(right_rot, right_rot.get_rect(center=right_wheel_center))
