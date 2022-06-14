from ctypes import Structure, c_uint64, cdll, c_char_p, create_string_buffer
from hashlib import blake2b
import platform
import pkg_resources

def load_library(path_name):
    if platform.system() == 'Windows':
        lib_ext = ".dll"
    elif platform.system() == 'Darwin':
        lib_ext = ".dylib"
    else:
        lib_ext = ".so"
    return cdll.LoadLibrary(pkg_resources.resource_filename('mclbn256', path_name+lib_ext))

#
# Define constants needed to replace the C headers
#
mclBn_CurveFp254BNb = 0
EMBEDDING_DEGREE = 12
DIMENSIONALITY = 3
PAIR_SCALE = 2
precomputedQcoeffSize = 70
MCLBN_FP_UNIT_SIZE = 4
MCLBN_FR_UNIT_SIZE = 4
MCLBN_COMPILED_TIME_VAR = MCLBN_FP_UNIT_SIZE + (MCLBN_FR_UNIT_SIZE * 10)
mclBnFr_bytes = c_uint64 * MCLBN_FR_UNIT_SIZE
mclBnFp_bytes = c_uint64 * MCLBN_FP_UNIT_SIZE
mclBnGT_bytes = c_uint64 * MCLBN_FP_UNIT_SIZE * EMBEDDING_DEGREE
mclBnG1_bytes = c_uint64 * MCLBN_FP_UNIT_SIZE * DIMENSIONALITY
mclBnG2_bytes = c_uint64 * MCLBN_FP_UNIT_SIZE * PAIR_SCALE * DIMENSIONALITY

