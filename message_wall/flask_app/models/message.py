from flask_app.config.mysqlconnection import connectToMySQL
from ..models import user
from flask import flash

class Message:
    db_name = 'wall_schema'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.content = db_data['content']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.creator = None 
        self.likers= []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO messages (content,user_id) VALUES(%(content)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM messages LEFT JOIN users on users.id = messages.user_id left join likes on messages.id = likes.message_id left join users as likers on likers.id = likes.user_id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)

        all_messages=[]

        for row in results:

            new_message = True

            liker_data = {
                'id':row['likers.id'],
                'first_name':row['likers.first_name'],
                'last_name':row['likers.last_name'],
                'email':row['likers.email'],
                'password':row['likers.password'],
                'created_at':row['likers.created_at'],
                'updated_at':row['likers.updated_at'],
            } 
            if len(all_messages)>0 and all_messages[len(all_messages)-1].id == row['id']:
                all_messages[len(all_messages)-1].likers.append(user.User(liker_data))
                new_message = False

            if new_message:
                this_message = cls(row)

                creator_data = {
                    'id':row['users.id'],
                    'first_name':row['first_name'],
                    'last_name':row['last_name'],
                    'email':row['email'],
                    'password':row['password'],
                    'created_at':row['users.created_at'],
                    'updated_at':row['users.updated_at'],
                    }

                this_creator = user.User(creator_data)
                this_message.creator = this_creator

                if row['likers.id'] is not None:
                    
                    this_message.likers.append(user.User(liker_data))
                all_messages.append(this_message)
        return all_messages

    @classmethod
    def like_message(cls,data):
        query = "INSERT INTO likes(message_id, user_id) VALUES (%(message_id)s, %(user_id)s );"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM messages WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)