from flask import Blueprint, render_template ,jsonify

main = Blueprint("main", __name__)

@main.route('/')
def index():
    # بنرجع الصفحة الرئيسية
    return render_template('index.html'), 200  # ✅ Status code 200 OK

@main.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Page not found"}), 404  # ❌ Status code 404

@main.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500  # 💥 Status code 500