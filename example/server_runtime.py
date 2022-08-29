from citrus import add_path, start, log_to_stream

log_to_stream()

add_path("server/services/")
add_path("server/components/")
add_path("shared/components/")

start("0.0.0.0")

# TODO: Implement pygame runtime
