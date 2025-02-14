import pygame
import animation
from animation import spirit_show_manager

piclist=[]
shopbg1 = pygame.image.load("material/2.18/bad_end1.png")
shopbg1 = pygame.transform.scale(shopbg1, (1200, 800))
shop1 = animation.Spirit_state(shopbg1, 0, 0, 1)
spirit_show_manager.spirits.append(shop1)
piclist.append(shop1)

shopbg2 = pygame.image.load("material/2.18/bad_end2.png")
shopbg2 = pygame.transform.scale(shopbg2, (1200, 800))
shop2 = animation.Spirit_state(shopbg2, 0, 0, 1)
spirit_show_manager.spirits.append(shop2)
piclist.append(shop2)

shopbg3 = pygame.image.load("material/2.18/bad_end3.png")
shopbg3 = pygame.transform.scale(shopbg3, (1200, 800))
shop3 = animation.Spirit_state(shopbg3, 0, 0, 1)
spirit_show_manager.spirits.append(shop3)
piclist.append(shop3)

shopbg4 = pygame.image.load("material/2.18/bad_end4.png")
shopbg4 = pygame.transform.scale(shopbg4, (1200, 800))
shop4 = animation.Spirit_state(shopbg4, 0, 0, 1)
spirit_show_manager.spirits.append(shop4)
piclist.append(shop4)



piclist2=[]
hopbg1 = pygame.image.load("material/2.18/good_end1.png")
hopbg1 = pygame.transform.scale(hopbg1, (1200, 800))
hop1 = animation.Spirit_state(hopbg1, 0, 0, 1)
spirit_show_manager.spirits.append(hop1)
piclist2.append(hop1)

hopbg2 = pygame.image.load("material/2.18/good_end2.png")
hopbg2 = pygame.transform.scale(hopbg2, (1200, 800))
hop2 = animation.Spirit_state(hopbg2, 0, 0, 1)
spirit_show_manager.spirits.append(hop2)
piclist2.append(hop2)

hopbg3 = pygame.image.load("material/2.18/good_end3.png")
hopbg3 = pygame.transform.scale(hopbg3, (1200, 800))
hop3 = animation.Spirit_state(hopbg3, 0, 0, 1)
spirit_show_manager.spirits.append(hop3)
piclist2.append(hop3)

hopbg4 = pygame.image.load("material/2.18/good_end4.png")
hopbg4 = pygame.transform.scale(hopbg4, (1200, 800))
hop4 = animation.Spirit_state(hopbg4, 0, 0, 1)
spirit_show_manager.spirits.append(hop4)
piclist2.append(hop4)

hopbg5 = pygame.image.load("material/2.18/good_end5.png")
hopbg5 = pygame.transform.scale(hopbg5, (1200, 800))
hop5 = animation.Spirit_state(hopbg5, 0, 0, 1)
spirit_show_manager.spirits.append(hop5)
piclist2.append(hop5)