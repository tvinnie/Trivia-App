import os
from unicodedata import category
from urllib.request import Request
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from pkg_resources import require

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [category.format() for category in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
  
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
        
    @app.route('/categories', methods=['GET'])
    def get_categories():
       check__on_cats = Category.query.order_by(Category.type).all()
       return jsonify({
        'success': True,
        'categories': {category.id: category.type for category in check__on_cats}
        })

    @app.route("/questions")
    def get_questions():
        selection_quiz = Question.query.all()
        selection_category = Category.query.all()

        current_question = paginate_questions(request, selection_quiz)
        current_category = [category.format() for category in selection_category]

        caregory_items = [(category.id, category.type) for category in selection_category]

        if len(current_question) == 0:
            abort(404)
        return jsonify(
            {
                "success": True,
                "questions": current_question,
                "total_questions":len(selection_quiz),
                "categories": current_category,
                'current_category': list(set([question['category']for question in current_question ]))
            }
        )

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id)\
                .one_or_none()

            if question is None:
                abort(404)
            else:
                question.delete()
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

        except Exception:
                abort(422)
   
    @app.route('/questions', methods=['POST'])
    def create_questions():
        body = request.get_json()

        new_answer = body.get('answer', None),
        new_category = body.get('category', None),
        new_difficulty = body.get('difficulty',None),
        another_quiz  = body.get('question', None)

        try:
            question = Question(answer=new_answer, category=new_category,
            difficulty=new_difficulty,question=another_quiz)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            return jsonify({
                'success':True,
                'created': question.id,
                'questions': current_questions,
                'total_questions':len(selection)
            })
        except Exception:
            abort(422)

    @app.route('/questions_search', methods=['POST'])
    def questions_search():
        data: request.get_json()
        term = data['searchTerm']

        try:
            questions = Question.query.filter(Question.question.ilike('%' + term + '%')).all()
            current_questions = paginate_questions(request, questions)
            categories = Category.query.order_by(Category.id).all()
            categories_items = [(category.id, category.type) for category in categories]

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                'success':True,
                'questions': current_questions,
                'total_questions': len(questions)
            })
        except Exception:
            abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def questions_by_category(category_id):
        try:
            questions = Question.query.filter_by(category=str(category_id)).all()
            current_questions = paginate_questions(request, questions)

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                'success':True,
                'questions': current_questions,
                'total_questions': len(questions)
            })
        except Exception:
            abort(422)

   
    @app.route('/quizzes', methods=['POST'])
    def quizzes():

        try:

            data_info = request.get_json()

            if not ('quiz_category' in data_info and 'previous_questions' in data_info):
                abort(422)

            category = data_info.get('quiz_category')
            previous_questions = data_info.get('previous_questions')

            if category['type'] == 'click':
                presentQuestions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()
            else:
                presentQuestions = Question.query.filter_by(
                    category=category['id']).filter(Question.id.notin_((previous_questions))).all()

            another_quiz = presentQuestions[random.randrange(
                0, len(presentQuestions))].format() if len(presentQuestions) > 0 else None

            return jsonify({
                'success': True,
                'question': another_quiz
            })
        except:
            abort(422)
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success':False,
            'error':404,
            'message':'Resource not Found'
        }),404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success':False,
            'error':400,
            'message':'Bad Request'
        }),400

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success':False,
            'error':422,
            'message':'Unprocessable'
        }),422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success':False,
            'error':500,
            'message':'Server Error'
        }),500

    return app