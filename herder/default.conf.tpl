upstream backend_hosts {
$hosts
}

server {
  listen       80;
  server_name  localhost;
  location /tick  {
    $upstream
  }

  location /nginx_status {
    stub_status on;
    access_log   on;
    allow 0.0.0.0;
  }
}
