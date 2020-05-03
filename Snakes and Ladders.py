import pygame
import random
import time

pygame.init()
pygame.mixer.init()

# SCREEN WIDTH AND SCREEN HEIGHT :
screen_w, screen_h = 1200, 675

# CREATING THE PYGAME DISPLAY :
gameWindow = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Snakes and Ladders")

# FONT :
font1 = pygame.font.SysFont("Franklin Gothic Demi Cond", 40)
font2 = pygame.font.SysFont("Franklin Gothic Demi Cond", 35)

# CLOCK AND FPS :
fps = 60
clock = pygame.time.Clock()

# LOADING THE SNAKES AND LADDERS BOARD :
board = pygame.image.load("data/images/board.png")
board = pygame.transform.scale(board, (896, 675)).convert_alpha()

# LOGO :
logo = pygame.image.load("data/images/logo.png").convert_alpha()

# DICE IMAGES :
dice_images = []
for i in range(1, 7):
    dice_i = pygame.image.load("data/images/dice/" + str(i) + ".jpg")
    dice_i = pygame.transform.scale(dice_i, (90, 83)).convert_alpha()
    dice_images.append(dice_i)

roll_dice = []
for i in range(1, 7):
    roll_i = pygame.image.load("data/images/dice/roll/" + str(i) + ".png")
    if i % 2 != 0:
        roll_i = pygame.transform.scale(roll_i, (120, 109)).convert_alpha()
    else:
        roll_i = pygame.transform.scale(roll_i, (90, 83)).convert_alpha()
    roll_dice.append(roll_i)

# SNAKES AND LADDERS LIST IN THE GIVEN BOARD :
ladders = {3: ([[207, 580], [121, 516], [35, 452]], 21),
           8: ([[637, 580], [716, 508], [809, 452]], 30),
           58: ([[207, 260], [247, 187], [293, 132]], 77),
           75: ([[465, 132], [458, 100], [465, 68]], 86),
           80: ([[35, 132], [35, 68], [52, 4]], 100),
           28: ([[637, 452], [565, 362], [485, 272], [410, 182], [335, 92], [293, 68]], 84),
           90: ([[809, 68], [810, 36], [809, 4]], 91)
           }

snakes = {17: (
    [[293, 516], [320, 490], [360, 510], [405, 510], [465, 460], [525, 505], [570, 525], [610, 505], [637, 516]], 13),
    52: (
        [[723, 260], [742, 260], [751, 290], [718, 335], [700, 375], [754, 422], [775, 400], [729, 400], [729, 435],
         [723, 452]], 29),
    57: (
        [[293, 260], [283, 240], [233, 260], [239, 300], [247, 340], [212, 380], [167, 340], [122, 308], [88, 338],
         [68, 358], [35, 388]], 40),
    62: (
        [[121, 196], [121, 206], [136, 236], [138, 266], [103, 286], [128, 311], [148, 351], [111, 381], [131, 421],
         [121, 452]], 22),
    88: (
        [[637, 68], [652, 68], [677, 138], [647, 188], [607, 188], [537, 228], [517, 288], [467, 328], [407, 328],
         [360, 378], [340, 428], [270, 428], [220, 468], [207, 516]], 18),
    95: ([[465, 4], [480, -15], [540, 12], [570, 2], [610, -15], [660, -10], [703, 20], [720, 80], [750, 90],
          [826, 90], [816, 150], [810, 210], [809, 260]], 51),
    97: ([[293, 4], [246, -15], [212, 15], [242, 45], [250, 75], [200, 95], [150, 105], [121, 132]], 79)
}

# STARTING COORDINATES :
starting_coords = {2: [[950, 590], [1090, 590]],
                   3: [[950, 590], [1090, 590], [1020, 460]],
                   4: [[950, 590], [1090, 590], [950, 460], [1090, 460]]}


# PLAYER CLASS
class Player:
    def __init__(self, current_block, coordinates, piece, is_open):
        self.current_block = current_block
        self.coordinates = coordinates
        self.piece = piece
        self.is_open = is_open


# FUNCTION TO WRITE ON THE SCREEN
def text_on_screen(text, color, x, y, font=font1):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


