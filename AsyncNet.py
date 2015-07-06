#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# AsyncNet.py - QuickNet �ӿ�
#
# NOTE:
# for more information, please see the readme file.
#
#======================================================================
import sys, time, os, struct
import ctypes
import socket

from ctypes import c_int, c_char, c_char_p, c_void_p, c_size_t, c_ulong
from ctypes import byref, c_long
c_intptr = c_size_t


#----------------------------------------------------------------------
# loading module
#----------------------------------------------------------------------
_HOME = os.environ.get('CHOME', os.path.abspath('.'))	# CANNON Ŀ¼
_HOME = os.path.abspath(_HOME)

def _loadlib (fn):
	try: _dl = ctypes.cdll.LoadLibrary(fn)
	except: return None
	return _dl

_unix = sys.platform[:3] != 'win' and True or False
_fdir = os.path.abspath(os.path.split(__file__)[0])
_search = [ _fdir, _HOME, '.', os.path.join(_HOME, 'bin'), './', '../bin' ]
_names = []
_names.append('AsyncNet.' + sys.platform)

_asndll = None
_dllname = ''

for root in _search:
	_path = os.path.abspath(root)
	for _fn in _names:
		_nm = os.path.abspath(os.path.join(_path, _fn))
		_dl = _loadlib(_nm)
		if not _dl: continue
		try: _test = _dl.asn_core_new
		except: continue
		_asndll = _dl
		_dllname = _nm
		break
	if _asndll:
		break

if _asndll == None:
	print 'can not load dynamic library AsyncNet'
	sys.exit(1)

GMASK = int(os.environ.get('CGMASK', '-1'))

CFFI_ENABLE = False

try:
	import cffi
	CFFI_ENABLE = True
except:
	pass

#----------------------------------------------------------------------
# cffi interface
#----------------------------------------------------------------------
if CFFI_ENABLE:
	ffi = cffi.FFI()
	ffi.cdef('''
	void asn_core_wait(size_t core, unsigned long millisec);
	void asn_core_notify(size_t core);
	long asn_core_read(size_t core, int *event, long *wparam, long *lparam, void *data, long size);
	long asn_core_send(size_t core, long hid, const void *ptr, long len);
	long asn_core_send_mask(size_t core, long hid, const void *ptr, long len, int mask);
	int asn_core_close(size_t core, long hid, int code);

	void asn_notify_wait(size_t notify, unsigned long millisec);
	void asn_notify_wake(size_t notify);
	long asn_notify_read(size_t notify, int *event, long *wparam, long *lparam, void *data, long maxsize);
	int asn_notify_send(size_t notify, int sid, short cmd, const void *data, long size);
	int asn_notify_close(size_t notify, int sid, int mode, int code);
	''')

	try:
		DLL = ffi.dlopen(_dllname)
	except:
		DLL = None
		CFFI_ENABLE = False

if CFFI_ENABLE:
	_cffi_asn_core_wait = DLL.asn_core_wait
	_cffi_asn_core_notify = DLL.asn_core_notify
	_cffi_asn_core_read = DLL.asn_core_read
	_cffi_asn_core_send = DLL.asn_core_send
	_cffi_asn_core_send_mask = DLL.asn_core_send_mask
	_cffi_asn_core_close = DLL.asn_core_close
	
	_cffi_asn_notify_wait = DLL.asn_notify_wait
	_cffi_asn_notify_wake = DLL.asn_notify_wake
	_cffi_asn_notify_read = DLL.asn_notify_read
	_cffi_asn_notify_send = DLL.asn_notify_send


#----------------------------------------------------------------------
# port interface
#----------------------------------------------------------------------
_asn_core_new = _asndll.asn_core_new
_asn_core_delete = _asndll.asn_core_delete
_asn_core_wait = _asndll.asn_core_wait
_asn_core_notify = _asndll.asn_core_notify
_asn_core_read = _asndll.asn_core_read
_asn_core_send = _asndll.asn_core_send
_asn_core_close = _asndll.asn_core_close
_asn_core_send_mask = _asndll.asn_core_send_mask
_asn_core_send_vector = _asndll.asn_core_send_vector
_asn_core_new_connect = _asndll.asn_core_new_connect
_asn_core_new_listen = _asndll.asn_core_new_listen
_asn_core_new_assign = _asndll.asn_core_new_assign
_asn_core_post = _asndll.asn_core_post
_asn_core_get_mode = _asndll.asn_core_get_mode
_asn_core_get_tag = _asndll.asn_core_get_tag
_asn_core_set_tag = _asndll.asn_core_set_tag
_asn_core_remain = _asndll.asn_core_remain
_asn_core_limit = _asndll.asn_core_limit
_asn_core_node_head = _asndll.asn_core_node_head
_asn_core_node_next = _asndll.asn_core_node_next
_asn_core_node_prev = _asndll.asn_core_node_prev
_asn_core_option = _asndll.asn_core_option
_asn_core_rc4_set_skey = _asndll.asn_core_rc4_set_skey
_asn_core_rc4_set_rkey = _asndll.asn_core_rc4_set_rkey
_asn_core_firewall = _asndll.asn_core_firewall
_asn_core_timeout = _asndll.asn_core_timeout
_asn_core_sockname = _asndll.asn_core_sockname
_asn_core_peername = _asndll.asn_core_peername
_asn_core_disable = _asndll.asn_core_disable

