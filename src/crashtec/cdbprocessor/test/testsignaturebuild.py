import unittest
import logging
import os

from crashtec.cdbprocessor import signaturebuilder
#from crashtec.infrastructure.public import definitions as infradefs
_logger = logging.getLogger("cdb_processor")

class TestProblemStackParser(unittest.TestCase):
    def test01_extrack_stack_lines(self):
        RESULT_LINES = ['057ef760 03d2dee6 0456a670 ffffffff 0000ffff ItvSdkUtil!CCompressedBuffer::CCompressedBuffer+0x97',
                        '057ef7a4 03d28cdc 057efa54 057efa64 057efa5c ItvSdkUtil!boost::lambda::new_ptr<CCompressedBuffer>::operator()<NMMSS::IFrameBuilder * const,NMMSS::ISample * const,unsigned int const ,unsigned short const ,unsigned short const ,char const *,unsigned int,unsigned __int64,bool>+0x86',
                        '057efaa8 03d26b34 057efd6c 057efb0c 00000002 ItvSdkUtil!CFrameFactory::CreateTypedFrame<ITV8::MFF::ICompressedBuffer,NMMSS::NMediaType::Video,boost::_bi::bind_t<CCompressedBuffer *,boost::lambda::new_ptr<CCompressedBuffer>,boost::_bi::list9<boost::arg<5>,boost::arg<1>,boost::arg<2>,boost::arg<3>,boost::arg<4>,boost::_bi::value<char const *>,boost::_bi::value<unsigned int>,boost::_bi::value<unsigned __int64>,boost::_bi::value<bool> > > >+0x7ac',
                        '057efc6c 6a7550bc 057efd6c 0000053c 97ead827 ItvSdkUtil!CFrameFactory::AllocateCompressedFrame+0x244',
                        '057efd9c 6a7443e5 00000011 01b2b010 0000053c Ipint_Virtual!Virtual::VideoSource::SendSample+0x8c',
                        '057efdf8 6a737eb0 057efe0c 6a73e38d 057efe1c Ipint_Virtual!Virtual::CFFMpegGrabber::ProcessNextPacket+0x185',
                        '057efe00 6a73e38d 057efe1c 057efe54 6a73f670 Ipint_Virtual!Virtual::CFFMpegGrabber::TimerHandler+0x10',
                        '057efe0c 6a73f670 6a737ea0 055e9be0 00000000 Ipint_Virtual!boost::asio::asio_handler_invoke<boost::asio::detail::binder1<boost::_bi::bind_t<void,boost::_mfi::mf1<void,Virtual::CFFMpegGrabber,boost::system::error_code const &>,boost::_bi::list2<boost::_bi::value<Virtual::CFFMpegGrabber *>,boost::arg<1> > >,boost::system::error_code> >+0xd',
                        '057efe54 6a47c1c5 055e7728 055e9158 00000000 Ipint_Virtual!boost::asio::detail::wait_handler<boost::_bi::bind_t<void,boost::_mfi::mf1<void,Virtual::CFFMpegGrabber,boost::system::error_code const &>,boost::_bi::list2<boost::_bi::value<Virtual::CFFMpegGrabber *>,boost::arg<1> > > >::do_complete+0xa0',
                        '057efeb8 6a47cb60 055e7728 057eff04 58940de2 IpUtil!boost::asio::detail::win_iocp_io_service::do_one+0x1a5',
                        '057efef4 6a47dcc4 057eff04 006707c8 00000000 IpUtil!boost::asio::detail::win_iocp_io_service::run+0xf0',
                        '057eff0c 6a609ed3 58940c52 00000000 00000000 IpUtil!boost::asio::io_service::run+0x24',
                        "057eff44 6a38c556 006707c8 58940c07 00000000 IpUtil!boost::`anonymous namespace'::thread_start_function+0x63",
                        '057eff7c 6a38c600 00000000 057eff94 758633ca msvcr100!_endthreadex+0x3f',
                        '057eff88 758633ca 055e9cc0 057effd4 76ec9ed2 msvcr100!_endthreadex+0xce',
                        '057eff94 76ec9ed2 055e9cc0 7333023a 00000000 kernel32!BaseThreadInitThunk+0xe',
                        '057effd4 76ec9ea5 6a38c59c 055e9cc0 00000000 ntdll!__RtlUserThreadStart+0x70',
                        '057effec 00000000 6a38c59c 055e9cc0 00000000 ntdll!_RtlUserThreadStart+0x1b']
        PEOCESSED_FILE_NAME = os.path.dirname(__file__) + "/test_data/406/results.txt"
        f = open(PEOCESSED_FILE_NAME, 'r')
        content = f.read()
        
        stack_parser = signaturebuilder.ProblemStackParser();
        self.assertEqual(RESULT_LINES, stack_parser.extrack_stack_lines(content))
    
    def test02_parseStackLines(self):
        PEOCESSED_FILE_NAME = os.path.dirname(__file__) + "/test_data/406/results.txt"
        f = open(PEOCESSED_FILE_NAME, 'r')
        content = f.read()
        stack_parser = signaturebuilder.ProblemStackParser();
        lines = stack_parser.extrack_stack_lines(content)
        stackEntries = stack_parser.strip_additional_info(lines)
        RESULT_STACK_ENTRIES = [
                    'ItvSdkUtil!CCompressedBuffer::CCompressedBuffer+0x97',
                    'ItvSdkUtil!boost::lambda::new_ptr<CCompressedBuffer>::operator()<NMMSS::IFrameBuilder * const,NMMSS::ISample * const,unsigned int const ,unsigned short const ,unsigned short const ,char const *,unsigned int,unsigned __int64,bool>+0x86',
                    'ItvSdkUtil!CFrameFactory::CreateTypedFrame<ITV8::MFF::ICompressedBuffer,NMMSS::NMediaType::Video,boost::_bi::bind_t<CCompressedBuffer *,boost::lambda::new_ptr<CCompressedBuffer>,boost::_bi::list9<boost::arg<5>,boost::arg<1>,boost::arg<2>,boost::arg<3>,boost::arg<4>,boost::_bi::value<char const *>,boost::_bi::value<unsigned int>,boost::_bi::value<unsigned __int64>,boost::_bi::value<bool> > > >+0x7ac',
                    'ItvSdkUtil!CFrameFactory::AllocateCompressedFrame+0x244', 
                    'Ipint_Virtual!Virtual::VideoSource::SendSample+0x8c',
                    'Ipint_Virtual!Virtual::CFFMpegGrabber::ProcessNextPacket+0x185',
                    'Ipint_Virtual!Virtual::CFFMpegGrabber::TimerHandler+0x10',
                    'Ipint_Virtual!boost::asio::asio_handler_invoke<boost::asio::detail::binder1<boost::_bi::bind_t<void,boost::_mfi::mf1<void,Virtual::CFFMpegGrabber,boost::system::error_code const &>,boost::_bi::list2<boost::_bi::value<Virtual::CFFMpegGrabber *>,boost::arg<1> > >,boost::system::error_code> >+0xd',
                    'Ipint_Virtual!boost::asio::detail::wait_handler<boost::_bi::bind_t<void,boost::_mfi::mf1<void,Virtual::CFFMpegGrabber,boost::system::error_code const &>,boost::_bi::list2<boost::_bi::value<Virtual::CFFMpegGrabber *>,boost::arg<1> > > >::do_complete+0xa0',
                    'IpUtil!boost::asio::detail::win_iocp_io_service::do_one+0x1a5',
                    'IpUtil!boost::asio::detail::win_iocp_io_service::run+0xf0',
                    'IpUtil!boost::asio::io_service::run+0x24', 
                    "IpUtil!boost::`anonymous namespace'::thread_start_function+0x63",
                    'msvcr100!_endthreadex+0x3f',
                    'msvcr100!_endthreadex+0xce',
                    'kernel32!BaseThreadInitThunk+0xe',
                    'ntdll!__RtlUserThreadStart+0x70',
                    'ntdll!_RtlUserThreadStart+0x1b']
        self.assertEqual(RESULT_STACK_ENTRIES, stackEntries)
        
        
        
