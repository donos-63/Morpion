import os
import pygame


class SongManager():
    __instance = None

    def __init__(self, play_song) -> None:
        self.__play_song = play_song

    def activate_songs(self, activate):
        '''
            activate songs in the game
        '''
        self.__play_song = activate

    def get_instance():
        '''
            singleton
        '''
        if(SongManager.__instance == None):
            SongManager.__instance = SongManager(False)
        
        return SongManager.__instance

    def user_play_notification(self, player):
        '''
            notification when user plays
        '''
        if not self.__play_song:
            return

        effect =  pygame.mixer.Sound(os.path.join('songs', player+'.wav'))
        effect.play()

    def menu_song(self):
        '''
            song played in menu
        '''
        if not self.__play_song:
            return

        pygame.mixer.music.load(os.path.join('songs', 'main_menu.mp3'))
        pygame.mixer.music.play(-1)


    def warning_alert(self):
        '''
            notification played for warnings
        '''
        if not self.__play_song:
            return

        effect =  pygame.mixer.Sound(os.path.join('songs', 'error.mp3'))
        effect.play()

    def fight(self):
        '''
            song played during party
        '''
        if not self.__play_song:
            return
        pygame.mixer.music.load(os.path.join('songs', 'fight.mp3'))
        pygame.mixer.music.play(-1)

    def end_of_party(self):
        '''
            song played at end of party
        '''
        if not self.__play_song:
            return
        
        pygame.mixer.music.load(os.path.join('songs', 'conclusion.mp3'))
        pygame.mixer.music.play(0)

    def game_over(self, winner):
        '''
            notification when party ended
        '''
        if not self.__play_song:
            return

        pygame.mixer.music.stop()
        if winner:
            effect =  pygame.mixer.Sound(os.path.join('songs', 'win_party.mp3'))        
        else:
            effect =  pygame.mixer.Sound(os.path.join('songs', 'eureka.mp3'))
        effect.play()