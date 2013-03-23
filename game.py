# -*- coding: utf-8 -*-
import pygame
import consts
from background import Background
import player


class Game():
    def __init__(self):
        pygame.init()

        pygame.joystick.init()

        if pygame.joystick.get_count() >= 1:
            for joystick_id in range(0, pygame.joystick.get_count()):
                joystick = pygame.joystick.Joystick(joystick_id)
                # Stop on first matching joystick
                if joystick.get_name() in consts.JOYSTICK:
                    print "Initializing Joystick id:%d" % joystick.get_id()
                    joystick.init()
                    self.joystick = joystick
                    print "%s (%d axis)" % (joystick.get_name(), joystick.get_numaxes())
                    break

        self.screen = pygame.display.set_mode(consts.RESOLUTION)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        # Blit background
        self.background = Background((0, 0))
        # TODO avoid acting on sprite and do actions on group?
        self.player = player.Player({
            'tilesGroup': 'umbrella',
            'x': 400,
            'y': 300
        })
        self.background.setMainSprite(self.player)

    def run(self):
        running = True
        # run until an event tells us to stop
        while running:
            pygame.time.Clock().tick(consts.FPS)
            running = self.handleEvents()
            self.background.update(self.screen.get_size())

            camera = - self.background.xCamera, - self.background.yCamera
            self.screen.blit(self.background.fond, (0, 0))
            # update screen
            rect = pygame.Rect(
                0,
                0,
                consts.RESOLUTION[0],
                consts.RESOLUTION[1]
            )
            pygame.display.update(rect)

    def handleEvents(self):
        # poll for pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # handle user input
            elif event.type == pygame.KEYDOWN:
                # if the user presses escape or 'q', quit the event loop.
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    return False
                # handle speed
                if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    self.player.speed = 6
                # movement control
                if event.key == pygame.K_UP:
                    self.player.moveVertical(-1)
                if event.key == pygame.K_DOWN:
                    self.player.moveVertical(1)
                if event.key == pygame.K_LEFT:
                    self.player.moveHorizontal(-1)
                if event.key == pygame.K_RIGHT:
                    self.player.moveHorizontal(1)
                if event.key == pygame.K_c:
                    #~ create new sprite
                    s = player.Player({
                        'tilesGroup': 'scholar',
                        'x': 300,
                        'y': 300,
                        'movePattern': {
                            'type': 'rect',
                            'attributes': {
                                'width': 200,
                                'height': 200
                            }
                        }
                    })
                    self.background.addSprite(s, Background.LAYER_CHARACTERS)

            elif event.type == pygame.JOYBUTTONDOWN:
                # Joystick control
                # handle speed
                if event.button == consts.JOYSTICK[self.joystick.get_name()]['button1']:
                    self.player.speed = 6
                # movement control
                if event.button == consts.JOYSTICK[self.joystick.get_name()]['up']:
                    self.player.moveVertical(-1)
                if event.button == consts.JOYSTICK[self.joystick.get_name()]['down']:
                    self.player.moveVertical(1)
                if event.button == consts.JOYSTICK[self.joystick.get_name()]['left']:
                    self.player.moveHorizontal(-1)
                if event.button == consts.JOYSTICK[self.joystick.get_name()]['right']:
                    self.player.moveHorizontal(1)

            elif event.type == pygame.KEYUP:
                # handle speed
                if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    self.player.speed = 3
                # stop movement control
                if event.key == pygame.K_UP:
                    self.player.moveVertical(1)
                if event.key == pygame.K_DOWN:
                    self.player.moveVertical(-1)
                if event.key == pygame.K_LEFT:
                    self.player.moveHorizontal(1)
                if event.key == pygame.K_RIGHT:
                    self.player.moveHorizontal(-1)

            elif event.type == pygame.JOYBUTTONUP:
                # Joystick control
                # handle speed
                if event.button == consts.JOYSTICK[self.joystick.get_name()]['button1']:
                    self.player.speed = 3
                # stop movement control
                if event.button == consts.JOYSTICK[self.joystick.get_name()]['up']:
                    self.player.moveVertical(1)
                if event.button == consts.JOYSTICK[self.joystick.get_name()]['down']:
                    self.player.moveVertical(-1)
                if event.button == consts.JOYSTICK[self.joystick.get_name()]['left']:
                    self.player.moveHorizontal(1)
                if event.button == consts.JOYSTICK[self.joystick.get_name()]['right']:
                    self.player.moveHorizontal(-1)

            if event.type == pygame.JOYAXISMOTION:
                # We won't need to slow diagonals
                self.player.axismove = True
                if abs(round(event.value, 1)) > 0.1:
                    # Reduce steps
                    value = round(event.value, 1)
                else:
                    # Try to handle back to the middle
                    value = 0
                # We must not add up those values, but use them as they are
                if event.axis == 1:
                    self.player.moveVertical(value, absolute=True)
                elif event.axis == 0:
                    self.player.moveHorizontal(value, absolute=True)
                pygame.event.pump()
            else:
                self.player.axismove = False

        # TODO make the sprite move too
        return True
