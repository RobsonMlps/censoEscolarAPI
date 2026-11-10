import sqlite3

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from helpers.logger import logger
from models.instituicaoensino import InstituicaoEnsinoSchema
from services.InstituicaoEnsinoService import InstituicaoEnsinoService

instituicaoEnsinoSchema = InstituicaoEnsinoSchema()
instituicoesEnsinoSchema = InstituicaoEnsinoSchema(many=True)

instituicao_ensino_bp = Blueprint(
    "instituicaoensino", __name__, url_prefix="/instituicoesensino"
)


def _read_payload():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return None, {"erro": "O corpo da requisição deve ser um objeto JSON."}, 400

    try:
        return instituicaoEnsinoSchema.load(payload), None, None
    except ValidationError as error:
        return None, {"erro": "Dados inválidos", "campos": error.messages}, 400


@instituicao_ensino_bp.get("/")
def get_all_instituicoes():
    try:
        instituicoes = InstituicaoEnsinoService().get_all()
        return jsonify(instituicoesEnsinoSchema.dump(instituicoes)), 200
    except sqlite3.Error:
        logger.exception("Erro ao listar instituições de ensino")
        return {"erro": "Não foi possível consultar o banco de dados."}, 500


@instituicao_ensino_bp.get("/<int:id>")
def get_instituicao_by_id(id):
    try:
        instituicao = InstituicaoEnsinoService().get_by_id(id)
    except sqlite3.Error:
        logger.exception("Erro ao consultar instituição de ensino")
        return {"erro": "Não foi possível consultar o banco de dados."}, 500

    if instituicao is None:
        return {"mensagem": "Instituição de ensino não encontrada"}, 404
    return jsonify(instituicaoEnsinoSchema.dump(instituicao)), 200


@instituicao_ensino_bp.post("/")
def post_instituicao():
    data, error_response, status = _read_payload()
    if error_response is not None:
        return error_response, status

    try:
        instituicao = InstituicaoEnsinoService().create(data)
    except sqlite3.Error:
        logger.exception("Erro ao inserir instituição de ensino")
        return {"erro": "Não foi possível salvar no banco de dados."}, 500

    return jsonify(instituicaoEnsinoSchema.dump(instituicao)), 201


@instituicao_ensino_bp.put("/<int:id>")
def put_instituicao(id):
    data, error_response, status = _read_payload()
    if error_response is not None:
        return error_response, status

    try:
        instituicao = InstituicaoEnsinoService().update(id, data)
    except sqlite3.Error:
        logger.exception("Erro ao atualizar instituição de ensino")
        return {"erro": "Não foi possível atualizar no banco de dados."}, 500

    if instituicao is None:
        return {"mensagem": "Instituição de ensino não encontrada"}, 404
    return jsonify(instituicaoEnsinoSchema.dump(instituicao)), 200


@instituicao_ensino_bp.delete("/<int:id>")
def delete_instituicao(id):
    try:
        excluida = InstituicaoEnsinoService().delete(id)
    except sqlite3.Error:
        logger.exception("Erro ao excluir instituição de ensino")
        return {"erro": "Não foi possível excluir no banco de dados."}, 500

    if not excluida:
        return {"mensagem": "Instituição de ensino não encontrada"}, 404
    return {"mensagem": "Instituição de ensino removida logicamente"}, 200
