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


    @app.route("/categories")
    def retrieve_categories():
        categories = Category.query.all()
        current_category = [category.format() for category in categories]
        return jsonify(
            {
                "success": True,
                "categories": current_category,
                "total_categories":len(categories),
            }
        )
    
    @app.route("/questions")
    def retrieve_questions():
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
        new_question  = body.get('question', None)

        try:
            question = Question(answer=new_answer, category=new_category,
            difficulty=new_difficulty,question=new_question)
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
        data = request.get_json()

        previous_questions = data['previous_questions']
        quiz_category = data['quiz_category']

        questions = None
        if quiz_category['type'] == 'click':
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category =quiz_category['id']).all()
        
        formatted_questions = [question.format() for question in questions]

        potential_questions = []

        for qn in formatted_questions:
            if qn['id'] not in previous_questions:
                potential_questions.append(qn)
        
        selected_question = None
        if len(potential_questions) > 0:
            selected_question = random.choice(potential_questions)

        return jsonify({
            "success":True,
            'question': selected_question
        })
    
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

    return app