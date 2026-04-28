from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.meal import Meal
from database import db
from datetime import datetime

# Blueprint das rotas de refeição
meal_bp = Blueprint('meal', __name__, url_prefix='/meal')


# ======================
# CRIAR REFEIÇÃO
# ======================
@meal_bp.route('/create', methods=['POST'])
@login_required
def create_meal():
    data = request.json

    name = data.get('name')
    description = data.get('description')
    in_diet = data.get('in_diet')

    if name is None or in_diet is None:
        return jsonify({'message': 'Dados inválidos'}), 400

    meal = Meal(
        name=name,
        description=description,
        in_diet=in_diet,
        date_time=datetime.utcnow(),
        user_id=current_user.id
    )

    db.session.add(meal)
    db.session.commit()

    return jsonify({'message': 'Refeição criada com sucesso'}), 201


# ======================
# LISTAR REFEIÇÕES DO USUÁRIO
# ======================
@meal_bp.route('', methods=['GET'])
@login_required
def list_meals():
    meals = Meal.query.filter_by(user_id=current_user.id).all()

    output = []
    for meal in meals:
        output.append({
            'id': meal.id,
            'name': meal.name,
            'description': meal.description,
            'in_diet': meal.in_diet,
            'date_time': meal.date_time.isoformat()
        })

    return jsonify(output), 200


# ======================
# BUSCAR REFEIÇÃO ESPECÍFICA
# ======================
@meal_bp.route('/<int:meal_id>', methods=['GET'])
@login_required
def get_meal(meal_id):
    meal = Meal.query.filter_by(
        id=meal_id,
        user_id=current_user.id
    ).first()

    if not meal:
        return jsonify({'message': 'Refeição não encontrada'}), 404

    return jsonify({
        'id': meal.id,
        'name': meal.name,
        'description': meal.description,
        'in_diet': meal.in_diet,
        'date_time': meal.date_time.isoformat()
    }), 200


# ======================
# ATUALIZAR REFEIÇÃO
# ======================
@meal_bp.route('/<int:meal_id>', methods=['PUT'])
@login_required
def update_meal(meal_id):
    data = request.json

    meal = Meal.query.filter_by(
        id=meal_id,
        user_id=current_user.id
    ).first()

    if not meal:
        return jsonify({'message': 'Refeição não encontrada'}), 404

    meal.name = data.get('name', meal.name)
    meal.description = data.get('description', meal.description)
    meal.in_diet = data.get('in_diet', meal.in_diet)

    db.session.commit()

    return jsonify({'message': 'Refeição atualizada com sucesso'}), 200


# ======================
# DELETAR REFEIÇÃO
# ======================
@meal_bp.route('/<int:meal_id>', methods=['DELETE'])
@login_required
def delete_meal(meal_id):
    meal = Meal.query.filter_by(
        id=meal_id,
        user_id=current_user.id
    ).first()

    if not meal:
        return jsonify({'message': 'Refeição não encontrada'}), 404

    db.session.delete(meal)
    db.session.commit()

    return jsonify({'message': 'Refeição deletada com sucesso'}), 200