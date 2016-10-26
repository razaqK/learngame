# coding: utf8
import unittest
from unittest import TestCase
import urlparse3


class TestUrlParse(TestCase):
    """Test for urlparse3 module"""
    def test_parse_url(self):
        """Test parsing url"""
        url = 'http://yandex.ru/mail/?id=123#anchor'
        parsed_url = urlparse3.parse_url(url)
        self.assertEqual(parsed_url.scheme, 'http')
        self.assertEqual(parsed_url.domain, 'yandex.ru')
        self.assertEqual(parsed_url.path, '/mail/')
        self.assertEqual(parsed_url.query, {'id': '123'})
        self.assertEqual(parsed_url.fragment, 'anchor')
        url = 'http://yandex.ru/mail/?id=123&id=321&id=43#anchor'
        parsed_url = urlparse3.parse_url(url)
        self.assertIsNotNone(parsed_url.query.get('id'))
        for i in parsed_url.query['id']:
            if i not in ['123', '321', '43']:
                self.assertIn(i, ['123', '321', '43'])
        url = 'http://google.com/path/'
        parsed_url = urlparse3.parse_url(url)
        parsed_url.query['cardNumber'] = '12345678910'
        self.assertEqual(parsed_url.geturl(),
                         'http://google.com/path/?cardNumber=12345678910')
                         
    def def_parsed_3d_level_domain(self):
        """Test parse 3rd level domain domain"""
        url = 'http://domain.com.ru/?id=123'
        parsed_url = urlparse3.parse_url(url)
        self.assertEqual(parsed_url.domain, 'domain.com.ru')
        self.assertEqual(parsed_url.query, {'id': '123'})

    def test_parse_http_auth_url(self):
        """Test parse url with username and password (http basic auth)"""
        url = 'http://admin:password@domain.com/path/?id=123#anchor'
        parsed_url = urlparse3.parse_url(url)
        self.assertEqual(parsed_url.username, 'admin')
        self.assertEqual(parsed_url.password, 'password')
        self.assertEqual(parsed_url.domain, 'domain.com')
        self.assertEqual(parsed_url.path, '/path/')
        self.assertEqual(parsed_url.query, {'id': '123'})
        self.assertEqual(parsed_url.fragment, 'anchor')
        self.assertEqual(parsed_url.geturl(), url)
        
    def test_parse_semicolo_url(self):
        url = 'http://google.com/?name=alex;id=321'
        parsed_url = urlparse3.parse_url(url)
        self.assertEqual(parsed_url.query['name'], 'alex')
        self.assertEqual(parsed_url.query['id'], '321')
                
    def test_join_url(self):
        """Test parse url, add new values to 'query' and join url back"""
        url = 'http://yandex.ru/mail/?id=123#anchor'
        parsed_url = urlparse3.parse_url(url)
        parsed_url.query['name'] = 'alex'
        self.assertEqual('http://yandex.ru/mail/?id=123&name=alex#anchor',
                         parsed_url.geturl())
        parsed_url.fragment = 'fragment'
        self.assertEqual('http://yandex.ru/mail/?id=123&name=alex#fragment',
                         parsed_url.geturl())
        url = 'http://yandex.ru/path/?id=1&id=2&id=3&name=alex#anchor'
        parsed_url = urlparse3.parse_url(url)
        self.assertEqual(len(set(parsed_url.query['id'])), 3, 
                         'Missing parameters in query')
        for i in parsed_url.query['id']:
            self.assertIn(i, ['1', '2', '3'])
        parsed_url.query['id'] = ['1', '2']
        self.assertEqual('http://yandex.ru/path/?id=1&id=2&name=alex#anchor',
                         parsed_url.geturl())
                         
        url = 'http://yandex.ru'
        parsed_url = urlparse3.parse_url(url)
        parsed_url.path = 'search'
        self.assertEqual('http://yandex.ru/search/', 
                         parsed_url.geturl())
        
        url = 'http://yandex.ru'
        parsed_url = urlparse3.parse_url(url)
        self.assertEqual('http://yandex.ru/', 
                         parsed_url.geturl())
                

if __name__ == '__main__':
    unittest.main()        
