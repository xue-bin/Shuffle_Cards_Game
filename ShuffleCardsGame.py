import random
import queue
import copy


def readCards():
    file_name = input("Please input cards file:")
    correct_cards = ['0C', '0D', '0H', '0S', '2C', '2D', '2H', '2S', '3C', '3D', '3H', '3S', '4C', '4D', '4H', '4S',
                     '5C', '5D', '5H', '5S', '6C', '6D', '6H', '6S', '7C', '7D', '7H', '7S', '8C', '8D', '8H', '8S',
                     '9C', '9D', '9H', '9S', 'AC', 'AD', 'AH', 'AS', 'JC', 'JD', 'JH', 'JS', 'KC', 'KD', 'KH', 'KS',
                     'QC', 'QD', 'QH', 'QS']
    cards = []
    try:
        cardFile = open(file_name)
        for card in cardFile.readlines():
            card = card.replace("\n", "")
            card = card.upper()
            cards.append(card)
        if (sorted(cards) != correct_cards):
            print("The cards file doesn't contain correct card")
            exit()
    except IOError as e:
        print("I/O error({0}: {1}".format(e.errno, e.strerror))
    except:
        print("Unexpected error")
    finally:
        cardFile.close()

    return cards


def distributeCards(cards):
    A = cards[0::2]
    B = cards[1::2]
    A_hand = queue.CircularQueue(52)
    B_hand = queue.CircularQueue(52)
    for i in A:
        A_hand.enqueue(i)
    for i in B:
        B_hand.enqueue(i)
    if (random.random() < 0.5):
        return A_hand, B_hand
    else:
        return B_hand, A_hand


def gameType():
    flag = True
    while flag:
        game_type = input("Which game type would like to play ?\nA war with 1, 2, or 3?")
        if (game_type == "1" or game_type == "2" or game_type == "3"):
            flag = False
    return int(game_type)


def compareCards(card1, card2):
    convert = {"2": 1,
               "3": 2,
               "4": 3,
               "5": 4,
               "6": 5,
               "7": 6,
               "8": 7,
               "9": 8,
               "0": 9,
               "J": 10,
               "Q": 11,
               "K": 12,
               "A": 13}
    c1 = convert[card1[0]]
    c2 = convert[card2[0]]
    if (c1 == c2):
        return 0
    elif (c1 > c2):
        return 1
    else:
        return -1


class OnTable:
    def __init__(self):
        self.__cards = []
        self.__faceUp = []

    def place(self, player, card, hidden):
        if (player == 1):
            self.__cards.insert(0, card)
            self.__faceUp.insert(0, hidden)
        else:
            self.__cards.append(card)
            self.__faceUp.append(hidden)

    def cleanTable(self):
        result = copy.deepcopy(self.__cards)
        self.__cards.clear()
        self.__faceUp.clear()
        return result

    def __str__(self):
        show = []
        for card, faceUp in zip(self.__cards, self.__faceUp):
            if (not faceUp):
                show.append(card)
            else:
                show.append("XX")
        return str(show)


def game():
    cards = readCards()
    A, B = distributeCards(cards)
    game_type = gameType()
    endGame = False
    cardsOnTable = OnTable()
    while not endGame:
        card1 = A.dequeue()
        cardsOnTable.place(1, card1, False)
        card2 = B.dequeue()
        cardsOnTable.place(2, card2, False)
        print(str(cardsOnTable))
        print("Player1: " + str(A.size()) + " cards")
        print("Player2: " + str(B.size()) + " cards")
        input("Press return key to continue")
        if (compareCards(card1, card2) == 1):
            tableCards = cardsOnTable.cleanTable()
            for i in tableCards:
                A.enqueue(i)
        elif (compareCards(card1, card2) == -1):
            tableCards = cardsOnTable.cleanTable()
            for i in tableCards:
                B.enqueue(i)
        else:
            countA=0
            while(countA<game_type and A.size()>0):
                cardsOnTable.place(1,A.dequeue(),True)
                countA+=1
            if (countA < game_type):
                tableCards = cardsOnTable.cleanTable()
                for i in tableCards:
                    B.enqueue(i)
                while (A.size() > 0):
                    B.enqueue(A.dequeue())
                endGame = True
            else:
                countB = 0
                while (countB < game_type and B.size() > 0):
                    cardsOnTable.place(2, B.dequeue(), True)
                    countB += 1
                if (countB < game_type):
                    tableCards = cardsOnTable.cleanTable()
                    for i in tableCards:
                        A.enqueue(i)
                    while (B.size() > 0):
                        A.enqueue(B.dequeue())
                    endGame = True

        if(A.size()==0 or B.size()==0):
            endGame=True

    if(A.size()>B.size()):
        print ("A is winner.")
    else:
        print ("B is winner.")

game()
