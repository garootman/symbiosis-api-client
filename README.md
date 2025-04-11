# symbiosis-client-py

- Python syncronous client for [Symbiosis Finance](https://symbiosis.finance/) REST API
- Client relies on [JS SDK ](https://github.com/symbiosis-finance/js-sdk) in part of  [configuration file](https://github.com/symbiosis-finance/js-sdk/blob/main/src/crosschain/config/mainnet.ts). If there is a new commit, Client will raise `InvalidCommit`


## ToDo Plan:


- [ ] Cover routes:
  - [X] Eth USDT -> Tron USDT
  - [ ] Eth USDT -> TON USDT
  - [ ] BSC DAI -> Tron TRX
  - [ ] TON TON -> BSC BNB
- [X] Main functionality
- [X] Rate limit + Singleton
- [X] Exception Codes
- [X] tox for Python versions
- [X] Pydantic models
- [ ] Test Stuck transactions functionality
- [ ] Testnet – when there are tokens available on Symbiosis
- [ ] Async client maybe?



### Sources:

- [Swagger](https://api.symbiosis.finance/crosschain/docs/)
- [Source Docs](https://docs.symbiosis.finance/developer-tools/symbiosis-api)


# symbiosis-api-client

[![PyPI - Version](https://img.shields.io/pypi/v/symbiosis-api-client.svg)](https://pypi.org/project/symbiosis-api-client)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/symbiosis-api-client.svg)](https://pypi.org/project/symbiosis-api-client)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install symbiosis-api-client
```

## License

`symbiosis-api-client` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