_asn_notify_new = _asndll.asn_notify_new
_asn_notify_delete = _asndll.asn_notify_delete
_asn_notify_wait = _asndll.asn_notify_wait
_asn_notify_wake = _asndll.asn_notify_wake
_asn_notify_read = _asndll.asn_notify_read
_asn_notify_listen = _asndll.asn_notify_listen
_asn_notify_remove = _asndll.asn_notify_remove
_asn_notify_change = _asndll.asn_notify_change
_asn_notify_send = _asndll.asn_notify_send
_asn_notify_close = _asndll.asn_notify_close
_asn_notify_get_port = _asndll.asn_notify_get_port
_asn_notify_allow_clear = _asndll.asn_notify_allow_clear
_asn_notify_allow_add = _asndll.asn_notify_allow_add
_asn_notify_allow_del = _asndll.asn_notify_allow_del
_asn_notify_allow_enable = _asndll.asn_notify_allow_enable
_asn_notify_sid_add = _asndll.asn_notify_sid_add
_asn_notify_sid_del = _asndll.asn_notify_sid_del
_asn_notify_sid_list = _asndll.asn_notify_sid_list
_asn_notify_sid_clear = _asndll.asn_notify_sid_clear
_asn_notify_option = _asndll.asn_notify_option
_asn_notify_token = _asndll.asn_notify_token
_asn_notify_trace = _asndll.asn_notify_trace

_asn_sock_new = _asndll.asn_sock_new
_asn_sock_delete = _asndll.asn_sock_delete
_asn_sock_connect = _asndll.asn_sock_connect
_asn_sock_assign = _asndll.asn_sock_assign
_asn_sock_close = _asndll.asn_sock_close
_asn_sock_state = _asndll.asn_sock_state
_asn_sock_fd = _asndll.asn_sock_fd
_asn_sock_remain = _asndll.asn_sock_remain
_asn_sock_send = _asndll.asn_sock_send
_asn_sock_recv = _asndll.asn_sock_recv
_asn_sock_send_vector = _asndll.asn_sock_send_vector
_asn_sock_recv_vector = _asndll.asn_sock_recv_vector
_asn_sock_process = _asndll.asn_sock_process
_asn_sock_rc4_set_skey = _asndll.asn_sock_rc4_set_skey
_asn_sock_rc4_set_rkey = _asndll.asn_sock_rc4_set_rkey
_asn_sock_nodelay = _asndll.asn_sock_nodelay
_asn_sock_sys_buffer = _asndll.asn_sock_sys_buffer
_asn_sock_keepalive = _asndll.asn_sock_keepalive


#----------------------------------------------------------------------
# prototypes
#----------------------------------------------------------------------
_asn_core_new.argtypes = []
_asn_core_new.restype = c_intptr
_asn_core_delete.argtypes = [ c_intptr ]
_asn_core_delete.restype = None
_asn_core_wait.argtypes = [ c_intptr, c_ulong ]
_asn_core_wait.restype = None
_asn_core_notify.argtypes = [ c_intptr ]
_asn_core_notify.restype = None
_asn_core_read.argtypes = [ c_intptr, c_void_p, c_void_p, c_void_p, c_char_p, c_long ]
_asn_core_read.restype = c_long
_asn_core_send.argtypes = [ c_intptr, c_long, c_char_p, c_long ]
_asn_core_send.restype = c_long
_asn_core_close.argtypes = [ c_intptr, c_long, c_int ]
_asn_core_close.restype = c_int
_asn_core_send_vector.argtypes = [ c_intptr, c_long, c_void_p, c_void_p, c_int, c_int ]
_asn_core_send_vector.restype = c_long
_asn_core_send_mask.argtypes = [ c_intptr, c_long, c_char_p, c_long, c_int ]
_asn_core_send_mask.restype = c_long
_asn_core_new_connect.argtypes = [ c_intptr, c_char_p, c_int, c_int ]
_asn_core_new_connect.restype = c_long
_asn_core_new_listen.argtypes = [ c_intptr, c_char_p, c_int, c_int ]
_asn_core_new_listen.restype = c_long
_asn_core_new_assign.argtypes = [ c_intptr, c_int, c_int, c_int ]
_asn_core_new_assign.restype = c_long
_asn_core_post.argtypes = [ c_intptr, c_long, c_long, c_void_p, c_long ]
_asn_core_post.restype = c_int
_asn_core_get_mode.argtypes = [ c_intptr, c_long ]
_asn_core_get_mode.restype = c_int
_asn_core_get_tag.argtypes = [ c_intptr, c_long ]
_asn_core_get_tag.restype = c_long
_asn_core_set_tag.argtypes = [ c_intptr, c_long, c_long ]
_asn_core_set_tag.restype = None
_asn_core_remain.argtypes = [ c_intptr, c_long ]
_asn_core_remain.restype = c_long
_asn_core_limit.argtypes = [ c_intptr, c_long, c_long ]
_asn_core_limit.restype = None
_asn_core_node_head.argtypes = [ c_intptr ]
_asn_core_node_head.restype = c_long
_asn_core_node_next.argtypes = [ c_intptr, c_long ]
_asn_core_node_next.restype = c_long
_asn_core_node_prev.argtypes = [ c_intptr, c_long ]
_asn_core_node_prev.restype = c_long
_asn_core_option.argtypes = [ c_intptr, c_long, c_int, c_long ]
_asn_core_option.restype = c_int
_asn_core_rc4_set_skey.argtypes = [ c_intptr, c_int, c_char_p, c_int ]
_asn_core_rc4_set_skey.restype = c_int
_asn_core_rc4_set_rkey.argtypes = [ c_intptr, c_int, c_char_p, c_int ]
_asn_core_rc4_set_rkey.restype = c_int
_asn_core_firewall.argtypes = [ c_intptr, c_void_p, c_void_p ]
_asn_core_firewall.restype = None
_asn_core_timeout.argtypes = [ c_intptr, c_int ]
_asn_core_timeout.restype = None
_asn_core_sockname.argtypes = [ c_intptr, c_long, c_char_p ]
_asn_core_sockname.restype = c_int
_asn_core_peername.argtypes = [ c_intptr, c_long, c_char_p ]
_asn_core_peername.restype = c_int
_asn_core_disable.argtypes = [ c_intptr, c_long, c_int ]
_asn_core_disable.restype = c_int

