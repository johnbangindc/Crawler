
# 这是一个自动生成的Python文件
def hello_world():
    print("Hello, world! Time is 'Fri Nov 10 15:09:07 2023'")


if __name__ == "__main__":
    hello_world()
    a = 1
             * \project	WonderTrader
 *
 * \author Wesley
 * \date 2020/03/30
 * 
 * \brief 
 */
#include "ParserUDP.h"
#include "../Includes/WTSVariant.hpp"
#include "../Includes/WTSDataDef.hpp"

#include <boost/bind.hpp>

 //By Wesley @ 2022.01.05
#include "../Share/fmtlib.h"
template<typename... Args>
inline void write_log(IParserSpi* sink, WTSLogLevel ll, const char* format, const Args&... args)
{
	if (sink == NULL)
		return;

	static thread_local char buffer[512] = { 0 };
	fmtutil::format_to(buffer, format, args...);

	sink->handleParserLog(ll, buffer);
}

#define UDP_MSG_SUBSCRIBE	0x100
#define UDP_MSG_PUSHTICK	0x200
#define UDP_MSG_PUSHORDQUE	0x201	//委托队列
#define UDP_MSG_PUSHORDDTL	0x202	//委托明细
#define UDP_MSG_PUSHTRANS	0x203	//逐笔成交

#pragma pack(push,1)

typedef struct UDPPacketHead
{
	uint32_t		_type;
} UDPPacketHead;
//UDP请求包
typedef struct _UDPReqPacket : UDPPacketHead
{
	char			_data[1020];
} UDPReqPacket;

//UDPTick数据包
template <typename T>
struct UDPDataPacket : UDPPacketHead
{
	T			_data;
};
#pragma pack(pop)
typedef UDPDataPacket<WTSTickStruct>	UDPTickPacket;
typedef UDPDataPacket<WTSOrdQueStruct>	UDPOrdQuePacket;
typedef UDPDataPacket<WTSOrdDtlStruct>	UDPOrdDtlPacket;
typedef UDPDataPacket<WTSTransStruct>	UDPTransPacket;


extern "C"
{
	EXPORT_FLAG IParserApi* createParser()
	{
		ParserUDP* parser = new ParserUDP();
		return parser;
	}

	EXPORT_FLAG void deleteParser(IParserApi* &parser)
	{
		if (NULL != parser)
		{
			delete parser;
			parser = NULL;
		}
	}
};



ParserUDP::ParserUDP()
	: _b_socket(NULL)
	, _s_socket(NULL)
	, _strand(_io_service)
	, _stopped(false)
	, _sink(NULL)
	, _connecting(false)
	, _s_inited(false)
{
}


ParserUDP::~ParserUDP()
{
}

bool ParserUDP::init( WTSVariant* config )
{
	_hots = config->getCString("host");
	_bport = config->getInt32("bport");
	_sport = config->getInt32("sport");
	_gpsize = config->getUInt32("gpsize");
	if (_gpsize == 0)
		_gpsize = 1000;

	ip::address addr = ip::address::from_string(_hots);
	_server_ep = ip::udp::endpoint(addr, _sport);

	_broad_ep = ip::udp::endpoint(ip::address_v4::any(), _bport);

	return true;
}

void ParserUDP::release()
{
	
}

bool ParserUDP::reconnect(uint32_t flag /* = 3 */)
{
	if(flag & 1)
	{//建立广播通道
		if (_b_socket != NULL)
		{
			_b_socket->close();
			delete _b_socket;
			_b_socket = NULL;
		}

		_b_socket = new ip::udp::socket(_io_service);

		_b_socket->open(_broad_ep.protocol());
		_b_socket->set_option(ip::udp::socket::reuse_address(true));
		_b_socket->set_option(ip::udp::socket::broadcast(true));
		_b_socket->set_option(ip::udp::socket::receive_buffer_size(8 * 1024 * 1024));
		_b_socket->bind(_broad_ep);

		_b_socket->async_receive_from(buffer(_b_buffer), _broad_ep,
			boost::bind(&ParserUDP::handle_read, this,
			boost::asio::placeholders::error,
			boost::asio::placeholders::bytes_transferred, true));
	}

	if (flag & 2)
	{
		std::queue<std::string> emptyQue;
		{
			StdUniqueLock lock(_mtx_queue);
			_send_queue.swap(emptyQue);

			//建立订阅通道
			if (_s_socket != NULL)
			{
				_s_socket->close();
				delete _s_socket;
				_s_socket = NULL;
			}

			_s_inited = false;
			_s_socket = new ip::udp::socket(_io_service, ip::udp::endpoint(ip::udp::v4(), 0));
		}

		subscribe();
	}
	return true;
}