#
# Headers for developer's convenience
#
class lib:
    def mclBnG1_setDst(dst, dstSize):
        """const char *dst, mclSize dstSize"""
        return int()
    def mclBnG1_clear(x):
        """mclBnG1 *x"""
        return None
    def mclBnG1_serialize(buf, maxBufSize, x):
        """void *buf, mclSize maxBufSize, const mclBnG1 *x"""
        return int()#mclSize()
    def mclBnG1_deserialize(x, buf, bufSize):
        """mclBnG1 *x, const void *buf, mclSize bufSize"""
        return int()#mclSize()
    def mclBnG1_getStr(buf, maxBufSize, x, ioMode):
        """char *buf, mclSize maxBufSize, const mclBnG1 *x, int ioMode"""
        return int()#mclSize()
    def mclBnG1_setStr(x, buf, bufSize, ioMode):
        """mclBnG1 *x, const char *buf, mclSize bufSize, int ioMode"""
        return int()
    def mclBnG1_neg(y, x):
        """mclBnG1 *y, const mclBnG1 *x"""
        return None
    def mclBnG1_dbl(y, x):
        """mclBnG1 *y, const mclBnG1 *x"""
        return None
    def mclBnG1_add(z, x, y):
        """mclBnG1 *z, const mclBnG1 *x, const mclBnG1 *y"""
        return None
    def mclBnG1_sub(z, x, y):
        """mclBnG1 *z, const mclBnG1 *x, const mclBnG1 *y"""
        return None
    def mclBnG1_normalize(y, x):
        """mclBnG1 *y, const mclBnG1 *x"""
        return None
    def mclBnG1_mul(z, x, y):
        """mclBnG1 *z, const mclBnG1 *x, const mclBnFr *y"""
        return None
    def mclBnG1_mulVec(z, x, y, n):
        """mclBnG1 *z, const mclBnG1 *x, const mclBnFr *y, mclSize n"""
        return None
    def mclBnFp_mapToG1(y, x):
        """mclBnG1 *y, const mclBnFp *x"""
        return int()
    def mclBnG1_hashAndMapTo(x, buf, bufSize):
        """mclBnG1 *x, const void *buf, mclSize bufSize"""
        return int()
    def mclBn_pairing(z, x, y):
        """mclBnGT *z, const mclBnG1 *x, const mclBnG2 *y"""
        return None
    def mclBn_millerLoop(z, x, y):
        """mclBnGT *z, const mclBnG1 *x, const mclBnG2 *y"""
        return None
    def mclBn_millerLoopVec(z, x, y, n):
        """mclBnGT *z, const mclBnG1 *x, const mclBnG2 *y, mclSize n"""
        return None
    def mclBn_precomputeG2(Qbuf, Q):
        """mclBn_precomputeG2(uint64_t *Qbuf, const mclBnG2 *Q);"""
        return None
    def mclBn_precomputedMillerLoop(f, P, Qbuf):
        """mclBnGT *f, const mclBnG1 *P, const uint64_t *Qbuf"""
        return None
    def mclBn_precomputedMillerLoop2(f, P1, Q1buf, P2, __):
        """mclBnGT *f, const mclBnG1 *P1, const uint64_t *Q1buf, const mclBnG1 *P2, const uint64_t __"""
        return None
    def mclBn_precomputedMillerLoop2mixed(f, P1, Q1, P2, __):
        """mclBnGT *f, const mclBnG1 *P1, const mclBnG2 *Q1, const mclBnG1 *P2, const uint64_t __"""
        return None
    def mclBnG1_isValid(x):
        """const mclBnG1 *x"""
        return bool()
    def mclBnG1_isValidOrder(x):
        """const mclBnG1 *x"""
        return bool()
    def mclBnG1_isEqual(x, y):
        """const mclBnG1 *x, const mclBnG1 *y"""
        return bool()
    def mclBnG1_isZero(x):
        """const mclBnG1 *x"""
        return bool()
    def mclBn_G1LagrangeInterpolation(out, xVec, yVec, k):
        """mclBnG1 *out, const mclBnFr *xVec, const mclBnG1 *yVec, mclSize k"""
        return int()
    def mclBn_G1EvaluatePolynomial(out, cVec, cSize, x):
        """mclBnG1 *out, const mclBnG1 *cVec, mclSize cSize, const mclBnFr *x"""
        return int()

    def mclBnG2_setDst(dst, dstSize):
        return int()
    def mclBnG2_clear(x):
        return None
    def mclBnG2_serialize(buf, maxBufSize, x):
        return int()#mclSize()
    def mclBnG2_deserialize(x, buf, bufSize):
        return int()#mclSize()
    def mclBnG2_getStr(buf, maxBufSize, x, ioMode):
        return int()#mclSize()
    def mclBnG2_setStr(x, buf, bufSize, ioMode):
        return int()
    def mclBnG2_neg(y, x):
        return None
    def mclBnG2_dbl(y, x):
        return None
    def mclBnG2_add(z, x, y):
        return None
    def mclBnG2_sub(z, x, y):
        return None
    def mclBnG2_normalize(y, x):
        return None
    def mclBnG2_mul(z, x, y):
        return None
    def mclBnG2_mulVec(z, x, y, n):
        return None
    def mclBnG2_hashAndMapTo(x, buf, bufSize):
        return int()
    def mclBnG2_isValid(x):
        return bool()
    def mclBnG2_isValidOrder(x):
        return bool()
    def mclBnG2_isEqual(x, y):
        return bool()
    def mclBnG2_isZero(x):
        return bool()

    def mclBnGT_clear(x):
        return None
    def mclBnGT_setInt(y, mclx):
        return None
    def mclBnGT_serialize(buf, maxBufSize, x):
        return int()#mclSize()
    def mclBnGT_deserialize(x, buf, bufSize):
        return int()#mclSize()
    def mclBnGT_getStr(buf, maxBufSize, x, ioMode):
        return int()#mclSize()
    def mclBnGT_setStr(x, buf, bufSize, ioMode):
        return int()
    def mclBnGT_inv(y, x):
        return None
    def mclBnGT_sqr(y, x):
        return None
    def mclBnGT_mul(z, x, y):
        return None
    def mclBnGT_div(z, x, y):
        return None
    def mclBnGT_neg(y, x):
        return None
    def mclBnGT_add(z, x, y):
        return None
    def mclBnGT_sub(z, x, y):
        return None
    def mclBnGT_pow(z, x, y):
        return None
    def mclBnGT_powVec(z, x, y, n):
        return None
    def mclBn_finalExp(y, x):
        """mclBn_finalExp(mclBnGT *y, const mclBnGT *x)"""
        return None
    def mclBnGT_isEqual(x, y):
        return bool()
    def mclBnGT_isZero(x):
        return bool()
    def mclBnGT_isOne(x):
        return bool()

    def mclBnFr_clear(x):
        return None
    def mclBnFp_clear(x):
        return None
    def mclBnFp2_clear(x):
        return None
    def mclBnFp_setInt(y, x):
        return None
    def mclBnFr_setInt(y, x):
        return None
    def mclBnFp_setLittleEndian(x, buf, bufSize):
        return int()
    def mclBnFr_setLittleEndian(x, buf, bufSize):
        return int()
    def mclBnFp_setLittleEndianMod(x, buf, bufSize):
        return int()
    def mclBnFr_setLittleEndianMod(x, buf, bufSize):
        return int()
    def mclBnFr_getLittleEndian(buf, maxBufSize, x):
        return int()#mclSize()
    def mclBnFp_getLittleEndian(buf, maxBufSize, x):
        return int()#mclSize()
    def mclBnFr_serialize(buf, maxBufSize, x):
        return int()#mclSize()
    def mclBnFp_serialize(buf, maxBufSize, x):
        return int()#mclSize()
    def mclBnFp2_serialize(buf, maxBufSize, x):
        return int()#mclSize()
    def mclBnFr_deserialize(x, buf, bufSize):
        return int()#mclSize()
    def mclBnFp_deserialize(x, buf, bufSize):
        return int()#mclSize()
    def mclBnFp2_deserialize(x, buf, bufSize):
        return int()#mclSize()
    def mclBnFr_getStr(buf, maxBufSize, x, ioMode):
        return int()#mclSize()
    def mclBnFp_getStr(buf, maxBufSize, x, ioMode):
        return int()#mclSize()
    def mclBnFr_setStr(x, buf, bufSize, ioMode):
        return int()
    def mclBnFp_setStr(x, buf, bufSize, ioMode):
        return int()
    def mclBnFr_setByCSPRNG(x):
        return int()
    def mclBnFp_setByCSPRNG(x):
        return int()
    def mclBnFr_neg(y, x):
        return None
    def mclBnFr_inv(y, x):
        return None
    def mclBnFr_sqr(y, x):
        return None
    def mclBnFr_add(z, x, y):
        return None
    def mclBnFr_sub(z, x, y):
        return None
    def mclBnFr_mul(z, x, y):
        return None
    def mclBnFr_div(z, x, y):
        return None
    def mclBnFp_neg(y, x):
        return None
    def mclBnFp_inv(y, x):
        return None
    def mclBnFp_sqr(y, x):
        return None
    def mclBnFp_add(z, x, y):
        return None
    def mclBnFp_sub(z, x, y):
        return None
    def mclBnFp_mul(z, x, y):
        return None
    def mclBnFp_div(z, x, y):
        return None
    def mclBnFp2_neg(y, x):
        return None
    def mclBnFp2_inv(y, x):
        return None
    def mclBnFp2_sqr(y, x):
        return None
    def mclBnFp2_add(z, x, y):
        return None
    def mclBnFp2_sub(z, x, y):
        return None
    def mclBnFp2_mul(z, x, y):
        return None
    def mclBnFp2_div(z, x, y):
        return None
    def mclBnFr_squareRoot(y, x):
        return int()
    def mclBnFp_squareRoot(y, x):
        return int()
    def mclBnFp2_squareRoot(y, x):
        return int()
    def mclBnFr_setHashOf(x, buf, bufSize):
        return int()
    def mclBnFp_setHashOf(x, buf, bufSize):
        return int()
    def mclBnFr_isValid(x):
        return bool()
    def mclBnFp_isValid(x):
        return bool()
    def mclBnFr_isEqual(x, y):
        return bool()
    def mclBnFr_isZero(x):
        return bool()
    def mclBnFr_isOne(x):
        return bool()
    def mclBnFr_isOdd(x):
        return bool()
    def mclBnFp_isEqual(x, y):
        return bool()
    def mclBnFp_isZero(x):
        return bool()
    def mclBnFp_isOne(x):
        return bool()
    def mclBnFp_isOdd(x):
        return bool()
    def mclBnFp2_isEqual(x, y):
        return bool()
    def mclBnFp2_isZero(x):
        return bool()
    def mclBnFp2_isOne(x):
        return bool()
    def mclBnFr_isNegative(x):
        return bool()
    def mclBnFp_isNegative(x):
        return bool()
    def mclBn_FrLagrangeInterpolation(out, xVec, yVec, k):
        return int()
    def mclBn_FrEvaluatePolynomial(out, cVec, cSize, x):
        return int()
    def mclBnFp_setBigEndianMod(x, buf, bufSize):
        return int()

