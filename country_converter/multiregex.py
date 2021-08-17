import re
import uuid


class Multiregex(object):
    """
    Heavily inspired by https://codereview.stackexchange.com/questions/40607/trying-multiple-regexes-against-a-single-string
    """

    def __init__(self, rules):
        merge = []
        self._messages = {}
        for regex, text in rules:
            name = "g" + str(uuid.uuid4()).replace("-", "")
            merge += ["(?P<%s>%s)" % (name, regex)]
            self._messages[name] = text

        restr = "|".join(merge)
        # print(restr)
        self._re = re.compile(restr, re.IGNORECASE)

    def __call__(self, s):
        result = self._re.search(s)
        if result:
            groups = result.groupdict()
            return next(
                ((self._messages[x], groups[x]) for x in groups.keys() if groups[x])
            )
