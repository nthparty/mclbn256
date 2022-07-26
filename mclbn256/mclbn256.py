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
    def mclBnG1_getBasePoint(x):
        """mclBnG1 *x"""
        return int()
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
        # https://github.com/herumi/mcl/blob/master/include/mcl/ec.hpp#L771-L786
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
    def mclBnG2_getBasePoint(x):
        """mclBnG2 *x"""
        return int()
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
        # https://github.com/herumi/mcl/blob/master/include/mcl/ec.hpp#L771-L786
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
    # _ = load_library("lib/libmcl")
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
    _fields_ = [("s", mclBnFr_bytes)]

    def __new__(cls, *args, **kwargs):
        s = Structure.__new__(cls)
        Fr.__init__(s, *args, **kwargs)
        return s

    def __init__(self, value=None, *args, **kw):
        super().__init__(*args, **kw)
        if isinstance(value, int):#value != None:
            self.setInt(value)
        elif isinstance(value, bytes):#value != None:     # isinstance(value, str)
            self.fromstr(value, 32)
        elif isinstance(value, Fr):#value != None:
            # self.__init__(bytes(value))  # or __init__(int(value))
            self.s = value.s
        elif isinstance(value, bytearray):
            self.__init__(bytes(value))
        else:
            self.setRnd()

    def __bytes__(self):
        return self.tostr(32)  # (for only `Fr`) this is the same as `self.serialize()`

    def __str__(self):
        return self.tostr(10).decode()

    def __int__(self):
        id = lambda s : s
        sign, unsign = (int.__neg__, Fr.__neg__) if self.is_negative() else (id, id)

        return sign(int.from_bytes(unsign(self).tostr(32), 'little'))
        #  -or-  return sign(int.from_bytes(unsign(self).serialize(), 'little'))

    def setInt(self, value):
        # r = 0x2523648240000001ba344d8000000007ff9f800000000010a10000000000000d
        # self.fromstr(int.to_bytes(value if value>=0 else r-value, 32, 'little'), 32)

        # self.fromstr(int.to_bytes(abs(value), 32, 'little'), 32)
        # if value < 0: lib.mclBnFr_neg(self.s, self.s)

        self.fromstr(int.to_bytes(abs(value), 32, 'little'), 32)
        if value < 0: self.negate()

        # self.fromstr(int.to_bytes(value, 32, 'little', signevalue=True), 32)

        # self.fromstr(int.to_bytes(value, 32, 'little'), 32)
        
        # lib.mclBnFr_setInt(self.value, value)

    def setRnd(self):
        lib.mclBnFr_setByCSPRNG(self.s)

    def randomize(self):
        self.setRnd()
        return self

    def fromstr(self, s, io_mode=16):
        ret = lib.mclBnFr_setStr(self.s, c_char_p(s), len(s), io_mode)
        if ret:
            raise ValueError("MCl failed to return from Fr:getStr, ioMode=" + str(io_mode))
        return self

    @classmethod
    def new_fromstr(cls, s, io_mode=16):
        return Fr().fromstr(s, io_mode)

    def tostr(self, io_mode=16, raw=True, length=1021):
        """
        See https://github.com/herumi/mcl/blob/master/include/mcl/op.hpp#L30-L108 for details.
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
        ret_len = lib.mclBnFr_getStr(sv, length, self.s, io_mode)
        if ret_len == 0:
            raise ValueError(("MCl failed to return from Fr:getStr, ioMode=" + str(io_mode)))
        return sv.value if not raw else sv.raw[:ret_len]

    def serialize(self, raw=True, length=1021):
        sv = create_string_buffer(b"\x00" * length)
        ret_len = lib.mclBnFr_serialize(sv, length, self.s)
        if ret_len == 0:
            raise ValueError("MCl failed to return from GT:serialize")
        return sv.value if not raw else sv.raw[:ret_len]

    def _deserialize(self, s, length=None):
        sv = create_string_buffer(s)
        ret_len = lib.mclBnFr_deserialize(self.s, sv, length or len(sv))  # or len(s)?
        if ret_len == 0:
            raise ValueError("MCl failed to return from GT:deserialize")
        return self

    @classmethod
    def deserialize(cls, s, length=None):
        return Fr()._deserialize(s, length)

    def is_zero(self):
        return bool(lib.mclBnFr_isZero(self.s))

    def is_one(self):
        return bool(lib.mclBnFr_isOne(self.s))

    def is_odd(self):
        return bool(lib.mclBnFr_isOdd(self.s))

    def is_valid(self):
        return bool(lib.mclBnFr_isValid(self.s))

    def is_negative(self):
        return bool(lib.mclBnFr_isNegative(self.s))

    def __neg__(self):
        ret = Fr()
        lib.mclBnFr_neg(ret.s, self.s)
        return ret

    # def __neg__in_place(self):
    #     lib.mclBnFr_neg(self.s, self.s)
    #     return self

    def negate(self):
        lib.mclBnFr_neg(self.s, self.s)

    def __invert__(self):
        ret = Fr()
        lib.mclBnFr_inv(ret.s, self.s)
        return ret

    def __add__(self, other):
        assert(isinstance(other, Fr))
        ret = Fr()
        lib.mclBnFr_add(ret.s, self.s, other.s)
        return ret

    def __sub__(self, other):
        assert(isinstance(other, Fr))
        ret = Fr()
        lib.mclBnFr_sub(ret.s, self.s, other.s)
        return ret

    def __mul__(self, other):
        assert(isinstance(other, Fr))
        ret = Fr()
        lib.mclBnFr_mul(ret.s, self.s, other.s)
        return ret

    def __pow__(self, other):
        #assert(isinstance(other, Fr))
        r = 0x2523648240000001ba344d8000000007ff9f800000000010a10000000000000d
        return Fr(int(self).__pow__(int(other), r))
        #return Fr(pow(int(self), int(other), r))

    # def __mod__(self, other):
    #     assert(isinstance(other, Fr))
    #     return self - ((self//other) * other)

    def __mod__(self, other):
        #assert(isinstance(other, Fr))
        return Fr(int(self).__mod__(int(other)))

    def __truediv__(self, other):
        assert(isinstance(other, Fr))
        ret = Fr()
        lib.mclBnFr_div(ret.s, self.s, other.s)
        return ret

    def __floordiv__(self, other):
        assert(isinstance(other, Fr))
        return Fr(int(self).__floordiv__(int(other)))

    def sqr(self):
        ret = Fr()
        lib.mclBnFr_sqr(ret.s, self.s)
        return ret

    def sqrt(self):
        ret = Fr()
        lib.mclBnFr_squareRoot(ret.s, self.s)
        return ret

    def __eq__(self, other):
        return bool(lib.mclBnFr_isEqual(self.s, other.s))

    def __ne__(self, other):
        return not bool(lib.mclBnFr_isEqual(self.s, other.s))

class Fp6Array(Structure):  # 4 * 6 * 70 unsigned longs = 13440 bytes per precomputed and memoized point in G2
    _fields_ = [("s6", mclBnFp_bytes * 6 * precomputedQcoeffSize)]
    def __bytes__(self):
        return bytes(self.s6)
    def __str__(self):
        return "<Fp6Array (use bytes to see contents) 14KB array>"

class GT(Structure):  # mclBnGT type in C
    _fields_ = [("d12", mclBnGT_bytes)]

    def __new__(cls, *args, **kwargs):
        s = Structure.__new__(cls)
        if not args == ():#len(args) > 0:
            GT.__init__(s, *args, **kwargs)
        return s

    def __init__(self, value=None, *args, **kw):
        super().__init__(*args, **kw)
        if isinstance(value, bytes):#value != None:     # isinstance(value, str)
            self.fromstr(value, 32)
        elif isinstance(value, GT):#value != None:
            self.d12 = value.d12
        elif isinstance(value, bytearray):
            self.__init__(bytes(value))

    def __bytes__(self):
        return self.tostr(32)#.serialize()

    def __str__(self):
        # return self.tostr(2048).decode()
        return self.tostr().decode()

    def clear(self):# -> void
        x = self.d12
        retval = lib.mclBnGT_clear(x)
        if retval:
            raise ValueError("MCl library call failed.")
        return retval

    def neg(self):# -> void
        result = GT()
        z = result.d12
        x = self.d12
        libretval = lib.mclBnGT_neg(z, x)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __neg__(self):
        return self.neg()

    def add(self, other):# -> void
        assert isinstance(other, GT)
        result = GT()
        z = result.d12
        x = self.d12
        y = other.d12
        libretval = lib.mclBnGT_add(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __add__(self, other):
        return self.add(other)

    def sub(self, other):# -> void
        assert isinstance(other, GT)
        result = GT()
        z = result.d12
        x = self.d12
        y = other.d12
        libretval = lib.mclBnGT_sub(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __sub__(self, other):
        return self.sub(other)

    def mul(self, other):# -> void
        assert isinstance(other, GT)
        result = GT()
        z = result.d12
        x = self.d12
        y = other.d12
        libretval = lib.mclBnGT_mul(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __mul__(self, other):
        return self.mul(other)

    def div(self, other):# -> void
        assert isinstance(other, GT)
        result = GT()
        z = result.d12
        x = self.d12
        y = other.d12
        libretval = lib.mclBnGT_div(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __truediv__(self, other):
        return self.div(other)

    def pow(self, other):# -> void
        is_Fr = isinstance(other, Fr)
        assert is_Fr or isinstance(other, GT)
        result = GT()
        z = result.d12
        x = self.d12
        y = other.s if is_Fr else other.d12
        libretval = (lib.mclBnGT_pow if is_Fr else lib.mclBnGT_powGeneric)(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __pow__(self, other):
        return self.pow(other)

    def final_exp(self):# -> void
        result = GT()
        z = result.d12
        x = self.d12
        libretval = lib.mclBn_finalExp(z, x)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def fromstr(self, s, io_mode=16):
        ret = lib.mclBnGT_setStr(self.d12, c_char_p(s), len(s), io_mode)
        if ret:
            raise ValueError("MCl failed to return from GT:getStr, ioMode=" + str(io_mode))
        return self

    @classmethod
    def new_fromstr(cls, s, io_mode=16):
        return GT().fromstr(s, io_mode)

    def tostr(self, io_mode=16, raw=True, length=1021):
        """
        See https://github.com/herumi/mcl/blob/master/include/mcl/op.hpp#L30-L108 for IOmode details
        See https://github.com/herumi/mcl/blob/master/include/mcl/ec.hpp#L1441-L1556 for serialize()
        //github.com/herumi/mcl/blob/0489e76cfae425ab9d3ec93952e9ae928ef86017/include/mcl/op.hpp#L30
        # define MCLBN_IO_EC_AFFINE 0
        # define MCLBN_IO_BINARY 2
        # define MCLBN_IO_DECIMAL 10
        # define MCLBN_IO_HEX_BIG_ENDIAN 16
        # define MCLBN_IO_BYTES 32
        # define MCLBN_IO_0xHEX_LITTLE_ENDIAN 144
        # define MCLBN_IO_EC_PROJ 1024  // Jacobi coordinate for G1/G2  // 0
        # define MCLBN_IO_SERIALIZE_HEX_STR 2048  // 144
        IoMode={IoAuto,IoBin,IoDec,IoHex,IoArray,IoArrayRaw,IoPrefix,IoBinPrefix,IoHexPrefix,IoEcAff
        ine,IoEcCompY,IoSerialize,IoFixedSizeByteSeq,IoEcProj,IoSerializeHexStr,IoEcAffineSerialize=
        0,2,10,16,32,64,128,130,144,0,256,512,512,1024,2048,4096}
        """
        sv = create_string_buffer(b"\x00" * length)
        ret_len = lib.mclBnGT_getStr(sv, length, self.d12, io_mode)
        if ret_len == 0:
            raise ValueError("MCl failed to return from GT:getStr, ioMode=" + str(io_mode))
        return sv.value if not raw else sv.raw[:ret_len]

    def serialize(self, raw=True, length=1021):
        sv = create_string_buffer(b"\x00" * length)
        ret_len = lib.mclBnGT_serialize(sv, length, self.d12)
        if ret_len == 0:
            raise ValueError("MCl failed to return from GT:serialize")
        return sv.value if not raw else sv.raw[:ret_len]

    def _deserialize(self, s, length=None):
        sv = create_string_buffer(s)
        ret_len = lib.mclBnGT_deserialize(self.d12, sv, length or len(sv))  # or len(s)?
        if ret_len == 0:
            raise ValueError("MCl failed to return from GT:deserialize")
        return self

    @classmethod
    def deserialize(cls, s, length=None):
        return GT()._deserialize(s, length)

    def equals(self, other):# -> int
        x = self.d12
        y = other.d12
        retval = lib.mclBnGT_isEqual(x, y)
        return bool(retval)  # same as `retval != 0`

    def __eq__(self, other):
        return self.equals(other)

    def __ne__(self, other):
        return not self.equals(other)

    def zero(self):# -> int
        x = self.d12
        retval = lib.mclBnGT_isZero(x)
        return retval

class G1(Structure):  # mclBnG1 type in C
    _fields_ = [("d", mclBnG1_bytes)]

    def __new__(cls, *args, **kwargs):
        # print('new')
        p = Structure.__new__(cls)
        G1.__init__(p, *args, **kwargs)
        return p
        # return Structure.__new__(cls, *args, **kwargs)#object.__new__(cls)

    def __bytes__(self):
        return self.serialize()

    def __init__(self, value=None, *args, **kw):
        super().__init__(*args, **kw)
        if isinstance(value, str) or isinstance(value, bytes):
            G1.hash(self, value)
        elif isinstance(value, G1):
            self.d = value.d
        elif isinstance(value, bytearray):
            self.__init__(bytes(value))
        else:
            # self.randomize()
            pass

    def __str__(self):
        return self.tostr().decode()

    def __hex__(self):
        return self.serialize().hex()

    @classmethod
    def fromhex(cls, h: str):
        return G1().deserialize(bytes.fromhex(h))
        #return cls().deserialize(bytes.fromhex(h))

    def randomize(self):
        sr = Fr(); sr.setRnd()
        lib.mclBnG1_hashAndMapTo(self.d, sr.s, 32)
        return self.mul_in_place(sr)

    @classmethod
    def random(cls):
        self = G1()
        sr = Fr(); sr.setRnd()
        lib.mclBnG1_hashAndMapTo(self.d, sr.s, 32)
        return self.mul_in_place(sr)

    # def hash(self, s):
    #     return lib.mclBnG1_hashAndMapTo(self.d, c_wchar_p(s), len(s))
    def hash(self, s):
        h = blake2b()
        if isinstance(s, str): s = s.encode()
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

    @classmethod
    def base_point(cls):# -> int
        # result = G1()
        # x = result.d
        # libretval = lib.mclBnG1_getBasePoint(x)
        # if not libretval == 0:
        #     raise ValueError("MCl library call failed.")
        # return result
        return G1.fromhex('12000000000000a7130000000000216108000000804d34ba01000040826423a5')

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
        y = other.s
        libretval = lib.mclBnG1_mul(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def mul_in_place(self, other: Fr):
        x = self.d
        y = other.s
        libretval = lib.mclBnG1_mul(x, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return self

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
        See https://github.com/herumi/mcl/blob/master/include/mcl/op.hpp#L30-L108 for details.
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
        #assert(isinstance(other, G2))
        if use_memo:
            if not other.coeff:
                other.coeff = other.precompute()

            result = GT()
            lib.mclBn_precomputedMillerLoop(result.d12, self.d, other.coeff.s6)
            return result.final_exp()
        else:
            result = GT()
            lib.mclBn_pairing(result.d12, self.d, other.d2)
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
    _fields_ = [("d2", mclBnG2_bytes)]
    coeff = None

    def __new__(cls, *args, **kwargs):
        q = Structure.__new__(cls)
        G2.__init__(q, *args, **kwargs)
        return q

    def __bytes__(self):
        return self.serialize()

    def __init__(self, value=None, *args, **kw):
        super().__init__(*args, **kw)
        if isinstance(value, str) or isinstance(value, bytes):
            G2.hash(self, value)
        elif isinstance(value, G2):
            self.d2 = value.d2
        elif isinstance(value, bytearray):
            self.__init__(bytes(value))
        else:
            # self.randomize()
            pass

    def __str__(self):
        return self.tostr().decode()

    def __hex__(self):
        return self.serialize().hex()

    @classmethod
    def fromhex(cls, h: str):
        return G2().deserialize(bytes.fromhex(h))
        #return cls().deserialize(bytes.fromhex(h))

    def randomize(self):
        sr = Fr(); sr.setRnd()
        lib.mclBnG2_hashAndMapTo(self.d2, sr.s, 32)
        return self.mul_in_place(sr)

    @classmethod
    def random(cls):
        self = G2()
        sr = Fr(); sr.setRnd()
        lib.mclBnG2_hashAndMapTo(self.d2, sr.s, 32)
        return self.mul_in_place(sr)

    def hash(self, s):
        h = blake2b()
        if isinstance(s, str): s = s.encode()
        h.update(s)
        h = h.digest()[:16]
        ret = lib.mclBnG2_hashAndMapTo(self.d2, c_char_p(h), 16)
        if not ret == 0:
            raise ValueError("MCl library call failed.")
        return self

    @classmethod
    def fromhash(cls, h):
        return G2().hash(h)  # same as `G2(h)`

    def valid(self):
        return bool(lib.mclBnG2_isValid(self.d2))

    def print_valid(self):
        is_valid = self.valid()
        print("This point is valid." if is_valid else "invalid!")

    def clear(self):# -> void
        x = self.d2
        retval = lib.mclBnG2_clear(x)
        if retval:
            raise ValueError("MCl library call failed.")
        return retval

    @classmethod
    def base_point(cls):# -> int
        # result = G2()
        # x = result.d2
        # libretval = not lib.mclBnG2_getBasePoint
        return G2.fromhex('2bfb03c82442ee910dbf9848bb8b64a4b6ed618c7e8c8deb2fb69e51bb101a06'
                          'f34cd5e7c1348c0db78437ae6b744d1f5baa82598ca70a31337873baf9aa1605')

    def neg(self):# -> void
        result = G2()
        z = result.d2
        x = self.d2
        libretval = lib.mclBnG2_neg(z, x)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __neg__(self):
        return self.neg()

    def dbl(self):# -> void
        result = G2()
        z = result.d2
        x = self.d2
        libretval = lib.mclBnG2_dbl(z, x)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def add(self, other):# -> void
        result = G2()
        z = result.d2
        x = self.d2
        y = other.d2
        libretval = lib.mclBnG2_add(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __add__(self, other):
        return self.add(other)

    def sub(self, other):# -> void
        result = G2()
        z = result.d2
        x = self.d2
        y = other.d2
        libretval = lib.mclBnG2_sub(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __sub__(self, other):
        return self.sub(other)

    def normalize(self):# -> void
        result = G2()
        z = result.d2
        x = self.d2
        libretval = lib.mclBnG2_normalize(z, x)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def mul(self, other):# -> void
        result = G2()
        z = result.d2
        x = self.d2
        y = other.s
        libretval = lib.mclBnG2_mul(z, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def mul_in_place(self, other: Fr):
        x = self.d2
        y = other.s
        libretval = lib.mclBnG2_mul(x, x, y)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return self

    def __mul__(self, other):
        return self.mul(other)

    def fromstr(self, s, io_mode=16):
        ret = lib.mclBnG2_setStr(self.d2, c_char_p(s), len(s), io_mode)
        if ret:
            raise ValueError("MCl failed to return from G2:getStr, ioMode=" + str(io_mode))
        return self

    @classmethod
    def new_fromstr(cls, s, io_mode=16):
        return G2().fromstr(s, io_mode)

    def tostr(self, io_mode=16, raw=True, length=1021):
        """
        See https://github.com/herumi/mcl/blob/master/include/mcl/op.hpp#L30-L108 for details.
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
        ret_len = lib.mclBnG2_getStr(sv, length, self.d2, io_mode)
        if ret_len == 0:
            print("MCl failed to return from G2:getStr, ioMode=" + str(io_mode))
        return sv.value if not raw else sv.raw[:ret_len]

    def serialize(self, raw=True, length=1021):
        sv = create_string_buffer(b"\x00" * length)
        ret_len = lib.mclBnG2_serialize(sv, length, self.d2)
        if ret_len == 0:
            raise ValueError("MCl failed to return from G2:serialize")
        return sv.value if not raw else sv.raw[:ret_len]

    def _deserialize(self, s, length=None):
        sv = create_string_buffer(s)
        ret_len = lib.mclBnG2_deserialize(self.d2, sv, length or len(sv))  # or len(s)?
        if ret_len == 0:
            raise ValueError("MCl failed to return from G2:deserialize")
        return self

    @classmethod
    def deserialize(cls, s, length=None):
        return G2()._deserialize(s, length)

    def pairing(self, other):# -> void
        # assert(isinstance(other, G1))
        if use_memo:
            if not self.coeff:
                self.coeff = self.precompute()

            result = GT()
            lib.mclBn_precomputedMillerLoop(result.d12, other.d, self.coeff.s6)  # sorted, so use the reverse order
            return result.final_exp()
        else:
            result = GT()
            lib.mclBn_pairing(result.d12, other.d, self.d2)  # sorted, so use the reverse order
            return result

    def precompute(self):# -> void
        result = Fp6Array()
        z = result.s6
        x = self.d2
        libretval = lib.mclBn_precomputeG2(z, x)
        if libretval == -1:
            raise ValueError("MCl library call failed.")
        return result

    def __matmul__(self, other):
        return self.pairing(other)

    def valid_order(self):# -> int
        x = self.d2
        retval = lib.mclBnG2_isValidOrder(x)
        return bool(retval)

    def equals(self, other):# -> int
        x = self.d2
        y = other.d2
        retval = lib.mclBnG2_isEqual(x, y)
        return bool(retval)  # same as `retval != 0`

    def __eq__(self, other):
        return self.equals(other)

    def __ne__(self, other):
        return not self.equals(other)

    def zero(self):# -> int
        x = self.d2
        retval = lib.mclBnG2_isZero(x)
        return retval


