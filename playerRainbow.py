from gameRainbow import endgames, colors, actions, action, card
from basePlayer import basePlayer


class playerCard:
    def __init__(self, theCard):
        self.card = theCard.copy()
        self.hint = card(colors.unknown, -1)


class player(basePlayer):
    def __init__(self):
        basePlayer.__init__(self)
        self.onStart.append(self.onStart)
        self.onGameEnd.append(self.onGameEnd)
        self.onTurnStart.append(self.onTurnStart)
        self.onHintColor.append(self.onHint)
        self.onHintNumber.append(self.onHint)
        self.onPlayerAction.append(self.resolveTurn)
        self.hands = []
        self.field = []
        self.discard = []
        self.currentPlayer = []
        self.hints = 8
        self.error = 0
        for i in range(5):
            self.field.append([])
            self.discard.append([])
        self.deckRemain = []
        self.playerIndex = -1

    def onStart(self, handStatus):
        self.hands = [playerCard(c) for c in handStatus]
        self.deckRemain = 50 - len(handStatus[0]) * len(handStatus)
        for i in range(len(handStatus)):
            if handStatus[i][0].number == -1:
                self.playerIndex = i
                break

    def turn(self):
        res = input().split()
        actionType = actions(int(res[0]))
        target = int(res[1])
        if actionType == actions.hintColor:
            return action(actionType, target, color=colors(int(res[2])))
        elif actionType == actions.hintNumber:
            return action(actionType, target, nunmber=int(res[2]))
        else:
            return action(actionType, target)

    def onGameEnd(self, reason, score):
        print("Game ended because of {},score:{}".format(reason, score))

    def onTurnStart(self, index):
        self.currentPlayer = index

    def resolveHint(self, target, hintInfo):
        for i, c in enumerate(hintInfo):
            if c.color == colors.unknown:
                self.hands[target][i].hint.number = c.number
            else:
                if (not self.hands[target][i].hint.color == colors.unknown) and (not self.hands[target][i].hint.color == c.color):
                    self.hands[target][i].hint.color = colors.rainbow
                else:
                    self.hands[target][i].hint.color = c.color

    def onHint(self, hintInfo):
        self.resolveHint(self.playerIndex, hintInfo)

    def resolveTurn(self, index, playerAction, **kwargs):
        unknownCard = card(colors.unknown, -1)
        if playerAction.actionType == actions.hintColor:
            self.hints -= 1
            # generates the hint
            hintInfo = []
            for i in self.hands[playerAction.target]:
                if i.card.color == playerAction.color:
                    hintInfo.append(card(playerAction.color, -1))
                else:
                    hintInfo.append(unknownCard.copy())
            self.resolveHint(playerAction.target, hintInfo)
        elif playerAction.actionType == actions.hintNumber:
            self.hints -= 1
            # generates the hint
            hintInfo = []
            for i in self.hands[playerAction.target]:
                if i.card.number == playerAction.number:
                    hintInfo.append(card(colors.unknown, i.number))
                else:
                    hintInfo.append(unknownCard.copy())
            self.resolveHint(playerAction.target, hintInfo)
        elif playerAction.actionType == actions.discard:
            # discard and draw
            discard = kwargs['discard']
            self.discard[discard.color.value].append(discard.copy())
            if self.deckRemain == 0:
                self.hands[index].pop(playerAction.target)
            else:
                draw = kwargs['draw']
                self.hands[index][playerAction.target] = playerCard(draw)
                self.deckRemain -= 1
        else:
            # attempt to play and draw
            play = kwargs['play']
            if len(self.field[play.color.value]) == 0 and play.number == 1 or play.number == \
                    self.field[play.color.value][-1].number + 1:
                self.field[play.color.value].append(play.copy())
                self.score += 1
                if play.number == 5:
                    self.hints += 1
            else:
                self.error += 1
                self.discard[play.color.value].append(play.copy())
            if self.deckRemain == 0:
                self.hands[index].pop(playerAction.target)
            else:
                draw = kwargs['draw']
                self.hands[index][playerAction.target] = playerCard(draw)
                self.deckRemain -= 1
