-- Base de datos: portafolio_db (debe existir)

-- Tabla: admin_user
CREATE TABLE admin_user (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL
);

-- Tabla: proyecto
CREATE TABLE proyecto (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    breve_descripcion VARCHAR(300) NOT NULL,
    descripcion TEXT NOT NULL,
    analisis TEXT NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    enlace_documentos VARCHAR(500),
    enlace_herramienta VARCHAR(500),
    enlace_github VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: hashtag
CREATE TABLE hashtag (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla: proyecto_hashtag (relación muchos a muchos)
CREATE TABLE proyecto_hashtag (
    proyecto_id INTEGER REFERENCES proyecto(id) ON DELETE CASCADE,
    hashtag_id INTEGER REFERENCES hashtag(id) ON DELETE CASCADE,
    PRIMARY KEY (proyecto_id, hashtag_id)
);

-- Tabla: medio
CREATE TABLE medio (
    id SERIAL PRIMARY KEY,
    url VARCHAR(500) NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('imagen', 'video')),
    orden INTEGER NOT NULL DEFAULT 0,
    proyecto_id INTEGER NOT NULL REFERENCES proyecto(id) ON DELETE CASCADE
);

-- Insertar usuario admin (opcional, puedes hacerlo desde Flask o aquí)
INSERT INTO admin_user (email, password_hash)
VALUES (
    'admin@portafolio.com',
    '$2b$12$TuHashBcryptAquí'  -- ⚠️ ¡NO uses una contraseña en texto plano!
);