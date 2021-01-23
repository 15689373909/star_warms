import flying
import config
import random
class Bee(flying.Flying):
    bee_count = 0  # 蜜蜂对象记数
    def __init__(self, image):
        Bee.bee_count += 1
        self.tag = "Bee_"+str(Bee.bee_count)
        # 蜜蜂移动的方向。True向右否则向左
        self.direct = True
        x = random.randint(0, config.GAME_WIDTH-image.width())
        y = 0 - image.height()
        w = image.width()
        h = image.width()
        super().__init__(x,y,w,h,image)

    def step(self, canvas):
        self.y += 3
        if self.direct:
            self.x += 3
            canvas.move(self.tag,3,3)
        else:
            self.x -= 3
            canvas.move(self.tag, -3, 3)
        # 判断向左还是向右
        if self.x >= config.GAME_WIDTH-self.w:
            self.direct = False
        elif self.x <=0:
            self.direct = True
    def out_of_bounds(self):
        if self.y > config.GAME_HEIGHT:
            return True
        else:
            return False