def G1_to_ECp(p):
    from bn254 import ECp
    if p.zero():
        return ECp()  # Note: bn254.ECp().toBytes(1) == b'\x02' + b"\x00" * 32
    return (
        lambda X : (lambda x : (x if x.setxy(*map(int, X.tostr(10).decode().split(' ')[-2:])) else None))(ECp())
    )(p)


def ECp_to_G1(x):
    # import bn254
    if x.isinf():
        return G1()#.fromstr(b"\x00"*32, 32)  # Note: bn254.ECp().toBytes(1) == b'\x02' + b"\x00" * 32
    try:
        return (
            lambda p : G1().fromstr(str(p).replace(',', ' ').replace('(', '1 ').replace(')', '').encode())
        )(x)
    except ValueError:
        return None


def G2_to_ECp2(q):
    from bn254 import ECp2, Fp, Fp2
    if q.zero():
        return ECp2()  # Note: bn254.ECp2().toBytes(1) == b'\x02' + b"\x00" * 64
    return (
        lambda Y: (
            lambda y: (
                # y if y.setxy(*map(int, Y.tostr(10).decode().split(' ')[-4:])) else None
                y if y.set(*(lambda u,v,t,w: (Fp2(Fp(u), Fp(v)), Fp2(Fp(t), Fp(w))) )(*map(int, Y.tostr(10).decode().split(' ')[-4:]))) else None
            ))(ECp2())
    )(q)


