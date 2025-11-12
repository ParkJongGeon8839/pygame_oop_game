import pygame
import sys
from background import Background
from player import Player
from arrow import Arrow
from song import Song

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800

class Game:
    def __init__(self):
        pygame.init()
        
        # pygame.mixer 초기화 실패해도 게임 계속 진행
        try:
            pygame.mixer.init()
            self.sound_enabled = True
        except:
            print("사운드 시스템을 사용할 수 없습니다. 무음 모드로 실행합니다.")
            self.sound_enabled = False
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("DDR Game")
        self.clock = pygame.time.Clock()

        self.state = "menu"
        self.bg = Background("images/background.jpg")
        self.player = Player()

        # 20개 노래 목록
        self.songs = [
            Song("CANON", "music/song1.mp3", 2, "images/bg_song1.jpg"),
            Song("Beethoven Virus", "music/song2.mp3", 3, "images/bg_song2.jpg"),
            Song("Get Up", "music/song3.mp3", 5, "images/bg_song3.jpg"),
            Song("Can Can", "music/song4.mp3", 4, "images/bg_song4.jpg"),
            Song("Legends Never Die", "music/song5.mp3", 3, "images/bg_song5.jpg"),
            Song("Dynamite", "music/song6.mp3", 4, "images/bg_song6.jpg"),
            Song("LOVE DIVE", "music/song7.mp3", 5, "images/bg_song7.jpg"),
            Song("Kitsch", "music/song8.mp3", 6, "images/bg_song8.jpg"),
            Song("Whiplash", "music/song9.mp3", 7, "images/bg_song9.jpg"),
            Song("Spicy", "music/song10.mp3", 8, "images/bg_song10.jpg"),
            Song("It Was Summer", "music/song11.mp3", 3, "images/bg_song11.jpg"),
            Song("Silver Scrapes", "music/song12.mp3", 4, "images/bg_song12.jpg"),
            Song("Last Christmas", "music/song13.mp3", 5, "images/bg_song13.jpg"),
            Song("Love Never Felt So Good", "music/song14.mp3", 4, "images/bg_song14.jpg"),
            Song("HAPPY", "music/song15.mp3", 6, "images/bg_song15.jpg"),
            Song("Because It’s Christmas", "music/song16.mp3", 7, "images/bg_song16.jpg"),
            Song("Winter Confession", "music/song17.mp3", 5, "images/bg_song17.jpg"),
            Song("Thank You for Being Born", "music/song18.mp3", 8, "images/bg_song18.jpg"),
            Song("Soda Pop", "music/song19.mp3", 9, "images/bg_song19.jpg"),
            Song("HOME SWEET HOME", "music/song20.mp3", 10, "images/bg_song20.jpg"),
        ]
        
        # 판정 라인 이미지 로드
        self.judgement_images = {}
        try:
            self.judgement_images = {
                "left": pygame.transform.scale(
                    pygame.image.load("images/game_left.png"), 
                    (Arrow.ARROW_SIZE, Arrow.ARROW_SIZE)
                ),
                "down": pygame.transform.scale(
                    pygame.image.load("images/game_up.png"),
                    (Arrow.ARROW_SIZE, Arrow.ARROW_SIZE)
                ),
                "center": pygame.transform.scale(
                    pygame.image.load("images/game_center.png"), 
                    (Arrow.ARROW_SIZE, Arrow.ARROW_SIZE)
                ),
                "up": pygame.transform.scale(
                    pygame.image.load("images/game_down.png"),
                    (Arrow.ARROW_SIZE, Arrow.ARROW_SIZE)
                ),
                "right": pygame.transform.scale(
                    pygame.image.load("images/game_right.png"), 
                    (Arrow.ARROW_SIZE, Arrow.ARROW_SIZE)
                ),
            }
        except Exception as e:
            print(f"판정 라인 이미지 로드 실패: {e}")
            # 기본 도형으로 대체 가능하도록 준비
        
        self.current_song = None
        self.current_difficulty = None
        self.current_speed = 1
        self.arrows = []
        self.timer = 0
        self.spawn_counter = 0
        self.pattern_index = 0
        self.current_pattern = []
        self.song_end_timer = -1
        
        self.selected_song_index = 0
        self.selected_difficulty_index = 0
        self.selected_speed_index = 0
        
        self.song_backgrounds = {}
        self.preview_song_index = -1

    def load_song_background(self, index):
        """곡 배경 이미지 로드 (캐싱)"""
        if index not in self.song_backgrounds:
            try:
                img = pygame.image.load(self.songs[index].background_image)
                self.song_backgrounds[index] = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except:
                self.song_backgrounds[index] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                self.song_backgrounds[index].fill((30, 30, 50))
        return self.song_backgrounds[index]

    def main_menu(self):
        font_title = pygame.font.SysFont(None, 100)
        font_sub = pygame.font.SysFont(None, 50)
        
        self.screen.fill((20, 20, 40))
        
        title = font_title.render("♪ DDR GAME ♪", True, (255, 100, 255))
        subtitle = font_sub.render("Press ENTER to Start", True, (255, 255, 255))
        
        self.screen.blit(title, (title.get_rect(center=(SCREEN_WIDTH//2, 250))))
        self.screen.blit(subtitle, (subtitle.get_rect(center=(SCREEN_WIDTH//2, 400))))
        
        # 사운드 상태 표시
        if not self.sound_enabled:
            sound_warning = pygame.font.SysFont(None, 35).render(
                "⚠ Sound System Unavailable - Silent Mode", 
                True, (255, 200, 100)
            )
            self.screen.blit(sound_warning, 
                           (sound_warning.get_rect(center=(SCREEN_WIDTH//2, 500))))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.preview_song_index = -1
                self.state = "select_song"

    def select_song_screen(self):
        """펌프 스타일 곡 선택 화면"""
        if self.sound_enabled and self.preview_song_index != self.selected_song_index:
            self.preview_song_index = self.selected_song_index
            song = self.songs[self.selected_song_index]
            song.load_music()
            song.play_music()
        
        font_title = pygame.font.SysFont(None, 80)
        font_info = pygame.font.SysFont(None, 50)
        font_sub = pygame.font.SysFont(None, 35)
        
        bg_img = self.load_song_background(self.selected_song_index)
        self.screen.blit(bg_img, (0, 0))
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        info_box_width = 900
        info_box_height = 400
        info_box_x = (SCREEN_WIDTH - info_box_width) // 2
        info_box_y = 150
        
        info_surface = pygame.Surface((info_box_width, info_box_height))
        info_surface.set_alpha(200)
        info_surface.fill((20, 20, 40))
        self.screen.blit(info_surface, (info_box_x, info_box_y))
        
        pygame.draw.rect(self.screen, (255, 200, 100), 
                        (info_box_x, info_box_y, info_box_width, info_box_height), 5)
        
        song = self.songs[self.selected_song_index]
        
        title = font_title.render(song.title, True, (255, 255, 100))
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, info_box_y + 80))
        self.screen.blit(title, title_rect)
        
        difficulties = ["Easy", "Normal", "Hard"]
        diff_y = info_box_y + 180
        
        for i, diff in enumerate(difficulties):
            total_diff = song.get_total_difficulty(diff)
            diff_text = font_info.render(
                f"{diff}: ★{total_diff}", 
                True, (100 + i*50, 255 - i*50, 100)
            )
            diff_rect = diff_text.get_rect(center=(SCREEN_WIDTH//2, diff_y + i * 60))
            self.screen.blit(diff_text, diff_rect)
        
        song_number = font_sub.render(
            f"Song {self.selected_song_index + 1} / {len(self.songs)}", 
            True, (200, 200, 200)
        )
        self.screen.blit(song_number, 
                        (song_number.get_rect(center=(SCREEN_WIDTH//2, info_box_y + 360))))
        
        arrow_font = pygame.font.SysFont(None, 100)
        if self.selected_song_index > 0:
            left_arrow = arrow_font.render("◄", True, (255, 255, 255))
            self.screen.blit(left_arrow, (50, SCREEN_HEIGHT//2 - 50))
        
        if self.selected_song_index < len(self.songs) - 1:
            right_arrow = arrow_font.render("►", True, (255, 255, 255))
            self.screen.blit(right_arrow, (SCREEN_WIDTH - 120, SCREEN_HEIGHT//2 - 50))
        
        instruction = font_sub.render("◄ ►: Select Song  |  ENTER: Choose", True, (150, 255, 255))
        self.screen.blit(instruction, 
                        (instruction.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.selected_song_index > 0:
                        self.selected_song_index -= 1
                elif event.key == pygame.K_RIGHT:
                    if self.selected_song_index < len(self.songs) - 1:
                        self.selected_song_index += 1
                elif event.key == pygame.K_RETURN:
                    if self.sound_enabled:
                        pygame.mixer.music.stop()
                    self.current_song = self.songs[self.selected_song_index]
                    self.current_song.load_music()
                    self.state = "select_difficulty"
                elif event.key == pygame.K_ESCAPE:
                    if self.sound_enabled:
                        pygame.mixer.music.stop()
                    self.preview_song_index = -1
                    self.state = "menu"

    def select_difficulty_screen(self):
        font_title = pygame.font.SysFont(None, 70)
        font_diff = pygame.font.SysFont(None, 50)
        
        self.screen.fill((20, 20, 40))
        
        title = font_title.render(f"♪ {self.current_song.title}", True, (255, 200, 100))
        self.screen.blit(title, (title.get_rect(center=(SCREEN_WIDTH//2, 80))))
        
        subtitle = font_diff.render("SELECT DIFFICULTY", True, (200, 200, 200))
        self.screen.blit(subtitle, (subtitle.get_rect(center=(SCREEN_WIDTH//2, 150))))
        
        difficulties = ["Easy", "Normal", "Hard"]
        colors = [(100, 255, 100), (255, 255, 100), (255, 100, 100)]
        
        for i, diff in enumerate(difficulties):
            total_diff = self.current_song.get_total_difficulty(diff)
            color = colors[i] if i == self.selected_difficulty_index else (150, 150, 150)
            text = font_diff.render(
                f"→ {diff} [★{total_diff}]" if i == self.selected_difficulty_index else f"  {diff} [★{total_diff}]", 
                True, color
            )
            self.screen.blit(text, (text.get_rect(center=(SCREEN_WIDTH//2, 250 + i * 80))))
        
        instruction = font_diff.render("↑↓: Select | ENTER: Next | ESC: Back", True, (150, 150, 255))
        self.screen.blit(instruction, (instruction.get_rect(center=(SCREEN_WIDTH//2, 600))))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_difficulty_index = (self.selected_difficulty_index - 1) % 3
                elif event.key == pygame.K_DOWN:
                    self.selected_difficulty_index = (self.selected_difficulty_index + 1) % 3
                elif event.key == pygame.K_RETURN:
                    self.current_difficulty = ["Easy", "Normal", "Hard"][self.selected_difficulty_index]
                    self.state = "select_speed"
                elif event.key == pygame.K_ESCAPE:
                    self.state = "select_song"

    def select_speed_screen(self):
        font_title = pygame.font.SysFont(None, 70)
        font_speed = pygame.font.SysFont(None, 50)
        font_desc = pygame.font.SysFont(None, 35)
        
        self.screen.fill((20, 20, 40))
        
        title = font_title.render(f"♪ {self.current_song.title}", True, (255, 200, 100))
        self.screen.blit(title, (title.get_rect(center=(SCREEN_WIDTH//2, 80))))
        
        subtitle = font_speed.render("SELECT SPEED", True, (200, 200, 200))
        self.screen.blit(subtitle, (subtitle.get_rect(center=(SCREEN_WIDTH//2, 150))))
        
        speeds = [1, 2, 3]
        speed_names = ["1x (Normal)", "2x (Fast)", "3x (Ultra Fast)"]
        colors = [(100, 255, 100), (255, 255, 100), (255, 100, 100)]
        descriptions = [
            "Standard speed",
            "+50% more arrows!",
            "+100% more arrows!!"
        ]
        
        for i, (speed, name) in enumerate(zip(speeds, speed_names)):
            color = colors[i] if i == self.selected_speed_index else (150, 150, 150)
            
            text = font_speed.render(
                f"→ {name}" if i == self.selected_speed_index else f"  {name}", 
                True, color
            )
            self.screen.blit(text, (text.get_rect(center=(SCREEN_WIDTH//2, 250 + i * 100))))
            
            desc = font_desc.render(descriptions[i], True, (180, 180, 180))
            self.screen.blit(desc, (desc.get_rect(center=(SCREEN_WIDTH//2, 290 + i * 100))))
        
        instruction = font_speed.render("↑↓: Select | ENTER: Start! | ESC: Back", True, (150, 150, 255))
        self.screen.blit(instruction, (instruction.get_rect(center=(SCREEN_WIDTH//2, 600))))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_speed_index = (self.selected_speed_index - 1) % 3
                elif event.key == pygame.K_DOWN:
                    self.selected_speed_index = (self.selected_speed_index + 1) % 3
                elif event.key == pygame.K_RETURN:
                    self.current_speed = speeds[self.selected_speed_index]
                    self.start_game()
                elif event.key == pygame.K_ESCAPE:
                    self.state = "select_difficulty"

    def start_game(self):
        """게임 시작 준비"""
        self.player = Player()
        self.arrows = []
        self.timer = 0
        self.spawn_counter = 0
        self.pattern_index = 0
        self.song_end_timer = -1
        self.pattern_complete = False
        self.game_start_time = pygame.time.get_ticks()
        self.game_started = False
        
        self.current_pattern = self.current_song.generate_pattern(
            self.current_difficulty, 
            self.current_speed
        )
        
        try:
            self.bg = Background(self.current_song.background_image)
        except:
            self.bg = Background("images/background.jpg")
        
        self.current_song.play_music()
        
        self.state = "play"

    def play_game(self):
        self.bg.draw(self.screen)
        self.timer += 1
        self.spawn_counter += 1
        
        elapsed_time = (pygame.time.get_ticks() - self.game_start_time) / 1000.0
        
        if elapsed_time < (self.current_song.length - 3.0) and self.pattern_index < len(self.current_pattern):
            spawn_interval = self.current_song.get_spawn_interval(
                self.current_difficulty, 
                self.current_speed
            )
            
            if self.spawn_counter >= spawn_interval:
                pattern = self.current_pattern[self.pattern_index]
                
                if isinstance(pattern, list):
                    for direction in pattern:
                        speed = self.current_song.get_arrow_speed(self.current_speed)
                        self.arrows.append(Arrow(direction, speed))
                else:
                    speed = self.current_song.get_arrow_speed(self.current_speed)
                    self.arrows.append(Arrow(pattern, speed))
                
                self.pattern_index += 1
                self.spawn_counter = 0
                
                if not self.game_started:
                    self.game_started = True
        else:
            if not self.pattern_complete:
                self.pattern_complete = True
                self.song_end_timer = 120

        for arrow in self.arrows[:]:
            arrow.update()
            arrow.draw(self.screen)

        directions = ["left", "down", "center", "up", "right"]
        
        for direction in directions:
            x = Arrow.positions[direction]
            y = Arrow.JUDGEMENT_LINE
            if direction in self.judgement_images:
                img = self.judgement_images[direction]
                rect = img.get_rect(center=(x, y))
                self.screen.blit(img, rect)

        if self.game_started:
            self.player.handle_input(self.arrows)
            self.player.check_missed_arrows(self.arrows)

        self.draw_ui()

        if not self.player.is_alive:
            self.current_song.stop_music()
            self.state = "gameover"

        if self.pattern_complete and self.song_end_timer > 0:
            self.song_end_timer -= 1
            if self.song_end_timer == 0:
                self.current_song.stop_music()
                if self.player.is_alive:
                    self.state = "result"

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.current_song.stop_music()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.current_song.stop_music()
                self.state = "menu"

    def draw_ui(self):
        """게임 UI 표시"""
        font_large = pygame.font.SysFont(None, 50)
        font_small = pygame.font.SysFont(None, 30)
        
        hp_bar_width = 600
        hp_bar_height = 40
        hp_bar_x = (SCREEN_WIDTH - hp_bar_width) // 2
        hp_bar_y = 20
        
        pygame.draw.rect(self.screen, (50, 50, 50), 
                        (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))
        
        hp_percentage = self.player.hp / self.player.max_hp
        current_hp_width = int(hp_bar_width * hp_percentage)
        
        if hp_percentage > 0.6:
            hp_color = (100, 255, 100)
        elif hp_percentage > 0.3:
            hp_color = (255, 255, 100)
        else:
            hp_color = (255, 100, 100)
        
        pygame.draw.rect(self.screen, hp_color, 
                        (hp_bar_x, hp_bar_y, current_hp_width, hp_bar_height))
        
        pygame.draw.rect(self.screen, (255, 255, 255), 
                        (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), 3)
        
        if self.player.combo > 0:
            combo_text = font_small.render(f"Combo: {self.player.combo}", True, (255, 150, 0))
            self.screen.blit(combo_text, (SCREEN_WIDTH - 200, 20))
        
        speed_text = font_small.render(f"{self.current_speed}x", True, (150, 255, 255))
        self.screen.blit(speed_text, (20, 20))
        
        if self.player.judgement_timer > 0:
            judgement_colors = {
                "Perfect": (255, 100, 255),
                "Great": (100, 255, 100),
                "Good": (255, 255, 100),
                "Miss": (255, 50, 50)
            }
            color = judgement_colors.get(self.player.last_judgement, (255, 255, 255))
            judgement_text = font_large.render(self.player.last_judgement, True, color)
            self.screen.blit(judgement_text, (judgement_text.get_rect(center=(SCREEN_WIDTH//2, 400))))

    def show_result(self):
        """결과 화면"""
        font_title = pygame.font.SysFont(None, 80)
        font_text = pygame.font.SysFont(None, 40)
        
        self.screen.fill((20, 20, 40))
        
        title = font_title.render("🎉 CLEAR! 🎉", True, (255, 200, 100))
        self.screen.blit(title, (title.get_rect(center=(SCREEN_WIDTH//2, 100))))
        
        info = font_text.render(
            f"{self.current_difficulty} | {self.current_speed}x Speed", 
            True, (200, 200, 255)
        )
        self.screen.blit(info, (info.get_rect(center=(SCREEN_WIDTH//2, 160))))
        
        results = [
            f"Final Score: {self.player.score}",
            f"Max Combo: {self.player.max_combo}",
            f"Accuracy: {self.player.get_accuracy():.1f}%",
            "",
            f"Perfect: {self.player.perfect_count}",
            f"Great: {self.player.great_count}",
            f"Good: {self.player.good_count}",
            f"Miss: {self.player.miss_count}",
        ]
        
        for i, line in enumerate(results):
            text = font_text.render(line, True, (255, 255, 255))
            self.screen.blit(text, (text.get_rect(center=(SCREEN_WIDTH//2, 230 + i * 45))))
        
        instruction = font_text.render("Press ENTER to continue", True, (150, 150, 255))
        self.screen.blit(instruction, (instruction.get_rect(center=(SCREEN_WIDTH//2, 620))))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = "menu"
    
    def show_gameover(self):
        """게임 오버 화면"""
        font_title = pygame.font.SysFont(None, 100)
        font_text = pygame.font.SysFont(None, 45)
        
        self.screen.fill((40, 20, 20))
        
        title = font_title.render("GAME OVER", True, (255, 100, 100))
        self.screen.blit(title, (title.get_rect(center=(SCREEN_WIDTH//2, 180))))
        
        subtitle = font_text.render("HP depleted!", True, (255, 150, 150))
        self.screen.blit(subtitle, (subtitle.get_rect(center=(SCREEN_WIDTH//2, 260))))
        
        results = [
            f"Final Score: {self.player.score}",
            f"Max Combo: {self.player.max_combo}",
            f"Perfect: {self.player.perfect_count} | Great: {self.player.great_count}",
            f"Good: {self.player.good_count} | Miss: {self.player.miss_count}",
        ]
        
        for i, line in enumerate(results):
            text = font_text.render(line, True, (255, 255, 255))
            self.screen.blit(text, (text.get_rect(center=(SCREEN_WIDTH//2, 350 + i * 50))))
        
        instruction = font_text.render("Press ENTER to continue", True, (150, 150, 255))
        self.screen.blit(instruction, (instruction.get_rect(center=(SCREEN_WIDTH//2, 600))))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = "menu"

    def run(self):
        while True:
            if self.state == "menu":
                self.main_menu()
            elif self.state == "select_song":
                self.select_song_screen()
            elif self.state == "select_difficulty":
                self.select_difficulty_screen()
            elif self.state == "select_speed":
                self.select_speed_screen()
            elif self.state == "play":
                self.play_game()
            elif self.state == "result":
                self.show_result()
            elif self.state == "gameover":
                self.show_gameover()

            self.clock.tick(60)