from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SubmitField,TextAreaField,RadioField
from wtforms.validators import Required,Email,EqualTo
from wtforms import ValidationError


	

class CommentForm(FlaskForm):
	description = TextAreaField('',validators=[Required()])
	submit = SubmitField() 

class PostForm(FlaskForm):
    title = StringField("title",validators=[Required()])
    post = TextAreaField("post",validators=[Required()])
    author = StringField("author",validators=[Required()])
    submit = SubmitField('post blog')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')