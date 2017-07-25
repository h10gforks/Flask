server{
    listen 80;
    server_name = my.server.ip.address:5432;   //5432 port in wsgi.py 
        location /{
            proxy_pass http://0.0.0.0:5432;
        }
}

