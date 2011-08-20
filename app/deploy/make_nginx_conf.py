# -*- encoding:utf8 -*-
#!/usr/bin/env python
import os
import django

base_dir = os.path.abspath(os.path.join(__file__, '..', '..'))
server = 'localhost'
port = 8001
name = 'localhost'

def print_nginx_conf():
    conf_template = \
    """
    upstream boiler {
            server %(server)s:%(port)d fail_timeout=0;
    }

    server {

            listen   80; ## listen for ipv4
            #listen   [::]:80 default ipv6only=on; ## listen for ipv6

            server_name  %(name)s;

	    log_format   main '$remote_addr - $remote_user [$time_local]  $status '
	    '"$request" $body_bytes_sent "$http_referer" '
	    '"$http_user_agent" "$http_x_forwarded_for"';

            access_log  /var/log/nginx/%(name)s.access.log;
            error_log  /var/log/nginx/%(name)s.error.log;

            keepalive_timeout 5;

            location /static/ {
                    root  %(app_dir)s;
            }

            location /media/ {
                    if ($query_string) {
                            expires max;
                    }
            }

            location /admin/media/ {
                    root %(django_dir)s/contrib;
            }

            location / {
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header Host $http_host;
                    proxy_redirect off;

                    if (!-f $request_filename) {
                            proxy_pass http://boiler;
                            break;
                    }
            }
    }
    """ % \
            {
            'app_dir': base_dir,
            'django_dir': os.path.abspath(os.path.dirname(django.__file__)),
            'server': server,
            'port': port,
            'name': name
            }

    print conf_template

if __name__ == "__main__":
    print_nginx_conf()