# FUNCTION TO ASCEND A PLAYER OVER A LADDER :
def ascend(players, turn):
    ladder = ladders[players[turn].current_block][0]
    index = 0
    players[turn].coordinates = ladder[index]

    change = time.time()
    while index < len(ladder):
        if time.time() - change > 0.2:
            index += 1
            if index == len(ladder):
                break
            players[turn].coordinates = ladder[index]
            change = time.time()

        gameWindow.blit(board, (0, 0))
        gameWindow.blit(logo, (885, -10))
        for player in players:
            gameWindow.blit(player.piece, player.coordinates)
        clock.tick(fps)
        pygame.display.update()

    players[turn].coordinates = ladder[-1].copy()  # .copy() is necessary
    players[turn].current_block = ladders[players[turn].current_block][1]


# FUNCTION TO DESCEND A PLAYER FROM A SNAKE :
def descend(players, turn):
    snake = snakes[players[turn].current_block][0]
    index = 0
    players[turn].coordinates = snake[index]

    change = time.time()
    while index < len(snake):
        if time.time() - change > 0.2:
            index += 1
            if index == len(snake):
                break
            players[turn].coordinates = snake[index]
            change = time.time()

        gameWindow.blit(board, (0, 0))
        gameWindow.blit(logo, (885, -10))
        for player in players:
            gameWindow.blit(player.piece, player.coordinates)
        clock.tick(fps)
        pygame.display.update()

    players[turn].coordinates = snake[-1].copy()  # .copy() is necessary
    players[turn].current_block = snakes[players[turn].current_block][1]


# RECURSIVE FUNCTION TO MOVE A PLAYER :
def move_player(players, turn, dice, won):
    if players[turn].current_block + dice > 100:
        return

    if dice == 1:  # BASE CASE
        if players[turn].current_block % 10 == 0:
            players[turn].coordinates[1] -= 64
        else:
            first_digit = players[turn].current_block // 10
            if first_digit % 2 == 0:
                players[turn].coordinates[0] += 86
            else:
                players[turn].coordinates[0] -= 86
        gameWindow.blit(board, (0, 0))
        gameWindow.blit(logo, (885, -10))
        for player in players:
            gameWindow.blit(player.piece, player.coordinates)

        clock.tick(fps)
        pygame.display.update()
        players[turn].current_block += 1
        if players[turn].current_block in ladders.keys():
            ascend(players, turn)
        elif players[turn].current_block in snakes.keys():
            descend(players, turn)
        if players[turn].current_block == 100:
            won.append(turn)
            if len(won) == len(players) - 1:
                game_over(won)

    else:
        if players[turn].current_block % 10 == 0:
            players[turn].coordinates[1] -= 64
        else:
            first_digit = players[turn].current_block // 10
            if first_digit % 2 == 0:
                players[turn].coordinates[0] += 86
            else:
                players[turn].coordinates[0] -= 86
        gameWindow.blit(board, (0, 0))
        gameWindow.blit(logo, (885, -10))
        for player in players:
            gameWindow.blit(player.piece, player.coordinates)
        clock.tick(fps)
        pygame.display.update()
        players[turn].current_block += 1
        time.sleep(0.4)

        move_player(players, turn, dice - 1, won)


# FUNCTION TO CHANGE THE TURN :
def change_turn(turn, num_players):
    if turn < num_players - 1:
        return turn + 1
    else:
        return 0


# FUNCTION TO ROLL THE DICE :
def dice_roll(players):
    index = 0
    change = time.time()
    dice = random.randint(1, 6)

    while index < len(roll_dice):
        if time.time() - change > 0.2:
            index += 1
            if index == len(roll_dice):
                break
            change = time.time()
        gameWindow.fill((255, 255, 255))
        if index % 2 == 0:
            gameWindow.blit(roll_dice[index], (985, 194))
        else:
            gameWindow.blit(roll_dice[index], (1003, 207))
        gameWindow.blit(board, (0, 0))
        gameWindow.blit(logo, (885, -10))
        for player in players:
            gameWindow.blit(player.piece, player.coordinates)
        clock.tick(fps)
        pygame.display.update()

    gameWindow.blit(dice_images[dice - 1], (1003, 207))
    clock.tick(fps)
    pygame.display.update()
    time.sleep(1)
    return dice, dice_images[dice - 1]


