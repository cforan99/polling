from flask import Flask, request, render_template, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
db = SQLAlchemy(app)


@app.route("/submit", methods=["POST"])
def add_comment():
	"""Adds comment to db"""

	text = request.form.get("text")
	timestamp = datetime.now()

	QUERY = """
		INSERT INTO Comments (comment, timestamp)
		VALUES (:text, :timestamp)
		"""

	db.session.execute(QUERY, {'text': text, 'timestamp': timestamp})
	db.session.commit()

	return


@app.route("/comments")
def list_comments():
	"""Returns JSON object of all comments in db"""
	
	QUERY = """
		SELECT id, comment FROM Comments
		"""

	db_cursor = db.session.execute(QUERY)
	rows = db_cursor.fetchall()

	print rows 

	comments = {}
	for row in rows:
		number, comment = row
		comments[number] = comment

	print comments

	return jsonify(comments)


if __name__ == "__main__":
	app.run()