mkdir -p ~/.flask/

echo "
[general]
email = \"ericvincentmagno@gmail.com\"
" > ~/.flask/credentials.toml

echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.flask/config.toml