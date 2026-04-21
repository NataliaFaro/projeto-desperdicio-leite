CREATE TABLE tb_desperdicio_leite (
    id NUMBER PRIMARY KEY,
    produtor VARCHAR2(100),
    data VARCHAR2(20),
    litros_produzidos NUMBER,
    litros_desperdicados NUMBER,
    percentual NUMBER,
    nivel VARCHAR2(20)
);
SELECT * FROM tb_desperdicio_leite;
SELECT * FROM tb_desperdicio_leite;