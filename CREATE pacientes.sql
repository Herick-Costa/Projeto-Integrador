CREATE TABLE IF NOT EXISTS pacientes (
    cpf character varying(16) PRIMARY KEY,
    nome character varying(255) NOT NULL,
    telefone character varying(20) NOT NULL,
    endereco character varying(255) NOT NULL,
    hepatite_b character varying(30),
    dupla_bacteriana character varying(30),
    febre_amarela character varying(30),
    influenza character varying(30),
    covid_19 character varying(30)
);

INSERT INTO pacientes (cpf, nome, telefone, endereco)
VALUES ('111.111.111-00', 'Teste 1', '(41) 99999-9999', 'Rua Principal, 123');

INSERT INTO pacientes (cpf, nome, telefone, endereco)
VALUES ('222.222.222-00', 'Teste 2', '(41) 98888-8888', 'Rua Principal, 456');

INSERT INTO pacientes (cpf, nome, telefone, endereco)
VALUES ('333.333.333-00', 'Teste 3', '(41) 977777-7777', 'Rua Secundaria, 789');

INSERT INTO pacientes (cpf, nome, telefone, endereco)
VALUES ('111.222.333-00', 'João da Silva', '(43) 91234-5678', 'Rua Brasil, 147');