_asn_notify_new.argtypes = [ c_int ]
_asn_notify_new.restype = c_intptr
_asn_notify_delete.argtypes = [ c_intptr ]
_asn_notify_delete.restype = None
_asn_notify_wait.argtypes = [ c_intptr, c_long ]
_asn_notify_wait.restype = None
_asn_notify_wake.argtypes = [ c_intptr ]
_asn_notify_wake.restype = None
_asn_notify_read.argtypes = [ c_intptr, c_void_p, c_void_p, c_void_p, c_char_p, c_long ]
_asn_notify_read.restype = c_long
_asn_notify_listen.argtypes = [ c_intptr, c_char_p, c_int, c_int ]
_asn_notify_listen.restype = c_long
_asn_notify_remove.argtypes = [ c_intptr, c_long, c_int ]
_asn_notify_remove.restype = c_int
_asn_notify_change.argtypes = [ c_intptr, c_int ]
_asn_notify_change.restype = None
_asn_notify_send.argtypes = [ c_intptr, c_int, c_int, c_void_p, c_int ]
_asn_notify_send.restype = c_int
_asn_notify_close.argtypes = [ c_intptr, c_int, c_int, c_int ]
_asn_notify_close.restype = c_int
_asn_notify_get_port.argtypes = [ c_intptr, c_long ]
_asn_notify_get_port.restype = c_int
_asn_notify_allow_clear.argtypes = [ c_intptr ]
_asn_notify_allow_clear.restype = None
_asn_notify_allow_add.argtypes = [ c_intptr, c_char_p ]
_asn_notify_allow_add.restype = None
_asn_notify_allow_del.argtypes = [ c_intptr, c_char_p ]
_asn_notify_allow_del.restype = None
_asn_notify_allow_enable.argtypes = [ c_intptr, c_int ]
_asn_notify_allow_enable.restype = None
_asn_notify_sid_add.argtypes = [ c_intptr, c_int, c_char_p, c_int ]
_asn_notify_sid_add.restype = None
_asn_notify_sid_del.argtypes = [ c_intptr, c_int ] 
_asn_notify_sid_del.restype = None
_asn_notify_sid_list.argtypes = [ c_intptr, c_void_p, c_int ]
_asn_notify_sid_list.restype = c_int
_asn_notify_sid_clear.argtypes = [ c_intptr ]
_asn_notify_sid_clear.restype = None
_asn_notify_option.argtypes = [ c_intptr, c_int, c_long ]
_asn_notify_option.restype = c_int
_asn_notify_token.argtypes = [ c_intptr, c_char_p, c_int ]
_asn_notify_token.restype = None
_asn_notify_trace.argtypes = [ c_intptr, c_char_p, c_int, c_int ]
_asn_notify_trace.restype = None

_asn_sock_new.argtypes = []
_asn_sock_new.restype = c_intptr
_asn_sock_delete.argtypes = [ c_intptr ]
_asn_sock_delete.restype = None
_asn_sock_connect.argtypes = [ c_intptr, c_char_p, c_int, c_int ]
_asn_sock_connect.restype = c_int
_asn_sock_assign.argtypes = [ c_intptr, c_int, c_int ]
_asn_sock_assign.restype = c_int
_asn_sock_close.argtypes = [ c_intptr ]
_asn_sock_close.restype = None
_asn_sock_state.argtypes = [ c_intptr ]
_asn_sock_state.restype = c_int
_asn_sock_fd.argtypes = [ c_intptr ]
_asn_sock_fd.restype = c_int
_asn_sock_remain.argtypes = [ c_intptr ]
_asn_sock_remain.restype = c_long
_asn_sock_send.argtypes = [ c_intptr, c_char_p, c_long, c_int ]
_asn_sock_send.restype = c_long
_asn_sock_recv.argtypes = [ c_intptr, c_char_p, c_long ]
_asn_sock_recv.restype = c_long
_asn_sock_send_vector.argtypes = [ c_intptr, c_void_p, c_void_p, c_int, c_int ]
_asn_sock_send_vector.restype = c_long
_asn_sock_recv_vector.argtypes = [ c_intptr, c_void_p, c_void_p, c_int ]
_asn_sock_recv_vector.restype = c_long
_asn_sock_process.argtypes = [ c_intptr ]
_asn_sock_process.restype = None
_asn_sock_rc4_set_skey.argtypes = [ c_intptr, c_char_p, c_int ]
_asn_sock_rc4_set_skey.restype = None
_asn_sock_rc4_set_rkey.argtypes = [ c_intptr, c_char_p, c_int ]
_asn_sock_rc4_set_rkey.restype = None
_asn_sock_nodelay.argtypes = [ c_intptr, c_int ]
_asn_sock_nodelay.restype = c_int
_asn_sock_sys_buffer.argtypes = [ c_intptr, c_long, c_long ]
_asn_sock_sys_buffer.restype = c_int
_asn_sock_keepalive.argtypes = [ c_intptr, c_int, c_int, c_int ]
_asn_sock_keepalive.restype = c_int


#----------------------------------------------------------------------
# �첽��ܣ�
# �����������Լ�����ȥ���׽��ֲ��ҿ��Թ�����listen���׽��֣���hid
# �������Ҫ�½���һ�������׽��֣������ new_listen(ip, port, head)
# ��᷵�ؼ����׽��ֵ�hid���������յ������׽��ֵ� NEW��Ϣ��Ȼ�����
# �ü����˿����������������룬����յ��������ӵ� NEW��Ϣ��
# ���Ҫ����һ������ȥ�����ӣ������ new_connect(ip, port, head)������
# �����ӵ� hid�����ҽ������յ� NEW��Ϣ��������ӳɹ����һ���� ESTAB
# ��Ϣ�����򣬽����յ� LEAVE��Ϣ��
#----------------------------------------------------------------------