# GAME OVER DISPLAY :
def game_over(won):

    pygame.mixer.music.load("data/audios/DJ Snake - Magenta Riddim.mp3")
    pygame.mixer.music.play()

    pedestal_1 = pygame.image.load("data/images/display/pedestal1.png").convert_alpha()
    pedestal_2 = pygame.image.load("data/images/display/pedestal2.png").convert_alpha()

    winners = []
    for index in won:
        winner_index = pygame.image.load("data/images/pieces/" + str(index + 1) + ".png").convert_alpha()
        winners.append(winner_index)

    exit_screen = False
    current_image = pedestal_1
    change = time.time()
    coordinates = [[557, 207], [262, 242], [832, 249]]

    while not exit_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_screen = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    home_screen()
        if time.time() - change >= 0.2:
            if current_image == pedestal_1:
                current_image = pedestal_2
            else:
                current_image = pedestal_1
            change = time.time()

        gameWindow.blit(current_image, (0, 0))
        for j in range(len(winners)):
            gameWindow.blit(winners[j], coordinates[j])
        clock.tick(fps)
        pygame.display.update()

    pygame.quit()
    quit()


# GAME LOOP FUNCTION :
def game_loop(num_players):

    pygame.mixer.music.stop()
    playlist = ["data/audios/Ed Sheeran - Shape Of You [Official].mp3",
                "data/audios/DJ Snake, Selena Gomez, Cardi B, Ozuna - Taki Taki.mp3",
                "data/audios/Sia - Cheap Thrills Ft. Sean Paul.mp3",
                "data/audios/Happy - Pharrell Williams (Original +) HD.mp3",
                "data/audios/Luis Fonsi - Despacito ft. Daddy Yankee.mp3"]

    playlist_i = 0
    pygame.mixer.music.load(playlist[0])
    pygame.mixer.music.play()
    change = time.time()

    players = []  # list of all players
    won = []
    turn = 0  # variable to decide turn
    colors = [(255, 255, 0), (54, 238, 8), (26, 202, 255), (255, 0, 0)]
    for j in range(num_players):
        piece = pygame.image.load("data/images/pieces/" + str(j + 1) + ".png")
        piece = pygame.transform.scale(piece, (55, 75)).convert_alpha()
        players.append(Player(0, starting_coords[num_players][j].copy(), piece, False))

    count6 = 0  # variable to count number of sixes
    exit_game = False
    dice_image = dice_images[0]

    while not exit_game:
        gameWindow.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            elif event.type == pygame.USEREVENT:
                if playlist_i == 2:
                    pygame.mixer.music.queue(playlist[2])
                    playlist_i = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dice, dice_image = dice_roll(players)
                    if dice == 6:
                        count6 += 1
                        if players[turn].current_block + count6 * 6 >= 100:
                            turn = change_turn(turn, num_players)
                            count6 = 0
                        else:
                            if count6 == 3:
                                turn = change_turn(turn, num_players)
                                count6 = 0
                    else:
                        if not players[turn].is_open:
                            if count6 == 0:
                                turn = change_turn(turn, num_players)
                            else:
                                players[turn].current_block = 1
                                players[turn].coordinates = [35, 580]
                                players[turn].is_open = True
                                move_player(players, turn, (count6 - 1) * 6 + dice, won)
                                count6 = 0
                                turn = change_turn(turn, num_players)
                        else:
                            if count6 == 0:
                                move_player(players, turn, dice, won)
                                turn = change_turn(turn, num_players)
                            else:
                                move_player(players, turn, (count6 * 6) + dice, won)
                                count6 = 0
                                turn = change_turn(turn, num_players)

                    while turn in won:
                        turn = change_turn(turn, num_players)

                elif event.key == pygame.K_w:
                    players[0].is_open = True
                    players[0].current_block = 98
                    players[0].coordinates = [35 + 2 * 86, 4]
                elif event.key == pygame.K_a:
                    players[1].is_open = True
                    players[1].current_block = 98
                    players[1].coordinates = [35 + 2 * 86, 4]
                elif event.key == pygame.K_s:
                    players[2].is_open = True
                    players[2].current_block = 98
                    players[2].coordinates = [35 + 2 * 86, 4]

        gameWindow.blit(board, (0, 0))
        gameWindow.blit(logo, (885, -10))
        pygame.draw.rect(gameWindow, colors[turn], [896, 300, 304, 25])
        pygame.draw.rect(gameWindow, (0, 0, 0), [896, 300, 304, 25], 2)
        pygame.draw.rect(gameWindow, (0, 0, 0), [896, 340, 304, 55])
        text_on_screen("PLAYER " + str(turn + 1) + "'S TURN", (255, 0, 0), 915, 345)
        pygame.draw.rect(gameWindow, colors[turn], [896, 410, 304, 25])
        pygame.draw.rect(gameWindow, (0, 0, 0), [896, 410, 304, 25], 2)

        for player in players:
            gameWindow.blit(player.piece, player.coordinates)
        gameWindow.blit(dice_image, (1003, 207))

        if time.time() - change >= 220:
            if playlist_i == 4:
                playlist_i = 0
            else:
                playlist_i += 1
            pygame.mixer.music.load(playlist[playlist_i])
            pygame.mixer.music.play()
            change = time.time()

        clock.tick(fps)
        pygame.display.update()

    pygame.quit()
    quit()


