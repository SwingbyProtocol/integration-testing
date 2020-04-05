# swingby-integration-testing
Integration testing framework for swingby

## Install

```bash
$ sudo apt install python3-pip
$ pip3 install behave
$ sudo apt-get install libsecp256k1-dev
$ pip3 install python-binance-chain
$ pip3 install bit
$ pip3 install urllib2
$ pip3 install pyee
export SW_EXEC=/path/to/node/executable # (i.e $GOBIN/swapd)
```

## Set private keys

```
export BTC_PKEY = "YOUR KEY"
export BNB_PKEY = "YOUR KEY"
```

## Presets

The `/presets` folder contains multiple config and keystore files. When starting a new node the `--preset <number>` can be used to initiate the node using these files. For example `--preset 101` will use the `test_cfg_101.toml` config along with the `test_keystore_101.json` keystore.
Presets < 100 are in the keygen stage and presets > 100 have fully generated keystores.

## Run

```bash
$ behave
```

## Useful commands

- `$ behave --logcapture` - show output on test failure
- `$ behave --stop` - stop on first failure
- `$ behave --steps-catalog` - view available steps
- `$ behave --include "peer|swap"` - run scenarios that match regex
- `$ behave ---exclude "peer|swap"` - exclude scenarios that match regex
