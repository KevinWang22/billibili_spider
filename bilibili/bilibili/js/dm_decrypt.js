/*变量r的代码*/
// Error函数
function error_s(t, e) {
    return RangeError("index out of range: " + t.pos + " + " + (e || 1) + " > " + t.len)
}

function Reader(t) {
    this.buf = t,
    this.pos = 0,
    this.len = t.length
}
function Reader_d(t, e) {
    return (t[e - 4] | t[e - 3] << 8 | t[e - 2] << 16 | t[e - 1] << 24) >>> 0
}
function readFloatLE(t, n) {
    var e = new Float32Array([-0])
    , i = new Uint8Array(e.buffer)
    return i[0] = t[n],
    i[1] = t[n + 1],
    i[2] = t[n + 2],
    i[3] = t[n + 3],
    e[0]
}
function readDoubleLE(t, n) {
    var e = new Float64Array([-0])
    , i = new Uint8Array(e.buffer)
    return i[0] = t[n],
    i[1] = t[n + 1],
    i[2] = t[n + 2],
    i[3] = t[n + 3],
    i[4] = t[n + 4],
    i[5] = t[n + 5],
    i[6] = t[n + 6],
    i[7] = t[n + 7],
    e[0]
}
function o_read(t, e, i) {
    if (i - e < 1)
        return "";
    for (var n, r = null, a = [], o = 0; e < i; )
        (n = t[e++]) < 128 ? a[o++] = n : n > 191 && n < 224 ? a[o++] = (31 & n) << 6 | 63 & t[e++] : n > 239 && n < 365 ? (n = ((7 & n) << 18 | (63 & t[e++]) << 12 | (63 & t[e++]) << 6 | 63 & t[e++]) - 65536,
        a[o++] = 55296 + (n >> 10),
        a[o++] = 56320 + (1023 & n)) : a[o++] = (15 & n) << 12 | (63 & t[e++]) << 6 | 63 & t[e++],
        o > 8191 && ((r || (r = [])).push(String.fromCharCode.apply(String, a)),
        o = 0);
    return r ? (o && r.push(String.fromCharCode.apply(String, a.slice(0, o))),
    r.join("")) : String.fromCharCode.apply(String, a.slice(0, o))
}
function r_merge(t, e, i) {
    for (var n = Object.keys(e), r = 0; r < n.length; ++r)
        void 0 !== t[n[r]] && i || (t[n[r]] = e[n[r]]);
    return t
}
Reader.prototype._slice = Uint8Array.prototype.subarray,
Reader.prototype.uint32 = (l = 4294967295,
function() {
    if (l = (127 & this.buf[this.pos]) >>> 0,
    this.buf[this.pos++] < 128)
        return l;
    if (l = (l | (127 & this.buf[this.pos]) << 7) >>> 0,
    this.buf[this.pos++] < 128)
        return l;
    if (l = (l | (127 & this.buf[this.pos]) << 14) >>> 0,
    this.buf[this.pos++] < 128)
        return l;
    if (l = (l | (127 & this.buf[this.pos]) << 21) >>> 0,
    this.buf[this.pos++] < 128)
        return l;
    if (l = (l | (15 & this.buf[this.pos]) << 28) >>> 0,
    this.buf[this.pos++] < 128)
        return l;
    if ((this.pos += 5) > this.len)
        throw this.pos = this.len,
        error_s(this, 10);
    return l
}
),
Reader.prototype.int32 = function() {
    return 0 | this.uint32()
}
,
Reader.prototype.sint32 = function() {
    var t = this.uint32();
    return t >>> 1 ^ -(1 & t) | 0
}
,
Reader.prototype.bool = function() {
    return 0 !== this.uint32()
}
,
Reader.prototype.fixed32 = function() {
    if (this.pos + 4 > this.len)
        throw error_s(this, 4);
    return Reader_d(this.buf, this.pos += 4)
}
,
Reader.prototype.sfixed32 = function() {
    if (this.pos + 4 > this.len)
        throw error_s(this, 4);
    return 0 | Reader_d(this.buf, this.pos += 4)
}
,
Reader.prototype.float = function() {
    if (this.pos + 4 > this.len)
        throw error_s(this, 4);
    var t = readFloatLE(this.buf, this.pos);
    return this.pos += 4,
    t
}
,
Reader.prototype.double = function() {
    if (this.pos + 8 > this.len)
        throw error_s(this, 4);
    var t = readDoubleLE(this.buf, this.pos);
    return this.pos += 8,
    t
}
,
Reader.prototype.bytes = function() {
    var t = this.uint32()
      , e = this.pos
      , i = this.pos + t;
    if (i > this.len)
        throw error_s(this, t);
    return this.pos += t,
    Array.isArray(this.buf) ? this.buf.slice(e, i) : e === i ? new this.buf.constructor(0) : this._slice.call(this.buf, e, i)
}
,
Reader.prototype.string = function() {
    var t = this.bytes();
    return o_read(t, 0, t.length)
}
,
Reader.prototype.skip = function(t) {
    if ("number" == typeof t) {
        if (this.pos + t > this.len)
            throw error_s(this, t);
        this.pos += t
    } else
        do {
            if (this.pos >= this.len)
                throw error_s(this)
        } while (128 & this.buf[this.pos++]);return this
}
,
Reader.prototype.skipType = function(t) {
    switch (t) {
    case 0:
        this.skip();
        break;
    case 1:
        this.skip(8);
        break;
    case 2:
        this.skip(this.uint32());
        break;
    case 3:
        for (; 4 != (t = 7 & this.uint32()); )
            this.skipType(t);
        break;
    case 5:
        this.skip(4);
        break;
    default:
        throw Error("invalid wire type " + t + " at offset " + this.pos)
    }
    return this
}
,
Reader.prototype.int64 = function() {
    return reader_u.call(this)["toNumber"](!1)
},
Reader.prototype.uint64 = function() {
    return reader_u.call(this)["toNumber"](!0)
},
Reader.prototype.sint64 = function() {
    return reader_u.call(this).zzDecode()["toNumber"](!1)
},
Reader.prototype.fixed64 = function() {
    return p.call(this)["toNumber"](!0)
},
Reader.prototype.sfixed64 = function() {
    return p.call(this)["toNumber"](!1)
}


