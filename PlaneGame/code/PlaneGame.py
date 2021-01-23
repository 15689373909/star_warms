import tkinter  #窗体标准库
import random  #随机数标准库
import time   #时间标准库
import bee    #自定义
import bullet   #自定义
import config   #自定义
import enemy_plane  #自定义
import hero_plane   #自定义
import image  #自定义

# 定义敌人列表，保存所有敌人(包含敌机和蜜蜂)
enemys = []

# 定义子弹列表，保存所有子弹
bullets = []

# 定义hp变量，保存战机对象
hp = ""

# 定义当前用户的分数和生命值
life = 3
score = 0

# 定义游戏状态
game_state = config.GAME_START

# 创建窗体
game_window = tkinter.Tk()

# 窗口文字设置
game_window.title('飞机大战')

# 窗口位置处理
screenwidth = game_window.winfo_screenwidth()
screenheight = game_window.winfo_screenheight()
size = '%dx%d+%d+%d' % (config.GAME_WIDTH, config.GAME_HEIGHT, (screenwidth-config.GAME_WIDTH)/2, 20)
game_window.geometry(size)

# 加载游戏用到的所有的图片
back, bee_image, bullet_image, hero,hero0, smallplane = image.load_image(tkinter)
start_image,stop_image = image.load_state_image(tkinter)
# 获取画布
window_canvas = tkinter.Canvas(game_window)
# 画布包装方式
window_canvas.pack(expand=tkinter.YES, fill=tkinter.BOTH)
def next_one():# 生成一个敌人
    a = random.randint(0,20)
    enemy = ""
    if a>=5:
        enemy = enemy_plane.EnemyPlane(smallplane)
    else:
        enemy = bee.Bee(bee_image)
    return enemy
# 用来协助控制时间
count = 0
def enter_action():# 10ms执行一次
    global count
    count += 1
    if count%40 == 0:
        enemy = next_one()# 生成一个敌人
        enemys.append(enemy)# 敌人添加到列表中
        window_canvas.create_image(enemy.x,enemy.y,anchor = tkinter.NW,image=enemy.image,tag=enemy.tag)
        if hp.double_fire>0:
            bu1,bu2 = hp.shoot_double(bullet_image)
            bullets.append(bu1)
            window_canvas.create_image(bu1.x,bu1.y,anchor=tkinter.NW,image=bu1.image,tag=bu1.tag)
            bullets.append(bu2)
            window_canvas.create_image(bu2.x,bu2.y,anchor=tkinter.NW,image=bu2.image,tag=bu2.tag)
        else:
            bul = hp.shoot(bullet_image)
            # 生成一个子弹
            bullets.append(bul)
            window_canvas.create_image(bul.x,bul.y,anchor=tkinter.NW,image=bul.image,tag=bul.tag)

def step_action():
    # 遍历所有的敌人和子弹，调用移动的方法
    for enemy in enemys:
        enemy.step(window_canvas)
    for bul in bullets:
        bul.step(window_canvas)
def call_back_click(event):
    global game_state
    # 如果游戏状态为启动状态，则修改状态为运行
    # 如果游戏状态为结束状态，则修改状态为启动状态
    if game_state == config.GAME_START:
        game_state = config.GAME_RUNNING
        # 画分和命
        window_canvas.create_text(10, 10, text="分数：%d" % (score), anchor=tkinter.NW, fill="red", font="time 24 bold",
                                  tag="SCORE")
        window_canvas.create_text(10, 50, text="生命：%d" % (life), anchor=tkinter.NW, fill="red", font="time 24 bold",
                                  tag="LIFE")
        # 删除启动图片
        window_canvas.delete("START")

    elif game_state == config.GAME_STOP:
        window_canvas.delete("BACK")
        window_canvas.delete("HP")
        window_canvas.delete("STOP")
        game_state = config.GAME_START
        game_start()


