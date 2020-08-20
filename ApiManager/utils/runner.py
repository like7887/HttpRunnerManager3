import logging
import os
import shutil
import time
from sys import version_info

from django.core.exceptions import ObjectDoesNotExist
from httprunner import HttpRunner, __version__
from ApiManager.models import TestCaseInfo, ModuleInfo, ProjectInfo, DebugTalk, TestSuite
from ApiManager.utils.common import getAllYml, timestamp_to_datetime
from ApiManager.utils.testcase import dump_python_file, dump_yaml_file, modify_validate, dump_yaml_to_dict, \
    fail_request_handle

logger = logging.getLogger('HttpRunnerManager')

def run_by_single(index, base_url, path):
    """
    加载单个case用例信息
    :param index: int or str：用例索引
    :param base_url: str：环境地址
    :return: dict
    """
    testcase_list = {
        'config': {
            'name': '',
            'verify': "false",
            'variables': {},
            'base_url': base_url
        }
    }
    testcase_list['teststeps'] = []

    try:
        obj = TestCaseInfo.objects.get(id=index)
    except ObjectDoesNotExist:
        return testcase_list

    include = eval(obj.include)
    request = eval(obj.request)
    name = obj.name
    project = obj.belong_project
    module = obj.belong_module.module_name
    #替换当前用例的端口
    if 'base_url' in request['request'] and request['request']['base_url']:
        testcase_list['config']['base_url'] = request['request']['base_url']
    testcase_list['config']['name'] = name
    testcase_dir_path = os.path.join(path, project)
    #加载全局变量
    if request['request']['url'] == '' and "variables" in request.keys():
        testcase_list['config']['variables'] = request['variables']
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
        try:
            debugtalk = DebugTalk.objects.get(belong_project__project_name=project).debugtalk
        except ObjectDoesNotExist:
            debugtalk = ''

        dump_python_file(os.path.join(testcase_dir_path, 'debugtalk.py'), debugtalk)

    testcase_dir_path = os.path.join(testcase_dir_path, module)

    if not os.path.exists(testcase_dir_path):
        os.mkdir(testcase_dir_path)

    for test_info in include:
        try:
            if isinstance(test_info, dict):
                config_id = test_info.pop('config')[0]
                config_request = eval(TestCaseInfo.objects.get(id=config_id).request)['config']
                testcase_list['teststeps'].append(modify_validate(config_request))
            else:
                id = test_info[0]
                pre_request = eval(TestCaseInfo.objects.get(id=id).request)
                testcase_list['teststeps'].append(modify_validate(pre_request))

        except ObjectDoesNotExist:
            return testcase_list

    if request['request']['url'] != '':
        testcase_list['teststeps'].append(modify_validate(request))
    testcase_dir_path = os.path.join(testcase_dir_path, name + '.yml')
    dump_yaml_file(testcase_dir_path, testcase_list)


def run_by_suite(index, base_url, path):
    obj = TestSuite.objects.get(id=index)

    include = eval(obj.include)

    for val in include:
        run_by_single(val[0], base_url, path)



def run_by_batch(test_list, base_url, path, type=None, mode=False):
    """
    批量组装用例数据
    :param test_list:
    :param base_url: str: 环境地址
    :param type: str：用例级别
    :param mode: boolean：True 同步 False: 异步
    :return: list
    """

    if mode:
        for index in range(len(test_list) - 2):
            form_test = test_list[index].split('=')
            value = form_test[1]
            if type == 'project':
                run_by_project(value, base_url, path)
            elif type == 'module':
                run_by_module(value, base_url, path)
            elif type == 'suite':
                run_by_suite(value, base_url, path)
            else:
                run_by_single(value, base_url, path)

    else:
        if type == 'project':
            for value in test_list.values():
                run_by_project(value, base_url, path)

        elif type == 'module':
            for value in test_list.values():
                run_by_module(value, base_url, path)
        elif type == 'suite':
            for value in test_list.values():
                run_by_suite(value, base_url, path)

        else:
            for index in range(len(test_list) - 1):
                form_test = test_list[index].split('=')
                index = form_test[1]
                run_by_single(index, base_url, path)


def run_by_module(id, base_url, path):
    """
    组装模块用例
    :param id: int or str：模块索引
    :param base_url: str：环境地址
    :return: list
    """
    obj = ModuleInfo.objects.get(id=id)
    test_index_list = TestCaseInfo.objects.filter(belong_module=obj, type=1).values_list('id')
    for index in test_index_list:
        run_by_single(index[0], base_url, path)


def run_by_project(id, base_url, path):
    """
    组装项目用例
    :param id: int or str：项目索引
    :param base_url: 环境地址
    :return: list
    """
    obj = ProjectInfo.objects.get(id=id)
    module_index_list = ModuleInfo.objects.filter(belong_project=obj).values_list('id')
    for index in module_index_list:
        module_id = index[0]
        run_by_module(module_id, base_url, path)


def run_test_by_type(id, base_url, path, type):
    if type == 'project':
        run_by_project(id, base_url, path)
    elif type == 'module':
        run_by_module(id, base_url, path)
    elif type == 'suite':
        run_by_suite(id, base_url, path)
    else:
        run_by_single(id, base_url, path)


def main_run_cases(testset_path):
    """
    批量运行测试用例方法，包含异步，同步运行方式
    :param testset_path: 测试用例本地地址
    :return: summary （dict运行结果）
    """
    runner = HttpRunner()
    test_dic, error_requests, sum_temps = [], [], []
    account_list = testset_path.split('\\')[-1].split('&')
    user_account = account_list[0] if len(account_list) > 1 else ""
    getAllYml(testset_path, test_dic)
    start_time = time.time()
    for test_case_dir in test_dic:
        logger.info("当前运行的用例文件为：{}".format(test_case_dir))
        try:
            runner.run_path(test_case_dir)
        except Exception as e:
            fail_request_datas = dump_yaml_to_dict(test_case_dir)
            fail_data = fail_request_handle(fail_request_datas, str(e))
            error_requests += fail_data
            logger.info("%s 接口处理报错: %s" % (fail_request_datas['config']['name'], str(e)))
        sum_temp = runner.get_summary()
        if sum_temp.success:
            sum_temp = timestamp_to_datetime(sum_temp)
            sum_temps += sum_temp
        logger.info("{} 文件执行完之后生成的结果为：{}".format(test_case_dir, sum_temp))
    end_time = time.time()
    duration = end_time - start_time
    shutil.rmtree(testset_path)
    summary = {'name': '出入口', 'success': True,
               'time': {'start_at': start_time, 'start_at_iso_format': start_time, 'end_time': end_time,
                        'duration': duration}, 'step_datas': []}

    summary['step_datas'] += sum_temps
    summary['step_datas'] += error_requests

    summary = timestamp_to_datetime(summary, type=False)
    summary['case_id'] = str(len(summary['step_datas']))
    hrun_version = __version__
    python_version = str(version_info.major) + "." + str(version_info.minor) + "." + str(version_info.micro)
    summary['platform'] = {'httprunner_version': hrun_version, 'python_version': python_version}
    summary['user_account'] = user_account
    logger.info("生成报告前的summary：{}".format(summary))
    return summary