ASYNC_EVT_NEW   = 0		# �����ӣ�wp=hid, lp=-1(����),0(����),>0(����)
ASYNC_EVT_LEAVE = 1		# ���ӶϿ���wp=hid, lp=tag ���������Ͽ������յ�
ASYNC_EVT_ESTAB = 2		# ���ӽ�����wp=hid, lp=tag ����������ȥ������
ASYNC_EVT_DATA  = 3		# �յ����ݣ�wp=hid, lp=tag
ASYNC_EVT_PROGRESS = 4	# �����������Ѿ�ȫ��������ɣ�wp=hid, lp=tag
ASYNC_EVT_PUSH = 5      # �� post���͹�������Ϣ

ASYNC_MODE_IN		= 1	# ���ͣ���������
ASYNC_MODE_OUT		= 2	# ���ͣ���������
ASYNC_MODE_LISTEN4	= 3	# ���ͣ�IPv4������
ASYNC_MODE_LISTEN6	= 4	# ���ͣ�IPv6������

HEADER_WORDLSB		= 0		# ͷ�������ֽ� little-endian
HEADER_WORDMSB		= 1		# ͷ�������ֽ� big-endian
HEADER_DWORDLSB		= 2		# ͷ�������ֽ� little-endian
HEADER_DWORDMSB		= 3		# ͷ�������ֽ� big-endian
HEADER_BYTELSB		= 4		# ͷ�������ֽ� little-endian
HEADER_BYTEMSB		= 5		# ͷ�������ֽ� big-endian
HEADER_EWORDLSB		= 6		# ͷ�������ֽڣ����������� little-endian
HEADER_EWORDMSB		= 7		# ͷ�������ֽڣ����������� big-endian
HEADER_EDWORDLSB	= 8		# ͷ�������ֽڣ����������� little-endian
HEADER_EDWORDMSB	= 9		# ͷ�������ֽڣ����������� big-endian
HEADER_EBYTELSB		= 10	# ͷ�������ֽڣ����������� little-endian
HEADER_EBYTEMSB		= 11	# ͷ�������ֽڣ����������� little-endian
HEADER_DWORDMASK	= 12	# ͷ�������ֽڣ��������������룩 little-endian
HEADER_RAWDATA		= 13	# ͷ����ԭʼ����������ͷ����־
HEADER_LINESPLIT	= 14	# ͷ������ͷ�����ǰ�'\n'�и����Ϣ


