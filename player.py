import pygame

class Player:
    def __init__(self):
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.perfect_count = 0
        self.great_count = 0
        self.good_count = 0
        self.miss_count = 0
        
        # HP 시스템 (펌프 방식)
        self.hp = 50
        self.max_hp = 100
        self.is_alive = True
        
        # 입력 처리를 위한 이전 키 상태 (5키 - 커스텀 키)
        self.prev_keys = {
            pygame.K_v: False,      # left
            pygame.K_u: False,      # down → up 방향
            pygame.K_h: False,      # center (스페이스바 → h)
            pygame.K_r: False,      # up → down 방향
            pygame.K_m: False       # right
        }
        
        # 판정 표시용
        self.last_judgement = ""
        self.judgement_timer = 0

    def handle_input(self, arrows):
        """키 입력 처리 - 한 번 누를 때만 반응 (커스텀 5키)"""
        keys = pygame.key.get_pressed()
        key_map = {
            pygame.K_v: "left",     # V 키 → left
            pygame.K_u: "up",       # U 키 → up 방향 (원래 DOWN 키)
            pygame.K_h: "center",   # H 키 → center (원래 스페이스바)
            pygame.K_r: "down",     # R 키 → down 방향 (원래 UP 키)
            pygame.K_m: "right"     # M 키 → right
        }
        
        for key, direction in key_map.items():
            # 키를 새로 눌렀을 때만 (이전엔 안눌렀고 지금 눌림)
            if keys[key] and not self.prev_keys[key]:
                self.check_hit(direction, arrows)
            
            self.prev_keys[key] = keys[key]
        
        # 판정 표시 타이머 감소
        if self.judgement_timer > 0:
            self.judgement_timer -= 1

    def check_hit(self, direction, arrows):
        """화살표 맞추기 체크"""
        hit_arrow = None
        best_distance = float('inf')
        
        # 가장 가까운 판정 영역 내 화살표 찾기
        for arrow in arrows:
            if arrow.direction == direction and arrow.is_in_judgement_zone() and not arrow.hit:
                distance = abs(arrow.rect.centery - arrow.JUDGEMENT_LINE)
                if distance < best_distance:
                    best_distance = distance
                    hit_arrow = arrow
        
        if hit_arrow:
            judgement, points = hit_arrow.get_judgement_accuracy()
            if judgement:
                hit_arrow.hit = True
                arrows.remove(hit_arrow)
                
                # 콤보 적용
                combo_bonus = 1 + (self.combo * 0.1)
                final_points = int(points * combo_bonus)
                self.score += final_points
                self.combo += 1
                
                if self.combo > self.max_combo:
                    self.max_combo = self.combo
                
                # 통계 및 HP 처리 (펌프 방식)
                if judgement == "Perfect":
                    self.perfect_count += 1
                    self.hp = min(self.max_hp, self.hp + 2)  # HP +2
                elif judgement == "Great":
                    self.great_count += 1
                    self.hp = min(self.max_hp, self.hp + 1)  # HP +1
                elif judgement == "Good":
                    self.good_count += 1
                    # Good은 HP 변화 없음 (0)
                
                # 판정 표시
                self.last_judgement = judgement
                self.judgement_timer = 20
    
    def check_missed_arrows(self, arrows):
        """화면 밖으로 나간 화살표 체크 (Miss 처리)"""
        for arrow in arrows[:]:
            # 화살표가 위로 완전히 벗어남
            if arrow.rect.bottom < -50 and not arrow.hit:
                arrows.remove(arrow)
                self.combo = 0
                self.miss_count += 1
                self.hp = max(0, self.hp - 3)  # HP -3
                
                # 판정 표시
                self.last_judgement = "Miss"
                self.judgement_timer = 20
                
                if self.hp <= 0:
                    self.is_alive = False

    def get_accuracy(self):
        """정확도 계산"""
        total = self.perfect_count + self.great_count + self.good_count + self.miss_count
        if total == 0:
            return 100.0
        return ((self.perfect_count + self.great_count * 0.8 + self.good_count * 0.5) / total) * 100