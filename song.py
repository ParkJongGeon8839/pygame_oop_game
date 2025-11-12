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
        """다양한 패턴 생성 (전체적으로 난이도 완화)"""
        total_diff = self.get_total_difficulty(difficulty_level)
        
        # 노래 길이에 따라 화살표 개수 계산 (더 줄임)
        arrows_per_second = 1.5 + (total_diff * 0.22)  # 1.8 -> 1.5, 0.28 -> 0.22
        base_arrows = int(self.length * arrows_per_second)
        
        # 배속에 따라 증가
        speed_increase = self.speed_settings[speed_level]["arrow_increase"]
        density_increase = self.difficulty_settings[difficulty_level]["pattern_density"]
        
        arrow_count = int(base_arrows * speed_increase * density_increase)
        
        patterns = []
        directions = ["left", "down", "center", "up", "right"]
        
        # 난이도별 동시타 확률 - 전체적으로 감소
        if difficulty_level == "Easy":
            combo_chance = 0.05  # 8% -> 5%
            max_combo = 2
        elif difficulty_level == "Normal":
            combo_chance = 0.10  # 15% -> 10%
            max_combo = 2
        else:  # Hard
            combo_chance = 0.18  # 25% -> 18%
            max_combo = 3
        
        # 곡 자체 난이도에 따라 추가 보정 (더 완만하게)
        combo_chance += (self.base_difficulty - 2) * 0.01  # 1.5% -> 1%
        
        i = 0
        while i < arrow_count:
            pattern_type = random.random()
            
            # 1. 계단 패턴 (빈도 감소)
            stair_chance = 0.08 + (total_diff * 0.008)  # 더 완만하게
            if pattern_type < stair_chance and total_diff >= 4:  # 난이도 3 -> 4
                if random.random() < 0.5:
                    stair = ["left", "down", "center", "up", "right"]
                else:
                    stair = ["right", "up", "center", "down", "left"]
                
                for step in stair:
                    if i < arrow_count:
                        patterns.append(step)
                        i += 1
            
            # 2. 동시타 (UP/DOWN 동시 불가)
            elif pattern_type < (stair_chance + combo_chance) and total_diff >= 4:  # 3 -> 4
                # Hard 모드에서도 3개 동시타 확률 감소
                if max_combo == 3:
                    combo_count = 2 if random.random() < 0.65 else 3  # 50% -> 65%
                else:
                    combo_count = 2
                
                # UP과 DOWN이 동시에 나오지 않도록 필터링
                valid_combo = False
                attempts = 0
                while not valid_combo and attempts < 10:
                    combo = random.sample(directions, combo_count)
                    if not ("up" in combo and "down" in combo):
                        valid_combo = True
                    attempts += 1
                
                if valid_combo:
                    patterns.append(combo)
                    i += 1
                else:
                    patterns.append(random.choice(directions))
                    i += 1
            
            # 3. 연타 패턴 (짧게)
            elif pattern_type < 0.32:  # 0.38 -> 0.32
                direction = random.choice(directions)
                repeat_count = random.randint(2, min(3, 2 + total_diff // 4))  # 더 짧게
                for _ in range(repeat_count):
                    if i < arrow_count:
                        patterns.append(direction)
                        i += 1
            
            # 4. 지그재그 패턴 (빈도 감소)
            elif pattern_type < 0.38 and total_diff >= 4:  # 0.46 -> 0.38, 3 -> 4
                zigzag = ["left", "right", "left", "right"]
                for step in zigzag:
                    if i < arrow_count:
                        patterns.append(step)
                        i += 1
            
            # 5. 센터 중심 패턴 (빈도 감소)
            elif pattern_type < 0.42 and total_diff >= 3:  # 0.52 -> 0.42, 2 -> 3
                center_pattern = ["center", random.choice(["left", "right"]), "center"]
                for step in center_pattern:
                    if i < arrow_count:
                        patterns.append(step)
                        i += 1
            
            # 6. 일반 랜덤 (비중 증가 - 58%)
            else:
                patterns.append(random.choice(directions))
                i += 1
        
        return patterns