from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from typing import Protocol, Optional, Literal
import geopack
from geopack import t89, t96, t01, t04
from geopack import geopack

ModelName = Literal["igrf", "t89", "t96", "t01", "t04"]

@dataclass(frozen=True)
class ParMod:
    """
    Wrapper around the 10-element GEOPACK/Tsyganenko parmod array.
    Store raw + any convenience accessors you want later.
    """
    raw: np.ndarray  # shape (10,)

    @staticmethod
    def from_any(x) -> "ParMod":
        arr = np.asarray(x, dtype=float).reshape(-1)
        if arr.size != 10:
            raise ValueError("parmod must have length 10")
        return ParMod(arr)

@dataclass(frozen=True)
class ModelContext:
    """
    Frozen context for a given time: GEOPACK recalc outputs, etc.
    """
    time: float
    ps: float  # result of geopack.recalc(time); name 'ps' matches your code


class MagneticFieldModel(Protocol):
    name: ModelName
    ctx: ModelContext
    parmod: ParMod

    def B_gsm(self, pos_re: np.ndarray) -> np.ndarray:
        """Return B (nT) in GSM at position in Earth radii (Re)."""
        ...

@dataclass(frozen=True)
class IGRFModel:
    name: ModelName
    ctx: ModelContext
    parmod: ParMod

    def B_gsm(self, pos_re: np.ndarray) -> np.ndarray:
        x, y, z = map(float, pos_re)
        return np.array(geopack.igrf_gsm(x, y, z), dtype=float)

@dataclass(frozen=True)
class T89Model:
    name: ModelName
    ctx: ModelContext
    parmod: ParMod

    def B_gsm(self, pos_re: np.ndarray) -> np.ndarray:
        x, y, z = map(float, pos_re)
        b_igrf = np.array(geopack.igrf_gsm(x, y, z), dtype=float)
        iopt = int(self.parmod.raw[0])
        b_ext  = np.array(t89.t89(iopt, self.ctx.ps, x, y, z), dtype=float)
        return b_igrf + b_ext

@dataclass(frozen=True)
class T96Model:
    name: ModelName
    ctx: ModelContext
    parmod: ParMod

    def B_gsm(self, pos_re: np.ndarray) -> np.ndarray:
        x, y, z = map(float, pos_re)
        b_igrf = np.array(geopack.igrf_gsm(x, y, z), dtype=float)
        b_ext  = np.array(t96.t96(self.parmod.raw, self.ctx.ps, x, y, z), dtype=float)
        return b_igrf + b_ext

@dataclass(frozen=True)
class T01Model:
    name: ModelName
    ctx: ModelContext
    parmod: ParMod

    def B_gsm(self, pos_re: np.ndarray) -> np.ndarray:
        x, y, z = map(float, pos_re)
        b_igrf = np.array(geopack.igrf_gsm(x, y, z), dtype=float)
        b_ext  = np.array(t01.t01(self.parmod.raw, self.ctx.ps, x, y, z), dtype=float)
        return b_igrf + b_ext

@dataclass(frozen=True)
class T04Model:
    name: ModelName
    ctx: ModelContext
    parmod: ParMod

    def B_gsm(self, pos_re: np.ndarray) -> np.ndarray:
        x, y, z = map(float, pos_re)
        b_igrf = np.array(geopack.igrf_gsm(x, y, z), dtype=float)
        b_ext  = np.array(t04.t04(self.parmod.raw, self.ctx.ps, x, y, z), dtype=float)
        return b_igrf + b_ext

def make_model(name: ModelName, time: float, parmod_any) -> MagneticFieldModel:
    parmod = ParMod.from_any(parmod_any)
    ps = geopack.recalc(time)
    ctx = ModelContext(time=time, ps=ps)

    if name == "igrf":
        return IGRFModel(name="igrf", ctx=ctx, parmod=parmod)

    if name == "t89":
        return T89Model(name="t89", ctx=ctx, parmod=parmod)

    if name == "t96":
        return T96Model(name="t96", ctx=ctx, parmod=parmod)

    if name == "t01":
        return T01Model(name="t01", ctx=ctx, parmod=parmod)

    if name == "t04":
        return T04Model(name="t04", ctx=ctx, parmod=parmod)

    raise ValueError(f"Unknown model: {name}")

def make_event_br_zero(model_rhs, *, s_min_event: float = 0.1):
    def br_event(s, pos):
        if s < s_min_event:
            return 1.0
        r = np.linalg.norm(pos)
        if r == 0.0:
            return 1.0
        rhat = pos / r
        return float(np.dot(model_rhs(s,pos), rhat))
    br_event.terminal = True
    br_event.direction = 0.0
    return br_event

def make_rhs_direction(model: MagneticFieldModel, *, direction: float):
    def rhs(s, pos):
        B = model.B_gsm(pos)
        n = np.linalg.norm(B)
        if not np.isfinite(n) or n == 0.0:
            return np.zeros(3)
        return direction * (B / n)
    return rhs