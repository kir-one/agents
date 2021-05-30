import pygame
import os
import neat
from config import *
from bird import *
from base import *
from pipe import *
import sys


def draw_window_dark(win, birds, pipes, base, score):
    win.blit(bg_night, (0, 0))

    for bird in birds:
        bird.draw(win)

    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    #
    text = the_stat.render(str(score), 1, (255, 255, 255))
    win.blit(text, (ancho // 2, 17))
    # text = the_stat.render("Gen: " + str(gen), 1, (255, 255, 255))
    # win.blit(text, (10, 10))
    pygame.display.update()

def draw_window_light(win, birds, pipes, base, score):
    win.blit(bg_day, (0, 0))

    for bird in birds:
        bird.draw(win)

    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    # estadístícas
    text = the_stat.render(str(score), 1, (255, 255, 255))
    win.blit(text, (ancho // 2, 17))
    # text = the_stat.render("Gen: " + str(gen), 1, (255, 255, 255))
    # win.blit(text, (10, 10))
    pygame.display.update()


def main(genomes, config):
    global gen
    gen += 1
    nets = []
    ge = []
    birds = []

    # retorno de los valores
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    run = True
    win = pygame.display.set_mode(ratio_aspect)
    clock = pygame.time.Clock()
    score = 0

    # instancias
    base = Base(620)
    pipes = [Pipe(400)]

    while run:
        clock.tick(90)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].pipe_top.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        if score == 30:
            break

        # se va añadiendo peso a los genomas
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += .1

            # aquí es donde la mágia ocurre
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > .5:
                bird.jump()

        #-------------------------------------------------#
        #       determinar cuál es la mejor especie
        # -------------------------------------------------#
        rem = []
        global noise
        add_pipe = False
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x - 50 < bird.x:
                    add_pipe = True
                    pipe.passed = True

                if bird.x < pipe.x + 49 < bird.x + 5 and noise:
                    score += 1
                    noise = False

            if pipe.x + pipe.pipe_top.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            for g in ge:
                g.fitness += 5
            noise = True
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                ge[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()

        if (gen + 2) % 2 > 0:
            draw_window_dark(win, birds, pipes, base, score)
        else:
            draw_window_light(win, birds, pipes, base, score)


def run(config_path):

    # se establecen los parametros del algortimo genético
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)


    # por cada generación habrán 50 especies
    winner = p.run(main, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "foward")
    run(config_path)
