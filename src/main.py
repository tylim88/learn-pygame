import pygame
from sys import exit


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("Runner")
    clock = pygame.time.Clock()
    test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
    game_active = True
    start_time = 0
    current_time = 0

    sky_surface = pygame.image.load("graphics/Sky.png").convert()
    ground_surface = pygame.image.load("graphics/ground.png").convert()

    snail_surf = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
    snail_rect = snail_surf.get_rect(bottomright=(600, 300))

    player_surf = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
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

    def display_score(**kwarg):
        score_surface = test_font.render(
            f"Score: {int(current_time / 1000)}", False, "Black"
        )
        score_rect = score_surface.get_rect(**kwarg)
        screen.blit(score_surface, score_rect)

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
                snail_rect.left = 800
            if game_active:
                if player_rect.bottom >= 300:
                    if (
                        event.type == pygame.MOUSEBUTTONDOWN
                        and player_rect.collidepoint(event.pos)
                    ):
                        player_gravity = -20

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        player_gravity = -20
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        game_active = True
                        snail_rect.left = 800
                        start_time = pygame.time.get_ticks()

        if game_active:
            screen.blit(sky_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))

            current_time = pygame.time.get_ticks() - start_time
            display_score(center=(400, 50))

            snail_rect.x -= 4
            if snail_rect.right <= 0:
                snail_rect.left = 800

            screen.blit(snail_surf, snail_rect)

            # player
            player_gravity += 1
            player_rect.y += player_gravity
            if player_rect.bottom >= 300:
                player_rect.bottom = 300
            screen.blit(player_surf, player_rect)

            # collision
            if snail_rect.colliderect(player_rect):
                game_active = False
        else:
            screen.fill((94, 129, 162))
            screen.blit(player_stand, player_stand_rect)

            display_score(topleft=(0, 0))
            screen.blit(title_surface, title_rect)
            screen.blit(start_surface, start_rect)

        pygame.display.update()
        clock.tick(60)
