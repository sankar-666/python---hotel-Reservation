from flask import Flask,render_template
from public import public
from admin import admin


app=Flask(__name__)

app.secret_key="prayulla"

app.register_blueprint(admin,url_prefix="/admin")
app.register_blueprint(public)

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

app.run(debug=True,port=5077,host="0.0.0.0")