"""Minimal Excel formula evaluator for the subset of functions used by the FluxMuse model.

Purpose: no LibreOffice here, so formulas written by openpyxl have no cached values.
This evaluator computes every formula cell straight from the in-memory workbook so the
build can assert that the Excel logic equals the independent Python mirror.

Supported: + - * / ^, comparisons (= <> < > <= >=), SUM MIN MAX AVERAGE IF AND OR
CHOOSE INDEX MATCH ROUND ABS IFERROR, cross-sheet refs (quoted or not), ranges.
Division by zero yields inf/nan (reported as an error) instead of raising.
"""
import re
import sys
import warnings

import numpy as np
from openpyxl.utils import column_index_from_string, get_column_letter

warnings.filterwarnings("ignore", category=RuntimeWarning)

REF_RE = re.compile(
    r"(?<![A-Za-z0-9_.])(?:(?P<sh>'[^']+'|[A-Za-z_][A-Za-z0-9_]*)!)?"
    r"\$?(?P<c1>[A-Z]{1,3})\$?(?P<r1>[0-9]+)(?![A-Za-z0-9_(])"
    r"(?::\$?(?P<c2>[A-Z]{1,3})\$?(?P<r2>[0-9]+))?")


class XLError(Exception):
    pass


def _flat(args):
    out = []
    for a in args:
        if isinstance(a, list):
            out.extend(a)
        else:
            out.append(a)
    return out


def _nums(args):
    return [np.float64(x) for x in _flat(args) if isinstance(x, (int, float, np.floating)) and not isinstance(x, bool)]


def SUM(*a):
    return np.float64(sum(_nums(a)))


def MIN(*a):
    n = _nums(a)
    return np.float64(min(n)) if n else np.float64(0)


def MAX(*a):
    n = _nums(a)
    return np.float64(max(n)) if n else np.float64(0)


def AVERAGE(*a):
    n = _nums(a)
    if not n:
        raise XLError("#DIV/0!")
    return np.float64(sum(n) / len(n))


def IF(c, a, b=False):
    return a if c else b


def AND(*a):
    return all(bool(x) for x in _flat(a))


def OR(*a):
    return any(bool(x) for x in _flat(a))


def CHOOSE(i, *opts):
    return opts[int(i) - 1]


def INDEX(rng, i, j=None):
    k = int(j) if (j is not None and int(i) == 1) else int(i)
    if k < 1 or k > len(rng):
        return "#REF!"   # Excel's IF is lazy; returning the error value keeps an untaken branch harmless
    return rng[k - 1]


def MATCH(val, rng, typ=0):
    for k, x in enumerate(rng):
        if x == val:
            return np.float64(k + 1)
    raise XLError("#N/A")


def ROUND(x, n=0):
    return np.float64(round(float(x), int(n)))


def ROUNDDOWN(x, n=0):
    f = 10.0 ** int(n)
    return np.float64(np.trunc(float(x) * f) / f)


def ABS(x):
    return np.float64(abs(x))


def MOD(a, b):
    if b == 0:
        raise XLError("#DIV/0!")
    return np.float64(a - b * np.floor(a / b))


FUNCS = dict(SUM=SUM, MIN=MIN, MAX=MAX, AVERAGE=AVERAGE, IF=IF, AND=AND, OR=OR, CHOOSE=CHOOSE,
             INDEX=INDEX, MATCH=MATCH, ROUND=ROUND, ROUNDDOWN=ROUNDDOWN, ABS=ABS, MOD=MOD)


class Evaluator:
    def __init__(self, wb):
        self.wb = wb
        self.cache = {}
        self.codes = {}
        self.env = dict(FUNCS)
        self.env["_r"] = self._r
        self.env["_g"] = self._g
        sys.setrecursionlimit(100000)

    # -- translation ---------------------------------------------------------
    def translate(self, sheet, formula):
        parts = formula.split('"')
        out = []
        for k, part in enumerate(parts):
            if k % 2 == 1:                       # inside a string literal
                out.append('"' + part + '"')
                continue

            def repl(mo):
                sh = mo.group("sh") or sheet
                sh = sh.strip("'")
                if mo.group("c2"):
                    return f'_g({sh!r},"{mo.group("c1")}{mo.group("r1")}","{mo.group("c2")}{mo.group("r2")}")'
                return f'_r({sh!r},"{mo.group("c1")}{mo.group("r1")}")'

            s = REF_RE.sub(repl, part)
            s = s.replace("<>", "!=")
            s = re.sub(r"(?<![<>!=])=(?!=)", "==", s)
            s = s.replace("^", "**")
            out.append(s)
        return "".join(out)

    # -- cell access ---------------------------------------------------------
    def _r(self, sheet, addr):
        return self.value(sheet, addr)

    def _g(self, sheet, a1, a2):
        m1 = re.match(r"([A-Z]+)(\d+)", a1)
        m2 = re.match(r"([A-Z]+)(\d+)", a2)
        c1, r1 = column_index_from_string(m1.group(1)), int(m1.group(2))
        c2, r2 = column_index_from_string(m2.group(1)), int(m2.group(2))
        return [self.value(sheet, f"{get_column_letter(c)}{r}") for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)]

    def value(self, sheet, addr):
        key = (sheet, addr)
        if key in self.cache:
            v = self.cache[key]
            if v is _PENDING:
                raise XLError(f"circular reference at {sheet}!{addr}")
            return v
        raw = self.wb[sheet][addr].value
        if isinstance(raw, str) and raw.startswith("="):
            self.cache[key] = _PENDING
            code = self.codes.get(key)
            if code is None:
                src = self.translate(sheet, raw[1:])
                try:
                    code = compile(src, f"{sheet}!{addr}", "eval")
                except SyntaxError as e:
                    self.cache.pop(key, None)
                    raise XLError(f"cannot parse {sheet}!{addr}: {raw} -> {src}") from e
                self.codes[key] = code
            try:
                res = eval(code, self.env)
            except Exception:
                self.cache.pop(key, None)
                raise
            if isinstance(res, (bool, np.bool_)):
                res = bool(res)
            elif isinstance(res, (int, float, np.floating)):
                res = np.float64(res)
            self.cache[key] = res
            return res
        if raw is None:
            v = np.float64(0)
        elif isinstance(raw, (int, float)) and not isinstance(raw, bool):
            v = np.float64(raw)
        else:
            v = raw
        self.cache[key] = v
        return v


_PENDING = object()


def is_error(v):
    if isinstance(v, str):
        return v.startswith("#") and v.rstrip("!?").upper() in ("#REF", "#N/A", "#DIV/0", "#VALUE", "#NAME", "#NUM", "#NULL")
    return isinstance(v, np.floating) and not np.isfinite(v)