class AsyncCore (object):

	def __init__ (self):
		self.obj = _asn_core_new()
		_asn_core_limit(self.obj, -1, 0x200000)
		self.__options = {
			'NODELAY' : 1, 'REUSEADDR': 2, 'KEEPALIVE':3, 'SYSSNDBUF':4,
			'SYSRCVBUF': 5, 'LIMITED': 6, 'MAXSIZE': 7, 'PROGRESS': 8 }
		self.buffer = ctypes.create_string_buffer('\000' * 0x200000)
		self.wparam = ctypes.c_long()
		self.lparam = ctypes.c_long()
		self.event = ctypes.c_int()
		if CFFI_ENABLE:
			self._buffer = ffi.new('unsigned char[]', 0x200000)
			self._wparam = ffi.new('long[1]')
			self._lparam = ffi.new('long[1]')
			self._event = ffi.new('int[1]')
			self.read = self.__cffi_read
			self.send = self.__cffi_send
		self.state = 0
	
	def __del__ (self):
		self.shutdown()
		self.buffer = None
	
	def shutdown (self):
		if self.obj:
			_asn_core_delete(self.obj)
			self.obj = 0
		return 0
	
	# �ȴ��¼���secondsΪ�ȴ���ʱ�䣬0��ʾ���ȴ�
	# һ��Ҫ�ȵ��� wait��Ȼ��������� readȡ����Ϣ��ֱ��û����Ϣ��
	def wait (self, seconds = 0):
		if self.obj:
			if CFFI_ENABLE:
				_cffi_asn_core_wait(self.obj, long(seconds * 1000))
				return True
			_asn_core_wait(self.obj, long(seconds * 1000))
			return True
		return False
	
	# ���� wait
	def notify (self):
		if self.obj:
			if CFFI_ENABLE:
				_cffi_asn_core_notify(self.obj)
				return True
			_asn_core_notify(self.obj)
			return True
		return False
	
	# ��ȡ��Ϣ�����أ�(event, wparam, lparam, data)
	# ���û����Ϣ������ (None, None, None, None)
	# event��ֵΪ��ASYNC_EVT_NEW/LEAVE/ESTAB/DATA��
	# ��ͨ�÷���ѭ�����ã�û����Ϣ�ɶ�ʱ������һ��waitȥ
	def read (self):
		if not self.obj:
			return (None, None, None, None)
		buffer, size = self.buffer, len(self.buffer)
		event, wparam, lparam = self.event, self.wparam, self.lparam
		hr = _asn_core_read(self.obj, byref(event), byref(wparam), byref(lparam), buffer, size)
		if hr < 0: return (None, None, None, None)
		data = buffer[:hr]
		return event.value, wparam.value, lparam.value, data

	# cffi speed up
	def __cffi_read (self):
		if not self.obj:
			return (None, None, None, None)
		buffer, size = self._buffer, len(self._buffer)
		event, wparam, lparam = self._event, self._wparam, self._lparam
		hr = _cffi_asn_core_read(self.obj, event, wparam, lparam, buffer, size)
		if hr < 0: return (None, None, None, None)
		data = ffi.buffer(buffer, hr)[:]
		return event[0], wparam[0], lparam[0], data

	#��������������֮��ͨ��data�õ��Զ˵���Ϣ
	def	parse_remote(self,data):
		head = ord(data[0])
		port = ord(data[2])*256+ord(data[3])
		ip = '.'.join([ str(ord(n)) for n in data[4:8] ])
		return head,port,ip

	# ��ĳ���ӷ������ݣ�hidΪ���ӱ�ʶ
	def send (self, hid, data, mask = 0):
		if not self.obj:
			raise Exception('no create AsyncCore obj')
		return _asn_core_send_mask(self.obj, hid, data, len(data), mask)

	# cffi ����
	def __cffi_send (self, hid, data, mask = 0):
		if not self.obj:
			return -1000
		return _cffi_asn_core_send_mask(self.obj, hid, data, len(data), mask)

	# �ر����ӣ�ֻҪ���ӶϿ����������Ͽ����Ǳ�close�ӿڶϿ��������յ� leave
	def close (self, hid, code = 1000):
		if not self.obj:
			raise Exception('no create AsyncCore obj')
		return _asn_core_close(self.obj, hid, code)
	
	# ����һ���µĶ������ӣ����� hid�����󷵻� <0
	def new_connect (self, ip, port, head = 0):
		if not self.obj:
			self.obj = _asn_core_new()
			_asn_core_limit(self.obj, -1, 0x200000)
		return _asn_core_new_connect(self.obj, ip, port, head)
	
	# ����һ���µļ������ӣ����� hid�����󷵻� <0, reuseΪ�Ƿ����� REUSEADDR
	def new_listen (self, ip, port, head = 0, reuse = False):
		if not self.obj:
			self.obj = _asn_core_new()
			_asn_core_limit(self.obj, -1, 0x200000)
		if not ip:
			ip = '0.0.0.0'
		if reuse: head |= 0x200
		return _asn_core_new_listen(self.obj, ip, port, head)

	# �ⲿ����һ���׽��֣�����AsyncCore�ڲ�������hid���˺��ڲ�ȫȨ����Ͽ���
	def new_assign (self, fd, head = 0, check_estab = True):
		if not self.obj:
			self.obj = _asn_core_new()
			_asn_core_limit(self.obj, -1, 0x200000)
		return _asn_core_new_assign(fd, head, check_estab and 1 or 0)
	
	# ����һ�� ASYNC_EVT_PUSH �� read�����յ��������� wait�ĵȴ���
	def post (self, wparam, lparam, data):
		if not self.obj:
			self.obj = _asn_core_new()
		return _asn_core_post(self.obj, wparam, lparam, data, len(data))
	
	# ȡ���������ͣ�ASYNC_MODE_IN/OUT/LISTEN4/LISTEN6
	def get_mode (self, hid):
		if not self.obj:
			raise Exception('no create AsyncCore obj')
		return _asn_core_get_mode(self.obj, hid)
	
	# ȡ�� tag
	def get_tag (self, hid):
		if not self.obj:
			raise Exception('no create AsyncCore obj')
		return _asn_core_get_tag(self.obj, hid)
	
	# ���� tag
	def set_tag (self, hid, tag):
		if not self.obj:
			raise Exception('no create AsyncCore obj')
		_asn_core_set_tag(self.obj, hid, tag)
	
	# ȡ��ĳ���ӵĴ����ͻ���(Ӧ�ò�)�еĴ��������ݴ�С
	# �����ж�ĳ���������ǲ��Ƿ�����ȥ����̫����(����ӵ������Զ��������)
	def remain (self, hid):
		if not self.obj:
			raise Exception('no create AsyncCore obj')
		return _asn_core_remain(self.obj, hid)
	
	# ���û�����Ʋ�����limited�Ǵ����ͻ���(remain)�������پͶϿ������ӣ�
	# ���Զ�˲����գ���������ӵ����������һֱ�����������ݣ���remainԽ��Խ��
	# ������ֵ��ϵͳ��Ҫ�����ߵ������ӣ���Ϊ��ɥʧ���������ˡ�
	# maxsize�ǵ������ݰ�������С��Ĭ����2MB�������ô�С��Ϊ�Ƿ���
	def limit (self, limited, maxsize):
		if not self.obj:
			raise Exception('no create AsyncCore obj')
		_asn_core_limit(self.obj, limited, maxsize)
		if maxsize > len(self.buffer):
			self.buffer = ctypes.create_string_buffer('0' * maxsize)
		return 0
	
	# ȡ�õ�һ�����ӱ�ʶ
	def node_head (self):
		if not self.obj:
			return -1
		return _asn_core_node_head(self.obj)
	
	# ȡ����һ�����ӱ�ʶ
	def node_next (self, hid):
		if not self.obj:
			return -1
		return _asn_core_node_next(self.obj, hid)

	# ȡ����һ�����ӱ�ʶ
	def node_prev (self, hid):
		if not self.obj:
			return -1
		return _asn_core_node_prev(self.obj, hid)
	
	# �������ӣ�optȡֵ�� __init__����� self.__options
	def option (self, hid, opt, value):
		if not self.obj:
			raise Exception('no create AsyncCore obj')
		if type(opt) in (type(''), type(u'')):
			opt = self.__options.get(opt.upper(), opt)
		_asn_core_option(self.obj, hid, opt, value)
	
	# ���ü�����Կ�����ͷ���
	def rc4_set_skey (self, hid, key):
		if not self.obj:
			raise Exception('no create AsyncCore obj')
		_asn_core_rc4_set_skey(self.obj, hid, key, len(key))

	# ���ü�����Կ�����շ���
	def rc4_set_rkey (self, hid, key):
		if not self.obj:
			raise Exception('no create AsyncCore obj')
		_asn_core_rc4_set_rkey(self.obj, hid, key, len(key))

	# ���ӳ�ʱ�ӿ�
	def timeout (self, seconds):
		if not self.obj:
			raise Exception('no create AsyncCore obj')
		_asn_core_timeout(self.obj, seconds)
	
	# ȡ�ý��˵�ַ
	def sockname (self, hid):
		if not self.obj:
			raise Exception('no create AsyncCore obj')
		data = self.buffer
		hr = _asn_core_sockname(self.obj, hid, data)
		if hr != 0:
			return None
		hr = data.value.split(':')
		if len(hr) != 2:
			return None
		port = -1
		try:
			port = int(hr[1])
		except:
			return None
		return (hr[0], port)
	
	# ȡ��Զ�˵�ַ
	def peername (self, hid):
		if not self.obj:
			raise Exception('no create AsyncCore obj')
		data = self.buffer
		hr = _asn_core_peername(self.obj, hid, data)
		if hr != 0:
			return None
		hr = data.value.split(':')
		if len(hr) != 2:
			return None
		port = -1
		try:
			port = int(hr[1])
		except:
			return None
		return (hr[0], port)
	
	# �Ƿ��ֹ����ĳ����Ϣ
	def disable (self, hid, value):
		if not self.obj:
			raise Exception('no create AsyncCore obj')
		return _asn_core_disable(self.obj, hid, value and 1 or 0)


