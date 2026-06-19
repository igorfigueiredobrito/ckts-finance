CREATE DATABASE IF NOT EXISTS finance_system;
USE finance_system;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    foto_perfil VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo ENUM('receita', 'despesa') NOT NULL,
    usuario_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    usuario_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE transacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    data DATE NOT NULL,
    usuario_id INT NOT NULL,
    categoria_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE transacao_tags (
    transacao_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (transacao_id, tag_id),
    FOREIGN KEY (transacao_id) REFERENCES transacoes(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Mock Inserts
INSERT INTO usuarios (nome, email, senha, foto_perfil) VALUES
('João Silva', 'joao@example.com', 'scrypt:32768:8:1$hash_exemplo_1', 'uploads/perfil_joao.jpg'),
('Maria Oliveira', 'maria@example.com', 'scrypt:32768:8:1$hash_exemplo_2', 'uploads/perfil_maria.jpg');

INSERT INTO categorias (nome, tipo, usuario_id) VALUES
('Salário', 'receita', 1),
('Alimentação', 'despesa', 1),
('Transporte', 'despesa', 1),
('Freelance', 'receita', 2),
('Lazer', 'despesa', 2);

INSERT INTO tags (nome, usuario_id) VALUES
('Fixo', 1),
('Uber', 1),
('Mercado', 1),
('Extra', 2),
('Cinema', 2);

INSERT INTO transacoes (descricao, valor, data, usuario_id, categoria_id) VALUES
('Salário de Janeiro', 5000.00, '2023-01-05', 1, 1),
('Compra no Supermercado', 350.50, '2023-01-10', 1, 2),
('Corrida de Uber', 25.00, '2023-01-12', 1, 3),
('Projeto Web', 1500.00, '2023-01-15', 2, 4),
('Ingressos Vingadores', 60.00, '2023-01-20', 2, 5);

INSERT INTO transacao_tags (transacao_id, tag_id) VALUES
(1, 1), -- Salário -> Fixo
(2, 3), -- Supermercado -> Mercado
(3, 2), -- Uber -> Uber
(4, 4), -- Projeto Web -> Extra
(5, 5); -- Ingressos -> Cinema
