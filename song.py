import random
import pygame

class Song:
    def __init__(self, title, file_path, base_difficulty, background_image):
        self.title = title
        self.file_path = file_path
        self.base_difficulty = base_difficulty
        self.background_image = background_image
        self.length = 0
        self.music_loaded = False  # 음악 로드 성공 여부
        
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
        """음악 로드 및 길이 가져오기 (실패해도 계속 진행)"""
        try:
            pygame.mixer.music.load(self.file_path)
            sound = pygame.mixer.Sound(self.file_path)
            self.length = sound.get_length()
            del sound
            self.music_loaded = True
            print(f"음악 로드 성공: {self.title}")
        except Exception as e:
            print(f"음악 로드 실패: {self.title} - {e}")
            print("무음 모드로 진행합니다.")
            self.length = 120  # 기본 길이 2분 (음악 없을 때)
            self.music_loaded = False
    
    def play_music(self):
        """음악 재생 (로드 성공했을 때만)"""
        if self.music_loaded:
            try:
                pygame.mixer.music.play()
            except Exception as e:
                print(f"음악 재생 실패: {e}")
        else:
            print(f"'{self.title}' 무음 모드로 플레이 중...")
    
    def stop_music(self):
        """음악 정지"""
        try:
            pygame.mixer.music.stop()
        except:
            pass
    
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
        """다양한 패턴 생성"""
        total_diff = self.get_total_difficulty(difficulty_level)
        
        arrows_per_second = 1.5 + (total_diff * 0.22)
        base_arrows = int(self.length * arrows_per_second)
        
        speed_increase = self.speed_settings[speed_level]["arrow_increase"]
        density_increase = self.difficulty_settings[difficulty_level]["pattern_density"]
        
        arrow_count = int(base_arrows * speed_increase * density_increase)
        
        patterns = []
        directions = ["left", "down", "center", "up", "right"]
        
        if difficulty_level == "Easy":
            combo_chance = 0.05
            max_combo = 2
        elif difficulty_level == "Normal":
            combo_chance = 0.10
            max_combo = 2
        else:  # Hard
            combo_chance = 0.18
            max_combo = 3
        
        combo_chance += (self.base_difficulty - 2) * 0.01
        
        i = 0
        while i < arrow_count:
            pattern_type = random.random()
            
            stair_chance = 0.08 + (total_diff * 0.008)
            if pattern_type < stair_chance and total_diff >= 4:
                if random.random() < 0.5:
                    stair = ["left", "down", "center", "up", "right"]
                else:
                    stair = ["right", "up", "center", "down", "left"]
                
                for step in stair:
                    if i < arrow_count:
                        patterns.append(step)
                        i += 1
            
            elif pattern_type < (stair_chance + combo_chance) and total_diff >= 4:
                if max_combo == 3:
                    combo_count = 2 if random.random() < 0.65 else 3
                else:
                    combo_count = 2
                
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
            
            elif pattern_type < 0.32:
                direction = random.choice(directions)
                repeat_count = random.randint(2, min(3, 2 + total_diff // 4))
                for _ in range(repeat_count):
                    if i < arrow_count:
                        patterns.append(direction)
                        i += 1
            
            elif pattern_type < 0.38 and total_diff >= 4:
                zigzag = ["left", "right", "left", "right"]
                for step in zigzag:
                    if i < arrow_count:
                        patterns.append(step)
                        i += 1
            
            elif pattern_type < 0.42 and total_diff >= 3:
                center_pattern = ["center", random.choice(["left", "right"]), "center"]
                for step in center_pattern:
                    if i < arrow_count:
                        patterns.append(step)
                        i += 1
            
            else:
                patterns.append(random.choice(directions))
                i += 1
        
        return patterns