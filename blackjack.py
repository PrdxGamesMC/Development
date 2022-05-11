
import random
import time


class BlackJack:
	def __init__(self):
		self.deck = self.Deck()
		self.player = self.Player(self.deck)
		self.dealer = self.Dealer(self.deck)
		
	def generate_deck(self):
		self.deck.generate()
		
	def shuffle_deck(self):
		self.deck.shuffle()
		
	def buy_in(self):
		try:
			self.player.bank = int(raw_input("Enter Buy In Amount: $"))
		except TypeError:
			self.buy_in()

	def mainloop(self):
		while True:
			self.reset()
			self.opening()
			self.players_turn()
			self.dealers_turn()
			self.payout()

	def opening(self):
		# Alternate Dealing Between Player And Dealer
		for c in range(2):
		self.player._hit()
		self.dealer._hit()

    def check_for_flag(self):
        if self.player.hands.hands[0].value == 21:
            self.player_has_21()

        if self.dealer.hands.hands[0].cards[1] == "A":
            self.insurance()
            return

        if self.dealer.hands.hands[0].value == 21:
            self.dealer_has_21()
            return

    def player_has_21(self):
        hand, value = self.player.hands.hands[0].cards, self.player.hands.hands[0].value
        dealers_hand, dealers_value = self.dealer.hands.hands[0].cards, self.dealer.hands.hands[0].value
        bar = "-" * (max(len(str("Your Hand: %s  Value:  %s" % (hand, value))), len(str("Dealers Hand:   %s  Value:  %s" % (dealers_hand, dealers_value)))) + 2)
        print(bar)
        print("Your Hand:\t%s\tValue:\t%s" % (hand, value))
        print("Dealers Hand:\t%s\tValue:\t%s" % (dealers_hand, dealers_value))
        print(bar)
        self.dealer.hands.hands[0].can_hit = False
        return

    def insurance(self):
        hand, value = self.player.hands.hands[self.player.current_hand].cards, self.player.hands.hands[self.player.current_hand].value
        dealers_hand, dealers_value = self.dealer.hidden_hand()

        bar = "-" * (max(len(str("Your Hand: %s  Value:  %s" % (hand, value))), len(str("Dealers Hand:   %s  Value:  %s" % (dealers_hand, dealers_value)))) + 2)
        print(bar)
        print("Your Hand:\t%s\tValue:\t%s" % (hand, value))
        print("Dealers Hand:\t%s\tValue:\t%s" % (dealers_hand, dealers_value))
        print(bar)

        if raw_input("Would You Like Insurance ($%s): " % str(self.player.bet * 0.5)) == "y":
            print("-$%s" % float(self.player.bet * 0.5))
            self.player.bank -= float(self.player.bet * 0.5)

            if self.dealer.hands.hands[0].value == 21:
                print("The Dealer Had 21!")
                print("+$%s" % self.player.bet)
                self.player.bank += self.player.bet
                return

            print("The Dealer Did Not Have 21!")
            return

        if self.dealer.hands.hands[0].value == 21:
            print("The Dealer Had 21!")
            self.player.hands.hands[0].can_hit = False
            return

        print("The Dealer Did Not Have 21!")

    def dealer_has_21(self):
        hand, value = self.player.hands.hands[0].cards, self.player.hands.hands[0].value
        dealers_hand, dealers_value = self.dealer.hands.hands[0].cards, self.dealer.hands.hands[0].value
        bar = "-" * (max(len(str("Your Hand: %s  Value:  %s" % (hand, value))), len(str("Dealers Hand:   %s  Value:  %s" % (dealers_hand, dealers_value)))) + 2)
        print(bar)
        print("Your Hand:\t%s\tValue:\t%s" % (hand, value))
        print("Dealers Hand:\t%s\tValue:\t%s" % (dealers_hand, dealers_value))
        print(bar)
        self.player.hands.hands[0].can_hit = False

    def players_turn(self):
        self.check_for_flag()
        self.player_mainloop()

    def player_mainloop(self):
        while self.player.hands.hands[self.player.current_hand].can_hit:
            hand, value = self.player.hands.hands[self.player.current_hand].cards, self.player.hands.hands[self.player.current_hand].value
            dealers_hand, dealers_value = self.dealer.hidden_hand()
            bar = "-" * (max(len(str("Your Hand: %s  Value:  %s" % (hand, value))), len(str("Dealers Hand:   %s  Value:  %s" % (dealers_hand, dealers_value)))) + 2)
            print(bar)
            print("Your Hand:\t%s\tValue:\t%s" % (hand, value))
            print("Dealers Hand:\t%s\tValue:\t%s" % (dealers_hand, dealers_value))
            print(bar)
            
            if raw_input("Would You Like To Hit Or Stand?: ") == "h":
                self.player._hit()
                continue
            self.player._stand()

        print("Your Hand:\t%s\tValue:\t%s" % (self.player.hands.hands[self.player.current_hand].cards,
                          self.player.hands.hands[self.player.current_hand].value))

    def dealers_turn(self):
        print("Dealers Hand:\t%s\tValue:\t%s" % (self.dealer.hands.hands[0].cards, self.dealer.hands.hands[0].value))
        
        if self.player.hands.hands[0].winnable:
            if len(self.player.hands.hands[0].cards) == 2:
                if self.player.hands.hands[0].value == 21:
                    return
            
            self.dealer.make_decision()
            self.dealer_mainloop()
        time.sleep(0.5)

    def dealer_mainloop(self):
        while self.dealer.hands.hands[0].can_hit:
            time.sleep(0.5)
            self.dealer._hit()
            print("Dealers Hand:\t%s\tValue:\t%s" % (self.dealer.hands.hands[0].cards, self.dealer.hands.hands[0].value))
            self.dealer.make_decision()
            
        self.dealer._stand()

    def payout(self):
        if self.dealer.hands.hands[0].value < self.player.hands.hands[0].value <= 21 or self.player.hands.hands[0].value <= 21 < self.dealer.hands.hands[0].value:
            if len(self.player.hands.hands[0].cards) == 2 and self.player.hands.hands[0].value == 21:
                win = 2.5 * self.player.bet
                self.player.bank += win
                print("BLACKJACK +$%s" % win)
                return
            
            win = 2 * self.player.bet
            self.player.bank += win
            print("YOU WON +$%s" % win)
            return
        
        if self.dealer.hands.hands[0].value == self.player.hands.hands[0].value:
            self.player.bank += self.player.bet
            print("PUSH +$0")
            return
        
        print("YOU LOST -$%s" % self.player.bet)

    def reset(self):
        self.player.reset()
        self.dealer.__init__(self.deck)
        self.player.bet = self.player.bank + 1
        
        while self.player.bet > self.player.bank or self.player.bet < 5:
            self.player.bet = int(raw_input("Balance: $%s\nEnter Amount You Would Like To Bet: $" % self.player.bank))
            
            if self.player.bet > self.player.bank:
                print("Bet Cannot Be Larger Than You Balance!")
                
            if self.player.bet < 5:
                print("Minimum Bet Is $5")
                
        self.player.bank -= self.player.bet

    class Player:
        def __init__(self, deck, bet=0, bank=0):
            self.deck = deck
            # On __init__() One Hand Will Be Generated, More Can Be Added By Splitting
            self.hands = [self.Hand()]
            self.current_hand = 0
            self.bank = bank
            self.bet = bet

        def _hit(self):
            a, v = self.deck.deal_card()
            self.hands.hands[self.current_hand].cards.append(a)
            self.hands.hands[self.current_hand].add_value(v)
            self.hands.hands[self.current_hand].update_hand()
            self.hands.hands[self.current_hand].clean_value()
            self.can_split = False

        def _stand(self):
            if not isinstance(self.hands.hands[self.current_hand].value, int):
                self.hands.hands[self.current_hand].value = max(self.hands.hands[self.current_hand].value)
                
            self.hands.hands[self.current_hand].can_hit = False
            self.hands.hands[self.current_hand].can_split = False

        def _split(self):
            pass

        def add_hand(self):
            card = [self.hands.hands[self.current_hand].cards.pop(1)]
            value = self.deck.card_to_value[card]
            self.hands.hands.insert(self.current_hand + 1, self.hands.Hand(self.deck, self.current_hand + 1, card, value, True))
            self.hands.hands[self.current_hand].value = self.deck.card_to_value[self.hands.hands[self.current_hand].cards[0]]
            self.hands.hands[self.current_hand].needs_card = True

        def reset(self):
            self.hands = self.Hands(self.deck)
            self.current_hand = 0

		class Hand:
			def __init__(self, deck, hand=0, cards=None, value=None, needs_card=False):
				if value is None
					value = [0, 0]
				if cards is None:
					cards = []
				self.deck = deck
				self.cards = cards
				self.hand = hand
				self.cards = cards
				self.value = value
				self.winnable = True
				self.can_hit = True
				self.can_double = True
				self.can_split = False
				self.needs_card = needs_card

			def add_value(self, v):
				# Ensures That 'self.value' Is A List Object
				if isinstance(self.value, int):
					self.value = [self.value, self.value]
                        
				# Adds Min And Max Of List'    
				self.value = [self.value[0] + v[0], self.value[1] + v[1]]

			def update_hand(self):
				if len(self.cards) == 2:
					if self.cards[0] == self.cards[1]:
						self.can_split = True
                            
				if self.value[0] == 21 or self.value[1] == 21:
					self.value = 21
					self.winnable, self.can_hit = True, False
					return
                    
				if self.value[0] > 21:
					self.winnable, self.can_hit = False, False
					print("BUST")
					return
                    
				if self.value[1] > 21:
					self.value = [self.value[0], self.value[0]]
					self.winnable, self.can_hit = True, True

			def clean_value(self):
				if isinstance(self.value, int):
					self.value = [self.value, self.value]
                        
				if self.value[0] == self.value[1]:
					self.value = self.value[0]

    class Dealer(Player):
        def make_decision(self):
            if isinstance(self.hands.hands[0].value, int):
                self.hands.hands[0].value = [self.hands.hands[0].value, self.hands.hands[0].value]
                
            if max(self.hands.hands[0].value) >= 17:
                self.hands.hands[0].can_hit = False
                self.hands.hands[0].value = self.hands.hands[0].value[1]

        def hidden_hand(self):
            return "['?', '%s']" % self.hands.hands[0].cards[1], self.deck.card_to_value[self.hands.hands[0].cards[1]]

    class Deck:
        def __init__(self):
            self.deck = []
            self.card_table = {
                0: ("A", [1, 11]),
                1: ("2", [2, 2]),
                2: ("3", [3, 3]),
                3: ("4", [4, 4]),
                4: ("5", [5, 5]),
                5: ("6", [6, 6]),
                6: ("7", [7, 7]),
                7: ("8", [8, 8]),
                8: ("9", [9, 9]),
                9: ("10", [10, 10]),
                10: ("J", [10, 10]),
                11: ("Q", [10, 10]),
                12: ("K", [10, 10])
            }
            self.card_to_value = {
                "A": [1, 11],
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5,
                "6": 6,
                "7": 7,
                "8": 8,
                "9": 9,
                "10": 10,
                "J": 10,
                "Q": 10,
                "K": 10
            }

        def generate(self):
            for d in range(4):
                for s in range(4):
                    for c in range(13):
                        self.deck.append(self.card_table[c])

        def shuffle(self):
            for c in range(0, 52 * 3):
                r = random.randint(0, 52 * 4 - 1)
                self.deck[c], self.deck[r] = self.deck[r], self.deck[c]

        def deal_card(self):
            return self.deck.pop()


BJ = BlackJack()
BJ.generate_deck()
BJ.shuffle_deck()
BJ.buy_in()
BJ.mainloop()
