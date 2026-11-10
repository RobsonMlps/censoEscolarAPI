from helpers.database import get_connection
from models.instituicaoensino import InstituicaoEnsino


class InstituicaoEnsinoRepository:
    fields = (
        "no_entidade",
        "co_entidade",
        "no_uf",
        "sg_uf",
        "co_uf",
        "no_municipio",
        "co_municipio",
        "nu_ano_censo",
        "qt_mat_bas",
        "qt_mat_inf",
        "qt_mat_fund",
        "qt_mat_med",
        "qt_mat_prof",
        "qt_mat_eja",
        "qt_mat_esp",
    )

    @staticmethod
    def row_to_instituicao(row):
        return InstituicaoEnsino(
            id=row[0],
            no_entidade=row[1],
            co_entidade=row[2],
            no_uf=row[3],
            sg_uf=row[4],
            co_uf=row[5],
            no_municipio=row[6],
            co_municipio=row[7],
            nu_ano_censo=row[8],
            qt_mat_bas=row[9],
            qt_mat_inf=row[10],
            qt_mat_fund=row[11],
            qt_mat_med=row[12],
            qt_mat_prof=row[13],
            qt_mat_eja=row[14],
            qt_mat_esp=row[15],
            created=row[16],
        )

    @staticmethod
    def _active_filter():
        return """
            NOT EXISTS (
                SELECT 1
                FROM tb_instituicao_ensino_excluida AS excluida
                WHERE excluida.id = escolas_nordeste_sudeste.rowid
            )
        """

    def get_instituicoes(self):
        connection = get_connection()
        cursor = connection.execute(f"""
            SELECT rowid, {", ".join(self.fields)}, NULL
            FROM escolas_nordeste_sudeste
            WHERE {self._active_filter()}
            ORDER BY rowid
        """)
        return [self.row_to_instituicao(row) for row in cursor.fetchall()]

    def get_instituicao(self, id):
        connection = get_connection()
        row = connection.execute(f"""
            SELECT rowid, {", ".join(self.fields)}, NULL
            FROM escolas_nordeste_sudeste
            WHERE rowid = ? AND {self._active_filter()}
        """, (id,)).fetchone()
        return self.row_to_instituicao(row) if row is not None else None

    def criar_instituicao(self, data):
        connection = get_connection()
        placeholders = ", ".join("?" for _ in self.fields)
        cursor = connection.execute(
            f"""
                INSERT INTO escolas_nordeste_sudeste ({", ".join(self.fields)})
                VALUES ({placeholders})
            """,
            tuple(data[field] for field in self.fields),
        )
        connection.commit()
        return self.get_instituicao(cursor.lastrowid)

    def atualizar_instituicao(self, id, data):
        connection = get_connection()
        assignments = ", ".join(f"{field} = ?" for field in self.fields)
        cursor = connection.execute(
            f"""
                UPDATE escolas_nordeste_sudeste
                SET {assignments}
                WHERE rowid = ? AND {self._active_filter()}
            """,
            (*[data[field] for field in self.fields], id),
        )
        if cursor.rowcount == 0:
            return None
        connection.commit()
        return self.get_instituicao(id)

    def excluir_instituicao(self, id):
        connection = get_connection()
        cursor = connection.execute(f"""
            INSERT OR IGNORE INTO tb_instituicao_ensino_excluida (id)
            SELECT rowid
            FROM escolas_nordeste_sudeste
            WHERE rowid = ? AND {self._active_filter()}
        """, (id,))
        if cursor.rowcount == 0:
            return False
        connection.commit()
        return True