void ParserUDP::subscribe()
{
	std::string data;
	data.resize(sizeof(UDPReqPacket), 0);
 * 
 * \brief 
 */
#include "ParserUDP.h"
#include "../Includes/WTSVariant.hpp"
#include "../Includes/WTSDataDef.hpp"

#include <boost/bind.hpp>

 //By Wesley @ 2022.01.05
#include "../Share/fmtlib.h"
template<typename... Args>
inline void write_log(IParserSpi* sink, WTSLogLevel ll, const char* format, const Args&... args)
{
	if (sink == NULL)
		return;

	static thread_local char buffer[512] = { 0 };
	fmtutil::format_to(buffer, format, args...);

	sink->handleParserLog(ll, buffer);
}

#define UDP_MSG_SUBSCRIBE	0x100
#define UDP_MSG_PUSHTICK	0x200
#define UDP_MSG_PUSHORDQUE	0x201	//委托队列
#define UDP_MSG_PUSHORDDTL	0x202	//委托明细
#define UDP_MSG_PUSHTRANS	0x203	//逐笔成交

#pragma pack(push,1)

typedef struct UDPPacketHead
{
	uint32_t		_type;
} UDPPacketHead;
//UDP请求包
typedef struct _UDPReqPacket : UDPPacketHead
{
	char			_data[1020];
} UDPReqPacket;
 *
 * \author Wesley
 * \date 2020/03/30
 * 
 * \brief 
 */
#include "ParserUDP.h"
#include "../Includes/WTSVariant.hpp"
#include "../Includes/WTSDataDef.hpp"

#include <boost/bind.hpp>

 //By Wesley @ 2022.01.05
#include "../Share/fmtlib.h"
template<typename... Args>
inline void write_log(IParserSpi* sink, WTSLogLevel ll, const char* format, const Args&... args)
{
	if (sink == NULL)
		return;

	static thread_local char buffer[512] = { 0 };
	fmtutil::format_to(buffer, format, args...);

	sink->handleParserLog(ll, buffer);
}

#define UDP_MSG_SUBSCRIBE	0x100
#define UDP_MSG_PUSHTICK	0x200
#define UDP_MSG_PUSHORDQUE	0x201	//委托队列
#define UDP_MSG_PUSHORDDTL	0x202	//委托明细
#define UDP_MSG_PUSHTRANS	0x203	//逐笔成交

#pragma pack(push,1)

typedef struct UDPPacketHead
{
	uint32_t		_type;
} UDPPacketHead;
//UDP请求包
typedef struct _UDPReqPacket : UDPPacketHead
{
	char			_data[1020];
} UDPReqPacket;

//UDPTick数据包
template <typename T>
struct UDPDataPacket : UDPPacketHead
{
	T			_data;
};
#pragma pack(pop)
typedef UDPDataPacket<WTSTickStruct>	UDPTickPacket;
typedef UDPDataPacket<WTSOrdQueStruct>	UDPOrdQuePacket;
typedef UDPDataPacket<WTSOrdDtlStruct>	UDPOrdDtlPacket;
typedef UDPDataPacket<WTSTransStruct>	UDPTransPacket;


extern "C"
{
	EXPORT_FLAG IParserApi* createParser()
	{
		ParserUDP* parser = new ParserUDP();
		return parser;
	}

	EXPORT_FLAG void deleteParser(IParserApi* &parser)
	{
		if (NULL != parser)
		{
			delete parser;
			parser = NULL;
		}
	}
};



ParserUDP::ParserUDP()
	: _b_socket(NULL)
	, _s_socket(NULL)
	, _strand(_io_service)
	, _stopped(false)
	, _sink(NULL)
	, _connecting(false)
	, _s_inited(false)
{
}


ParserUDP::~ParserUDP()
{
}

bool ParserUDP::init( WTSVariant* config )
{
	_hots = config->getCString("host");
	_bport = config->getInt32("bport");
	_sport = config->getInt32("sport");
 * \project	WonderTrader
 *
 * \author Wesley
 * \date 2020/03/30
 * 
 * \brief 
 */
#include "ParserUDP.h"
#include "../Includes/WTSVariant.hpp"
#include "../Includes/WTSDataDef.hpp"

#include <boost/bind.hpp>

 //By Wesley @ 2022.01.05
#include "../Share/fmtlib.h"
template<typename... Args>
inline void write_log(IParserSpi* sink, WTSLogLevel ll, const char* format, const Args&... args)
{
	if (sink == NULL)
		return;

	static thread_local char buffer[512] = { 0 };
	fmtutil::format_to(buffer, format, args...);

	sink->handleParserLog(ll, buffer);
}

#define UDP_MSG_SUBSCRIBE	0x100
#define UDP_MSG_PUSHTICK	0x200
#define UDP_MSG_PUSHORDQUE	0x201	//委托队列
#define UDP_MSG_PUSHORDDTL	0x202	//委托明细
#define UDP_MSG_PUSHTRANS	0x203	//逐笔成交

#pragma pack(push,1)

typedef struct UDPPacketHead
{
	uint32_t		_type;
} UDPPacketHead;
//UDP请求包
typedef struct _UDPReqPacket : UDPPacketHead
{
	char			_data[1020];
} UDPReqPacket;

//UDPTick数据包
template <typename T>
struct UDPDataPacket : UDPPacketHead
{
	T			_data;
};
#pragma pack(pop)
typedef UDPDataPacket<WTSTickStruct>	UDPTickPacket;
typedef UDPDataPacket<WTSOrdQueStruct>	UDPOrdQuePacket;
typedef UDPDataPacket<WTSOrdDtlStruct>	UDPOrdDtlPacket;
typedef UDPDataPacket<WTSTransStruct>	UDPTransPacket;


extern "C"
{
	EXPORT_FLAG IParserApi* createParser()
	{
		ParserUDP* parser = new ParserUDP();
		return parser;
	}

	EXPORT_FLAG void deleteParser(IParserApi* &parser)
	{
		if (NULL != parser)
		{
			delete parser;
			parser = NULL;
		}
	}
};



ParserUDP::ParserUDP()
	: _b_socket(NULL)
	, _s_socket(NULL)
	, _strand(_io_service)
	, _stopped(false)
	, _sink(NULL)
	, _connecting(false)
	, _s_inited(false)