class TestStackEntry(unittest.TestCase):
    def test_get_module_name(self):
        TEST_CASES = [
                      ("ItvSdkUtil!CCompressedBuffer::CCompressedBuffer@0x97", "ItvSdkUtil"),
                      ("video@0x2884a2", "video")
                      # TODO: handle cases when we have only address
                      ]
        for (signature, moduleName) in TEST_CASES:
            stack_entry = signaturebuilder.StackEntry(signature)
            self.assertEqual(stack_entry.get_module_name(), moduleName)
#         
#     def test_buildSignature(self):
#         testCases = [("/test_data/406/results.txt", "/test_data/406/AppHost-4408-APP_HOST.Ipint_12-11-07_2011-12-16.dmp", 'ItvSdkUtil!CCompressedBuffer::CCompressedBuffer@0x97', False, "AxxonSmartIp"),
#                      ("/test_data/205/results.txt", "/test_data/205/video.06-07-2011.16-05-18.dmp", 'video@0x2884a2', False, "Intellect"),
#                      ("/test_data/719/results.txt", "/test_data/719/AxxonNext-5404_12-20-47_2012-08-08.dmp", "KERNELBASE@0xd36f | mscorwks!GetMetaDataInternalInterface@0x300e1 | mscorwks!GetMetaDataInternalInterface@0x32fdf | 0x5eaf021 | 0x5eae939 | 0x5eae812 | 0x21c55c19 | 0x21c5f873 | 0x21c5f820 | System_Windows_Forms_ni@0xa5ec1e | System_Windows_Forms_ni@0x...", True, None)
#                      ]
#         for (resultFile, dumpFile, signature, truncated, product) in testCases:
#             f = open(os.path.dirname(__file__) + resultFile, 'r')
#             content = f.read()
#             f.close()  
#             modules = ModuleUtils.Modules(gLogger, 
#                                           os.path.dirname(__file__) + dumpFile,
#                                           infradefs.PLATFORM_WIN64)
#             
#             lines = signatureParser.extractStackLines(content)
#             stackEntries = signatureParser.parseStackLines(lines)
#             (returnSignature, returnTruncated, returnProduct) = stackAnalyzer.buildSignature(stackEntries, modules)
#             self.assertEqual(signature, returnSignature)
#             self.assertEqual(product, returnProduct)
#             self.assertEqual(truncated, returnTruncated)
            
         
if __name__ == '__main__':
    unittest.main()