#----------------------------------------------------------------------
# ������ TCP
#----------------------------------------------------------------------
class AsyncSock (object):

	def __init__ (self):
		self.obj = 0
		self.buffer = ctypes.create_string_buffer('\000' * 0x200000)
	
	def __del__ (self):
		if self.obj:
			_asn_sock_delete(self.obj)
		self.obj = 0
		self.buffer = None
	
	def connect (self, ip, port, head = 0):
		if not self.obj:
			self.obj = _asn_sock_new()
		return _asn_sock_connect(self.obj, ip, port, head)
	
	def assign (self, fd, head = 0):
		if not self.obj:
			self.obj = _asn_sock_new()
		return _asn_sock_assign(self.obj, fd, head)
	
	def close (self):
		if self.obj:
			_asn_sock_close(self.obj)
			_asn_sock_delete(self.obj)
		self.obj = 0
	
	def state (self):
		if not self.obj:
			raise Exception('no create AsyncSock obj')
		return _asn_sock_state(self.obj)
	
	def fd (self):
		if not self.obj:
			raise Exception('no create AsyncSock obj')
		return _asn_sock_fd(self.obj)

	def remain (self):
		if not self.obj:
			raise Exception('no create AsyncSock obj')
		return _asn_sock_remain(self.obj)
	
	def send (self, data):
		if not self.obj:
			raise Exception('no create AsyncSock obj')
		return _asn_sock_send(self.obj, data, len(data))
	
	def recv (self):
		if not self.obj:
			raise Exception('no create AsyncSock obj')
		buffer = self.buffer
		hr = _asn_sock_recv(self.obj, buffer, 0x200000)
		if hr <= 0:
			return None
		return buffer[:hr]
	
	def process (self):
		if self.obj:
			_asn_sock_process(self.obj)
		return 0
	
	def rc4_set_skey (self, key):
		if not self.obj:
			raise Exception('no create AsyncSock obj')
		_asn_sock_rc4_set_skey(self.obj, key, len(key))
	
	def rc4_set_rkey (self, key):
		if not self.obj:
			raise Exception('no create AsyncSock obj')
		_asn_sock_rc4_set_rkey(self.obj, key, len(key))
	
	def nodelay (self, nodelay):
		if not self.obj:
			raise Exception('no create AsyncSock obj')
		nodelay = nodelay and 1 or 0
		return _asn_sock_nodelay(self.obj, nodelay)
	
	def sys_buffer (self, rcvbuf = -1, sndbuf = -1):
		if not self.obj:
			raise Exception('no create AsyncSock obj')
		return _asn_sock_sys_buffer(self.obj, rcvbuf, sndbuf)
	
	def keepalive (self, keepcnt, idle, interval):
		if not self.obj:
			raise Exception('no create AsyncSock obj')
		return _asn_sock_keepalive(self.obj, keepcnt, idle, interval)


#----------------------------------------------------------------------
# ��β����
#----------------------------------------------------------------------


#----------------------------------------------------------------------
# �첽��Ϣ��
# ʹ�� AsyncCore�����ڲ����ӹ��������ṩ����͸������ϢͶ�ݻ��ơ�
# ֻ��Ҫ���� sid(server id)���ɣ����ع����κ����ӵĽ�����ά��������
#----------------------------------------------------------------------
ASYNC_NOTIFY_EVT_DATA			= 1
ASYNC_NOTIFY_EVT_NEW_IN			= 2
ASYNC_NOTIFY_EVT_NEW_OUT		= 4
ASYNC_NOTIFY_EVT_CLOSED_IN		= 8
ASYNC_NOTIFY_EVT_CLOSED_OUT		= 16
ASYNC_NOTIFY_EVT_ERROR			= 32
ASYNC_NOTIFY_EVT_CORE			= 64

