import pygame

class Arrow:
    # 클래스 변수는 한 번만 로드
    arrow_images = None
    
    # 판정 라인 위치 (위쪽)
    JUDGEMENT_LINE = 100
    
    # 화살표 크기 (2배로 크게)
    ARROW_SIZE = 130
    
    # 화면 중앙 기준으로 화살표 위치 설정 (1200x700 기준)
    positions = {
        "left": 450,   # 중앙(600) - 150
        "down": 550,   # 중앙(600) - 50
        "up": 650,     # 중앙(600) + 50
        "right": 750   # 중앙(600) + 150
    }

    @classmethod
    def load_images(cls):
        """이미지 한 번만 로드 및 리사이즈"""
        if cls.arrow_images is None:
            cls.arrow_images = {
                "up": pygame.transform.scale(
                    pygame.image.load("images/up.png"), 
                    (cls.ARROW_SIZE, cls.ARROW_SIZE)
                ),
                "down": pygame.transform.scale(
                    pygame.image.load("images/down.png"), 
                    (cls.ARROW_SIZE, cls.ARROW_SIZE)
                ),
                "left": pygame.transform.scale(
                    pygame.image.load("images/left.png"), 
                    (cls.ARROW_SIZE, cls.ARROW_SIZE)
                ),
                "right": pygame.transform.scale(
                    pygame.image.load("images/right.png"), 
                    (cls.ARROW_SIZE, cls.ARROW_SIZE)
                )
            }

    def __init__(self, direction, speed):
        Arrow.load_images()
        self.direction = direction
        self.image = Arrow.arrow_images[direction]
        self.speed = speed
        self.hit = False
        
        # 화면 아래에서 시작 (y=750, 화면 높이 700 기준)
        self.rect = self.image.get_rect(center=(Arrow.positions[direction], 750))

    def update(self):
        # 위로 이동 (아래에서 위로)
        self.rect.y -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def is_in_judgement_zone(self):
        """판정 영역 내에 있는지 확인"""
        return 60 < self.rect.centery < 140  # 판정 라인 ±40 픽셀
    
    def get_judgement_accuracy(self):
        """정확도 계산 (Perfect, Great, Good, Miss)"""
        distance = abs(self.rect.centery - Arrow.JUDGEMENT_LINE)
        if distance <= 15:
            return "Perfect", 100
        elif distance <= 30:
            return "Great", 50
        elif distance <= 40:
            return "Good", 25
        else:
            return None, 0