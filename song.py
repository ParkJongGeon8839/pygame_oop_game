import random
import pygame

class Song:
    def __init__(self, title, file_path, base_difficulty, background_image):
        self.title = title
        self.file_path = file_path
        self.base_difficulty = base_difficulty
        self.background_image = background_image
        self.length = 0
        
        self.difficulty_settings = {
            "Easy": {
                "pattern_density": 1.0,
                "difficulty_boost": 0
            },
            "Normal": {
                "pattern_density": 1.4,
                "difficulty_boost": 1
            },
            "Hard": {
                "pattern_density": 1.8,
                "difficulty_boost": 2
            }
        }
        
        self.speed_settings = {
            1: {
                "speed_multiplier": 1.0,
                "spawn_interval": 50,
                "arrow_increase": 1.0
            },
            2: {
                "speed_multiplier": 1.5,
                "spawn_interval": 35,
                "arrow_increase": 1.5
            },
            3: {
                "speed_multiplier": 2.0,
                "spawn_interval": 25,
                "arrow_increase": 2.0
            }
        }
    
    def load_music(self):
        """음악 로드 및 길이 가져오기"""
        try:
            pygame.mixer.music.load(self.file_path)
            sound = pygame.mixer.Sound(self.file_path)
            self.length = sound.get_length()
            del sound
        except Exception as e:
            print(f"음악 로드 실패: {e}")
            self.length = 180
    
    def play_music(self):
        """음악 재생"""
        try:
            pygame.mixer.music.play()
        except Exception as e:
            print(f"음악 재생 실패: {e}")
    
    def stop_music(self):
        """음악 정지"""
        pygame.mixer.music.stop()
    
    def get_arrow_speed(self, speed_level):
        """배속에 따른 화살표 속도"""
        base_speed = 3 + (self.base_difficulty * 0.5)
        multiplier = self.speed_settings[speed_level]["speed_multiplier"]
        return base_speed * multiplier
    
    def get_spawn_interval(self, difficulty_level, speed_level):
        """난이도와 배속에 따른 화살표 생성 간격"""
        base_interval = self.speed_settings[speed_level]["spawn_interval"]
        difficulty_factor = self.difficulty_settings[difficulty_level]["pattern_density"]
        song_factor = 1 - (self.base_difficulty * 0.05)
        
        return int(base_interval * song_factor / difficulty_factor)
    
    def get_total_difficulty(self, difficulty_level):
        """실제 난이도 표시"""
        boost = self.difficulty_settings[difficulty_level]["difficulty_boost"]
        return self.base_difficulty + boost
    
    def generate_pattern(self, difficulty_level, speed_level):
        """노래 길이 기반 패턴 생성"""
        total_diff = self.get_total_difficulty(difficulty_level)
        
        # 노래 길이에 따라 화살표 개수 계산
        arrows_per_second = 2 + (total_diff * 0.3)
        base_arrows = int(self.length * arrows_per_second)
        
        # 배속에 따라 증가
        speed_increase = self.speed_settings[speed_level]["arrow_increase"]
        density_increase = self.difficulty_settings[difficulty_level]["pattern_density"]
        
        arrow_count = int(base_arrows * speed_increase * density_increase)
        
        patterns = []
        directions = ["left", "down", "up", "right"]
        
        i = 0
        while i < arrow_count:
            # 연속 패턴 또는 단일 노트
            consecutive_chance = 0.2 + (total_diff * 0.05) + (speed_level * 0.1)
            
            if random.random() < consecutive_chance:
                direction = random.choice(directions)
                repeat_count = random.randint(2, min(3 + speed_level, 6))
                for _ in range(repeat_count):
                    if i < arrow_count:
                        patterns.append(direction)
                        i += 1
            else:
                patterns.append(random.choice(directions))
                i += 1
        
        return patterns