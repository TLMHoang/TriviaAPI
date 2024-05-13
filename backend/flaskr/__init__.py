import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app():
    # create and configure the app
    app = Flask(__name__)
    # if test_config is None:
        # setup_db(app)
    # else:
    setup_db(app)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories')
    @cross_origin()
    def get_categories():
        categories = Category.query.order_by(Category.id).all()

        # Format the data to send back
        formatted_categories = {category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'categories': formatted_categories
        })


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

    def paginate_questions(request):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.order_by(Question.id).limit(QUESTIONS_PER_PAGE).offset(start).all()
        
        if len(questions) <= 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
            'total_questions': Question.query.count(),
            'current_questions': len(questions),
            'categories': [category.format() for category in Category.query.all()],
            'current_category': None
        })
    
    def paginate_questions_with_data(request, questions, current_category = None):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
            'total_questions': Question.query.count(),
            'current_questions': len(questions),
            'categories': [category.format() for category in Category.query.all()],
            'current_category': current_category
        })

    @app.route('/questions')
    @cross_origin()
    def get_questions():
        return paginate_questions(request)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    @cross_origin()
    def delete_question(question_id):
        try:
            question = Question.query.get_or_404(question_id)
            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422) 

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        question = body.get('question')
        answer = body.get('answer')
        category = body.get('category')
        difficulty = body.get('difficulty')

        if not (question and answer and category and difficulty):
            abort(422)

        try:
            question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id
            })
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', '')  

        try:
            results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            if len(results) <= 0:
                abort(404)
            return paginate_questions_with_data(request, results)
        except Exception as e:
            abort(404) 

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        category = Category.query.get_or_404(category_id)

        try:
            results = Question.query.filter(Question.category == str(category.id)).all()
            return paginate_questions_with_data(request, results, category.type) 
        except Exception as e:
            abort(404)

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
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        try:
            data = request.get_json()
    
            category_id = data.get('quiz_category', {'id': 0})['id']
            previous_questions = data.get('previous_questions', [])
            if category_id == 0:
                available_questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                available_questions = Question.query.filter(
                    Question.category == category_id,
                    Question.id.notin_(previous_questions)
                ).all()
    
            if available_questions:
                question = random.choice(available_questions)
                return jsonify({'success': True, 'question': question.format()})
            else:
                return jsonify({'success': True, 'question': None})
            
        except Exception as e:  
            abort(404)


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)  
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422

    return app