function u_a(t, e) {
    this.lo = t >>> 0,
    this.hi = e >>> 0
}
var a = u_a.zero = new u_a(0,0);
a.toNumber = function() {
    return 0
}
,
a.zzEncode = a.zzDecode = function() {
    return this
}
,
a.length = function() {
    return 1
}
;
var o = u_a.zeroHash = "\0\0\0\0\0\0\0\0";
u_a.fromNumber = function(t) {
    if (0 === t)
        return a;
    var e = t < 0;
    e && (t = -t);
    var i = t >>> 0
      , n = (t - i) / 4294967296 >>> 0;
    return e && (n = ~n >>> 0,
    i = ~i >>> 0,
    ++i > 4294967295 && (i = 0,
    ++n > 4294967295 && (n = 0))),
    new u_a(i,n)
}
,
// 没有用的
u_a.from = function(t) {
    if ("number" == typeof t)
        return u_a.fromNumber(t);
    if (n.isString(t)) {
        if (!n.Long)
            return u_a.fromNumber(parseInt(t, 10));
        t = n.Long.fromString(t)
    }
    return t.low || t.high ? new u_a(t.low >>> 0,t.high >>> 0) : a
}
,
u_a.prototype.toNumber = function(t) {
    if (!t && this.hi >>> 31) {
        var e = 1 + ~this.lo >>> 0
          , i = ~this.hi >>> 0;
        return e || (i = i + 1 >>> 0),
        -(e + 4294967296 * i)
    }
    return this.lo + 4294967296 * this.hi
}
,
// 没有用的
u_a.prototype.toLong = function(t) {
    return n.Long ? new n.Long(0 | this.lo,0 | this.hi,Boolean(t)) : {
        low: 0 | this.lo,
        high: 0 | this.hi,
        unsigned: Boolean(t)
    }
}
;
var s = String.prototype.charCodeAt;
u_a.fromHash = function(t) {
    return t === o ? a : new u_a((s.call(t, 0) | s.call(t, 1) << 8 | s.call(t, 2) << 16 | s.call(t, 3) << 24) >>> 0,(s.call(t, 4) | s.call(t, 5) << 8 | s.call(t, 6) << 16 | s.call(t, 7) << 24) >>> 0)
}
,
u_a.prototype.toHash = function() {
    return String.fromCharCode(255 & this.lo, this.lo >>> 8 & 255, this.lo >>> 16 & 255, this.lo >>> 24, 255 & this.hi, this.hi >>> 8 & 255, this.hi >>> 16 & 255, this.hi >>> 24)
}
,
u_a.prototype.zzEncode = function() {
    var t = this.hi >> 31;
    return this.hi = ((this.hi << 1 | this.lo >>> 31) ^ t) >>> 0,
    this.lo = (this.lo << 1 ^ t) >>> 0,
    this
}
,
u_a.prototype.zzDecode = function() {
    var t = -(1 & this.lo);
    return this.lo = ((this.lo >>> 1 | this.hi << 31) ^ t) >>> 0,
    this.hi = (this.hi >>> 1 ^ t) >>> 0,
    this
}
,
u_a.prototype.length = function() {
    var t = this.lo
      , e = (this.lo >>> 28 | this.hi << 4) >>> 0
      , i = this.hi >>> 24;
    return 0 === i ? 0 === e ? t < 16384 ? t < 128 ? 1 : 2 : t < 2097152 ? 3 : 4 : e < 16384 ? e < 128 ? 5 : 6 : e < 2097152 ? 7 : 8 : i < 128 ? 9 : 10
}