# GAME LOOP FUNCTION (VS COMPUTER) :
def game_loop_vs_computer(num_players):

    pygame.mixer.music.stop()
    playlist = ["data/audios/Ed Sheeran - Shape Of You [Official].mp3",
                "data/audios/DJ Snake, Selena Gomez, Cardi B, Ozuna - Taki Taki.mp3",
                "data/audios/Sia - Cheap Thrills Ft. Sean Paul.mp3",
                "data/audios/Happy - Pharrell Williams (Original +) HD.mp3",
                "data/audios/Luis Fonsi - Despacito ft. Daddy Yankee.mp3"]

    playlist_i = 0
    pygame.mixer.music.load(playlist[0])
    pygame.mixer.music.play()
    change = time.time()

    players = []  # list of all players
    won = []
    turn = 0  # variable to decide turn
    colors = [(255, 255, 0), (54, 238, 8), (26, 202, 255), (255, 0, 0)]
    for j in range(num_players):
        piece = pygame.image.load("data/images/pieces/" + str(j + 1) + ".png")
        piece = pygame.transform.scale(piece, (55, 75)).convert_alpha()
        players.append(Player(0, starting_coords[num_players][j].copy(), piece, False))

    count6 = 0  # variable to count number of sixes
    exit_game = False
    dice_image = dice_images[0]

    while not exit_game:
        gameWindow.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dice, dice_image = dice_roll(players)
                    if dice == 6:
                        count6 += 1
                        if players[turn].current_block + count6 * 6 >= 100:
                            turn = change_turn(turn, num_players)
                            count6 = 0
                        else:
                            if count6 == 3:
                                turn = change_turn(turn, num_players)
                                count6 = 0
                    else:
                        if not players[turn].is_open:
                            if count6 == 0:
                                turn = change_turn(turn, num_players)
                            else:
                                players[turn].current_block = 1
                                players[turn].coordinates = [35, 580]
                                players[turn].is_open = True
                                move_player(players, turn, (count6 - 1) * 6 + dice, won)
                                count6 = 0
                                turn = change_turn(turn, num_players)
                        else:
                            if count6 == 0:
                                move_player(players, turn, dice, won)
                                turn = change_turn(turn, num_players)
                            else:
                                move_player(players, turn, (count6 * 6) + dice, won)
                                count6 = 0
                                turn = change_turn(turn, num_players)

                    while turn in won:
                        turn = change_turn(turn, num_players)

                elif event.key == pygame.K_w:
                    players[0].is_open = True
                    players[0].current_block = 98
                    players[0].coordinates = [35 + 2 * 86, 4]
                elif event.key == pygame.K_a:
                    players[1].is_open = True
                    players[1].current_block = 98
                    players[1].coordinates = [35 + 2 * 86, 4]
                elif event.key == pygame.K_s:
                    players[2].is_open = True
                    players[2].current_block = 98
                    players[2].coordinates = [35 + 2 * 86, 4]

        gameWindow.blit(board, (0, 0))
        gameWindow.blit(logo, (885, -10))
        for player in players:
            gameWindow.blit(player.piece, player.coordinates)
        gameWindow.blit(dice_image, (1003, 207))

        if turn != 0:
            pygame.draw.rect(gameWindow, colors[turn], [896, 300, 304, 25])
            pygame.draw.rect(gameWindow, (0, 0, 0, 0), [896, 300, 304, 25], 2)
            pygame.draw.rect(gameWindow, (0, 0, 0), [896, 340, 304, 55])
            text_on_screen("COMPUTER " + str(turn) + "'S TURN", (255, 0, 0), 905, 347, font2)
            pygame.draw.rect(gameWindow, colors[turn], [896, 410, 304, 25])
            pygame.draw.rect(gameWindow, (0, 0, 0, 0), [896, 410, 304, 25], 2)
            clock.tick(fps)
            pygame.display.update()
            time.sleep(1)
            dice, dice_image = dice_roll(players)
            if dice == 6:
                count6 += 1
                if players[turn].current_block + count6 * 6 >= 100:
                    turn = change_turn(turn, num_players)
                    count6 = 0
                else:
                    if count6 == 3:
                        turn = change_turn(turn, num_players)
                        count6 = 0
            else:
                if not players[turn].is_open:
                    if count6 == 0:
                        turn = change_turn(turn, num_players)
                    else:
                        players[turn].current_block = 1
                        players[turn].coordinates = [35, 580]
                        players[turn].is_open = True
                        move_player(players, turn, (count6 - 1) * 6 + dice, won)
                        count6 = 0
                        turn = change_turn(turn, num_players)
                else:
                    if count6 == 0:
                        move_player(players, turn, dice, won)
                        turn = change_turn(turn, num_players)
                    else:
                        move_player(players, turn, (count6 * 6) + dice, won)
                        count6 = 0
                        turn = change_turn(turn, num_players)
            while turn in won:
                turn = change_turn(turn, num_players)

        if turn == 0:
            pygame.draw.rect(gameWindow, colors[0], [896, 300, 304, 25])
            pygame.draw.rect(gameWindow, (0, 0, 0, 0), [896, 300, 304, 25], 2)
            pygame.draw.rect(gameWindow, (0, 0, 0), [896, 340, 304, 55])
            text_on_screen("PLAYER'S TURN", (255, 0, 0), 929, 345)
            pygame.draw.rect(gameWindow, colors[0], [896, 410, 304, 25])
            pygame.draw.rect(gameWindow, (0, 0, 0, 0), [896, 410, 304, 25], 2)

        if time.time() - change >= 220:
            if playlist_i == 4:
                playlist_i = 0
            else:
                playlist_i += 1
            pygame.mixer.music.load(playlist[playlist_i])
            pygame.mixer.music.play()
            change = time.time()

        clock.tick(fps)
        pygame.display.update()

    pygame.quit()
    quit()


