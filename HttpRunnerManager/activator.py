import logging

logger = logging.getLogger('HttpRunnerManager')

def process(request, **kwargs):
    logger.info("请求详细参数kwargs：{}".format(kwargs))
    app = kwargs.pop('app', None)
    fun = kwargs.pop('function', None)
    index = kwargs.pop('id', None)
    file = kwargs.pop('file',None)
    if app == 'api':
        app = 'ApiManager'
    try:
        app = __import__("%s.views" % app)
        view = getattr(app, 'views')
        fun = getattr(view, fun)
        # 执行view.py中的函数，并获取其返回值
        if file and index:
            result = fun(request,index,file)
        elif index:
            result = fun(request, index)
        else:
            result = fun(request)
    except (ImportError, AttributeError):
        raise

    return result
