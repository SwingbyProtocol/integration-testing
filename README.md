# Swingby integration testing framework

Testing framework built to ensure the quality of Swingby network.

## Supported services

* Swap-daemon node
* BTC transaction indexer
* Pre-staking API

## Install

```bash
$ docker build . -t swingby-teser
$ docker run -it swingby-tester
$ behave -t @peers
```

## Useful behave commands

- `$ behave --logcapture` - show output on test failure
- `$ behave --stop` - stop on first failure
- `$ behave --steps-catalog` - view available steps
- `$ behave --include "peer|swap"` - run scenarios that match regex
- `$ behave ---exclude "peer|swap"` - exclude scenarios that match regex


## Set private keys

```
export BTC_PKEY = "YOUR KEY"
export BNB_PKEY = "YOUR KEY"
```

## Presets

The `/presets` folder contains multiple config and keystore files. When starting a new node the `--preset <number>` can be used to initiate the node using these files. For example `--preset 101` will use the `test_cfg_101.toml` config along with the `test_keystore_101.json` keystore.
Presets < 100 are in the keygen stage and presets > 100 have fully generated keystores.

## Useful links

* [Website](https://swingby.network)
* [Swingby explorer](https://bridge-testnet.swingby.network/explorer)
* [Swingby network dashboard](https://testnet-node.swingby.network/)