# SELECT NUMBER OF PLAYERS :
def num_of_players(vs_comp):
    vs_2 = pygame.image.load("data/images/display/vs2.png").convert_alpha()
    vs_3 = pygame.image.load("data/images/display/vs3.png").convert_alpha()
    vs_4 = pygame.image.load("data/images/display/vs4.png").convert_alpha()

    vs = [vs_2, vs_3, vs_4]
    exit_screen = False
    current = 0

    while not exit_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_screen = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if current == 2:
                        current = 0
                    else:
                        current += 1
                elif event.key == pygame.K_UP:
                    if current == 0:
                        current = 2
                    else:
                        current -= 1
                elif event.key == pygame.K_RETURN:
                    if vs_comp:
                        game_loop_vs_computer(current + 2)
                    else:
                        game_loop(current + 2)

        gameWindow.blit(vs[current], (0, 0))
        clock.tick(fps)
        pygame.display.update()

    pygame.quit()
    quit()


# CHOOSE VERSUS :
def choose_versus():
    vs_computer = pygame.image.load("data/images/display/vscomputer.png").convert_alpha()
    vs_friends = pygame.image.load("data/images/display/vsfriends.png").convert_alpha()

    exit_screen = False
    vs_comp = True

    while not exit_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_screen = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    vs_comp = not vs_comp
                elif event.key == pygame.K_RETURN:
                    num_of_players(vs_comp)
        if vs_comp:
            gameWindow.blit(vs_computer, (0, 0))
        else:
            gameWindow.blit(vs_friends, (0, 0))

        clock.tick(fps)
        pygame.display.update()

    pygame.quit()
    quit()


# HOME SCREEN :
def home_screen():

    background_music = pygame.mixer.music.load("data/audios/DJ Snake - Magenta Riddim.mp3")
    pygame.mixer.music.play()

    home_screen_1 = pygame.image.load("data/images/display/homescreen1.png").convert_alpha()
    home_screen_2 = pygame.image.load("data/images/display/homescreen2.png").convert_alpha()

    exit_screen = False
    current_image = home_screen_1
    change = time.time()

    while not exit_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_screen = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    choose_versus()

        if time.time() - change >= 0.2:
            if current_image == home_screen_1:
                current_image = home_screen_2
            else:
                current_image = home_screen_1
            change = time.time()

        gameWindow.blit(current_image, (-3, -50))
        clock.tick(fps)
        pygame.display.update()

    pygame.quit()
    quit()


home_screen()
