from ctypes import Structure, c_uint64, cdll, c_char_p, create_string_buffer
from hashlib import blake2b
import platform
import pkg_resources

if platform.system() == 'Windows':
    lib_name = "libmclbn256.dll"
else:
    lib_name = "libmclbn256.so"
lib_path = pkg_resources.resource_filename('mclbn256', lib_name)

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
def __init():
    global lib
    lib = cdll.LoadLibrary(lib_path)
    if lib.mclBn_init(mclBn_CurveFp254BNb, MCLBN_COMPILED_TIME_VAR): print("Failed to load MCl's BN254 binary.")
__init()

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

    def setStr(self, s, io_mode=16):
        ret = lib.mclBnFr_setStr(self.d, c_char_p(s), len(s), io_mode)
        if ret:
            raise ValueError("MCl failed to return from Fr:setStr")
    def setRnd(self):
        lib.mclBnFr_setByCSPRNG(self.d)

    def randomize(self):
        self.setRnd()
        return self

    def tostr(self, io_mode=16):
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
        svLen = 1024
        sv = create_string_buffer(b"\x00" * svLen)
        ret = lib.mclBnFr_getStr(sv, svLen, self.d, io_mode)
        if ret == 0:
            print(("MCl failed to return from Fr:getStr, ioMode=" + str(io_mode)))
            # raise ValueError("MCl failed to return from Fr:getStr, ioMode=" + str(io_mode))
        return sv.value

    def serialize(self):
        svLen = 1024
        sv = create_string_buffer(b"\x00" * svLen)
        ret = lib.mclBnFr_serialize(sv, svLen, self.d)
        if ret == 0:
            raise ValueError("MCl failed to return from GT:serialize")
        return sv.value

    def deserialize(self, s):
        svLen = 1024
        sv = create_string_buffer(s)
        ret = lib.mclBnFr_deserialize(self.d, sv, svLen)
        if ret == 0:
            raise ValueError("MCl failed to return from GT:deserialize")
        return self

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