function reader_u() {
        var t = new u_a(0,0)
          , e = 0;
        if (!(this.len - this.pos > 4)) {
            for (; e < 3; ++e) {
                if (this.pos >= this.len)
                    throw error_s(this);
                if (t.lo = (t.lo | (127 & this.buf[this.pos]) << 7 * e) >>> 0,
                this.buf[this.pos++] < 128)
                    return t
            }
            return t.lo = (t.lo | (127 & this.buf[this.pos++]) << 7 * e) >>> 0,
            t
        }
        for (; e < 4; ++e)
            if (t.lo = (t.lo | (127 & this.buf[this.pos]) << 7 * e) >>> 0,
            this.buf[this.pos++] < 128)
                return t;
        if (t.lo = (t.lo | (127 & this.buf[this.pos]) << 28) >>> 0,
        t.hi = (t.hi | (127 & this.buf[this.pos]) >> 4) >>> 0,
        this.buf[this.pos++] < 128)
            return t;
        if (e = 0,
        this.len - this.pos > 4) {
            for (; e < 5; ++e)
                if (t.hi = (t.hi | (127 & this.buf[this.pos]) << 7 * e + 3) >>> 0,
                this.buf[this.pos++] < 128)
                    return t
        } else
            for (; e < 5; ++e) {
                if (this.pos >= this.len)
                    throw error_s(this);
                if (t.hi = (t.hi | (127 & this.buf[this.pos]) << 7 * e + 3) >>> 0,
                this.buf[this.pos++] < 128)
                    return t
            }
        throw Error("invalid varint encoding")
    }


// DmSegMobileReply$decode.types[0].decode(r,r.uint32())
function DanmakuElem$decode(r,l){
  if(!(r instanceof Reader))
  r=Reader.create(r)
  var c=l===undefined?r.len:r.pos+l,m=new function DanmakuElem(p){
                                              if(p)for(var ks=Object.keys(p),i=0;i<ks.length;++i)if(p[ks[i]]!=null)
                                              this[ks[i]]=p[ks[i]]
                                            }
  while(r.pos<c){
  var t=r.uint32()
  switch(t>>>3){
  case 1:
  m.id=r.int64()
  break
  case 2:
  m.progress=r.int32()
  break
  case 3:
  m.mode=r.int32()
  break
  case 4:
  m.fontsize=r.int32()
  break
  case 5:
  m.color=r.uint32()
  break
  case 6:
  m.midHash=r.string()
  break
  case 7:
  m.content=r.string()
  break
  case 8:
  m.ctime=r.int64()
  break
  case 9:
  m.weight=r.int32()
  break
  case 10:
  m.action=r.string()
  break
  case 11:
  m.pool=r.int32()
  break
  case 12:
  m.idStr=r.string()
  break
  case 13:
  m.attr=r.int32()
  break
  default:
  r.skipType(t&7)
  break
  }
  }
  return m
}

