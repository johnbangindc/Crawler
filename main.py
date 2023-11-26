
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

