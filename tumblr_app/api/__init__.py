from .helpers import validate_params, validate_blogname
from .tumblr_request import TumblrRequest
try:
    import urllib.request as urllib2
except ImportError:
    pass


class TumblrClient(object):

    def __init__(self, client_key, client_secret="", oauth_token="",
                 oauth_secret="", host="https://api.tumblr.com"):

        self.request = TumblrRequest(client_key, client_secret,
                                     oauth_token, oauth_secret, host)

    def info(self):
        return self.send_api_request("get", "/v2/user/info")

    @validate_blogname
    def avatar(self, blogname, size=64):
        url = "/v2/blog/{0}/avatar/{1}".format(blogname, size)
        return self.send_api_request("get", url)

    def likes(self, **kwargs):
        return self.send_api_request("get", "/v2/user/likes", kwargs,
                                     ["limit", "offset", "before", "after"])

    def following(self, **kwargs):
       return self.send_api_request("get", "/v2/user/following", kwargs,
                                     ["limit", "offset"])

    def dashboard(self, **kwargs):
        return self.send_api_request("get", "/v2/user/dashboard", kwargs,
                                     ["limit", "offset", "type", "since_id", "reblog_info", "notes_info"])

    def tagged(self, tag, **kwargs):
        kwargs.update({'tag': tag})
        return self.send_api_request("get", '/v2/tagged', kwargs,
                                     ['before', 'limit', 'filter', 'tag', 'api_key'], True)

    @validate_blogname
    def posts(self, blogname, type=None, **kwargs):
        if type is None:
            url = '/v2/blog/{0}/posts'.format(blogname)
        else:
            url = '/v2/blog/{0}/posts/{1}'.format(blogname, type)
        return self.send_api_request("get", url, kwargs,
                                     ['id', 'tag', 'limit', 'offset', 'reblog_info', 'notes_info', 'filter', 'api_key'], True)

    @validate_blogname
    def blog_info(self, blogname):
        url = "/v2/blog/{0}/info".format(blogname)
        return self.send_api_request("get", url, {}, ['api_key'], True)

    @validate_blogname
    def followers(self, blogname, **kwargs):
        url = "/v2/blog/{0}/followers".format(blogname)
        return self.send_api_request("get", url, kwargs, ['limit', 'offset'])

    @validate_blogname
    def blog_likes(self, blogname, **kwargs):
        url = "/v2/blog/{0}/likes".format(blogname)
        return self.send_api_request("get", url, kwargs,
                                     ['limit', 'offset', 'before', 'after'], True)

    @validate_blogname
    def queue(self, blogname, **kwargs):
        url = "/v2/blog/{0}/posts/queue".format(blogname)
        return self.send_api_request("get", url, kwargs,
                                     ['limit', 'offset', 'filter'])

    @validate_blogname
    def drafts(self, blogname, **kwargs):
        url = "/v2/blog/{0}/posts/draft".format(blogname)
        return self.send_api_request("get", url, kwargs, ['filter'])

    @validate_blogname
    def submission(self, blogname, **kwargs):
        url = "/v2/blog/{0}/posts/submission".format(blogname)
        return self.send_api_request("get", url, kwargs, ["offset", "filter"])

    @validate_blogname
    def follow(self, blogname):
        url = "/v2/user/follow"
        return self.send_api_request("post", url, {'url': blogname}, ['url'])

    @validate_blogname
    def unfollow(self, blogname):
        url = "/v2/user/unfollow"
        return self.send_api_request("post", url, {'url': blogname}, ['url'])

    def like(self, id, reblog_key):
        url = "/v2/user/like"
        params = {'id': id, 'reblog_key': reblog_key}
        return self.send_api_request("post", url, params, ['id', 'reblog_key'])

    def unlike(self, id, reblog_key):
        url = "/v2/user/unlike"
        params = {'id': id, 'reblog_key': reblog_key}
        return self.send_api_request("post", url, params, ['id', 'reblog_key'])

    @validate_blogname
    def create_photo(self, blogname, **kwargs):
        kwargs.update({"type": "photo"})
        return self._send_post(blogname, kwargs)

    @validate_blogname
    def create_text(self, blogname, **kwargs):
        kwargs.update({"type": "text"})
        return self._send_post(blogname, kwargs)

    @validate_blogname
    def create_quote(self, blogname, **kwargs):
        kwargs.update({"type": "quote"})
        return self._send_post(blogname, kwargs)

    @validate_blogname
    def create_link(self, blogname, **kwargs):
        kwargs.update({"type": "link"})
        return self._send_post(blogname, kwargs)

    @validate_blogname
    def create_chat(self, blogname, **kwargs):
        kwargs.update({"type": "chat"})
        return self._send_post(blogname, kwargs)

    @validate_blogname
    def create_audio(self, blogname, **kwargs):
        kwargs.update({"type": "audio"})
        return self._send_post(blogname, kwargs)

    @validate_blogname
    def create_video(self, blogname, **kwargs):
        kwargs.update({"type": "video"})
        return self._send_post(blogname, kwargs)

    @validate_blogname
    def reblog(self, blogname, **kwargs):
        url = "/v2/blog/{0}/post/reblog".format(blogname)

        valid_options = ['id', 'reblog_key', 'comment'] + \
            self._post_valid_options(kwargs.get('type', None))
        if 'tags' in kwargs and kwargs['tags']:
            # Take a list of tags and make them acceptable for upload
            kwargs['tags'] = ",".join(kwargs['tags'])
        return self.send_api_request('post', url, kwargs, valid_options)

    @validate_blogname
    def delete_post(self, blogname, id):
        url = "/v2/blog/{0}/post/delete".format(blogname)
        return self.send_api_request('post', url, {'id': id}, ['id'])

    @validate_blogname
    def edit_post(self, blogname, **kwargs):
        url = "/v2/blog/{0}/post/edit".format(blogname)

        if 'tags' in kwargs and kwargs['tags']:
            # Take a list of tags and make them acceptable for upload
            kwargs['tags'] = ",".join(kwargs['tags'])

        valid_options = ['id'] + \
            self._post_valid_options(kwargs.get('type', None))
        return self.send_api_request('post', url, kwargs, valid_options)

    # Parameters valid for /post, /post/edit, and /post/reblog.
    def _post_valid_options(self, post_type=None):
        # These options are always valid
        valid = ['type', 'state', 'tags', 'tweet', 'date', 'format', 'slug']

        # Other options are valid on a per-post-type basis
        if post_type == 'text':
            valid += ['title', 'body']
        elif post_type == 'photo':
            valid += ['caption', 'link', 'source', 'data']
        elif post_type == 'quote':
            valid += ['quote', 'source']
        elif post_type == 'link':
            valid += ['title', 'url', 'description']
        elif post_type == 'chat':
            valid += ['title', 'conversation']
        elif post_type == 'audio':
            valid += ['caption', 'external_url', 'data']
        elif post_type == 'video':
            valid += ['caption', 'embed', 'data']

        return valid

    def _send_post(self, blogname, params):
        url = "/v2/blog/{0}/post".format(blogname)
        valid_options = self._post_valid_options(params.get('type', None))

        if 'tags' in params:
            # Take a list of tags and make them acceptable for upload
            params['tags'] = ",".join(params['tags'])

        return self.send_api_request("post", url, params, valid_options)

    def send_api_request(self, method, url, params={}, valid_parameters=[], needs_api_key=False):
        if needs_api_key:
            params.update({'api_key': self.request.client_key})
            valid_parameters.append('api_key')

        files = []
        if 'data' in params:
            if isinstance(params['data'], list):
                for idx, data in enumerate(params['data']):
                    with open(data, 'rb') as f:
                        files.append(('data['+str(idx)+']', data, f.read()))
            else:
                with open(params['data'], 'rb') as f:
                    files = [('data', params['data'], f.read())]
            del params['data']

        validate_params(valid_parameters, params)
        if method == "get":
            return self.request.get(url, params)
        else:
            return self.request.post(url, params, files)
