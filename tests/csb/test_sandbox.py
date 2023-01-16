import os
from typing import Self

import responses
from box import Box
from responses import matchers


@responses.activate
def submit_file(self, file: str, force: bool = False):
    with open("sandboxtest.txt", "rb") as f:
        data = f.read()

    params = { "force": int(force) }

    assert  print(self._post(params=params, data=data))