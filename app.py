# Importing all previous classes and relevant packages
from constants import *
from background import Background
from enemy import *
from blast import *
from bullet import *
import pyxel
from random import random


class App:
    """
    This class will define how the game works
    """
    def __init__(self):
        """
        Method creating Board object by loading all images, sounds, and features of the game
        """
        # Creating empty frame titled with the game
        pyxel.init(constants.GAME_WIDTH, constants.GAME_HEIGHT, title="1942")
        # Loading all relevant images
        pyxel.image(2).load(0, 0, "sprites.png")  # (327 x 786)
        pyxel.image(0).load(200, 200, "heart.png")  # (16 x 16)
        pyxel.image(0).load(0, 0, "playerhelix1.png")
        pyxel.image(0).load(30, 0, "playerhelix2.png")
        pyxel.image(1).load(0, 200, "regular.png")
        pyxel.image(0).load(100, 100, "red.png")
        pyxel.image(0).load(132, 132, "bombardier.png")
        pyxel.image(1).load(0, 0, "superbombardier.png")
        pyxel.image(1).load(0, 100, "1942.png")
        # Parameters of pyxel sound: bank, notes, timbre, volume, effect, and level
        # First sound: Player shooting
        pyxel.sound(0).set("a3a2c1a1", "p", "6", "s", 6)
        # Second sound: Collision blast
        pyxel.sound(1).set("a3a2c2c2", "n", "6532", "s", 10)

        """
        Game features
        @param scene: initial game mode is the starting screen
        @param score: keep track of player score 
        @param high_score: keep track of highest score
        @param frame_counter: limit duration for each game 
            since the frame count includes the game over screen
        """
        self.__scene = SCENE_TITLE
        self.__score = 0
        self.__high_score = 0
        self.__frame_counter = 0
        self.__frame_display = False
        self.__lives_left = True

        # All relevant lists that need to be interacted with
        self.__master_list = [constants.enemy_list, constants.bullet_list, constants.blast_list]

        # Generate background and player sprite
        self.__background = Background()
        self.player = Player(pyxel.width / 2, pyxel.height - 20)

        # Declaring Red enemy counter
        self.__red_generate = False
        self.__red_counter = 0

        # Run the game
        pyxel.run(self.__update, self.__draw)

    def __update(self):
        """
        First main method to run the game that records all changes and interactions between the game elements
        """
        # Option to quit game at anytime
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Constantly moving background
        self.__background.update()

        # Updating based on current scene
        if self.__scene == constants.SCENE_TITLE:
            self.__update_title_scene()
        elif self.__scene == constants.SCENE_PLAY:
            self.__update_play_scene()
        elif self.__scene == constants.SCENE_GAMEOVER:
            self.__update_gameover_scene()

    # Checks for an overlap in the position of two elements
    def __check_collision(self, a: object, b: object) -> bool:
        return a.x + a.w > b.x and b.x + b.w > a.x and a.y + a.h > b.y and b.y + b.h > a.y

    # ---------------------------- UPDATING LISTS ------------------------
    # Updates each element in a list
    def __update_list(self, a_list):
        for num in range(len(a_list)):
            for elem in a_list[num]:
                elem.update()

    # Draws each element in a list
    def __draw_list(self, a_list):
        for num in range(len(a_list)):
           for elem in a_list[num]:
                elem.draw()

    # Removes each dead element in a list
    def __cleanup_list(self, a_list):
        for num in range(len(a_list)):
            i = 0
            while i < len(a_list[num]):
                elem = a_list[num][i]
                if not elem.alive:
                    a_list[num].pop(i)
                else:
                    i += 1

    # Resets a list for the next games
    def __clear_list(self, a_list):
        for num in range(len(a_list)):
            a_list[num].clear()

    # --------------------------------------------------------------------------
    def __update_title_scene(self):
        # Before each game the only possible change from the loading screen is to start a new game
        if pyxel.btnp(pyxel.KEY_P):
            self.__scene = constants.SCENE_PLAY

    def __update_play_scene(self):
        # Activated during the game

        # _______________________________ LEVEL LENGTH _____________________________
        # Setting a maximum level length using frame_counter parameter
        self.__frame_counter += pyxel.frame_count / pyxel.frame_count
        if self.__frame_counter % constants.GAME_FRAME_LENGTH == 0:
            self.__scene = constants.SCENE_GAMEOVER

        # _____________________________ ENEMY GENERATION _____________________________
        # Generating Regular enemies
        if self.__frame_counter % 160 == 0:
            # 60% chance of generating a Regular enemy swarm
            if int(random() * 10) < 6:
                for _ in range(randint(3, 5)):
                    Regular(random() * (pyxel.width - constants.PLAYER_WIDTH),
                            (random()*30) - 3*constants.PLAYER_HEIGHT)

        # Generating Red enemies
        if self.__frame_counter % 70 == 0:
            # 40% chance of generating a Red enemy swarm
            if int(random() * 10) < 4:
                if random() > 0.5:
                    direction = True
                else:
                    direction = False
                aux2 = random() * 100
                aux3 = random() * 100
                # Swarms of 1-3
                if self.__red_counter < randint(2, 4):
                    Red(aux2, aux3, direction)
                    aux2 += randint(15, 20)
                    aux3 -= randint(20, 25)
                    self.__red_counter += 1
                else:
                    self.__red_counter = 0

        # Generating Bombardier enemies
        if self.__frame_counter % 600 == 0:
            Bombardier(0, random() * (pyxel.height / 2), self.player.x, self.player.y)

        # Generating Super Bombardier enemies
        if self.__frame_counter % 800 == 0:
            SuperBombardier((random() * pyxel.width)-(constants.SBOMB_ENEMY_WIDTH / 3), pyxel.height)

        # _____________________________ INTERACTIONS _____________________________
        # Player bullets kill the enemy
        for a in constants.enemy_list:
            for b in constants.bullet_list:
                if b.entity == "player" and self.__check_collision(a, b):
                    # Checking for BONUS for killing entire Red swarm
                    if type(a) == Red:
                        a.killed_red[1].append(1)
                        if len(a.killed_red[0]) == len(a.killed_red[1]):
                            self.__score += RED_SCORE_BONUS
                            self.player.loops_allowed += 1
                    # Personalizing blast location and score increase based on Enemy plane type
                    if a.type == "Regular":
                        a.alive = False
                        self.__score += REG_SCORE
                        constants.blast_list.append(Blast(a.x + REG_ENEMY_WIDTH / 2, a.y + REG_ENEMY_HEIGHT / 2))
                    elif a.type == "Red":
                        a.alive = False
                        self.__score += RED_SCORE
                        constants.blast_list.append(Blast(a.x + RED_ENEMY_WIDTH / 2, a.y + RED_ENEMY_HEIGHT / 2))
                    else:
                        a.lives -= 1
                        if a.type == "Bombardier":
                            self.__score += BOMB_SCORE_SHOT
                            if a.lives == 0:
                                a.alive = False
                                self.__score += BOMB_SCORE_KILL
                                constants.blast_list.append(Blast(a.x + BOMB_ENEMY_WIDTH / 2, a.y + BOMB_ENEMY_HEIGHT / 2))
                        else:
                            self.__score += SBOMB_SCORE_SHOT
                            if a.lives == 0:
                                a.alive = False
                                self.__score += SBOMB_SCORE_KILL
                                constants.blast_list.append(Blast(a.x + SBOMB_ENEMY_WIDTH / 2, a.y + SBOMB_ENEMY_HEIGHT / 2))
                    # Either way, the bullet disappears
                    b.alive = False
                    pyxel.play(1, 1)

        # Enemy bullets take player lives when not turning
        for bullet in constants.bullet_list:
            if not self.player.loop \
                    and (bullet.entity == "enemy" or bullet.entity == "enemy_red") \
                    and self.__check_collision(self.player, bullet):
                bullet.alive = False
                self.player.lives -= 1
                constants.blast_list.append(Blast(self.player.x + constants.PLAYER_WIDTH / 2,
                                        self.player.y + constants.PLAYER_HEIGHT / 2))
                pyxel.play(1, 1)

                # No lives left means the game ends
                if self.player.lives == 0:
                    self.__scene = constants.SCENE_GAMEOVER

        # Touching the enemies takes player lives when not turning
        for enemy in constants.enemy_list:
            if type(enemy) != SuperBombardier and type(enemy) != Bombardier:
                if not self.player.loop and self.__check_collision(self.player, enemy):
                    enemy.alive = False
                    self.player.lives -= 1
                    constants.blast_list.append(Blast(self.player.x + constants.PLAYER_WIDTH / 2,
                                                      self.player.y + constants.PLAYER_HEIGHT / 2))
                    pyxel.play(1, 1)
                    # No lives left means the game ends
                    if self.player.lives == 0:
                        self.__scene = SCENE_GAMEOVER

        self.player.update()
        self.__update_list(self.__master_list)
        self.__cleanup_list(self.__master_list)

    def __update_gameover_scene(self):
        # After game finishes
        self.__update_list(self.__master_list)
        # self.cleanup_list(self.master_list)
        self.__clear_list(self.__master_list)

        # Reset features
        if pyxel.btnp(pyxel.KEY_P):
            self.__scene = constants.SCENE_PLAY
            self.player.x = (constants.GAME_WIDTH / 2) + (constants.PLAYER_WIDTH / 2)
            self.player.y = constants.GAME_HEIGHT - 40
            self.__score = 0
            self.player.lives = 3
            self.player.loops_allowed = 3
            self.__frame_counter = 0
            self.__lives_left = True

            self.__clear_list(self.__master_list)

    def __draw(self):
        """
        Second main method to run the game that displays all changes and interactions between the game elements
        """
        pyxel.cls(0)

        # Constantly updating background
        self.__background.draw()

        # Updating based on current scene
        if self.__scene == constants.SCENE_TITLE:
            self.__draw_title_scene()
        elif self.__scene == constants.SCENE_PLAY:
            self.__draw_play_scene()
        elif self.__scene == constants.SCENE_GAMEOVER:
            self.__draw_gameover_scene()

    def __draw_title_scene(self):

        pyxel.blt(75, 127, 1, 0, 100, 100, 26, colkey = 0)
        pyxel.text(115, 160, "LEVEL 8", pyxel.frame_count % 16)
        pyxel.text(82, 252, "-PRESS P TO PLAY-", 13)
        # Updating high score
        if self.__score > self.__high_score:
            self.__high_score = self.__score
        pyxel.text(10, 10, "HI-SCORE %i points" % self.__high_score, 13)

    def __draw_play_scene(self):
        # Displaying sprites
        self.player.draw()
        self.__draw_list(self.__master_list)

        # Displaying important information
        if self.__frame_display:
            pyxel.text(62, 252, "-%i-" % (500 - self.__frame_counter), 13)
        pyxel.text(constants.GAME_WIDTH - 75, 20, "SCORE %i" % self.__score, 13)
        pyxel.text(constants.GAME_WIDTH - 100, constants.GAME_HEIGHT - 20, "HI-SCORE %i points" % self.__high_score, 13)
        pyxel.text(20, constants.GAME_HEIGHT - 20, "TURNS %i" % self.player.loops_allowed, 13)

        # Displaying player lives as hearts
        heart_x_shift = 10
        for i in range(self.player.lives):
            pyxel.blt(heart_x_shift, 10, 0, 200, 200, 16, 16, colkey=0)
            heart_x_shift += 20

    def __draw_gameover_scene(self):
        # Draw sprites without player plane
        self.__draw_list(self.__master_list)

        # Bonus for remaining player lives
        if self.__lives_left:
            self.__score += 20 * self.player.lives
            self.__lives_left = False

        # Updating high score and displaying own score if lower
        if self.__score > self.__high_score:
            self.__high_score = self.__score
            pyxel.text(75, 127, "NEW HIGH SCORE: %i points" % self.__high_score, 10)
        else:
            pyxel.text(75, 127, "HIGHEST SCORE: %i points" % self.__high_score, 10)
            pyxel.text(79, 135, "YOUR SCORE: %i points" % self.__high_score, 10)

        # Different message depending on whether player beat the high score or not
        if self.player.lives > 0:
            pyxel.text((GAME_WIDTH / 2) - 30, (GAME_HEIGHT / 2) - 50, "LEVEL CLEARED!", 8)
        else:
            pyxel.text((GAME_WIDTH / 2) - 20, (GAME_HEIGHT / 2) - 50, "GAME OVER", 8)

        # Option to start new game or quit
        pyxel.text(85, 222, "-PRESS P TO PLAY-", 13)
        pyxel.text(85, 232, "-PRESS Q TO EXIT-", 13)