// a.protoMessage[t].decode(new Uint8Array(i.data))
function DmSegMobileReply$decode(r,l){
  if(!(r instanceof Reader))
  r=new Reader(r)
  var c=l===undefined?r.len:r.pos+l,m=new function DmSegMobileReply(p){
                                              this.elems=[]
                                              if(p)for(var ks=Object.keys(p),i=0;i<ks.length;++i)if(p[ks[i]]!=null)
                                              this[ks[i]]=p[ks[i]]
                                            }
  while(r.pos<c){
  var t=r.uint32()
  switch(t>>>3){
  case 1:
  if(!(m.elems&&m.elems.length))
  m.elems=[]
  m.elems.push(DanmakuElem$decode(r,r.uint32()))
  break
  default:
  r.skipType(t&7)
  break
  }
  }
  return m
}

/*以下是参数n的代码*/

// types[0].toObject()
function DanmakuElem$toObject(m,o){
  if(!o)
  o={}
  var d={}
  if(o.defaults){
  d.id=0
  d.progress=0
  d.mode=0
  d.fontsize=0
  d.color=0
  d.midHash=""
  d.content=""
  d.ctime=0
  d.weight=0
  d.action=""
  d.pool=0
  d.idStr=""
  d.attr=0
  }
  if(m.id!=null&&m.hasOwnProperty("id")){
  if(typeof m.id==="number")
  d.id=o.longs===String?String(m.id):m.id
  else
  d.id=o.longs===String?util.Long.prototype.toString.call(m.id):o.longs===Number?new util.LongBits(m.id.low>>>0,m.id.high>>>0).toNumber():m.id
  }
  if(m.progress!=null&&m.hasOwnProperty("progress")){
  d.progress=m.progress
  }
  if(m.mode!=null&&m.hasOwnProperty("mode")){
  d.mode=m.mode
  }
  if(m.fontsize!=null&&m.hasOwnProperty("fontsize")){
  d.fontsize=m.fontsize
  }
  if(m.color!=null&&m.hasOwnProperty("color")){
  d.color=m.color
  }
  if(m.midHash!=null&&m.hasOwnProperty("midHash")){
  d.midHash=m.midHash
  }
  if(m.content!=null&&m.hasOwnProperty("content")){
  d.content=m.content
  }
  if(m.ctime!=null&&m.hasOwnProperty("ctime")){
  if(typeof m.ctime==="number")
  d.ctime=o.longs===String?String(m.ctime):m.ctime
  else
  d.ctime=o.longs===String?util.Long.prototype.toString.call(m.ctime):o.longs===Number?new util.LongBits(m.ctime.low>>>0,m.ctime.high>>>0).toNumber():m.ctime
  }
  if(m.weight!=null&&m.hasOwnProperty("weight")){
  d.weight=m.weight
  }
  if(m.action!=null&&m.hasOwnProperty("action")){
  d.action=m.action
  }
  if(m.pool!=null&&m.hasOwnProperty("pool")){
  d.pool=m.pool
  }
  if(m.idStr!=null&&m.hasOwnProperty("idStr")){
  d.idStr=m.idStr
  }
  if(m.attr!=null&&m.hasOwnProperty("attr")){
  d.attr=m.attr
  }
  return d
}

// a.protoMessage[t].toObject()
function DmSegMobileReply$toObject(m,o){
  if(!o)
  o={}
  var d={}
  if(o.arrays||o.defaults){
  d.elems=[]
  }
  if(m.elems&&m.elems.length){
  d.elems=[]
  for(var j=0;j<m.elems.length;++j){
  d.elems[j]=DanmakuElem$toObject(m.elems[j],o)
  }
  }
  return d
}

function dataDecodeMain(i) {
    let r = DmSegMobileReply$decode(new Uint8Array(i))
    let n = DmSegMobileReply$toObject(r);
    return n
}

module.exports = {
    dataDecodeMain
}