#
# Load DLL or DyLib from the wheel (or disk?)
#
def __init_lib():
    global lib
    lib = load_library("lib/libmcl")
    lib = load_library("libmclbn256")
    if lib.mclBn_init(mclBn_CurveFp254BNb, MCLBN_COMPILED_TIME_VAR): print("Failed to load MCl's BN254 binary.")
__init_lib()

#
# Configuration options
#
use_memo = True
def disable_memoization(): global use_memo; use_memo = False
def reenable_memoization(): global use_memo; use_memo = True

#
# C-Types based on the structs defined in bn.h
#
class Fr(Structure):
    _fields_ = [("d", mclBnFr_bytes)]

    def __init__(self, value=None, *args, **kw):
        super().__init__(*args, **kw)
        if value:
            self.setInt(value)
        else:
            self.setRnd()

    def __str__(self):
        return self.tostr().decode()

    def setInt(self, d):
        lib.mclBnFr_setInt(self.d, d)
    def setRnd(self):
        lib.mclBnFr_setByCSPRNG(self.d)

    def randomize(self):
        self.setRnd()
        return self

    def fromstr(self, s, io_mode=16):
        ret = lib.mclBnFr_setStr(self.d, c_char_p(s), len(s), io_mode)
        if ret:
            raise ValueError("MCl failed to return from Fr:getStr, ioMode=" + str(io_mode))
        return self

    @classmethod
    def new_fromstr(cls, s, io_mode=16):
        return Fr().fromstr(s, io_mode)

    def tostr(self, io_mode=16, raw=True, length=1021):
        """
        # define MCLBN_IO_EC_AFFINE 0
        # define MCLBN_IO_BINARY 2
        # define MCLBN_IO_DECIMAL 10
        # define MCLBN_IO_HEX_BIG_ENDIAN 16
        # define MCLBN_IO_BYTES 32
        # define MCLBN_IO_0xHEX_LITTLE_ENDIAN 144
        # define MCLBN_IO_EC_PROJ 1024  // Jacobi coordinate for G1/G2  // 0
        # define MCLBN_IO_SERIALIZE_HEX_STR 2048  // 144
        """
        sv = create_string_buffer(b"\x00" * length)
        ret_len = lib.mclBnFr_getStr(sv, length, self.d, io_mode)
        if ret_len == 0:
            raise ValueError(("MCl failed to return from Fr:getStr, ioMode=" + str(io_mode)))
        return sv.value if not raw else sv.raw[:ret_len]

    def serialize(self, raw=True, length=1021):
        sv = create_string_buffer(b"\x00" * length)
        ret_len = lib.mclBnFr_serialize(sv, length, self.d)
        if ret_len == 0:
            raise ValueError("MCl failed to return from GT:serialize")
        return sv.value if not raw else sv.raw[:ret_len]

    def _deserialize(self, s, length=None):
        sv = create_string_buffer(s)
        ret_len = lib.mclBnFr_deserialize(self.d, sv, length or len(sv))  # or len(s)?
        if ret_len == 0:
            raise ValueError("MCl failed to return from GT:deserialize")
        return self

    @classmethod
    def deserialize(cls, s, length=None):
        return Fr()._deserialize(s, length)

    def isZero(self):
        return bool(lib.mclBnFr_isZero(self.d))

    def isOne(self):
        return bool(lib.mclBnFr_isOne(self.d))

    def __neg__(self):
        ret = Fr()
        lib.mclBnFr_neg(ret.d, self.d)
        return ret

    def __invert__(self):
        ret = Fr()
        lib.mclBnFr_inv(ret.d, self.d)
        return ret

    def __add__(self, rhs):
        assert(type(rhs) is Fr)
        ret = Fr()
        lib.mclBnFr_add(ret.d, self.d, rhs.d)
        return ret

    def __sub__(self, rhs):
        assert(type(rhs) is Fr)
        ret = Fr()
        lib.mclBnFr_sub(ret.d, self.d, rhs.d)
        return ret

    def __mul__(self, rhs):
        assert(type(rhs) is Fr)
        ret = Fr()
        lib.mclBnFr_mul(ret.d, self.d, rhs.d)
        return ret

    def __div__(self, rhs):
        assert(type(rhs) is Fr)
        ret = Fr()
        lib.mclBnFr_div(ret.d, self.d, rhs.d)
        return ret

    def __eq__(self, rhs):
        return bool(lib.mclBnFr_isEqual(self.d, rhs.d))

    def __ne__(self, rhs):
        return not bool(lib.mclBnFr_isEqual(self.d, rhs.d))

