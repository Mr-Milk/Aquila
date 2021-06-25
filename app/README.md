# How to run

For development

```shell
cargo watch -x 'run --bin app' --workdir src
```

For deployment

```shell
cargo install --path . --root .

# To run the server
./bin/app
```