class AsyncNotify (object):

	def __init__ (self, sid = 0):
		self.obj = _asn_notify_new(sid)
		self.__options = {
			'PROFILE' : 0, 'IDLE': 1, 'HEATBEAT':2, 'KEEPALIVE':3,
			'SYSSNDBUF':4, 'SYSRCVBUF': 5, 'LIMITED': 6, 'SIGN_TIMEOUT': 7, 
			'RETRY_TIMEOUT':8, 'NET_TIMEOUT':9, 'EVTMASK':10, 'LOGMASK':11 }
		self.buffer = ctypes.create_string_buffer('\000' * 0x200000)
		self.wparam = ctypes.c_long()
		self.lparam = ctypes.c_long()
		self.event = ctypes.c_int()
		if CFFI_ENABLE:
			self._buffer = ffi.new('unsigned char[]', 0x200000)
			self._wparam = ffi.new('long[1]')
			self._lparam = ffi.new('long[1]')
			self._event = ffi.new('int[1]')
			self.read = self.__cffi_read
			self.send = self.__cffi_send
		self.option('PROFILE', 1)
	
	def __del__ (self):
		self.shutdown()
		self.buffer = None
	
	def shutdown (self):
		if self.obj:
			_asn_notify_delete(self.obj)
			self.obj = 0
		return 0
	
	# �ȴ���������Ϣ
	def wait (self, seconds = 0):
		if self.obj:
			if CFFI_ENABLE:
				_cffi_asn_notify_wait(self.obj, long(seconds * 1000))
				return True
			_asn_notify_wait(self.obj, long(seconds * 1000))
			return True
		return False
	
	# ���ѵȴ�
	def wake (self):
		if self.obj:
			if CFFI_ENABLE:
				_cffi_asn_notify_wake(self.obj)
				return True
			_asn_notify_wake(self.obj)
			return True
		return False
	
	# ��ȡ��Ϣ�����أ�(event, wparam, lparam, data)
	# ���û����Ϣ������ (None, None, None, None)
	# event��ֵΪ��ASYNC_NOTIFY_EVT_DATA/NEW_IN/NEW_OUT/ERROR ��
	# ��ͨ�÷���ѭ�����ã�û����Ϣ�ɶ�ʱ������һ��waitȥ
	def read (self):
		if not self.obj:
			return (None, None, None, None)
		buffer, size = self.buffer, len(self.buffer)
		event, wparam, lparam = self.event, self.wparam, self.lparam
		hr = _asn_notify_read(self.obj, byref(event), byref(wparam), byref(lparam), buffer, size)
		if hr < 0: return (None, None, None, None)
		data = buffer[:hr]
		return event.value, wparam.value, lparam.value, data
	
	# cffi speed up
	def __cffi_read (self):
		if not self.obj:
			return (None, None, None, None)
		buffer, size = self._buffer, len(self._buffer)
		event, wparam, lparam = self._event, self._wparam, self._lparam
		hr = _cffi_asn_notify_read(self.obj, event, wparam, lparam, buffer, size)
		if hr < 0: return (None, None, None, None)
		data = ffi.buffer(buffer, hr)[:]
		return event[0], wparam[0], lparam[0], data
	
	# �½����������ؼ��� listen_id
	def listen (self, ip, port, reuseaddr = False):
		if not self.obj:
			return -1000
		return _asn_notify_listen(self.obj, ip, port, reuseaddr and 1 or 0)
	
	# �رռ���
	def remove (self, listen_id):
		if not self.obj:
			return -1000
		return _asn_notify_remove(self.obj, listen_id)
	
	# ȡ�ö˿�
	def get_port (self, listen_id):
		if not self.obj:
			return -1000
		return _asn_notify_get_port(self.obj, listen_id)
	
	# �ı������ sid�����繹��ʱ��������0����������Ҫ�ٸ���
	def change (self, newsid):
		if not self.obj:
			return -1000
		_asn_notify_change(self.obj, newsid)

	# ��ĳ̨ server��������
	def send (self, sid, cmd, data):
		if not self.obj:
			return -1000
		return _asn_notify_send(self.obj, sid, cmd, data, len(data))
	
	# cffi ����
	def __cffi_send (self, sid, cmd, data):
		if not self.obj:
			return -1000
		return _cffi_asn_notify_send(self.obj, sid, cmd, data, len(data))

	# �ر�ĳ̨�����������ӣ�mode=1�ⲿ�����������ӣ�mode=2����ȥ������
	def close (self, sid, mode, code):
		if not self.obj:
			return -1000
		return _asn_notify_close(self.obj, sid, mode, code)
	
	# ��� ip������
	def allow_clear (self):
		if not self.obj:
			return False
		_asn_notify_allow_clear(self.obj)
		return True
	
	# ��� ip������
	def allow_add (self, ip = '127.0.0.1'):
		if not self.obj:
			return False
		_asn_notify_allow_add(self.obj, ip)
		return True
	
	# ɾ�� ip������
	def allow_del (self, ip = '127.0.0.1'):
		if not self.obj:
			return False
		_asn_notify_allow_del(self.obj, ip)
		return True
	
	# �Ƿ����� ip������
	def allow_enable (self, enable = True):
		if not self.obj:
			return False
		_asn_notify_allow_enable(self.obj, enable and 1 or 0)
		return True
	
	# һ�������ð�����
	def allow (self, allowip = []):
		if not self.obj:
			return False
		if allowip in (None, False):
			self.allow_enable(False)
			return False
		self.allow_clear()
		for ip in allowip:
			self.allow_add(ip)
		self.allow_enable(True)
		return True
			
	# ����һ̨��������sid->(ip, port)
	def sid_add (self, sid, ip, port):
		if not self.obj:
			return False
		_asn_notify_sid_add(self.obj, sid, ip, port)
		return True
	
	# ɾ��һ̨������
	def sid_del (self, sid):
		if not self.obj:
			return False
		_asn_notify_sid_del(self.obj, sid)
		return True
	
	# ���sid�б�
	def sid_clear (self):
		if not self.obj:
			return False
		_asn_notify_sid_clear(self.obj)
		return True
	
	# ������֤ǩ��
	def login_token (self, text):
		if not self.obj:
			return False
		_asn_notify_token(self.obj, text, len(text))
		return True

	# �������ӣ�optȡֵ�� __init__����� self.__options
	def option (self, opt, value):
		if not self.obj:
			raise Exception('no create AsyncNotify obj')
		if type(opt) in (type(''), type(u'')):
			opt = self.__options.get(opt.upper(), opt)
		return _asn_notify_option(self.obj, opt, value)
	
	# ������־��
	# prefixΪ�ļ����ַ���ǰ׺��Noneʱ�ر��ļ����
	# stdoutΪTrueʱ���������׼���
	# colorΪ��ɫ
	def trace (self, prefix, stdout = False, color = -1):
		if not self.obj:
			return False
		_asn_notify_trace(self.obj, prefix, stdout, color)
		return True


