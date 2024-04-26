from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    characters = db.relationship('CharacterSheet', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class CharacterSheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    character_name = db.Column(db.String(100), nullable=False)
    player_name = db.Column(db.String(100), nullable=True)
    class_level = db.Column(db.String(50), nullable=True)
    background = db.Column(db.String(100), nullable=True)
    race = db.Column(db.String(50), nullable=True)
    alignment = db.Column(db.String(50), nullable=True)
    experience_points = db.Column(db.Integer, nullable=True)
    inspiration = db.Column(db.Boolean, nullable=True)
    strength = db.Column(db.Integer, nullable=True)
    dexterity = db.Column(db.Integer, nullable=True)
    constitution = db.Column(db.Integer, nullable=True)
    intelligence = db.Column(db.Integer, nullable=True)
    wisdom = db.Column(db.Integer, nullable=True)
    charisma = db.Column(db.Integer, nullable=True)
    proficiency_bonus = db.Column(db.Integer, nullable=True)
    armor_class = db.Column(db.Integer, nullable=True)
    initiative = db.Column(db.Integer, nullable=True)
    speed = db.Column(db.Integer, nullable=True)
    hit_point_maximum = db.Column(db.Integer, nullable=True)
    current_hit_points = db.Column(db.Integer, nullable=True)
    temporary_hit_points = db.Column(db.Integer, nullable=True)
    hit_dice_total = db.Column(db.String(50), nullable=True)
    hit_dice = db.Column(db.String(50), nullable=True)
    death_save_successes = db.Column(db.Integer, nullable=True)
    death_save_failures = db.Column(db.Integer, nullable=True)
    personality_traits = db.Column(db.Text, nullable=True)
    ideals = db.Column(db.Text, nullable=True)
    bonds = db.Column(db.Text, nullable=True)
    flaws = db.Column(db.Text, nullable=True)
    features_traits = db.Column(db.Text, nullable=True)
    character_backstory = db.Column(db.Text, nullable=True)
    allies_organizations = db.Column(db.Text, nullable=True)
    additional_features_traits = db.Column(db.Text, nullable=True)
    spellcasting_class = db.Column(db.String(100), nullable=True)
    spellcasting_ability = db.Column(db.String(50), nullable=True)
    spell_save_dc = db.Column(db.Integer, nullable=True)
    spell_attack_bonus = db.Column(db.Integer, nullable=True)
    character_appearance = db.Column(db.Text, nullable=True)
    character_image = db.Column(db.String(255), nullable=True)
    faction_symbol_image = db.Column(db.String(255), nullable=True)

    skills = db.relationship('Skill', backref='character_sheet', lazy='dynamic', cascade='all,delete')
    saving_throws = db.relationship('SavingThrow', backref='character_sheet', lazy='dynamic', cascade='all,delete')
    attacks = db.relationship('Attack', backref='character_sheet', lazy='dynamic', cascade='all,delete')
    equipment = db.relationship('Equipment', backref='character_sheet', lazy='dynamic', cascade='all,delete')
    spells = db.relationship('Spell', backref='character_sheet', lazy='dynamic', cascade='all,delete')
    currencies = db.relationship('Currency', backref='character_sheet', lazy='dynamic', cascade='all,delete')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_sheet_id = db.Column(db.Integer, db.ForeignKey('character_sheet.id'), nullable=False)
    skill_name = db.Column(db.String(100))
    is_proficient = db.Column(db.Boolean)
    modifier = db.Column(db.Integer)

class SavingThrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_sheet_id = db.Column(db.Integer, db.ForeignKey('character_sheet.id'), nullable=False)
    save_name = db.Column(db.String(100))
    is_proficient = db.Column(db.Boolean)
    modifier = db.Column(db.Integer)

class Attack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_sheet_id = db.Column(db.Integer, db.ForeignKey('character_sheet.id'), nullable=False)
    name = db.Column(db.String(100))
    attack_bonus = db.Column(db.Integer)
    damage_type = db.Column(db.String(50))

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_sheet_id = db.Column(db.Integer, db.ForeignKey('character_sheet.id'), nullable=False)
    item_name = db.Column(db.String(100))
    item_description = db.Column(db.Text)
    item_image = db.Column(db.String(255))  # URL to image stored in S3

class Spell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_sheet_id = db.Column(db.Integer, db.ForeignKey('character_sheet.id'), nullable=False)
    spell_name = db.Column(db.String(100))
    level = db.Column(db.Integer)
    is_prepared = db.Column(db.Boolean)
    slots_total = db.Column(db.Integer)
    slots_used = db.Column(db.Integer)

class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_sheet_id = db.Column(db.Integer, db.ForeignKey('character_sheet.id'), nullable=False)
    cp = db.Column(db.Integer)
    sp = db.Column(db.Integer)
    ep = db.Column(db.Integer)
    gp = db.Column(db.Integer)
    pp = db.Column(db.Integer)
