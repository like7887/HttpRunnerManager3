# Create your tasks here
from __future__ import absolute_import, unicode_literals

import os

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from ApiManager.models import ProjectInfo
from ApiManager.utils.emails import send_email_reports
from ApiManager.utils.operation import add_test_reports
from ApiManager.utils.runner import run_by_project, run_by_module, run_by_suite, main_run_cases
from ApiManager.utils.testcase import get_time_stamp
from loguru import logger


@shared_task
def main_hrun(testset_path, report_name):
    """
    用例运行
    :param testset_path: dict or list
    :param report_name: str
    :return:
    """
    logger.info("运行用例")

    #运行测试用例
    summary = main_run_cases(testset_path)
    report_path = add_test_reports(summary, report_name=report_name)
    os.remove(report_path)


@shared_task
def project_hrun(name, base_url, project, receiver):
    """
    异步运行整个项目
    :param env_name: str: 环境地址
    :param project: str
    :return:
    """
    logger.info("异步运行整个项目")
    id = ProjectInfo.objects.get(project_name=project).id

    testcase_dir_path = os.path.join(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]), "suite")
    testcase_dir_path = os.path.join(testcase_dir_path, get_time_stamp())

    run_by_project(id, base_url, testcase_dir_path)

    # 运行测试用例
    summary = main_run_cases(testcase_dir_path)
    report_path = add_test_reports(summary, report_name=name)

    if receiver != '':
        send_email_reports(receiver, report_path)
    os.remove(report_path)


@shared_task
def module_hrun(name, base_url, module, receiver):
    """
    异步运行模块
    :param env_name: str: 环境地址
    :param project: str：项目所属模块
    :param module: str：模块名称
    :return:
    """
    logger.info("异步运行模块")
    module = list(module)

    testcase_dir_path = os.path.join(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]), "suite")
    testcase_dir_path = os.path.join(testcase_dir_path, get_time_stamp())

    try:
        for value in module:
            run_by_module(value[0], base_url, testcase_dir_path)
    except ObjectDoesNotExist:
        return '找不到模块信息'

    summary = main_run_cases(testcase_dir_path)


    report_path = add_test_reports(summary, report_name=name)

    if receiver != '':
        send_email_reports(receiver, report_path)
    os.remove(report_path)


@shared_task
def suite_hrun(name, base_url, suite, receiver):
    """
    异步运行模块
    :param env_name: str: 环境地址
    :param project: str：项目所属模块
    :param module: str：模块名称
    :return:
    """
    logger.info("异步运行套件")

    suite = list(suite)

    testcase_dir_path = os.path.join(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]), "suite")
    testcase_dir_path = os.path.join(testcase_dir_path, get_time_stamp())

    try:
        for value in suite:
            run_by_suite(value[0], base_url, testcase_dir_path)
    except ObjectDoesNotExist:
        return '找不到Suite信息'

    summary = main_run_cases(testcase_dir_path)
    report_path = add_test_reports(summary, report_name=name)

    if receiver != '':
        send_email_reports(receiver, report_path)
    os.remove(report_path)
