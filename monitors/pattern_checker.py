class PatternChecker:
    def __init__(self, fail_patterns=None, pass_patterns=None, ignore_case=False):
        self.fail_patterns = fail_patterns or []
        self.pass_patterns = pass_patterns or []
        self.ignore_case = ignore_case

    def _normalize(self, text):
        return text.lower() if self.ignore_case else text

    def find_fail(self, text):
        target = self._normalize(text)
        for pattern in self.fail_patterns:
            p = self._normalize(pattern)
            if p in target:
                return pattern
        return None

    def find_pass(self, text):
        target = self._normalize(text)
        for pattern in self.pass_patterns:
            p = self._normalize(pattern)
            if p in target:
                return pattern
        return None