class Fp6Array(Structure):  # 4 * 6 * 70 unsigned longs = 13440 bytes per precomputed and memoized point in G2
    _fields_ = [("d", mclBnFp_bytes * 6 * precomputedQcoeffSize)]
    def __bytes__(self):
        return bytes(self.d)
    def __str__(self):
        return "<Fp6Array (use bytes to see contents) 14KB array>"

class GT(Structure):  # mclBnGT type in C
    _fields_ = [("d", mclBnGT_bytes)]
    def __bytes__(self):
        return bytes(self.d)
    def __str__(self):
        return self.tostr().decode()

    def clear(self):# -> void
        x = self.d
        retval = lib.mclBnGT_clear(x)
        if retval:
            raise ValueError("MCl library call failed.")
        return retval

    def neg(self):# -> void
        result = GT()
        z = result.d
        x = self.d
        libretval = lib.mclBnGT_neg(z, x)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __neg__(self):
        return self.neg()

    def add(self, other):# -> void
        result = GT()
        z = result.d
        x = self.d
        y = other.d
        libretval = lib.mclBnGT_add(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __add__(self, other):
        return self.add(other)

    def sub(self, other):# -> void
        result = GT()
        z = result.d
        x = self.d
        y = other.d
        libretval = lib.mclBnGT_sub(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __sub__(self, other):
        return self.sub(other)

    def mul(self, other):# -> void
        result = GT()
        z = result.d
        x = self.d
        y = other.d
        libretval = lib.mclBnGT_mul(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __mul__(self, other):
        return self.mul(other)

    def pow(self, other):# -> void
        result = GT()
        z = result.d
        x = self.d
        y = other.d
        libretval = lib.mclBnGT_pow(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __pow__(self, other):
        return self.pow(other)

    def final_exp(self):# -> void
        result = GT()
        z = result.d
        x = self.d
        libretval = lib.mclBn_finalExp(z, x)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def fromstr(self, s, io_mode=16):
        ret = lib.mclBnGT_setStr(self.d, c_char_p(s), len(s), io_mode)
        if ret:
            raise ValueError("MCl failed to return from GT:getStr, ioMode=" + str(io_mode))
        return self

    @classmethod
    def new_fromstr(cls, s, io_mode=16):
        return GT().fromstr(s, io_mode)

    def tostr(self, io_mode=16, raw=True, length=1021):
        """
        # define MCLBN_IO_EC_AFFINE 0
        # define MCLBN_IO_BINARY 2
        # define MCLBN_IO_DECIMAL 10
        # define MCLBN_IO_HEX_BIG_ENDIAN 16
        # define MCLBN_IO_BYTES 32
        # define MCLBN_IO_0xHEX_LITTLE_ENDIAN 144
        # define MCLBN_IO_EC_PROJ 1024  // Jacobi coordinate for G1/G2  // 0
        # define MCLBN_IO_SERIALIZE_HEX_STR 2048  // 144
        """
        sv = create_string_buffer(b"\x00" * length)
        ret_len = lib.mclBnGT_getStr(sv, length, self.d, io_mode)
        if ret_len == 0:
            raise ValueError("MCl failed to return from GT:getStr, ioMode=" + str(io_mode))
        return sv.value if not raw else sv.raw[:ret_len]

    def serialize(self, raw=True, length=1021):
        sv = create_string_buffer(b"\x00" * length)
        ret_len = lib.mclBnGT_serialize(sv, length, self.d)
        if ret_len == 0:
            raise ValueError("MCl failed to return from GT:serialize")
        return sv.value if not raw else sv.raw[:ret_len]

    def _deserialize(self, s, length=None):
        sv = create_string_buffer(s)
        ret_len = lib.mclBnGT_deserialize(self.d, sv, length or len(sv))  # or len(s)?
        if ret_len == 0:
            raise ValueError("MCl failed to return from GT:deserialize")
        return self

    @classmethod
    def deserialize(cls, s, length=None):
        return GT()._deserialize(s, length)

    def equals(self, other):# -> int
        x = self.d
        y = other.d
        retval = lib.mclBnGT_isEqual(x, y)
        return bool(retval)  # same as `retval != 0`

    def __eq__(self, other):
        return self.equals(other)

    def __ne__(self, other):
        return not self.equals(other)

    def zero(self):# -> int
        x = self.d
        retval = lib.mclBnGT_isZero(x)
        return retval

class G1(Structure):  # mclBnG1 type in C
    _fields_ = [("d", mclBnG1_bytes)]

    def __init__(self, value=None, *args, **kw):
        super().__init__(*args, **kw)
        if value:
            self.hash(value)
        else:
            # self.randomize()
            pass

    def __str__(self):
        return self.tostr().decode()

    def randomize(self):
        sr = Fr(); sr.setRnd()
        lib.mclBnG1_hashAndMapTo(self.d, sr.d, 32)
        return self.mul(sr)

    # def hash(self, s):
    #     return lib.mclBnG1_hashAndMapTo(self.d, c_wchar_p(s), len(s))
    def hash(self, s):
        h = blake2b()
        if type(s) is str: s = s.encode()
        h.update(s)
        h = h.digest()[:16]
        ret = lib.mclBnG1_hashAndMapTo(self.d, c_char_p(h), 16)
        if not ret == 0:
            raise ValueError("MCl library call failed.")
        return self

    @classmethod
    def fromhash(cls, h):
        return G1().hash(h)  # same as `G1(h)`

    def valid(self):
        return bool(lib.mclBnG1_isValid(self.d))

    def print_valid(self):
        is_valid = self.valid()
        print("This point is valid." if is_valid else "invalid!")

    def clear(self):# -> void
        x = self.d
        retval = lib.mclBnG1_clear(x)
        if retval:
            raise ValueError("MCl library call failed.")
        return retval

    def neg(self):# -> void
        result = G1()
        z = result.d
        x = self.d
        libretval = lib.mclBnG1_neg(z, x)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __neg__(self):
        return self.neg()

    def dbl(self):# -> void
        result = G1()
        z = result.d
        x = self.d
        libretval = lib.mclBnG1_dbl(z, x)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def add(self, other):# -> void
        result = G1()
        z = result.d
        x = self.d
        y = other.d
        libretval = lib.mclBnG1_add(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __add__(self, other):
        return self.add(other)

    def sub(self, other):# -> void
        result = G1()
        z = result.d
        x = self.d
        y = other.d
        libretval = lib.mclBnG1_sub(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __sub__(self, other):
        return self.sub(other)

    def normalize(self):# -> void
        result = G1()
        z = result.d
        x = self.d
        libretval = lib.mclBnG1_normalize(z, x)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def mul(self, other: Fr):# -> void     # Would it be good for me to enforce ordering?  Oblivious would just do this anyway.
        result = G1()
        z = result.d
        x = self.d
        y = other.d
        libretval = lib.mclBnG1_mul(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __mul__(self, other):  # Again: Would it be good for me to enforce ordering?  Oblivious would just do this anyway.
        return self.mul(other)

    def fromstr(self, s, io_mode=16):
        ret = lib.mclBnG1_setStr(self.d, c_char_p(s), len(s), io_mode)
        if ret:
            raise ValueError("MCl failed to return from G1:getStr, ioMode=" + str(io_mode))
        return self

    @classmethod
    def new_fromstr(cls, s, io_mode=16):
        return G1().fromstr(s, io_mode)

    def tostr(self, io_mode=16, raw=True, length=1021):
        """
        # define MCLBN_IO_EC_AFFINE 0
        # define MCLBN_IO_BINARY 2
        # define MCLBN_IO_DECIMAL 10
        # define MCLBN_IO_HEX_BIG_ENDIAN 16
        # define MCLBN_IO_BYTES 32
        # define MCLBN_IO_0xHEX_LITTLE_ENDIAN 144
        # define MCLBN_IO_EC_PROJ 1024  // Jacobi coordinate for G1/G2  // 0
        # define MCLBN_IO_SERIALIZE_HEX_STR 2048  // 144
        """
        sv = create_string_buffer(b"\x00" * length)
        ret_len = lib.mclBnG1_getStr(sv, length, self.d, io_mode)
        if ret_len == 0:
            raise ValueError("MCl failed to return from G1:getStr, ioMode=" + str(io_mode))
        return sv.value if not raw else sv.raw[:ret_len]

    def serialize(self, raw=True, length=1021):
        sv = create_string_buffer(b"\x00" * length)
        ret_len = lib.mclBnG1_serialize(sv, length, self.d)
        if ret_len == 0:
            raise ValueError("MCl failed to return from G1:serialize")
        return sv.value if not raw else sv.raw[:ret_len]

    def _deserialize(self, s, length=None):
        sv = create_string_buffer(s)
        ret_len = lib.mclBnG1_deserialize(self.d, sv, length or len(sv))  # or len(s)?
        if ret_len == 0:
            raise ValueError("MCl failed to return from G1:deserialize")
        return self

    @classmethod
    def deserialize(cls, s, length=None):
        return G1()._deserialize(s, length)

    def pairing(self, other):# -> void
        #assert(type(other) is G2)
        if use_memo:
            if not other.coeff:
                other.coeff = other.precompute()

            result = GT()
            lib.mclBn_precomputedMillerLoop(result.d, self.d, other.coeff.d)
            return result.final_exp()
        else:
            result = GT()
            lib.mclBn_pairing(result.d, self.d, other.d)
            return result

    def __matmul__(self, other):
        return self.pairing(other)

    def valid_order(self):# -> int
        x = self.d
        retval = lib.mclBnG1_isValidOrder(x)
        return bool(retval)

    def equals(self, other):# -> int
        x = self.d
        y = other.d
        retval = lib.mclBnG1_isEqual(x, y)
        return bool(retval)  # same as `retval != 0`

    def __eq__(self, other):
        return self.equals(other)

    def __ne__(self, other):
        return not self.equals(other)

    def zero(self):# -> int
        x = self.d
        retval = lib.mclBnG1_isZero(x)
        return retval

class G2(Structure):  # mclBnG2 type in C, see bn.h
    _fields_ = [("d", mclBnG2_bytes)]
    coeff = None

    def __init__(self, value=None, *args, **kw):
        super().__init__(*args, **kw)
        if value:
            self.hash(value)
        else:
            # self.randomize()
            pass

    def __str__(self):
        return self.tostr().decode()

    def randomize(self):
        sr = Fr(); sr.setRnd()
        lib.mclBnG2_hashAndMapTo(self.d, sr.d, 32)
        return self.mul(sr)

    def hash(self, s):
        h = blake2b()
        if type(s) is str: s = s.encode()
        h.update(s)
        h = h.digest()[:16]
        ret = lib.mclBnG2_hashAndMapTo(self.d, c_char_p(h), 16)
        if not ret == 0:
            raise ValueError("MCl library call failed.")
        return self

    @classmethod
    def fromhash(cls, h):
        return G2().hash(h)  # same as `G2(h)`

    def valid(self):
        return bool(lib.mclBnG2_isValid(self.d))

    def print_valid(self):
        is_valid = self.valid()
        print("This point is valid." if is_valid else "invalid!")

    def clear(self):# -> void
        x = self.d
        retval = lib.mclBnG2_clear(x)
        if retval:
            raise ValueError("MCl library call failed.")
        return retval

    def neg(self):# -> void
        result = G2()
        z = result.d
        x = self.d
        libretval = lib.mclBnG2_neg(z, x)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __neg__(self):
        return self.neg()

    def dbl(self):# -> void
        result = G2()
        z = result.d
        x = self.d
        libretval = lib.mclBnG2_dbl(z, x)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def add(self, other):# -> void
        result = G2()
        z = result.d
        x = self.d
        y = other.d
        libretval = lib.mclBnG2_add(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __add__(self, other):
        return self.add(other)

    def sub(self, other):# -> void
        result = G2()
        z = result.d
        x = self.d
        y = other.d
        libretval = lib.mclBnG2_sub(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __sub__(self, other):
        return self.sub(other)

    def normalize(self):# -> void
        result = G2()
        z = result.d
        x = self.d
        libretval = lib.mclBnG2_normalize(z, x)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def mul(self, other):# -> void
        result = G2()
        z = result.d
        x = self.d
        y = other.d
        libretval = lib.mclBnG2_mul(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __mul__(self, other):
        return self.mul(other)

    def fromstr(self, s, io_mode=16):
        ret = lib.mclBnG2_setStr(self.d, c_char_p(s), len(s), io_mode)
        if ret:
            raise ValueError("MCl failed to return from G2:getStr, ioMode=" + str(io_mode))
        return self

    @classmethod
    def new_fromstr(cls, s, io_mode=16):
        return G2().fromstr(s, io_mode)

    def tostr(self, io_mode=16, raw=True, length=1021):
        """
        # define MCLBN_IO_EC_AFFINE 0
        # define MCLBN_IO_BINARY 2
        # define MCLBN_IO_DECIMAL 10
        # define MCLBN_IO_HEX_BIG_ENDIAN 16
        # define MCLBN_IO_BYTES 32
        # define MCLBN_IO_0xHEX_LITTLE_ENDIAN 144
        # define MCLBN_IO_EC_PROJ 1024  // Jacobi coordinate for G1/G2  // 0
        # define MCLBN_IO_SERIALIZE_HEX_STR 2048  // 144
        """
        sv = create_string_buffer(b"\x00" * length)
        ret_len = lib.mclBnG2_getStr(sv, length, self.d, io_mode)
        if ret_len == 0:
            print("MCl failed to return from G2:getStr, ioMode=" + str(io_mode))
        return sv.value if not raw else sv.raw[:ret_len]

    def serialize(self, raw=True, length=1021):
        sv = create_string_buffer(b"\x00" * length)
        ret_len = lib.mclBnG2_serialize(sv, length, self.d)
        if ret_len == 0:
            raise ValueError("MCl failed to return from G2:serialize")
        return sv.value if not raw else sv.raw[:ret_len]

    def _deserialize(self, s, length=None):
        sv = create_string_buffer(s)
        ret_len = lib.mclBnG2_deserialize(self.d, sv, length or len(sv))  # or len(s)?
        if ret_len == 0:
            raise ValueError("MCl failed to return from G2:deserialize")
        return self

    @classmethod
    def deserialize(cls, s, length=None):
        return G2()._deserialize(s, length)

    def pairing(self, other):# -> void
        # assert(type(other) is G1)
        if use_memo:
            if not self.coeff:
                self.coeff = self.precompute()

            result = GT()
            lib.mclBn_precomputedMillerLoop(result.d, other.d, self.coeff.d)  # sorted, so use the reverse order
            return result.final_exp()
        else:
            result = GT()
            lib.mclBn_pairing(result.d, other.d, self.d)  # sorted, so use the reverse order
            return result

    def precompute(self):# -> void
        result = Fp6Array()
        z = result.d
        x = self.d
        libretval = lib.mclBn_precomputeG2(z, x)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __matmul__(self, other):
        return self.pairing(other)

    def valid_order(self):# -> int
        x = self.d
        retval = lib.mclBnG2_isValidOrder(x)
        return bool(retval)

    def equals(self, other):# -> int
        x = self.d
        y = other.d
        retval = lib.mclBnG2_isEqual(x, y)
        return bool(retval)  # same as `retval != 0`

    def __eq__(self, other):
        return self.equals(other)

    def __ne__(self, other):
        return not self.equals(other)

    def zero(self):# -> int
        x = self.d
        retval = lib.mclBnG2_isZero(x)
        return retval


def assert_bilinearity():
    a = Fr()  # random by default
    b = Fr()
    P = G1().hash("1")
    Q = G2().hash("1")
    assert(P.valid())
    assert(Q.valid())

    aP = P * a
    bQ = Q * b
    e = P @ Q
    assert(e ** a == aP @ Q)
    assert(e ** b == P @ bQ)
    assert(e ** Fr(3) == e * e * e)

    s = Fr(646453563245)
    t = Fr(857462736753)
    p = G1().hash("some row")
    q = G2().hash("another row")
    assert(p.valid())
    assert(q.valid())

    assert(((p * s) @ (q * t)) == (p @ (q * s * t)))
    assert(((p * s * ~t) @ (q * t)) == (p @ (q * s)))
    assert(((p * s) @ q) == ((p * ~t) @ (q * s * t)))


def assert_serializable():
    s = Fr(646453563245)
    t = Fr(857462736753)
    p = G1().hash("some row")
    q = G2().hash("another row")
    assert(p.valid())
    assert(q.valid())

    #disable_memoization()
    for _ in range(32):
        s.randomize()
        t.randomize()
        for _ in range(32):
            p.randomize()
            q.randomize()
            e = p @ q

            for mode in [0, 10, 16, 32, 144, 1024, 2048]:  # Binary mode (2) will likely require a length to be passed for it to work.
                assert(s == Fr.new_fromstr(s.tostr(mode), mode))
                assert(p == G1.new_fromstr(p.tostr(mode), mode))
                assert(q == G2.new_fromstr(q.tostr(mode), mode))
                assert(e == GT.new_fromstr(e.tostr(mode), mode))

            assert(s == Fr.deserialize(s.serialize()))
            assert(p == G1.deserialize(p.serialize()))
            assert(q == G2.deserialize(q.serialize()))
            assert(e == GT.deserialize(e.serialize()))


def assert_sane():
    s = Fr()
    t = Fr()
    p = G1("p")
    q = G2("q")
    assert(p.valid())
    assert(q.valid())

    e = (p * s) @ q
    assert(q * s * t @ (p * ~t) == e)

    assert (s == Fr.deserialize(s.serialize()))
    assert (p == G1.deserialize(p.serialize()))
    assert (q == G2.deserialize(q.serialize()))
    assert (e == GT.deserialize(e.serialize()))


# assert_bilinearity()
# assert_serializable()
assert_sane()
