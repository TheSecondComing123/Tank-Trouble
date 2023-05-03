class Player:
    def __init__(self, id, controller_id):
        self.id = id #player1, player2, etc
        self.controller_id = controller_id #the controller instance_id, -1 if not using

