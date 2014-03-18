from wtforms import Form, TextField, validators

class CreatingForm(Form):
    text = TextField('Story', [validators.Length(min=20, max=1024)])
    
