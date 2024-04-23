from game import game
from SimplePlayer import SimplePlayer  # 假设 SimplePlayer 类定义在 player.py 文件中

'''
# 创建玩家实例
players = [SimplePlayer() for _ in range(4)]  # 假设游戏需要4个玩家

# 初始化游戏并开始
the_game = game(players=players)
score = the_game.start()

print(f"Game ended with score: {score}")
'''
highest_score = 0

# 定义一个函数来启动新游戏
def start_new_game(players):
    # 初始化游戏类实例，将玩家列表作为参数传递
    the_game = game(players=players)
    # 开始游戏，并获取最终得分
    score = the_game.start()
    # 打印游戏结束原因和得分
    print(f"Game ended with score: {score}")
    # 可以在这里添加逻辑，比如询问是否继续游戏
    global highest_score

    if score >highest_score:
        highest_score = score
    print(f"Current highest score: {highest_score}")

# 创建玩家实例列表
players = [SimplePlayer() for _ in range(3)]  # 假设你想添加5个计算机玩家

# 无限循环，直到外部条件打破循环
while True:
    start_new_game(players)
    # 这里可以添加一个输入提示，询问玩家是否想重新开始
    #play_again = input("Do you want to play again? (yes/no): ")
    #if play_again.lower() != 'yes':
    #    break