import os
import sys
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from data.main import main
import cProfile

if __name__=='__main__':
    main()
    pg.quit()
    sys.exit()







