import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import date, datetime
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
import json
from functions import *

###Date and time###
def dateTimee():
    timp = datetime.now()
    timp_curent = timp.strftime("%H:%M:%S")

    data = date.today()
    data_curenta = data.strftime("%b-%d-%Y")
    return timp_curent, data_curenta


#################################
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
# Configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# Modules
db = SQLAlchemy(app)

# DB model
class add_log_db(db.Model):
    __tablename__ = 'logs'
    log_id = db.Column(db.Integer, primary_key=True)
    numeUser = db.Column(db.String(256), index=True)
    cheie = db.Column(db.String(256), index=True)
    validare_cheie = db.Column(db.String(256), index=True)
    timp_arg = db.Column(db.String(256), index=True)
    data_arg = db.Column(db.String(256), index=True)
    ip_add = db.Column(db.String(256), index=True)


# Schema Objects
class AddLogObject(SQLAlchemyObjectType):
    class Meta:
        model = add_log_db
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_posts = SQLAlchemyConnectionField(AddLogObject)


class CreatePost(graphene.Mutation):
    class Arguments:
        cheie = graphene.String(required=True)
        numeUser = graphene.String(required=True)

    post = graphene.Field(lambda: AddLogObject)

    def mutate(self, info, cheie, numeUser):
        f = open('private_key.json', )
        data = json.load(f)
        key_from_json = data['private_key']
        f.close()
        if cheie == key_from_json:
            validare_cheie = "cheie valida"
            a = dateTimee()
            timp_curent = a[0]
            data_curenta = a[1]
            ip_address = flask.request.remote_addr
            post = add_log_db(numeUser=numeUser, cheie=cheie, validare_cheie=validare_cheie, timp_arg=timp_curent, data_arg=data_curenta,
                              ip_add=ip_address)
            db.session.add(post)
            db.session.commit()
            LED_verde_Blink()
        else:
            validare_cheie = "cheie invalida"
            a = dateTimee()
            timp_curent = a[0]
            data_curenta = a[1]
            ip_address = flask.request.remote_addr
            post = add_log_db(numeUser=numeUser, cheie=cheie, validare_cheie=validare_cheie, timp_arg=timp_curent, data_arg=data_curenta,
                              ip_add=ip_address)
            db.session.add(post)
            db.session.commit()
            LED_rosu_Blink()
        return CreatePost(post=post)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


#### routes

app.add_url_rule(
    '/',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # for having the GraphiQL interface
    )
)

##################################