def call_back_move(event):
    if game_state == config.GAME_RUNNING:
        old_x = hp.x
        old_y = hp.y
        hp.x = event.x - hp.w/2
        hp.y = event.y - hp.h/2
        window_canvas.move("HP", hp.x-old_x, hp.y-old_y)


def out_of_bounds_action():
    # 获取所有敌人和所有的子弹，每一个判断是否越界
    for enemy in enemys:
        if enemy.out_of_bounds():
            window_canvas.delete(enemy.tag)
            enemys.remove(enemy)
    for bul in bullets:
        if bul.out_of_bounds():
            window_canvas.delete(bul.tag)
            bullets.remove(bul)


def bmob_action():
    # 判断每一个子弹和每一个敌人的碰撞
    # 子弹和敌人碰撞
    for bul in bullets:
        isbmob = False
        for enemy in enemys:
            if bul.bmob(enemy):
                enemys.remove(enemy)
                window_canvas.delete(enemy.tag)
                # global score
                # score += 5
                # isbmob = True
                #
                if isinstance(enemy, bee.Bee):
                    a = random.randint(0, 5)
                    if a == 0:
                        global life
                        life += 1
                    else:
                        hp.double_fire += 10
                elif isinstance(enemy, enemy_plane.EnemyPlane):
                    global score
                    score += 5
        if isbmob:
            bullets.remove(bul)
            window_canvas.delete(bul.tag)
    for enemy in enemys:
        if hp.bomb(enemy):
            life -= 1
            enemys.remove(enemy)
            window_canvas.delete(enemy.tag)
            if life < 0:# 如果生命值小于0 游戏结束
                global game_state
                game_state = config.GAME_STOP
                # 清空子弹列表和敌人列表
                # 画游戏结束的状态
                game_over()

def draw_action():
    # 画分和，命
    window_canvas.delete("SCORE")
    window_canvas.delete("LIFE")
    window_canvas.create_text(10,10,text="分数：%d"%(score),anchor=tkinter.NW,fill="red",font="time 24 bold",tag="SCORE")
    window_canvas.create_text(10,50,text="生命：%d"%(life),anchor=tkinter.NW,fill="red",font="time 24 bold",tag="LIFE")
def game_over():
    global game_state
    game_state = config.GAME_STOP
    for bul in bullets:
        window_canvas.delete(bul.tag)
    for enemy in enemys:
        window_canvas.delete(enemy.tag)
    bullets.clear()
    enemys.clear()
    window_canvas.create_image(0,0,anchor=tkinter.NW,image=stop_image,tag="STOP")
def game_start():
    global life
    global score
    life = 3
    score = 0
    # 画游戏背景
    window_canvas.create_image(0, 0, anchor=tkinter.NW, image=back, tag="BACK")
    # 创建英雄对象
    global hp
    hp = hero_plane.HeroPlane(hero)
    window_canvas.create_image(hp.x, hp.y, anchor=tkinter.NW, image=hp.image, tag="HP")
    window_canvas.create_image(0, 0, anchor=tkinter.NW, image=start_image, tag="START")
def game():
    if game_state == config.GAME_START:
        game_start()
        # 鼠标监听
        window_canvas.bind("<Motion>",call_back_move)
        window_canvas.bind("<Button-1>",call_back_click)

    while True:
        if game_state == config.GAME_RUNNING:
            # 敌人子弹入场
            enter_action()
            # 敌人和子弹动起来
            step_action()
            # 删除越界的敌人和子弹
            out_of_bounds_action()
            # 检测碰撞
            bmob_action()
            if life >= 0:
                # 画分和命
                draw_action()
                # 更新显示
        game_window.update()
        # 休眠10ms
        time.sleep(0.01)


if __name__ == "__main__":
#当.py文件被直接运行时，if __name__ == '__main__'之下的代码块将被运行；
#当.py文件以模块形式被导入时，if __name__ == '__main__'之下的代码块不被运行。
    game()
    game_window.mainloop()