import pygame
from sys import exit
from random import randint, choice


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "fly":
            fly_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            fly_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(
            "graphics/Player/player_walk_1.png"
        ).convert_alpha()
        player_walk_2 = pygame.image.load(
            "graphics/Player/player_walk_2.png"
        ).convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -25
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("Runner")
    clock = pygame.time.Clock()
    test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
    game_active = True
    start_time = 0
    current_time = 0
    bg_music = pygame.mixer.Sound("audio/music.wav")
    bg_music.set_volume(0.3)
    bg_music.play(loops=-1)

    # Groups
    player = pygame.sprite.GroupSingle()
    player.add(Player())

    obstacle_group = pygame.sprite.Group()

    sky_surface = pygame.image.load("graphics/Sky.png").convert()
    ground_surface = pygame.image.load("graphics/ground.png").convert()

    # Obstacle
    snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
    snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
    snail_frames = [snail_frame_1, snail_frame_2]
    snail_frame_index = 0
    snail_surf = snail_frames[snail_frame_index]

    fly_frame_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
    fly_frame_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
    fly_frames = [fly_frame_1, fly_frame_2]
    fly_frame_index = 0
    fly_surf = fly_frames[fly_frame_index]

    obstacle_rect_list = []

    player_walk_1 = pygame.image.load(
        "graphics/Player/player_walk_1.png"
    ).convert_alpha()
    player_walk_2 = pygame.image.load(
        "graphics/Player/player_walk_2.png"
    ).convert_alpha()
    player_walk = [player_walk_1, player_walk_2]
    player_index = 0
    player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()

    player_surf = player_walk[player_index]
    player_rect = player_surf.get_rect(midbottom=(80, 300))
    player_gravity = 0

    # Intro Screen
    player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
    player_stand_rect = player_stand.get_rect(center=(400, 200))

    # title
    title_surface = test_font.render(
        "Runner",
        False,
        "Black",
    )
    title_rect = title_surface.get_rect(center=(400, 50))

    # start
    start_surface = test_font.render(
        "Press Space Bar to Start",
        False,
        "Black",
    )
    start_rect = start_surface.get_rect(center=(400, 350))

    # timer
    obstacle_time = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_time, 1500)

    snail_animation_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(snail_animation_timer, 500)

    fly_animation_timer = pygame.USEREVENT + 3
    pygame.time.set_timer(fly_animation_timer, 200)

    def display_score(**kwarg):
        score_surface = test_font.render(
            f"Score: {int(current_time / 1000)}", False, "Black"
        )
        score_rect = score_surface.get_rect(**kwarg)
        screen.blit(score_surface, score_rect)

    def obstacle_movement(obstacle_list):
        if obstacle_list:
            for obstacle_rect in obstacle_list:
                obstacle_rect.x -= 5

                if obstacle_rect.bottom == 300:
                    screen.blit(snail_surf, obstacle_rect)
                else:
                    screen.blit(fly_surf, obstacle_rect)

            obstacle_list = [
                obstacle for obstacle in obstacle_list if obstacle.x > -100
            ]

        return obstacle_list

    def collisions(player, obstacles):
        if obstacles:
            for obstacle_rect in obstacles:
                if player.colliderect(obstacle_rect):
                    return False
        return True

    def player_animation():
        global player_surf, player_index
        # play walking animation if the player is on floor
        # display the jump surface when player is not on floor
        if player_rect.bottom < 300:
            player_surf = player_jump
        else:
            player_index += 0.1
            if player_index >= len(player_walk):
                player_index = 0
            player_surf = player_walk[int(player_index)]

    def collision_sprite():
        if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
            obstacle_group.empty()
            return False
        return True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # opposite of pygame.init
                exit()
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                and game_active == False
            ):
                game_active = True

            if game_active:
                if player_rect.bottom >= 300:
                    if (
                        event.type == pygame.MOUSEBUTTONDOWN
                        and player_rect.collidepoint(event.pos)
                    ):
                        player_gravity = -25

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        player_gravity = -25
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        game_active = True
                        start_time = pygame.time.get_ticks()
                        current_time = pygame.time.get_ticks()
                if event.type == obstacle_time:
                    obstacle_group.add(
                        Obstacle(choice(["fly", "snail", "snail", "snail"]))
                    )
                    # if randint(0, 2):
                    #     obstacle_rect_list.append(
                    #         snail_surf.get_rect(bottomright=(randint(900, 1100), 300))
                    #     )
                    # else:
                    #     obstacle_rect_list.append(
                    #         fly_surf.get_rect(bottomright=(randint(900, 1100), 210))
                    #     )
                if event.type == snail_animation_timer:
                    if snail_frame_index == 0:
                        snail_frame_index = 1
                    else:
                        snail_frame_index = 0
                    snail_surf = snail_frames[snail_frame_index]
                    if fly_frame_index == 0:
                        fly_frame_index = 1
                    else:
                        fly_frame_index = 0
                    fly_surf = fly_frames[fly_frame_index]

        if game_active:
            screen.blit(sky_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))

            current_time = pygame.time.get_ticks() - start_time
            display_score(center=(400, 50))

            # player
            # player_gravity += 1
            # player_rect.y += player_gravity
            # if player_rect.bottom >= 300:
            #     player_rect.bottom = 300
            # player_animation()
            # screen.blit(player_surf, player_rect)

            player.draw(screen)
            player.update()

            obstacle_group.draw(screen)
            obstacle_group.update()

            # Obstacle movement
            # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

            # collision
            game_active = collision_sprite()

        else:
            screen.fill((94, 129, 162))
            screen.blit(player_stand, player_stand_rect)
            obstacle_rect_list.clear()
            player_rect.midbottom = (80, 300)
            player_gravity = 0
            start_time = pygame.time.get_ticks()
            display_score(topleft=(0, 0))
            screen.blit(title_surface, title_rect)
            screen.blit(start_surface, start_rect)

        pygame.display.update()
        clock.tick(60)
