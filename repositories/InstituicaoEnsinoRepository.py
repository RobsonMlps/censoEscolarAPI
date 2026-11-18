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
        if not row:
            return None
        # Mapeamento limpo baseado nos campos e no retorno do banco
        return InstituicaoEnsino(
            no_entidade=row[0],
            co_entidade=row[1],
            no_uf=row[2],
            sg_uf=row[3],
            co_uf=row[4],
            no_municipio=row[5],
            co_municipio=row[6],
            nu_ano_censo=row[7],
            qt_mat_bas=row[8],
            qt_mat_inf=row[9],
            qt_mat_fund=row[10],
            qt_mat_med=row[11],
            qt_mat_prof=row[12],
            qt_mat_eja=row[13],
            qt_mat_esp=row[14],
        )

    def _active_filter(self):
        return """
            NOT EXISTS (
                SELECT 1
                FROM tb_instituicao_ensino_excluida AS excluida
                WHERE excluida.co_entidade = escolas_nordeste_sudeste.co_entidade
            )
        """

    def get_instituicoes(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT {", ".join(self.fields)}
            FROM escolas_nordeste_sudeste
            WHERE {self._active_filter()}
            ORDER BY co_entidade
        """)
        rows = cursor.fetchall()
        cursor.close()
        return [self.row_to_instituicao(row) for row in rows]

    def get_instituicao(self, co_entidade):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(f"""
            SELECT {", ".join(self.fields)}
            FROM escolas_nordeste_sudeste
            WHERE co_entidade = %s AND {self._active_filter()}
        """, (co_entidade,))
        row = cursor.fetchone()
        cursor.close()
        return self.row_to_instituicao(row) if row is not None else None

    def criar_instituicao(self, data):
        connection = get_connection()
        cursor = connection.cursor()
        placeholders = ", ".join("%s" for _ in self.fields)
        
        cursor.execute(
            f"""
                INSERT INTO escolas_nordeste_sudeste ({", ".join(self.fields)})
                VALUES ({placeholders})
            """,
            tuple(data[field] for field in self.fields),
        )
        connection.commit()
        co_entidade_criada = data["co_entidade"]
        cursor.close()
        return self.get_instituicao(co_entidade_criada)

    def atualizar_instituicao(self, co_entidade, data):
        connection = get_connection()
        cursor = connection.cursor()
        assignments = ", ".join(f"{field} = %s" for field in self.fields)
        cursor.execute(
            f"""
                UPDATE escolas_nordeste_sudeste
                SET {assignments}
                WHERE co_entidade = %s AND {self._active_filter()}
            """,
            (*[data[field] for field in self.fields], co_entidade),
        )
        if cursor.rowcount == 0:
            cursor.close()
            return None
        connection.commit()
        cursor.close()
        return self.get_instituicao(co_entidade)

    def excluir_instituicao(self, co_entidade):
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(f"""
            INSERT INTO tb_instituicao_ensino_excluida (co_entidade)
            SELECT co_entidade
            FROM escolas_nordeste_sudeste
            WHERE co_entidade = %s AND {self._active_filter()}
            ON CONFLICT (co_entidade) DO NOTHING
        """, (co_entidade,))
        
        if cursor.rowcount == 0:
            cursor.close()
            return False
        connection.commit()
        cursor.close()
        return True