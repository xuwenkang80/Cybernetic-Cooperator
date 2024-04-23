import numpy as np
from game import colors

# 假设这是您的玩家类
class MyPlayer:
    def __init__(self):
        self.hand = []  # 假设这是玩家手牌的初始化

    def get_hand_encoding(self):
        # 将手牌编码为长度为5的数组，其中每项代表一张手牌的[颜色值, 数值]。
        # 如果手牌不足5张，用[-1, -1]填充。
        hand_encoding = np.array([[c.color.value, c.number] for c in self.hand])
        padded_hand_encoding = np.full((5, 2), -1)  # 创建一个5x2的数组，填充-1
        padded_hand_encoding[:hand_encoding.shape[0], :hand_encoding.shape[1]] = hand_encoding
        return padded_hand_encoding
def encode_hands(players):
    hands_matrix = np.zeros((4, 5, 2))  # 创建一个4x5x2的数组，填充0
    for i, player in enumerate(players):
        hands_matrix[i] = player.get_hand_encoding()
    return hands_matrix

# 假设这是您的游戏循环
def game_loop(players):
    # 获取手牌信息并编码为矩阵
    hands_matrix = encode_hands(players)
    
    # 打印矩阵
    print("Hands Matrix:\n", hands_matrix)
    
    # 此处省略了游戏逻辑和监听器的调用...

# 假设您有4个玩家实例
players = [MyPlayer() for _ in range(4)]

# 运行游戏循环
game_loop(players)