from citrus import add_path, start

add_path("client/components")
add_path("client/controllers")
add_path("shared/components")

start("127.0.0.1")
