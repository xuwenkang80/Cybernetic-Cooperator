from game import actions, card, action
from basePlayer import basePlayer
import random

class SimplePlayer(basePlayer):
    def __init__(self):
        basePlayer.__init__(self)
        # 初始化 onStart 监听器
        self.onStart.append(self.onStartListener)

    def onStartListener(self, handStatus):
        # 这里可以初始化一些逻辑，比如记录手牌信息
        pass

    def turn(self):
        # 选择打出第一张手牌，因为索引通常是从0开始的
        target_card_index = random.randrange(0,4)
        # 构造一个打出牌的action
        return action(actionType=actions.play, target=target_card_index)

# 其他必要的方法可以根据需要实现，但在这个简单的例子中，我们只覆盖了必需的 turn 方法。