from flask import Flask, render_template,g,request,redirect,url_for
from flask_socketio import SocketIO,send,emit,join_room,leave_room
from flask_login import login_user,logout_user,current_user ,login_required,login_manager,LoginManager
from models import User,Infos,db
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.db';
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
app.secret_key = 'OrzQAQ'

db.init_app(app);

socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


infos = Infos();

@login_manager.user_loader
def load_user(id):
    return  User.query.get(id);

@socketio.on('battle')
def handle_battle(Sta):
    room = infos.userRoom[current_user.id];
    if(len(infos.getroom(room).board) == 84):
        return;
    tim = time.time();
    infos.getroom(room).addChess(Sta);
    Sta["tim"]=infos.getroom(room).updLeft(int(Sta["o"]),tim);
    emit('battle',Sta,room=room);
    if len(infos.getroom(room).board) == 84:
        emit('gameover',{},room=room);

@socketio.on('loginRoom')
def loginroom(val):
    room = infos.userRoom[current_user.id];
    join_room(room);
    stTim = time.time();
    emit('romsta', {"o":infos.getroom(room).state,"time":stTim,"user":infos.getroom(room).user}, room=room);
    if infos.getroom(room).state == 15:
        infos.getroom(room).start(time.time());


@socketio.on('wantFace')
def giveFace(use):
    if current_user.id not in infos.userRoom:
        return;
    room = infos.userRoom[current_user.id];
    join_room(room);
    if infos.getroom(room).state != 15:
        emit('romsta', {"o":infos.getroom(room).state,"time":time.time(),"user":infos.getroom(room).user});
        return;
    cur = time.time() - infos.getroom(room).lastTime;
    board = {"val":infos.getroom(room).board,"timer":infos.getroom(room).left,"cur":int(cur),"user":infos.getroom(room).user};
    emit('loadSta', board);

@app.route("/index")
def index():
    return render_template('index.html');

@app.route("/login",methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("u");
        password = request.form.get("p");
        repeat = request.form.get("rp","");
        if repeat == "":
            user = User.query.filter_by(username=username).first();
            if user is not None and user.check_password(password):
                login_user(user);
                return redirect(request.args.get('next','index'));
            else:
                return render_template("login.html",message="User not exist or Wrong password!");
        else:
            if password != repeat:
                return render_template("register.html",message="confirm password not same") 
            if User.query.filter_by(username=username).first() is not None:
                return render_template("register.html",message="User exist!");
            if len(username) > 15:
                return render_template("register.html",message="User name too long!");
            nuser = User(username,password);
            db.session.add(nuser);
            db.session.commit();
            login_user(nuser);
            return  redirect("/index");
    if request.method == 'GET':
        return render_template("login.html",message="");


@app.route("/room/<room>")
@login_required
def roomIndex(room):
    if infos.userInRoom(current_user.id,room):
        sta = 15 - (1 << infos.userChair[current_user.id]);
    else:
        infos.setRoom(current_user.id,room);
        sta = infos.getroom(room).state;
    return render_template('room.html', sta=sta, room=room);

@app.route("/room/<room>/play/<_ind>")
@login_required
def handle_query(room,_ind):
    ind = int(_ind);
    if infos.userInRoom(current_user.id,room):
        return render_template("playGround.html"
                              ,play = infos.userChair[current_user.id]
                              ,first="false");

    if infos.tryInRoom(current_user.id, room, ind):
        return render_template("playGround.html",play = ind,first="true")
    else:
        return redirect("/room/%s" % (room,));

@app.route("/room/<room>/ob")
@login_required
def ob(room):
    infos.userRoom[current_user.id] = room;
    return render_template("playGround.html",play = -1,first="false")

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=80);

