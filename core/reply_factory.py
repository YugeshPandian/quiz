
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id,session):
    question=PYTHON_QUESTION_LIST[current_question_id]
    if answer in question['options']:
        session[f"{question['user_answer']}"] = answer
        return True,current_question_id
    else:
        return False, current_question_id


def get_next_question(current_question_id):
   
    if current_question_id is None:
        return PYTHON_QUESTION_LIST[0]["question_text"], 0
    id_quest=len(PYTHON_QUESTION_LIST)
    if current_question_id in range(id_quest):
        return PYTHON_QUESTION_LIST[current_question_id + 1]["question_text"], current_question_id + 1



def generate_final_response(session):
    scores_obtained=0
    total_questions=len(PYTHON_QUESTION_LIST)
    for question in PYTHON_QUESTION_LIST:
        user_answer = session.get(f"{question['user_answer']}")

        if user_answer == question["answer"]:
            scores_obtained += 1

        final_response=f'Your Score is {scores_obtained}\n'
    if scores_obtained == total_questions:
        final_response+='Wow Great All are Correct'
    elif scores_obtained < (total_questions/2):
        final_response+='Your Score is Below the Average'
    return final_response
