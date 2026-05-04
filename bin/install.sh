# Setup local environment:
cd `dirname $0`/..

if [ ! -f config.toml ]; then
    cp ./bin/default-config.toml ./config.toml
fi
