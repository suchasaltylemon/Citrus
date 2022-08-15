from citrus import add_path, start

add_path("client/components")
add_path("client/controllers")
add_path("shared/components")

start("0.0.0.0")
