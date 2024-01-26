import logging

from flask import Blueprint, render_template, request, redirect

from app.db import add_question, get_questions, get_correct

bp = Blueprint("tests", __name__)

filename = "data.txt"


@bp.route("/")
def root():
    poll_data = get_questions()
    poll_data = [dict(row) for row in poll_data]
    return render_template("poll.html", data=poll_data, number_of_ques=len(poll_data))


@bp.route("/add_test", methods=["GET", "POST"])
def add_test():
    if request.method == "GET":
        return render_template("add_test.html")
    else:
        number_of_ques = int(request.form.get("numberOfQuestions"))
        for number in range(1, number_of_ques+1):
            question = request.form.get(f"question{number}")
            answers = request.form.get(f"answers{number}")
            correct = request.form.get(f"correct{number}")
            add_question(question, answers, correct)
        return redirect("/")


@bp.route("/poll")
def poll():
    # Потрібно перевірити, чи користувач ввів правильну відповідь
    # В базі проводимо пошук за запитанням (написати свій власний файл db.py)
    # і перевіряємо, чи співпадає зі value
    # Виводимо користувачу, на скільки запитань він правильно відповів (наприклад, 10/12)

    number_of_ques = request.args.get('numberOfQues', "NOTHING")
    counter = 0

    for key, value in request.args.items():
        if "field" in key:
            question = key.split('_')
            print(question)

            if question:
                user_answer = value
                correct_answer = get_correct(question[1])
                print(f"{user_answer} - {correct_answer}  <--------------")

                if user_answer == correct_answer:
                    counter += 1

    poll_data = f"Ви відповіли правильно на {counter}/{number_of_ques} питань."

    # Переробляємо thankyou.html під це все діло
    return render_template("thankyou.html", data=poll_data)