class Fp6Array(Structure):
    # _fields_ = [("d", 2 * mclBnGT_bytes)]  # I think Q_coeff precomputed G2 pairing may be made of two mclBnGT types
    # _fields_ = [("d", mclBnG2_bytes)]
    # _fields_ = [("d", c_uint64 * 1680)]
    _fields_ = [("d", mclBnFp_bytes * 6 * precomputedQcoeffSize)]
    def __bytes__(self):
        return bytes(self.d)
    def __str__(self):
        return self.tostr().decode()

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

    def tostr(self, io_mode=16):
        """
        # define MCLBN_IO_EC_AFFINE 0
        # define MCLBN_IO_BINARY 2
        # define MCLBN_IO_DECIMAL 10
        # define MCLBN_IO_HEX_BIG_ENDIAN 16
        # define MCLBN_IO_0xHEX_LITTLE_ENDIAN 144
        # define MCLBN_IO_EC_PROJ 1024  // Jacobi coordinate for G1/G2
        # define MCLBN_IO_SERIALIZE_HEX_STR 2048
        """
        svLen = 1024
        sv = create_string_buffer(b"\x00" * svLen)
        ret = lib.mclBnFr_getStr(sv, svLen, self.d, io_mode)


        # for i in range(0, 5000):
        #     sv = create_string_buffer(b"\x00" * svLen)
        #     print(i, "{0:b}".format(i), lib.mclBnFr_getStr(sv, svLen, self.d, i), sv.value)


        if ret == 0:
            raise ValueError("MCl failed to return from GT:getStr, ioMode=" + str(io_mode))
        return sv.value

    def serialize(self):
        svLen = 1024
        sv = create_string_buffer(b"\x00" * svLen)
        ret = lib.mclBnGT_serialize(sv, svLen, self.d)
        if ret == 0:
            raise ValueError("MCl failed to return from GT:serialize")
        return sv.value

    def deserialize(self, s):
        svLen = 1024
        sv = create_string_buffer(s)
        ret = lib.mclBnGT_deserialize(self.d, sv, svLen)
        if ret == 0:
            raise ValueError("MCl failed to return from GT:deserialize")
        return self

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

    def tostr(self, io_mode=16):
        """
        # define MCLBN_IO_EC_AFFINE 0
        # define MCLBN_IO_BINARY 2
        # define MCLBN_IO_DECIMAL 10
        # define MCLBN_IO_HEX_BIG_ENDIAN 16
        # define MCLBN_IO_0xHEX_LITTLE_ENDIAN 144
        # define MCLBN_IO_EC_PROJ 1024  // Jacobi coordinate for G1/G2
        # define MCLBN_IO_SERIALIZE_HEX_STR 2048
        """
        svLen = 1024
        sv = create_string_buffer(b"\x00" * svLen)
        ret = lib.mclBnFr_getStr(sv, svLen, self.d, io_mode)


        # for i in range(0, 5000):
        #     sv = create_string_buffer(b"\x00" * svLen)
        #     print(i, "{0:b}".format(i), lib.mclBnFr_getStr(sv, svLen, self.d, i), sv.value)


        if ret == 0:
            raise ValueError("MCl failed to return from G1:getStr, ioMode=" + str(io_mode))
        return sv.value

    def serialize(self):
        svLen = 1024
        sv = create_string_buffer(b"\x00" * svLen)
        ret = lib.mclBnG1_serialize(sv, svLen, self.d)
        if ret == 0:
            raise ValueError("MCl failed to return from G1:serialize")
        return sv.value

    def deserialize(self, s):
        svLen = 1024
        sv = create_string_buffer(s)
        ret = lib.mclBnG1_deserialize(self.d, sv, svLen)
        if ret == 0:
            raise ValueError("MCl failed to return from G1:deserialize")
        return self

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

    def tostr(self, io_mode=16):
        """
        # define MCLBN_IO_EC_AFFINE 0
        # define MCLBN_IO_BINARY 2
        # define MCLBN_IO_DECIMAL 10
        # define MCLBN_IO_HEX_BIG_ENDIAN 16
        # define MCLBN_IO_0xHEX_LITTLE_ENDIAN 144
        # define MCLBN_IO_EC_PROJ 1024  // Jacobi coordinate for G1/G2
        # define MCLBN_IO_SERIALIZE_HEX_STR 2048
        """
        svLen = 1024
        sv = create_string_buffer(b"\x00" * svLen)
        ret = lib.mclBnFr_getStr(sv, svLen, self.d, io_mode)


        # for i in range(0, 5000):
        #     sv = create_string_buffer(b"\x00" * svLen)
        #     print(i, "{0:b}".format(i), lib.mclBnFr_getStr(sv, svLen, self.d, i), sv.value)


        if ret == 0:
            print("MCl failed to return from G2:getStr, ioMode=" + str(io_mode))
            # raise ValueError("MCl failed to return from G2:getStr, ioMode=" + str(io_mode))
        return sv.value

    def serialize(self):
        svLen = 1024
        sv = create_string_buffer(b"\x00" * svLen)
        ret = lib.mclBnG2_serialize(sv, svLen, self.d)
        if ret == 0:
            raise ValueError("MCl failed to return from G2:serialize")
        return sv.value

    def deserialize(self, s):
        svLen = 1024
        sv = create_string_buffer(s)
        ret = lib.mclBnG2_deserialize(self.d, sv, svLen)
        if ret == 0:
            raise ValueError("MCl failed to return from G2:deserialize")
        return self

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
        #print([e[0] for e in enumerate(list(z)) if e[1] == 0][0:10])
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