#----------------------------------------------------------------------
# demo of AsyncCore
#----------------------------------------------------------------------
def test_async_core():
	# ����һ�� AsyncCore
	core = AsyncCore()
	# ����һ���µļ��� hid��ͷ��ģʽ HEADER_WORDLSB
	hid_listen = core.new_listen('127.0.0.1', 8001, HEADER_WORDLSB)
	if hid_listen < 0:
		print 'can not listen on port 8001'
		return -1
	print 'listen on localhost:8001 hid=%xh'%hid_listen
	# ����һ���µ����� hid
	hid_connect = core.new_connect('127.0.0.1', 8001, HEADER_WORDLSB)
	if hid_connect < 0:
		print 'can not connect to localhost:8001'
		return -2
	print 'connect to localhost:8001 hid=%xh'%hid_connect
	established = False
	timeslap = time.time()
	hid_accept = -1
	index = 0
	while True:
		# �ȴ���Ϣ
		core.wait(0.1)
		# ����ǰ������Ϣ
		while True:
			event, hid, tag, data = core.read()
			if event == None: # û��Ϣ�ͷ���
				break
			# �½� hid��������������ǽ��������ӣ����ǵ��� new_listen / new_connect
			if event == ASYNC_EVT_NEW:
				print time.strftime('[%Y-%m-%d %H:%M:%S]'), 'new hid=%xh'%hid
				if core.get_mode(hid) == ASYNC_MODE_IN:
					hid_accept = hid	# hid_listen��� hid���յ�һ���µ� hid
					print time.strftime('[%Y-%m-%d %H:%M:%S]'), 'accept hid=%xh'%hid
			# ���� hid����������������ⲿ���ߣ���ʱ�����߱��� AsyncCore.close(hid)
			elif event == ASYNC_EVT_LEAVE:
				print time.strftime('[%Y-%m-%d %H:%M:%S]'), 'leave hid=%xh'%hid
			# ���ӽ�����ֻ�� new_connect��ȥ�����ӳɹ�����յ�
			elif event == ASYNC_EVT_ESTAB:
				if hid == hid_connect:
					established = True
				print time.strftime('[%Y-%m-%d %H:%M:%S]'), 'estab hid=%xh'%hid
			# �յ�����
			elif event == ASYNC_EVT_DATA:
				if hid == hid_accept:			# accepted hid
					core.send(hid, data)		# echo back
				elif hid == hid_connect:
					print time.strftime('[%Y-%m-%d %H:%M:%S]'), 'recv', data
		# ��ʱ��������
		if established:
			current = time.time()
			if current > timeslap:
				timeslap = current + 1
				core.send(hid_connect, 'ECHO\x00%d'%index)
				index += 1
	return 0


#----------------------------------------------------------------------
# demo of AsyncNotify
#----------------------------------------------------------------------
def test_async_notify():
	n1 = AsyncNotify(2001)			# ���������ڵ�
	n2 = AsyncNotify(2002)
	
	n1.listen('127.0.0.1', 8001)	# ������ͬ�˿�
	n2.listen('127.0.0.1', 8002)

	n1.login_token('1234')			# ���û�����֤��Կ
	n2.login_token('1234')

	n1.sid_add(2002, '127.0.0.1', 8002)		# ������� sid
	n2.sid_add(2001, '127.0.0.1', 8001)

	n1.send(2002, 1, 'hello')		# ֱ���� n2��������
	n1.send(2002, 2, 'world !!')

	n1.trace(None, True, -1)		# ���ò������־���ļ�����ʾ����Ļ
	n2.trace(None, True, 5)			# ������־����ɫ
	n1.option('logmask', 0xff)
	n2.option('logmask', 0xff)

	import time
	ts = time.time() + 1
	index = 0

	while 1:
		time.sleep(0.001)
		n1.wait(0)
		n2.wait(0)
		while 1:	# n1�������ݲ���ʾ
			e, w, l, d = n1.read()
			if e == None:
				break
			if e == ASYNC_NOTIFY_EVT_DATA:
				print 'RECV cmd=%d data=%s'%(l, repr(d))
		while 1:	# n2�������ݲ�ԭ������ȥ
			e, w, l, d = n2.read()
			if e == None:
				break
			if e == ASYNC_NOTIFY_EVT_DATA:
				n2.send(w, l, d)
		if time.time() > ts:	# ÿ��һ�뷢��һ�����ݵ� n2
			ts = time.time() + 1
			n1.send(2002, 3, 'index:\x00 %d'%index)
			index += 1
	return 0



#----------------------------------------------------------------------
# demo of AsyncCore post
#----------------------------------------------------------------------
def test_async_post():
	import threading
	def mythread(core):
		index = 0
		while 1:
			time.sleep(1)
			core.post(1, index, 'Post from mythread ' + str(index))
			index += 1
		return 0

	core = AsyncCore()

	th = threading.Thread(None, mythread, 'name', [core])
	th.setDaemon(True)
	th.start()

	start = time.time()
	while 1:
		core.wait(5)
		ts = time.time() - start
		while 1:
			evt, wp, lp, data = core.read()
			if evt == None:
				break
			print '[%.3f] evt=%d wp=%d lp=%d data=%s'%(ts, evt, wp, lp, repr(data))
		
	return 0


#----------------------------------------------------------------------
# testing case
#----------------------------------------------------------------------
if __name__ == '__main__':
	#test_async_core()
	test_async_notify()
		
	
