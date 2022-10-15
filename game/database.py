"""This module consists of the functions related to data read and write."""


from datetime import datetime
import pymongo

class Database():
    """This is the database class consisting of the read and write operations to the database.
    """

    def __init__(self, URI='mongodb://localhost:27017'):
        """Constructor of the database class which connects to a mongodb database.

        Args:
            URI (str, optional): The database URI of mongodb. Defaults to 'mongodb://localhost:27017'.
        """

        self.client = pymongo.MongoClient(URI)
        self.db = self.client['cop701_assignment_2']
        self.square_col = self.db['squares']
        self.players_col = self.db['players']
        self.players_col.delete_many({})

    def insert_points(self, squares):
        """Insert all of the coordinates of the squares.
        Each time before inserting all of the points the database clears its previous records.

        Args:
            squares (dictionary): {'id':int,'x0':int,'y0':int}
        """

        self.square_col.delete_many({})
        self.square_col.insert_many(squares)

    def insert_player(self, player):
        """Insert a single player to the database.

        Args:
            player (dictionary): {'id':int,'name':str,'points':0}
        """

        self.players_col.insert_one(player)

    def find_square_id(self, square_id, player_id, clicked_at):
        """Find a square with the given id and whether it is clicked previously.

        Args:
            square_id (int): id the of the square
            player_id (int): id of the player who currently has clicked the square.
            clicked_at (datetime.datetime): timestamp when the player has clicked on the square.

        Returns:
            tuple: id of the player who has previously clicked on the square and id of the player who is actual owner of the square points as of now.
        """
        
        old_doc = {'id':square_id}
        doc = self.square_col.find_one(old_doc) 
        previously_clicked_at = doc.get('clicked_at')
        final_clicker = None 
        if previously_clicked_at is None:
            new_doc = {"$set": {"player_id":player_id, "clicked_at": clicked_at}}
            self.square_col.update_one(old_doc, new_doc)
            player_old_doc = self.players_col.find_one({"id":player_id})
            player_new_doc = {"$set":{"points":int(player_old_doc.get('points'))+5}}
            self.players_col.update_one(player_old_doc, player_new_doc)
            final_clicker = player_id 
            current_clicker = player_id 
            actual_clicker = player_id
        else:
            previously_clicked_at = datetime.strptime(previously_clicked_at, '%Y-%m-%d %H:%M:%S.%f')
            clicked_at = datetime.strptime(clicked_at, '%Y-%m-%d %H:%M:%S.%f')
            
            if previously_clicked_at > clicked_at:
                current_clicker = doc.get('player_id')
                current_clicker_old_doc = self.players_col.find_one({'id':current_clicker})
                current_clicker_new_doc = {"$set": {"points":int(current_clicker_old_doc.get('points'))-5}}
                self.players_col.update_one(current_clicker_old_doc, current_clicker_new_doc)

                actual_clicker = player_id
                actual_clicker_old_doc = self.players_col.find_one({'id':actual_clicker})
                actual_clicker_new_doc = {"$set": {"points":int(actual_clicker_old_doc.get('points'))+5}}
                self.players_col.update_one(actual_clicker_old_doc, actual_clicker_new_doc)

                new_doc = {"$set": {"player_id":player_id, "clicked_at": clicked_at}}
                self.square_col.update_one(old_doc, new_doc)
                final_clicker = player_id 

            else:
                final_clicker = doc.get('player_id')
                current_clicker = final_clicker
                actual_clicker = final_clicker
        return (current_clicker, actual_clicker)

    def game_over_request(self, player_id):
        """Updates a player row when that player's game is over.

        Args:
            player_id (int): id of the player

        Returns:
            bool: whether all of the players game is over or not
        """

        old_doc = {"id":player_id} 
        new_doc = {"$set":{"game_over":True}}
        self.players_col.update_one(old_doc, new_doc)

        count_1 = self.players_col.count_documents({"game_over":True})
        count_2 = self.players_col.count_documents({})
        # print(f'server the req of {player_id}: {count_1}, {count_2}')
        return count_1==count_2

    def get_players(self):
        """Returns list of all players

        Returns:
            mongodb doc list: list of all players
        """

        return self.players_col.find({})

    def get_final_ranks(self):
        """Returns list of all players

        Returns:
            list: list of all players
        """
        all_players = self.get_players()
        final_ranks = [] 
        for index, player in enumerate(all_players):
            name = player.get('name')
            points = player.get('points')
            final_ranks.append([index+1, name, points])
        
        return final_ranks

    def decrease_player(self, player_id):
        """When a player disconnects from the server, server keeps a updates the player row such that the player is disconnected.

        Args:
            player_id (int): id of the dis-connecting player

        Returns:
            int: how many players are still connected to the server
        """
        
        old = {'id':player_id}
        new_doc = {"$set":{'closed':True}}
        self.players_col.update_one(old,new_doc)

        count1 = self.players_col.count_documents({'closed':True})
        count2 = self.players_col.count_documents({})
        return count2-count1 


        # new_doc = {"$set": {'clicked_by':player_id, 'clicked_at':clicked_at}}