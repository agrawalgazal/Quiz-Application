from django.core.exceptions import ValidationError


def validate_levels(value):


    if value!='E' and value!='M' and value!='H' and value!='X':
        raise ValidationError("not a valid level")
    
def validate_user_answer(value):
    if(len(value)>200):
        raise ValidationError("length is greather than 200")
    
def validate_topic_name(value):

    if value[-1]!='E' and value[-1]!='M' and value[-1]!='H' and value[-1]!='E':
        raise ValidationError("not a valid level")
    
def validate_question_response_time(value):

    if value>30:
        raise ValidationError("question submission time is must not exceed 30 seconds")
    

def validate_attempt(value):

    if value<0:
        raise ValidationError("attempt can't be negative")




    

