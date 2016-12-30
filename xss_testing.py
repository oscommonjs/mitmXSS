import unittest
import xss

class xssFinderTests(unittest.TestCase):
    def test_getXSSInfo(self):
        # First type of exploit: <script>PAYLOAD</script>
        # Exploitable: 
        self.assertEqual(myxss.getXSSInfo(b"<html><script>%s</script><html>" % myxss.fullPayload,
                                          "https://example.com",
                                          "End of URL"),
                         {'Line': myxss.fullPayload.decode('utf-8'),
                          'Exploit': '</script><script>alert(0)</script><script>',
                          'URL': 'https://example.com',
                          'Injection Point': "End of URL"})
        self.assertEqual(myxss.getXSSInfo(b"<html><script>%s</script><html>" % myxss.fullPayload.replace(b"'", b"%27").replace(b'"', b"%22"),
                                          "https://example.com",
                                          "End of URL"),
                         {'Line': myxss.fullPayload.replace(b"'", b"%27").replace(b'"', b"%22").decode('utf-8'),
                          'Exploit': '</script><script>alert(0)</script><script>',
                          'URL': 'https://example.com',
                          'Injection Point': "End of URL"})
        # Non-Exploitable:
        self.assertEqual(myxss.getXSSInfo(b"<html><script>%s</script><html>" % myxss.fullPayload.replace(b"'", b"%27").replace(b'"', b"%22").replace(b"/", b"%2F"),
                                          "https://example.com",
                                          "End of URL"),
                         None)
        # Second type of exploit: <script>t='PAYLOAD'</script>
        # Exploitable: 
        self.assertEqual(myxss.getXSSInfo(b"<html><script>t='%s';</script></html>" % myxss.fullPayload.replace(b"<", b"%3C").replace(b">", b"%3E").replace(b"\"", b"%22"),
                                          "https://example.com",
                                          "End of URL"),
                         {'Line': myxss.fullPayload.replace(b"<", b"%3C").replace(b">", b"%3E").replace(b"\"", b"%22").decode('utf-8'),
                          'Exploit': "';alert(0);g='",
                          'URL': 'https://example.com',
                          'Injection Point': "End of URL"})
        # Non-Exploitable:
        self.assertEqual(myxss.getXSSInfo(b"<html><script>t='%s';</script></html>" % myxss.fullPayload.replace(b"<", b"%3C").replace(b">", b"%3E").replace(b"\"", b"%22").replace(b"'", b"%22"),
                                          "https://example.com",
                                          "End of URL"),
                         None)
        # Third type of exploit: <script>t="PAYLOAD"</script>
        # Exploitable:
        self.assertEqual(myxss.getXSSInfo(b"<html><script>t=\"%s\";</script></html>" % myxss.fullPayload.replace(b"<", b"%3C").replace(b">", b"%3E").replace(b"'", b"%27"),
                                          "https://example.com",
                                          "End of URL"),
                         {'Line': myxss.fullPayload.replace(b"<", b"%3C").replace(b">", b"%3E").replace(b"'", b"%27").decode('utf-8'),
                          'Exploit': '";alert(0);g="',
                          'URL': 'https://example.com',
                          'Injection Point': "End of URL"})
        # Non-Exploitable:
        self.assertEqual(myxss.getXSSInfo(b"<html><script>t=\"%s\";</script></html>" % myxss.fullPayload.replace(b"<", b"%3C").replace(b">", b"%3E").replace(b"'", b"%27").replace(b"\"", b"%22"),
                                          "https://example.com",
                                          "End of URL"),
                         None)
        # Fourth type of exploit: <a href='PAYLOAD'>Test</a>
        # Exploitable: 
        self.assertEqual(myxss.getXSSInfo(b"<html><a href='%s'>Test</a></html>" % myxss.fullPayload,
                                          "https://example.com",
                                          "End of URL"),
                         {'Line': myxss.fullPayload.decode('utf-8'),
                          'Exploit': "'><script>alert(0)</script>",
                          'URL': 'https://example.com',
                          'Injection Point': "End of URL"})
        # Non-Exploitable:
        self.assertEqual(myxss.getXSSInfo(b"<html><a href='%s'>Test</a></html>" % myxss.fullPayload.replace(b"'", b"%27"),
                                          "https://example.com",
                                          "End of URL"),
                         None)
        # Fifth type of exploit: <a href="PAYLOAD">Test</a>
        # Exploitable: 
        self.assertEqual(myxss.getXSSInfo(b"<html><a href=\"%s\">Test</a></html>" % myxss.fullPayload.replace(b"'", b"%27"),
                                          "https://example.com",
                                          "End of URL"),
                         {'Line': myxss.fullPayload.replace(b"'", b"%27").decode('utf-8'),
                          'Exploit': "\"><script>alert(0)</script>",
                          'URL': 'https://example.com',
                          'Injection Point': "End of URL"})
        # Non-Exploitable:
        self.assertEqual(myxss.getXSSInfo(b"<html><a href=\"%s\">Test</a></html>" % myxss.fullPayload.replace(b"'", b"%27").replace(b"\"", b"%22"),
                                         "https://example.com",
                                         "End of URL"),
                        None)
        # Sixth type of exploit: <a href=PAYLOAD>Test</a>
        # Exploitable:
        self.assertEqual(myxss.getXSSInfo(b"<html><a href=%s>Test</a></html>" % myxss.fullPayload,
                                          "https://example.com",
                                          "End of URL"),
                         {'Line': myxss.fullPayload.decode('utf-8'),
                          'Exploit': "><script>alert(0)</script>",
                          'URL': 'https://example.com',
                          'Injection Point': "End of URL"})
        # Non-Exploitable
        self.assertEqual(myxss.getXSSInfo(b"<html><a href=%s>Test</a></html>" % myxss.fullPayload.replace(b"<", b"%3C").replace(b">", b"%3E"),
                                          "https://example.com",
                                          "End of URL"),
                         None)
        # Seventh type of exploit: <html>PAYLOAD</html>
        # Exploitable:
        self.assertEqual(myxss.getXSSInfo(b"<html><b>%s</b></html>" % myxss.fullPayload,
                                          "https://example.com",
                                          "End of URL"),
                         {'Line': myxss.fullPayload.decode('utf-8'),
                          'Exploit': "<script>alert(0)</script>",
                          'URL': 'https://example.com',
                          'Injection Point': "End of URL"})
        # Non-Exploitable
        self.assertEqual(myxss.getXSSInfo(b"<html><b>%s</b></html>" % myxss.fullPayload.replace(b"<", b"%3C").replace(b">", b"%3E").replace(b"/", b"%2F"),
                                          "https://example.com",
                                           "End of URL"),
                         None)
        
if __name__ == '__main__':
    unittest.main()
