import flying
import bullet
class HeroPlane(flying.Flying):
    def __init__(self, image, x=150, y=450):
        self.double_fire = 0
        w = image.width()
        h = image.height()
        super().__init__(x,y,w,h,image)
    def bomb(self, enemy):
        if enemy.x - self.w <= self.x <= enemy.x + enemy.w:
            if enemy.y-self.h <= self.y <= enemy.y + enemy.h:
                return True
        return False

    def shoot(self,bullet_image):
        if self.double_fire <= 0:
            x = (self.w - bullet_image.width()) / 2 + self.x + 1
            y = self.y - bullet_image.height()
            bul = bullet.Bullet(x,y,bullet_image)
            return bul
    def shoot_double(self,bullet_image):
        if self.double_fire >= 0:
            x1 = self.x + self.w/4
            x2 = self.x + self.w/4*3
            y = self.y - bullet_image.height()
            bu1 = bullet.Bullet(x1,y,bullet_image)
            bu2 = bullet.Bullet(x2,y,bullet_image)
            self.double_fire -= 2
            return bu1,bu2



