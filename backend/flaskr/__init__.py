import os
import random
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
  @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
  """
    CORS(app, resources={r"*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
  """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorizations, True"
        )
        response.headers.add(
            "Access-Control-Allow-Methods",
            "GET,POST,PATCH,DELETE,OPTIONS"
        )
        return response

    """
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  """

    @app.route("/questions", methods=["GET"])
    def index():
        try:
            page = request.args.get("page", 1, type=int)
            Questionlist = Question.query.paginate(
                page, QUESTIONS_PER_PAGE, False
            ).items
            Question_page = Question.query.paginate(
                page, QUESTIONS_PER_PAGE, False
            ).pages

            list_of_formatted_questions = []

            for question in Questionlist:
                list_of_formatted_questions.append(question.format())

            total_questions = Question_page * QUESTIONS_PER_PAGE

            if total_questions == 0:
                return not_found(404)

            if not (page <= Question_page):
                return not_found(404)

            categories_id = {}
            categories = Category.query.all()

            for category in categories:
                categories_id[category.id] = category.type

            response_object = {
                "success": True,
                "questions": list_of_formatted_questions,
                "total_questions": total_questions,
                "categories": categories_id,
                "current_category": None,
            }
            return jsonify(response_object)
        except:
            return Internal_Server_Error(500)

    """
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  """

    @app.route("/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):
        try:
            question = Question.query.get(id)

            if question is None:
                return Bad_Request(400)

            db.session.delete(question)
            db.session.commit()

            response_object = {
                "success": True,
                "message": f"The question with ID: {id} was successfully deleted.",
            }
            return jsonify(response_object)
            db.session.close()
        except:
            db.session.rollback()
            db.session.close()
            return unprocessable(422)

    """
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  """

    @app.route("/post_questions", methods=["POST"])
    def post_question():
        try:
            request_data = request.get_json()
            question = request_data["question"]
            answer = request_data["answer"]
            category = request_data["category"]
            difficulty = request_data["difficulty"]

            try:
                question_model = Question(
                    question=question,
                    answer=answer,
                    category=int(category) + 1,
                    difficulty=difficulty,
                )

                db.session.add(question_model)
                db.session.commit()
                response_object = {
                    "success": True,
                    "message": f"The question: '{question}' has been added to the Trivia",
                }
            except:
                db.session.rollback()
                db.session.close()
                response_object = {
                    "success": False,
                    "message": f"The question: '{question}' has been refused due to invalid inputs.",
                }
            finally:
                return jsonify(response_object)
        except:
            return Bad_Request(400)

    @app.route("/categories")
    def get_available_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            categories_list = [category.type for category in categories]
            response_object = {
                "success": True,
                "categories": categories_list,
                "number_of_categories": len(categories_list),
            }
            return jsonify(response_object)
        except:
            return unprocessable(422)

    """
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  """

    @app.route("/questions", methods=["POST"])
    def search_questions():
        try:
            request_data = request.get_json()
            search_key = request_data["searchTerm"]

            results = Question.query.filter(
                Question.question.ilike(f"%{search_key}%")
            ).all()

            if len(results) == 0:
                return not_found(404)

            list_of_results = [question.format() for question in results]
            response_object = {
                "success": True,
                "questions": list_of_results,
                "current_category": None,
                "total_questions": len(list_of_results),
            }
            return jsonify(response_object)
        except:
            return unprocessable(422)

    """
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  """

    @app.route("/categories/<int:id>/questions")
    def get_By_category(id):
        try:
            current_category = Category.query.get(id)

            if current_category is None:
                return not_found(404)

            current_category = current_category.format()

            relevant_questions = Question.query.filter(
                Question.category == id).all()

            questions_for_currrent_category = [
                question.format() for question in relevant_questions
            ]

            response_object = {
                "success": True,
                "questions": questions_for_currrent_category,
                "total_questions": len(questions_for_currrent_category),
                "current_category": current_category["type"],
            }

            return jsonify(response_object)
        except:
            db.session.rollback()
            abort(500)

        finally:
            db.session.close()

    """
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  """
    @app.route("/quizzes", methods=["POST"])
    def get_questions_for_quiz():
        try:
            questions = []
            next_ques = []

            data = request.get_json()
            previous_questions = data.get("previous_questions")
            quiz_category = data.get("quiz_category")

            if (
                quiz_category is None
                or quiz_category is {}
                or quiz_category["id"] is None
            ):
                return Bad_Request(400)

            if int(quiz_category["id"]) == -1:
                questions = Question.query.all()
            else:
                category_id = int(quiz_category["id"]) + 1
                questions = Question.query.filter(
                    Question.category == category_id
                ).all()

            if len(previous_questions) > 0:
                for pre_q in previous_questions:
                    for q in questions:

                        if q.format()["id"] == pre_q:
                            questions.remove(q)

            if len(questions) != 0:
                next_ques_id = random.randrange(0, len(questions))
                next_ques = questions[next_ques_id]

                return jsonify(
                    {
                        "success": True,
                        "question": next_ques.format(),
                    }
                )
            else:
                return jsonify(
                    {
                        "success": True,
                        "question": None,
                    }
                )
        except:
            return Internal_Server_Error(500)

    """
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False,
                        "error": 404,
                        "message": "Not found"}
                       ), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False,
                        "error": 422,
                        "message": "unprocessable"}
                       ), 422

    @app.errorhandler(400)
    def Bad_Request(error):
        return jsonify({"success": False,
                        "error": 400,
                        "message": "Bad Request"}
                       ), 400

    @app.errorhandler(500)
    def Internal_Server_Error(error):
        return jsonify(
            {"success": False,
             "error": 500,
             "message": "Internal Server Error"}
        ), 500

    return app
