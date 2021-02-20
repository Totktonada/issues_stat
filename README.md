## Overview

The script shows GitHub open issues statistics splitted by labels.

More options like splitting by a milestone may be added later.

TODO: Add csv output support under --csv option.

## Requirements

* Python (2 or 3)
* requests

## How to use

Add a token on [Personal access token][gh_token] GitHub page, give
`repo:public_repo` access and copy the token to `token.txt`.

Run like so:

```sh
./issues_stat.py tarantool/tarantool
```

The example of output:

```
<..skipped..>
luajit             64
lua                65
vinyl              73
good first issue   91
flaky test         93
sql                220
bug                236
qa                 248
feature            564
```

[gh_token]: https://github.com/settings/tokens
