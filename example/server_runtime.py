from citrus import add_path, start

add_path("server/services/")
add_path("server/components/")
add_path("shared/components/")

start("0.0.0.0")
