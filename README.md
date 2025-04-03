API para consulta del reglamento de transito , topicos de programacion , 

python --version
Python 3.12.0

instalar los requerimientos.txt

para inicar el servicio : python manage.py runserver 0.0.0.0:8000    // para ser accesible desde la red local

python manage.py runserve  // para ser accesible desde localhost

EndPoint: http://192.168.0.9:8000/api/query/?q=consulta

Respuesta esperada : 

respuesta json : 

{
    "query": "hola",
    "results": [
        {
            "content": "Olivera, Walter Juvenal Delgadillo Terceros, Nilda Copa Condori.\nContribuidor DeveNet.net\nPublicador   DeveNet.net"
        },
        {
            "content": "Artículo transitorio 4°.-"
        }
    ]
}

