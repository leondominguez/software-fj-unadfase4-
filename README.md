# Software FJ — UNAD Fase 4

Empresa llamada **Software FJ** que ofrece varios tipos de servicios: reservas de salas, alquiler de equipos y asesorías especializadas.

---

## Comandos de despliegue y clonado

```bash
git clone git@github.com:leondominguez/software-fj-unadfase4-.git
```

### Traer lo nuevo de `main` a tu rama

```bash
# Crear la rama local donde trabajarás
git checkout -b feature/estudiante1-claseoarchivo

# Traer los cambios más actuales de main
git pull origin main
```
>No olviden siempre verificar con git fecht si hay cambios en la rama principal y traeerse esos cambios con git pull

### Hacer commits

```bash
# Verificar que estás en tu rama
git branch

# Agregar todo lo de tu rama (o un archivo.py específico)
git add .

# Crear el commit
git commit -m "cambio realizado"

# Subir los cambios
git push origin feature/estudiante1-entidades
```

---

## Requisitos

- Python 3.9 o superior
- Sin dependencias externas (solo biblioteca estándar)

---

## Estructura modular planeada

```text
software-fj-unadfase4/
│
├── .gitignore
├── README.md
│
├── excepciones.py          ← Est. 1
├── entidades.py            ← Est. 1
├── servicios.py            ← Est. 2
├── reserva.py              ← Est. 3
├── repositorios.py         ← Est. 3
├── gestores.py             ← Est. 4
├── logger_config.py        ← Est. 4
├── main.py                 ← Est. 5
│
├── logs/
│   └── .gitkeep
│
└── referencia/
    └── monolito_original.py
```

> `referencia/monolito_original.py` es el código aportado inicialmente por uno de los compañeros. Se usará como base guía para no perder lo avanzado y modularizar el proyecto. Como es un proyecto pequeño, podemos usar una estructura de una sola raíz con varios archivos para separar responsabilidades.

---

## Ramas por estudiante

| Integrante | Rama | Archivos a cargo |
|---|---|---|
| Est. 1 | `feature/estudiante1-entidades` | `excepciones.py`, `entidades.py` |
| Est. 2 | `feature/estudiante2-servicios` | `servicios.py` |
| Est. 3 | `feature/estudiante3-reserva-repo` | `reserva.py`, `repositorios.py` |
| Est. 4 | `feature/estudiante4-gestores-logger` | `gestores.py`, `logger_config.py` |
| Est. 5 | `feature/estudiante5-main-docs` | `main.py`, `README.md` |