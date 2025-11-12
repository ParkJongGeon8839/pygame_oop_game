import pygame

class Arrow:
    # 클래스 변수는 한 번만 로드
    arrow_images = None
    
    # 판정 라인 위치 (위쪽으로 더 올림)
    JUDGEMENT_LINE = 80
    
    # 화살표 크기 (조금 작게)
    ARROW_SIZE = 100
    
    # 화면 중앙 기준으로 5키 위치 설정 (1200x700 기준)
    positions = {
        "left": 300,    # 왼쪽
        "down": 450,    # 왼쪽-아래
        "center": 600,  # 중앙
        "up": 750,      # 오른쪽-위
        "right": 900    # 오른쪽
    }

    @classmethod
    def load_images(cls):
        """이미지 한 번만 로드 및 리사이즈 - UP/DOWN 교체"""
        if cls.arrow_images is None:
            cls.arrow_images = {
                "left": pygame.transform.scale(
                    pygame.image.load("images/bg_left.png"), 
                    (cls.ARROW_SIZE, cls.ARROW_SIZE)
                ),
                "down": pygame.transform.scale(
                    pygame.image.load("images/bg_up.png"),  # DOWN과 UP 교체
                    (cls.ARROW_SIZE, cls.ARROW_SIZE)
                ),
                "center": pygame.transform.scale(
                    pygame.image.load("images/bg_center.png"), 
                    (cls.ARROW_SIZE, cls.ARROW_SIZE)
                ),
                "up": pygame.transform.scale(
                    pygame.image.load("images/bg_down.png"),  # UP과 DOWN 교체
                    (cls.ARROW_SIZE, cls.ARROW_SIZE)
                ),
                "right": pygame.transform.scale(
                    pygame.image.load("images/bg_right.png"), 
                    (cls.ARROW_SIZE, cls.ARROW_SIZE)
                )
            }

    def __init__(self, direction, speed):
        Arrow.load_images()
        self.direction = direction
        self.image = Arrow.arrow_images[direction]
        self.speed = speed
        self.hit = False
        
        # 화면 아래에서 시작
        self.rect = self.image.get_rect(center=(Arrow.positions[direction], 750))

    def update(self):
        # 위로 이동
        self.rect.y -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def is_in_judgement_zone(self):
        """판정 영역 내에 있는지 확인 (범위 확대)"""
        return 40 < self.rect.centery < 160  # 판정 라인 ±60 픽셀 (더 넓게)
    
    def get_judgement_accuracy(self):
        """정확도 계산 (판정 범위 완화 - 90% 정도 일치)"""
        distance = abs(self.rect.centery - Arrow.JUDGEMENT_LINE)
        if distance <= 25:  # 이전 15 -> 25
            return "Perfect", 100
        elif distance <= 45:  # 이전 30 -> 45
            return "Great", 50
        elif distance <= 60:  # 이전 40 -> 60
            return "Good", 25
        else:
            return None, 0