CREATE DATABASE IF NOT EXISTS finance_system;
USE finance_system;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    foto_perfil VARCHAR(255),
    role ENUM('admin', 'user') DEFAULT 'user',
    status ENUM('ativo', 'bloqueado') DEFAULT 'ativo',
    telefone VARCHAR(20),
    cpf VARCHAR(14) UNIQUE,
    data_nascimento DATE,
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



-- Tabelas do novo Módulo SaaS (Relacionamento N:N)
CREATE TABLE planos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    preco DECIMAL(10, 2) NOT NULL,
    descricao VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE usuario_planos (
    usuario_id INT NOT NULL,
    plano_id INT NOT NULL,
    data_assinatura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('ativo', 'cancelado') DEFAULT 'ativo',
    PRIMARY KEY (usuario_id, plano_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (plano_id) REFERENCES planos(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Mock Inserts
INSERT INTO usuarios (nome, email, senha, foto_perfil, role, status) VALUES
('Master Admin', 'admin@finance.com', 'scrypt:32768:8:1$hash_exemplo_admin', NULL, 'admin', 'ativo');
