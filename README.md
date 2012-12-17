fastnu-csd-audit
================

FAST NU Academic Audit System




Required python packages: 

south
reportlab 
tl 
tl.rename 
django-grappelli (https://django-grappelli.readthedocs.org/en/latest/quickstart.html)




# Apache Configuration Sample 

    Listen 8000


Alias /static/admin/img/ /home/nam/fastnu-csd-audit/csdexec/media/img/
Alias /static/admin/ /home/nam/fastnu-csd-audit/csdexec/media/
Alias /static/grappelli/ /usr/local/lib/python2.7/dist-packages/grappelli/static/grappelli/


NameVirtualHost *:8000

<VirtualHost *:8000>
    DocumentRoot /var/www/
    ServerName FASTNUCSD

    <Directory /css>

    </Directory>
    # Other directives here
    WSGIScriptAlias / /home/nam/fastnu-csd-audit/csdexec/csdexec/wsgi.py



</VirtualHost>
~                   
