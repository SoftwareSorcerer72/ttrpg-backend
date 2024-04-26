from flask import request, jsonify
from .extensions import db, jwt
from .models import User, CharacterSheet
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User, CharacterSheet, Skill, SavingThrow, Attack, Equipment, Spell, Currency

def register_routes(app):

    @app.route('/')
    def home():
        return "Welcome to TTRPG Grimoire!", 200

    @app.route('/signup', methods=['POST'])
    def signup():
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return jsonify({'message': 'User already exists'}), 409
        new_user = User(username=data['username'], email=data['email'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        return jsonify({'message': 'Invalid credentials'}), 401

    @app.route('/user', methods=['PUT'])
    @jwt_required()
    def edit_user():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        data = request.get_json()
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200

    @app.route('/user', methods=['DELETE'])
    @jwt_required()
    def delete_user():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200

    @app.route('/character', methods=['POST'])
    @jwt_required()
    def create_character():
        user_id = get_jwt_identity()
        data = request.get_json()
        if data is None:
            return jsonify({'message': 'Invalid request body'}), 400
        skills_data = data.pop('skills', [])
        new_character = CharacterSheet(user_id=user_id, **data)
        db.session.add(new_character)
        db.session.commit()
        skills = [Skill(character_sheet_id=new_character.id, **skill_data) for skill_data in skills_data]
        db.session.add_all(skills)
        db.session.commit()
        return jsonify({'message': 'Character sheet created'}), 201

    @app.route('/character', methods=['GET'])
    @jwt_required()
    def view_characters():
        user_id = get_jwt_identity()
        characters = CharacterSheet.query.filter_by(user_id=user_id).all()
        return jsonify([char.to_dict() for char in characters]), 200
    
    @app.route('/character/<int:id>', methods=['GET'])
    @jwt_required()
    def get_character(id):
        user_id = get_jwt_identity()
        character = CharacterSheet.query.filter_by(user_id=user_id, id=id).first()
        if character is None:
            return jsonify({'message': 'Character not found'}), 404
        return jsonify(character.to_dict()), 200



    @app.route('/character/<int:character_id>', methods=['PUT'])
    @jwt_required()
    def edit_character(character_id):
        character = CharacterSheet.query.get(character_id)
        data = request.get_json()
        if data is None:
            return jsonify({'message': 'Invalid request body'}), 400
    
        for key, value in data.items():
            if hasattr(character, key):
                setattr(character, key, value)
    
        db.session.commit()
        return jsonify({'message': 'Character sheet updated'}), 200
    

    @app.route('/character/<int:character_id>', methods=['DELETE'])
    @jwt_required()
    def delete_character(character_id):
        character = CharacterSheet.query.get(character_id)
        db.session.delete(character)
        db.session.commit()
        return jsonify({'message': 'Character sheet deleted'}), 200