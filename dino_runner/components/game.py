import pygame
from dino_runner.utils.constants import BG,ICON, RUNNING,SCREEN_HEIGHT,SCREEN_WIDTH,TITLE,FPS
from dino_runner.components.dinosaur.dinosaur import Dinosaur
from dino_runner.components.obtacles.obstaclemanager import ObstacleManager
from dino_runner.components.menu_score.text_utils import *
from dino_runner.components.player_hearts.PlayerHeartManager import PlayerHeartsManager
from dino_runner.components.powerups.powerupmanager import PowerUpManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) 
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed=20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()

        self.points = 0
        self.running = True


        self.death_count =0
        self.player_heart_manager = PlayerHeartsManager()
        self.power_up_manager = PowerUpManager()

    def run(self):
        self.obstacle_manager.reset_obstacles(self)
        self.player_heart_manager.reset_hearts()
        self.power_up_manager.reset_power_ups(self.points)
        self.playing = True
        while self.playing:
            self.events()
            self.updates()
            self.draw()

    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing=False
                self.running=False

    def updates(self):
        user_input=pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.points,self.game_speed,self.player)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255,255,255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score()       
        self.player_heart_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_with =BG.get_width()
        self.screen.blit(BG,(self.x_pos_bg,self.y_pos_bg))
        self.screen.blit(BG,(image_with+self.x_pos_bg,self.y_pos_bg))
        if self.x_pos_bg<=-image_with:
            self.screen.blit(BG,(image_with+self.x_pos_bg,self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def score(self):
        self.points = self.points + 1
        # hacemos que el juego aumente de velocidad
        if self.points % 100 == 0:
            self.game_speed = self.game_speed + 1
        
        # imprimimos el score
        score, score_rect = get_score_element(self.points)
        self.screen.blit(score,score_rect)
        self.player.check_invincibility(self.screen)


    def show_menu(self):
        self.running = True
        white_color =(255,255,255)
        self.screen.fill(white_color)

        self.print_menu_elements(self.death_count)

        pygame.display.update()

        self.handle_key_events_on_menu()

    def print_menu_elements(self,death_count=0):

        half_screen_height = SCREEN_HEIGHT //2
        half_screen_width = SCREEN_WIDTH //2

        if death_count == 0:
            text,text_rect=get_centerd_message("press any key to start")
            self.screen.blit(text,text_rect)
        elif death_count >0:
            text,text_rect = get_centerd_message("press any key to restard")
            score,score_rect =get_centerd_message("your score:" + str(self.points), height = half_screen_height+50)
            self.screen.blit(score,score_rect)
            self.screen.blit(text,text_rect)

        self.screen.blit(RUNNING[0], (half_screen_width-20 , half_screen_height-140))

    def handle_key_events_on_menu(self):
        
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                print("dino: goood bay¡¡¡")
                self.running= False
                self.playing= False
                pygame.display.quit()
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                self.__init__()
                self.run()

                

