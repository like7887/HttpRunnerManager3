import io
import json
import time

import yaml


def get_time_stamp(user_account=None):
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d-%H-%M-%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s-%03d" % (data_head, data_secs) if user_account is None else "%s&%s-%03d" % (user_account,data_head, data_secs)
    return time_stamp


def dump_yaml_file(yaml_file, data):
    """ load yaml file and check file content format
    """
    with io.open(yaml_file, 'w', encoding='utf-8') as stream:
        yaml.dump(data, stream, indent=4, default_flow_style=False, encoding='utf-8')


def _dump_json_file(json_file, data):
    """ load json file and check file content format
    """
    with io.open(json_file, 'w', encoding='utf-8') as stream:
        json.dump(data, stream, indent=4, separators=(',', ': '), ensure_ascii=False)


def dump_python_file(python_file, data):
    with io.open(python_file, 'w', encoding='utf-8') as stream:
        stream.write(data)


def modify_validate(request):
    if not isinstance(request,dict):
        raise ValueError("request的值为：{}，不是一个dict".format(request))
    if 'validate' in request.keys():
        validates = []
        for validate in request['validate']:
            new_validate = {}
            if validate.get('comparator') == "equals":
                new_validate['eq'] = [validate.get('check'), validate.get('expected')]
                validates.append(new_validate)
        request['validate'] = validates
    return request

def dump_yaml_to_dict(yaml_file_name_path,param=None):
    """
        根据文件名称获取yaml数据，并转换成json字符
        可以通过param读取指定字段
        :param yaml_file_name:yaml文件名称
        :param param:传入参数
        :return:
        """
    yaml_data = {}
    try:
        with open(yaml_file_name_path, encoding='utf-8') as stream:
            yaml_data = yaml.safe_load(stream)
            if param is not None:
                yaml_data = yaml_data[param]
    except FileNotFoundError as file_exception:
        print("文件未找到:".format(str(file_exception)))
        raise file_exception
    finally:
        stream.close()
    return yaml_data

def fail_request_handle(fail_datas,error_info):
    result_datas = []
    for fail_data in fail_datas['teststeps']:
        fail_data['request']['body'] = fail_data['request'].pop('json')
        result = {'success': False,'name': fail_data['name'],'data':{'success': False,'req_resps':[{'request':fail_data['request'],'response':{'status_code':'error','body': error_info}}]}}
        result_datas.append(result)
    return result_datas

class AnalysisError(Exception):
    pass

if __name__ == '__main__':
    import MySQLdb as Database
    version = Database.version_info
    print(version)