def ECp2_to_G2(y):
    # import bn254
    if y.isinf():
        return G2()#.fromstr(b"\x00"*64, 64)  # Note: bn254.ECp2().toBytes(1) == b'\x02' + b"\x00" * 64
    try:
        return G2().fromstr(
            ('1 ' + ' '.join(map(str, (lambda y1, y2: list(y1.get()) + list(y2.get()))(*y.get())))).encode(), 10
        )
    except ValueError:
        return None


def ECp_serialize(p):
    # import bn254
    if p.isinf():
        return b"\x00"*32  # bytes([0]*32)
    try:
        return (
                lambda p: bytes((lambda x, y: (lambda ps: (lambda ret,_: ret)(
                    ps, ps.append(ps.pop() ^ ((y%2)<<7)))
                                               )(list(x.to_bytes(32, 'little'))))(*p.get()))
        )(p)
    except ValueError:
        return None


def assert_compatible():
    for _ in range(128):
        X = G1().randomize()
        x = G1_to_ECp(X)

        assert ECp_to_G1(x) + ECp_to_G1(x) == ECp_to_G1(x.add(x))
        assert G1_to_ECp(X).add(G1_to_ECp(X)) == G1_to_ECp(X + X)
        assert G1_to_ECp(ECp_to_G1(x)) == x
        assert ECp_to_G1(G1_to_ECp(X)) == X
        assert G1_to_ECp(ECp_to_G1(x) + ECp_to_G1(x)) == x.add(x)
        assert G1_to_ECp(ECp_to_G1(x) + ECp_to_G1(x)) == x.dbl()
        assert ECp_to_G1(G1_to_ECp(X).add(G1_to_ECp(X))) == X + X
        assert ECp_to_G1(G1_to_ECp(X).add(G1_to_ECp(X))) == X.dbl()

        # print(x)
        # print(X)

        Y = G2().randomize()
        y = G2_to_ECp2(Y)

        assert ECp2_to_G2(y) + ECp2_to_G2(y) == ECp2_to_G2(y.add(y))
        assert G2_to_ECp2(Y).add(G2_to_ECp2(Y)) == G2_to_ECp2(Y + Y)
        assert G2_to_ECp2(ECp2_to_G2(y)) == y
        assert ECp2_to_G2(G2_to_ECp2(Y)) == Y
        assert G2_to_ECp2(ECp2_to_G2(y) + ECp2_to_G2(y)) == y.add(y)
        assert G2_to_ECp2(ECp2_to_G2(y) + ECp2_to_G2(y)) == y.dbl()
        assert ECp2_to_G2(G2_to_ECp2(Y).add(G2_to_ECp2(Y))) == Y + Y
        assert ECp2_to_G2(G2_to_ECp2(Y).add(G2_to_ECp2(Y))) == Y.dbl()

        # print(y)
        # print(Y)

        x = G1_to_ECp(X)  # Note: Many `x._()` methods mutate `x`, such as `.add` and `.dbl` used above.
        assert G1().deserialize(ECp_serialize(x)) == X and X.serialize() == ECp_serialize(x)

    # Test infinity/zero conversions
    from bn254 import ECp, ECp2
    assert G1_to_ECp(ECp_to_G1(ECp())) == ECp()
    assert ECp_to_G1(G1_to_ECp(G1())) == G1()
    assert G2_to_ECp2(ECp2_to_G2(ECp2())) == ECp2()
    assert ECp2_to_G2(G2_to_ECp2(G2())) == G2()
    assert G1().deserialize(ECp_serialize(ECp())) == G1() and G1().serialize() == ECp_serialize(ECp())


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


assert_sane()
# assert_bilinearity()
# assert_serializable()
# assert_compatible()
