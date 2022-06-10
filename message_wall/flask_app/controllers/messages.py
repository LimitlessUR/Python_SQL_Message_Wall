from flask import render_template, session,flash,redirect, request
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message


@app.route('/create/message',methods=['POST'])
def create_message():
    
    data = {
        "content": request.form["content"],
        "user_id": session["user_id"]
    }
    Message.save(data)
    return redirect('/dashboard')

@app.route('/messages/<int:message_id>/like',methods=['POST'])
def like_message(message_id):
    
    liker_data = {
        "message_id": message_id,
        "user_id": session["user_id"]
    }
    Message.like_message(liker_data)
    return redirect('/dashboard')

@app.route('/destroy/message/<int:id>')
def destroy_message(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Message.destroy(data)
    return redirect('/dashboard')

