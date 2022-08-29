from citrus import add_path, start

add_path("server/services/")
add_path("server/components/")
add_path("shared/components/")

start("0.0.0.0", port=7777, do_debug=True, log_path="./server.log", log_to_stream=True)

# TODO: Implement pygame runtime
