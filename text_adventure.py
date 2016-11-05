#!/usr/bin/env python3
# encoding: utf-8
# 使用python3 方便处理中文编码 否则设置好编码sys.

from random import randint
import random

# log for debug
import logging
LOG_FILE = "/tmp/log_file.log"
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(LOG_FILE)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class Character:
    def __init__(self):
        self.name = ""
        self.health = 1
        self.health_max = 1

    def do_damage(self, enemy):
        damage = min(
            max(
                randint(0, self.health) - randint(0, enemy.health), 0),
            enemy.health)
        enemy.health = enemy.health - damage
        if damage == 0:
            print("{} evades {}'s attack.".format(enemy.name, self.name))
        else:
            print(("{} hurts {}!".format(self.name, enemy.name)))
        return enemy.health <= 0


class Enemy(Character):
    def __init__(self, player):
        Character.__init__(self)
        self.name = '小妖精'
        self.health = randint(1, player.health)


class Player(Character):
    def __init__(self):
        Character.__init__(self)
        self.state = 'normal'
        self.health = 10
        self.health_max = 10

    def quit(self):
        print(("{} 找不到路回家，饿死途中.\nR.I.P.".format(self.name)))
        self.health = 0

    def help(self):
        print(list(Commands.keys()))

    def status(self):
        print(("{} 的生命力: {}/{}".format((self.name, self.health, self.health_max
                                        ))))

    def tired(self):
        print("{} feels tired.".format(self.name))
        self.health = max(1, self.health - 1)

    def rest(self):
        if self.state != 'normal':
            print("{} can't rest now!".format(self.name))
            self.enemy_attacks()
        else:
            print("{} rests.".format(self.name))
            if randint(0, 1):
                self.enemy = Enemy(self)
                print("{} is rudely awakened by {}!".format((self.name,
                                                             self.enemy.name)))
                self.state = 'fight'
                self.enemy_attacks()
            else:
                if self.health < self.health_max:
                    self.health = self.health + 1
                else:
                    print("{} slept too much.".format(self.name))
                    self.health = self.health - 1

    def explore(self):
        if self.state != 'normal':
            print("{} is too busy right now!".format(self.name))
            self.enemy_attacks()
        else:
            print("{} explores a twisty passage.".format(self.name))
            if randint(0, 1):
                self.enemy = Enemy(self)
                print("{} encounters {}!".format((self.name, self.enemy.name)))
                self.state = 'fight'
            else:
                if randint(0, 1): self.tired()

    def flee(self):
        if self.state != 'fight':
            print("{} runs in circles for a while.".format(self.name))
            self.tired()
        else:
            if randint(1, self.health + 5) > randint(1, self.enemy.health):
                print("{} flees from {}.".format((self.name, self.enemy.name)))
                self.enemy = None
                self.state = 'normal'
            else:
                print("{} couldn't escape from {}!".format((self.name,
                                                            self.enemy.name)))
                self.enemy_attacks()

    def attack(self):
        if self.state != 'fight':
            print("{} swats the air, without notable results.".format(
                self.name))
            self.tired()
        else:
            if self.do_damage(self.enemy):
                print("{} executes {}!".format((self.name, self.enemy.name)))
                self.enemy = None
                self.state = 'normal'
                if randint(0, self.health) < 10:
                    self.health = self.health + 1
                    self.health_max = self.health_max + 1
                    print("{} feels stronger!".format(self.name))
            else:
                self.enemy_attacks()

    def enemy_attacks(self):
        if self.enemy.do_damage(self):
            print("{} was slaughtered by {}!!!\nR.I.P." %
                  (self.name, self.enemy.name))


Commands = {
    '退出': Player.quit,
    'help': Player.help,
    '状态': Player.status,
    '休息': Player.rest,
    '探险': Player.explore,
    '逃跑': Player.flee,
    '进攻': Player.attack,
}

# 游戏开始
p = Player()
p.name = input("用户名? ")
print("(返回'help'以获取帮助)\n")
print("hi，{} ，欢迎开启你的MBA学习旅程，系统正在为您分配学习伙伴...".format(p.name))

bots = ["哆啦A梦", "哆啦B梦", "哆啦C梦"]
your_bot = random.choice(bots)
print("你好哇，{} ，我是{}, 接下来我将陪伴你一同学习".format(p.name, your_bot))

# loop
# todo http无状态请求
while (p.health > 0):
    line = input("> ")
    args = line.split()
    if len(args) > 0:
        commandFound = False
        for c in list(Commands.keys()):
            if args[0] == c: #[:len(args[0])]:
                Commands[c](p)
                commandFound = True
                break
        if not commandFound:
            print("抱歉，{} 无法接受该指令.".format(p.name))
