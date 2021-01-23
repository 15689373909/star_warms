import flying
class Bullet(flying.Flying):
    bullet_count = 0
    def __init__(self, x,y, image):
        Bullet.bullet_count += 1
        self.tag = "Bullet_"+str(Bullet.bullet_count)
        w = image.width()
        h = image.height()
        super().__init__(x, y, w, h, image)
    def step(self, canvas):
        canvas.move(self.tag, 0, -5)
        self.y -= 5
    def out_of_bounds(self):
        if self.y < (0 - self.h):
            return True
        else:
            return False
    def bmob(self,enemy):
        if enemy.x - self.w <= self.x <= enemy.x+enemy.w:
            if enemy.y-self.h <= self.y <= enemy.y + enemy.h:
                return True
        return False