def big_test():


    # print("init")
    # mclBn_init()
    # print("init'd")

    P = Fr()
    Q = Fr()
    P.setRnd()
    Q.setInt(7)
    # Q.setStr("34982034824")
    R = P + Q
    S = Q + P
    assert(R == S)



    # p = (c_uint64 * 4) * 3
    # lib.mclBnG1_getBasePoint(p)







    g = G1()
    g.hash("Hello, World")
    print(g.tostr())

    p = G1()
    p.hash("Hello, Wyatt John Howe")
    print(p.tostr())

    q = G1()
    print(g.equals(q))
    is_zero = q.zero()
    print("This point is" + ("" if is_zero else " not") + " zero.")
    q.hash("Hello, World")


    # print(5)
    # lib.mclBnG1_isValid(q)
    # is_valid = q.valid()
    # print(6)
    # print("This point is valid." if is_valid else "invalid!")
    q.print_valid()

    is_zero = q.zero()
    print("This point is" + ("" if is_zero else " not") + " zero.")


    print(g.equals(p))
    print(g.equals(q))



    # print(bytes(g.mul(p).add(p).sub(p).sub(p))[20:40])
    # print(bytes(p.mul(g).sub(p))[20:40])


    print(g.add(p).sub(p).sub(p).serialize())
    print(g.sub(p).serialize())


    print("g", g.serialize())

    print("g", g.deserialize(g.serialize()))

    print("g", g.deserialize(g.serialize()).serialize())
    # print("g", p.deserialize(g.serialize()).serialize())
    print("p", g.deserialize(p.serialize()).serialize())

    print("\n\n\n\n\n")





    s = Fr(); s.setRnd()
    t = Fr(); t.setInt(7)


    print(g.mul(s).mul(t).serialize())
    print(g.mul(t).mul(s).serialize())
    print(g.mul(t).mul(t).serialize())
    print(g.mul(s).mul(s).serialize())




    # r = G1().randomize()
    # r.print_valid()
    # print(bytes(r.serialize()))



    r1 = G1().randomize()
    r1.print_valid()
    print(bytes(r1.serialize()))

    r2 = G1().randomize()
    r2.print_valid()
    print(bytes(r2.serialize()))

    print(r1.equals(r1))
    print(r2.equals(r2))
    print(r1.equals(r2))
    print(r2.equals(r1))


    print(
        r1.mul(s).mul(t).equals(
            r1.mul(t).mul(s)
        )
    )




    ###################################################




    # print("init")
    # mclBn_init()
    # print("init'd")

    P = Fr()
    Q = Fr()
    P.setRnd()
    Q.setInt(7)
    # Q.setStr("34982034824")
    R = P + Q
    S = Q + P
    assert(R == S)



    # p = (c_uint64 * 4) * 3
    # lib.mclBnG2_getBasePoint(p)






    g = G2()
    print("1")
    g.hash("Hello, World")
    print("2")

    p = G2()
    print("3")
    p.hash("Hello, Wyatt")
    print("4")

    q = G2()
    print("4")
    print(g.equals(q))
    print("4")
    is_zero = q.zero()
    print("This point is" + ("" if is_zero else " not") + " zero.")
    q.hash("Hello, World")


    # print(5)
    # lib.mclBnG2_isValid(q)
    # is_valid = q.valid()
    # print(6)
    # print("This point is valid." if is_valid else "invalid!")
    q.print_valid()

    is_zero = q.zero()
    print("This point is" + ("" if is_zero else " not") + " zero.")


    print(g.equals(p))
    print(g.equals(q))



    # print(bytes(g.mul(p).add(p).sub(p).sub(p))[20:40])
    # print(bytes(p.mul(g).sub(p))[20:40])


    print(g.add(p).sub(p).sub(p).serialize())
    print(g.sub(p).serialize())


    print("g", g.serialize())

    print("g", g.deserialize(g.serialize()))

    print("g", g.deserialize(g.serialize()).serialize())
    # print("g", p.deserialize(g.serialize()).serialize())
    print("p", g.deserialize(p.serialize()).serialize())

    print("\n\n\n\n\n")





    s = Fr(); s.setRnd()
    # s = Fr(); s.setInt(7)
    t = Fr(); t.setInt(7)
    # s.tostr()

    print(g.mul(s).mul(t).serialize())
    print(g.mul(t).mul(s).serialize())
    print(g.mul(t).mul(t).serialize())
    print(g.mul(s).mul(s).serialize())




    # r = G2().randomize()
    # r.print_valid()
    # print(bytes(r.serialize()))



    r1 = G2().randomize()
    r1.print_valid()
    print(bytes(r1.serialize()))

    r2 = G2().randomize()
    r2.print_valid()
    print(bytes(r2.serialize()))

    print(r1.equals(r1))
    print(r2.equals(r2))
    print(r1.equals(r2))
    print(r2.equals(r1))


    print(
        r1.mul(s).mul(t).equals(
            r1.mul(t).mul(s)
        )
    )



    print("\n\n\n\n\n")
    ###################################################



    r1 = G1().randomize()
    r1.print_valid()
    print(bytes(r1.serialize()));print()


    r2 = G2().randomize()
    r2.print_valid()
    print(bytes(r2.serialize()));print()


    r3 = r1.pairing(r2)
    print(bytes(r3.serialize()));print()


    r4 = r2.pairing(r1)
    print(bytes(r4.serialize()));print()

    print(r3.equals(r4))


    r5 = r1.mul(s).pairing(r2)
    print(bytes(r5.serialize()));print()


    r6 = r1.pairing(r2.mul(s))
    print(bytes(r6.serialize()));print()


    print(r5.equals(r6))
    # print(
    #     (r1.pairing(r2.mul(s))), (
    #     ((r1.mul(s)).pairing(r2))
    # ))





    for _ in range(1,10):
        pass




    # bytes(P)
    # print(bytes(g))
    # print(bytes(p))
    # print(bytes(q))





























