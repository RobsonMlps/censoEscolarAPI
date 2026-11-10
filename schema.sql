CREATE TABLE IF NOT EXISTS tb_instituicao_ensino (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    no_entidade TEXT NOT NULL,
    co_entidade TEXT NOT NULL,
    no_uf TEXT NOT NULL,
    sg_uf TEXT NOT NULL,
    co_uf INTEGER NOT NULL,
    no_municipio TEXT NOT NULL,
    co_municipio INTEGER NOT NULL,
    nu_ano_censo INTEGER NOT NULL CHECK (nu_ano_censo >= 0),
    qt_mat_bas INTEGER NOT NULL CHECK (qt_mat_bas >= 0),
    qt_mat_inf INTEGER NOT NULL CHECK (qt_mat_inf >= 0),
    qt_mat_fund INTEGER NOT NULL CHECK (qt_mat_fund >= 0),
    qt_mat_med INTEGER NOT NULL CHECK (qt_mat_med >= 0),
    qt_mat_prof INTEGER NOT NULL CHECK (qt_mat_prof >= 0),
    qt_mat_eja INTEGER NOT NULL CHECK (qt_mat_eja >= 0),
    qt_mat_esp INTEGER NOT NULL CHECK (qt_mat_esp >= 0),
    created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
