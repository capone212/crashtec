import unittest
import logging
import os

from crashtec.cdbprocessor import callstackparser
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
        
        stack_parser = callstackparser.ProblemStackParser();
        self.assertEqual(RESULT_LINES, stack_parser.extrack_stack_lines(content))
    
    def test02_strip_additional_info_5_hexgroups(self):
        TEST_LINES = [
                 '0006fe98 7739bde5 7739be1a 03ca4f28 00000000 ntdll!KiFastSystemCallRet',
                 '0006fec4 77396558 03ca4f28 00000000 00000000 user32!NtUserPeekMessage+0xc',
                 '0006fef0 78238326 03ca4f28 00000000 00000000 user32!PeekMessageA+0xda',
                 '0006ff20 7820ccec 00f5dec0 000aaff7 00000000 mfc80!CWinThread::Run+0x7d [f:\dd\vctools\vc7libs\ship\atlmfc\src\mfc\thrdcore.cpp @ 636]',
                 '0006ff30 0079f42a 00400000 00000000 000aaff7 mfc80!AfxWinMain+0x69 [f:\dd\vctools\vc7libs\ship\atlmfc\src\mfc\winmain.cpp @ 47]',
                 '0006ffc0 77e6f1eb 00000000 00000000 7ffd8000 video!__tmainCRTStartup+0x140 [f:\sp\vctools\crt_bld\self_x86\crt\src\crtexe.c @ 589]',
                 '0006fff0 00000000 0079f607 00000000 78746341 kernel32!BaseProcessStart+0x23'
                 ]

        stack_parser = callstackparser.ProblemStackParser();
        stack_entries = stack_parser.strip_additional_info(TEST_LINES)
        RESULT_STACK_ENTRIES = ['ntdll!KiFastSystemCallRet',
                                'user32!NtUserPeekMessage+0xc',
                                'user32!PeekMessageA+0xda',
                                'mfc80!CWinThread::Run+0x7d',
                                'mfc80!AfxWinMain+0x69',
                                'video!__tmainCRTStartup+0x140',
                                'kernel32!BaseProcessStart+0x23'
                                ]
        self.assertEqual(RESULT_STACK_ENTRIES, stack_entries, "Unexpected result from strip_additional_info() function")

    def test03_strip_additional_info_2_hexgroups(self):
        TEST_LINES = [
                    '00fdca30 00280287 video!CamInfo::SetListen+0x47',
                    '00fdca3c 003967e5 video!CMonitorFrame::AddCam+0xb55',
                    '00fdcc4c 003a73cf video!CMonitorFrame::ReceiveCore+0x1bef',
                    '00fddd58 00345d09 video!CMainFrame::OnReceiveMsg+0x569',
                    '00fdfadc 601ff596 mfc100!CWnd::OnWndMsg+0x2f5',
                    '00fdfbc0 0035e0ca video!CMainFrame::WindowProc+0x7a',
                    '00fdfbe0 601fd667 mfc100!AfxCallWndProc+0xb5',
                    '00fdfc58 601fd8f3 mfc100!AfxWndProc+0x37'
                 ]

        stack_parser = callstackparser.ProblemStackParser();
        stack_entries = stack_parser.strip_additional_info(TEST_LINES)
        RESULT_STACK_ENTRIES = [
                                'video!CamInfo::SetListen+0x47',
                                'video!CMonitorFrame::AddCam+0xb55',
                                'video!CMonitorFrame::ReceiveCore+0x1bef',
                                'video!CMainFrame::OnReceiveMsg+0x569',
                                'mfc100!CWnd::OnWndMsg+0x2f5',
                                'video!CMainFrame::WindowProc+0x7a',
                                'mfc100!AfxCallWndProc+0xb5',
                                'mfc100!AfxWndProc+0x37'
                                ]
        self.assertEqual(RESULT_STACK_ENTRIES, stack_entries, "Unexpected result from strip_additional_info() function")
    
    def test04_strip_additional_info_win64(self):
        TEST_LINES = [
                    '00000000`0619ee30 00000000`591a14f1 : 00000000`0619ef98 00000000`0619ef70 ffffffff`00000001 000007fe`f1a80110 : KERNELBASE!RaiseException+0x39',
                    '00000000`0619ef00 000007fe`f1aa34ec : 000007fe`f1a80000 00000000`0619f0e0 00000000`03e24ef0 00000000`046fa6c8 : msvcr100!CxxThrowException+0x81',
                    '00000000`0619ef70 000007fe`f1a80000 : 00000000`0619f0e0 00000000`03e24ef0 00000000`046fa6c8 ffffffff`fffffffe : Ipint_SonyIpela+0x234ec',
                    '00000000`0619ef78 00000000`0619f0e0 : 00000000`03e24ef0 00000000`046fa6c8 ffffffff`fffffffe 000007fe`f1beacb0 : Ipint_SonyIpela',
                    '00000000`0619ef80 00000000`03e24ef0 : 00000000`046fa6c8 ffffffff`fffffffe 000007fe`f1beacb0 00000000`00000000 : 0x619f0e0',
                    '00000000`0619ef88 00000000`046fa6c8 : ffffffff`fffffffe 000007fe`f1beacb0 00000000`00000000 0000006e`6f697400 : 0x3e24ef0',
                    '00000000`0619ef90 ffffffff`fffffffe : 000007fe`f1beacb0 00000000`00000000 0000006e`6f697400 000007fe`f1beaca0 : 0x46fa6c8',
                    '00000000`0619ef98 000007fe`f1beacb0 : 00000000`00000000 0000006e`6f697400 000007fe`f1beaca0 00000000`00000000 : 0xffffffff`fffffffe',
                    '00000000`0619efa0 00000000`00000000 : 0000006e`6f697400 000007fe`f1beaca0 00000000`00000000 00000000`00000000 : Ipint_SonyIpela+0x16acb0'
                 ]

        stack_parser = callstackparser.ProblemStackParser();
        stack_entries = stack_parser.strip_additional_info(TEST_LINES)
        RESULT_STACK_ENTRIES = [
                                'KERNELBASE!RaiseException+0x39',
                                'msvcr100!CxxThrowException+0x81',
                                'Ipint_SonyIpela+0x234ec',
                                'Ipint_SonyIpela',
                                '0x619f0e0',
                                '0x3e24ef0',
                                '0x46fa6c8',
                                '0xffffffff`fffffffe',
                                'Ipint_SonyIpela+0x16acb0'
                                ]
        self.assertEqual(RESULT_STACK_ENTRIES, stack_entries, "Unexpected result from strip_additional_info() function")
    
    def test05_strip_additional_info_win64_5_groups(self):
        TEST_LINES = [
                    '00000000`591a14f1 : 00000000`0619ef98 00000000`0619ef70 ffffffff`00000001 000007fe`f1a80110 : KERNELBASE!RaiseException+0x39',
                    '000007fe`f1aa34ec : 000007fe`f1a80000 00000000`0619f0e0 00000000`03e24ef0 00000000`046fa6c8 : msvcr100!CxxThrowException+0x81',
                    '000007fe`f1a80000 : 00000000`0619f0e0 00000000`03e24ef0 00000000`046fa6c8 ffffffff`fffffffe : Ipint_SonyIpela+0x234ec',
                    '00000000`0619f0e0 : 00000000`03e24ef0 00000000`046fa6c8 ffffffff`fffffffe 000007fe`f1beacb0 : Ipint_SonyIpela',
                    '00000000`03e24ef0 : 00000000`046fa6c8 ffffffff`fffffffe 000007fe`f1beacb0 00000000`00000000 : 0x619f0e0',
                    '00000000`046fa6c8 : ffffffff`fffffffe 000007fe`f1beacb0 00000000`00000000 0000006e`6f697400 : 0x3e24ef0',
                    'ffffffff`fffffffe : 000007fe`f1beacb0 00000000`00000000 0000006e`6f697400 000007fe`f1beaca0 : 0x46fa6c8',
                    '000007fe`f1beacb0 : 00000000`00000000 0000006e`6f697400 000007fe`f1beaca0 00000000`00000000 : 0xffffffff`fffffffe',
                    '00000000`00000000 : 0000006e`6f697400 000007fe`f1beaca0 00000000`00000000 00000000`00000000 : Ipint_SonyIpela+0x16acb0'
                 ]

        stack_parser = callstackparser.ProblemStackParser();
        stack_entries = stack_parser.strip_additional_info(TEST_LINES)
        RESULT_STACK_ENTRIES = [
                                'KERNELBASE!RaiseException+0x39',
                                'msvcr100!CxxThrowException+0x81',
                                'Ipint_SonyIpela+0x234ec',
                                'Ipint_SonyIpela',
                                '0x619f0e0',
                                '0x3e24ef0',
                                '0x46fa6c8',
                                '0xffffffff`fffffffe',
                                'Ipint_SonyIpela+0x16acb0'
                                ]
        self.assertEqual(RESULT_STACK_ENTRIES, stack_entries, "Unexpected result from strip_additional_info() function")
        
        
class TestStackEntry(unittest.TestCase):
    def test_get_module_name(self):
        TEST_CASES = [
                      ("ItvSdkUtil!CCompressedBuffer::CCompressedBuffer@0x97", "ItvSdkUtil"),
                      ("video@0x2884a2", "video")
                      # TODO: handle cases when we have only address
                      ]
        for (signature, moduleName) in TEST_CASES:
            stack_entry = callstackparser.StackEntry(signature)
            self.assertEqual(stack_entry.get_module_name(), moduleName)
            

#from crashtec.utils import debug
#debug.init_debug_logger(_logger)
         
if __name__ == '__main__':
    unittest.main()
