from repositories.InstituicaoEnsinoRepository import InstituicaoEnsinoRepository


class InstituicaoEnsinoService:
    def __init__(self):
        self.instituicaoEnsinoRepository = InstituicaoEnsinoRepository()

    def get_all(self):
        return self.instituicaoEnsinoRepository.get_instituicoes()

    def get_by_id(self, id):
        return self.instituicaoEnsinoRepository.get_instituicao(id)

    def create(self, data):
        return self.instituicaoEnsinoRepository.criar_instituicao(data)

    def update(self, id, data):
        return self.instituicaoEnsinoRepository.atualizar_instituicao(id, data)

    def delete(self, id):
        return self.instituicaoEnsinoRepository.excluir_instituicao(id)
