#!/usr/bin/env python
import argparse
import contextlib as clib
import json
import urllib2 as urllib

'''Google URL Shortener simple API key - not required (start with ?key=s)'''
api_key = ''

'''Google URL Shortener API url.'''
google_api_url = 'https://www.googleapis.com/urlshortener/v1/url'

'''Expand request url expansion.'''
expand_request = '?shortUrl='

'''Stats request url expansion.'''
stats_request = '&projection=FULL'

class SimpleUrlShortener:
    '''
    Simple URL Shortener using Google URL Shortener API (goo.gl)
    '''

    def __init__(self, _action, _raw_output, _input_urls=[]):
        '''
        Class initializer.
        :param _action: Action that will be performed on URLs.
        :param _raw_output: If create/expand should print raw output.
        :param _input_urls: List of URLs.
        :return: None
        '''
        self.action = _action
        self.raw_output = _raw_output
        self.input_urls = _input_urls
        self.output_urls = []

    def __request_details(self, request):
        '''
        Show request details.
        :param request: Request to be checked.
        :return: None
        '''
        assert isinstance(request, urllib.Request)
        print 'Request details:'
        print '* Request type:\t', request.get_type()
        print '* Request method:\t', request.get_method()
        print '* Headers:\t', request.header_items()
        print '* Full URL:\t', request.get_full_url()
        print '* Data:\t', request.get_data()
        print ''

    def __show_create(self, create_response):
        '''
        Print output from create action.
        :param create_response: Dictionary containing response from create action.
        :return: None
        '''
        assert isinstance(create_response, dict)

        if not self.raw_output:
            print '* Shorten URL *'
            print 'Long URL:\t', create_response['longUrl']
            print 'Short URL:\t', create_response['id']
        else:
            print create_response['id']

    def __show_expand(self, expand_response):
        '''
        Print output from expand action.
        :param expand_response: Dictionary containing response from expand action.
        :return: None
        '''
        assert isinstance(expand_response, dict)

        if not self.raw_output:
            print '* Expand URL *'
            print 'Long URL:\t', expand_response['longUrl']
            print 'Short URL:\t', expand_response['id']
            print 'Link Status:\t', expand_response['status']
        else:
            print expand_response['id']

    def __show_stats(self, stats_response):
        '''
        Print output from stats action.
        :param stats_response: Dictionary containing response from stats action.
        :return: None
        '''
        assert isinstance(stats_response, dict)
        print '* URL Stats *'
        print 'Long URL:\t', stats_response['longUrl']
        print 'Short URL:\t', stats_response['id']
        print 'Link Status:\t', stats_response['status']
        print '*** Details ***'
        print 'Creation date:\t', stats_response['created']
        print 'Short URL clicks:\t', stats_response['analytics']['allTime']['shortUrlClicks']
        print 'Long URL clicks:\t', stats_response['analytics']['allTime']['longUrlClicks']

    def __url_create(self, long_url):
        '''
        Make create request.
        :param long_url: Long URL to be shortened.
        :return: Create request.
        '''
        data = json.dumps({"longUrl": long_url})
        request = urllib.Request(google_api_url + api_key, data, {'Content-Type': 'application/json'})
        return request

    def __url_expand(self, short_url):
        '''
        Make expand request.
        :param short_url: Short URL to be expanded
        :return: Expand request.
        '''
        request = urllib.Request(google_api_url + expand_request + short_url)
        return request

    def __url_stats(self, input_url):
        '''
        Make stats request.
        :param input_url: URL to be shown in detail
        :return: Stats request
        '''
        request = urllib.Request(google_api_url + expand_request + input_url + stats_request)
        return request

    def __send_request(self, url_request):
        '''
        Send request to server.
        :param url_request: Request to bes sent.
        :return: Dictionary containing request response.
        '''
        assert isinstance(url_request, urllib.Request)
        with clib.closing(urllib.urlopen(url_request)) as connection:
            response = connection.read()
        return json.loads(response)

    def gather_urls(self, input_urls):
        '''
        Gather input URLs
        :param input_urls: List of Input URLs
        :return: None
        '''
        self.input_urls = input_urls

    def perform_action(self):
        '''
        Perform action on input URLs
        :return: None
        '''
        for url in self.input_urls:
            if self.action == 'create':
                request = self.__url_create(url)
                response = self.__send_request(request)
                self.__show_create(response)
            elif self.action == 'expand':
                request = self.__url_expand(url)
                response = self.__send_request(request)
                self.__show_expand(response)
            elif self.action == 'stats':
                request = self.__url_stats(url)
                response = self.__send_request(request)
                self.__show_stats(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple Console URL Shortener using Google URL Shortener API (goo.gl)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--create', action='store_true',  help='Create new short url. <default>')
    group.add_argument('-e', '--expand', action='store_true', help='Expand short url.')
    group.add_argument('-s', '--stats', action='store_true', help='Show short url statistics.')
    parser.add_argument('-r', '--raw_output', action='store_true', help='Raw output (valid only with create/expand).')
    parser.add_argument('input_urls', nargs='+', type=str, help='Input URLs')
    args = parser.parse_args()

    action = ''
    if args.expand:
        action = 'expand'
    elif args.stats:
        action = 'stats'
    else:
        action = 'create'

    shortener = SimpleUrlShortener(action, args.raw_output)
    shortener.gather_urls(args.input_urls)
    shortener.perform_action()


