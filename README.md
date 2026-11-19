# software-fj-unadfase4-
empresa llamada Software FJ que ofrece varios tipos de servicios (reservas de salas, alquiler de equipos y asesorías especializadas)

## comandos de despliegue y clonado

git clone git@github.com:leondominguez/software-fj-unadfase4-.git 

# trae lo nuevo de main a tu rama
git checkout checkout -b feature/estudiante1-claseoarchivo → para crear la rama local donde trabajaras
git pull origin main → para traer los cambios mas actuales de main
    


##hacer commits
git branch → verificar que estes en tu rama
git add . → si vas a agregar todo lo de tu rama archivo.py 
git commit -m "cambio realizado"
git push origin feature/estudiante1-entidades

## Requisitos
- Python 3.9 o superior
- Sin dependencias externas (solo biblioteca estándar)

## Esctructura modular planeada.
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
    └── monolito_original.py → este es el codigo aportado inicialmente por uno de los compañeros asi que se usara de base guia para no perder lo avanzado.y modularizar el proyecto. 
        como es un proyecto pequeño podemos usar una estructura de una sola raiz con varios archivos para separar responsabilidades.


## ramas por estudiante
Integrante	Rama	Archivos de los que debera encargarse.
Est. 1	feature/estudiante1-entidades	excepciones.py, entidades.py
Est. 2	feature/estudiante2-servicios	servicios.py
Est. 3	feature/estudiante3-reserva-repo	reserva.py, repositorios.py
Est. 4	feature/estudiante4-gestores-logger	gestores.py, logger_config.py
Est. 5	feature/estudiante5-main-docs	main.py, README.md