def test_pairing_algebra():
    a = Fr()
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

    return True  # print("pass")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    big_test()

    # # print_('testing')
    #
    # for _ in range(99):
    #     test_pairing_algebra()
    #
    # test_pairing_preeoptimization()



    import timeit

    P = G1().hash("Pp")
    Q = G2().hash("Qq")
    count = 10000
    start_time = timeit.default_timer()

    e = P @ Q
    for _ in range(count):
        e = e + P @ Q
        # le = Q @ P
        # re = P @ Q
        # print(bytes(le))
        # print(bytes(re))
        # print(le == re)

    elapsed = timeit.default_timer() - start_time
    elapsed_avg = elapsed/count
    print(bytes(e))
    print(elapsed, "seconds elapsed")
    print(str(round(1000*elapsed_avg, 2))+"ms per operation")
    print()


    P = G1().hash("pP")
    Q = G2().hash("qQ")
    count = 10000
    start_time = timeit.default_timer()

    e = P @ Q
    for _ in range(count):
        e = e + Q @ P
        # le = Q @ P
        # re = P @ Q
        # print(bytes(le))
        # print(bytes(re))
        # print(le == re)

    elapsed = timeit.default_timer() - start_time
    elapsed_avg = elapsed/count
    print(bytes(e))
    print(elapsed, "seconds elapsed")
    print(str(round(1000*elapsed_avg, 2))+"ms per operation")
    print()

    disable_memoization()


    P = G1().hash("pp")
    Q = G2().hash("qq")
    count = 10000
    start_time = timeit.default_timer()

    e = P @ Q
    for _ in range(count):
        e = e + P @ Q
        # le = Q @ P
        # re = P @ Q
        # print(bytes(le))
        # print(bytes(re))
        # print(le == re)

    elapsed = timeit.default_timer() - start_time
    elapsed_avg = elapsed/count
    print(bytes(e))
    print(elapsed, "seconds elapsed")
    print(str(round(1000*elapsed_avg, 2))+"ms per operation")
    print()


    P = G1().hash("PP")
    Q = G2().hash("QQ")
    count = 10000
    start_time = timeit.default_timer()

    e = P @ Q
    for _ in range(count):
        e = e + Q @ P
        # le = Q @ P
        # re = P @ Q
        # print(bytes(le))
        # print(bytes(re))
        # print(le == re)

    elapsed = timeit.default_timer() - start_time
    elapsed_avg = elapsed/count
    print(bytes(e))
    print(elapsed, "seconds elapsed")
    print(str(round(1000*elapsed_avg, 2))+"ms per operation")
    print()


assert(test_pairing_algebra())  # Does not return on fail.  Vacuous assert.
