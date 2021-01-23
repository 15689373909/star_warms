import flying
import config
import random
class EnemyPlane(flying.Flying):
    enemy_plane_count = 0
    def __init__(self, image):
        EnemyPlane.enemy_plane_count += 1
        self.tag = "Enemy_plane_"+str(EnemyPlane.enemy_plane_count)
        x = random.randint(0, config.GAME_WIDTH-image.width())
        y = 0 - image.height()
        w = image.width()
        h = image.width()
        super().__init__(x,y,w,h,image)
    def step(self, canvas):  #移动
        canvas.move(self.tag, 0, 5)  
        self.y += 5
    def out_of_bounds(self):   #超出边界
        if self.y > config.GAME_HEIGHT:
            return True
        else:
            return False