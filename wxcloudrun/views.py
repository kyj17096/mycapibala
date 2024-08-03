from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from volcenginesdkarkruntime import Ark

client = Ark(api_key="75548df3-2038-4ae2-9235-db694978cbe9")
@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    family_name = request.args.get('family_name')
    gender = request.args.get('gender')
    birth_date = request.args.get('birth_date')
    qiwang = request.args.get('qiwang')
    name_word_number = request.args.get('name_word_number')
    question_str = "请帮忙根据以下信息取9个不同的名字，姓氏:"+family_name+",性别:"+gender+",出生年月日:"+birth_date+",名字字数:"+name_word_number+",字面意思:"+qiwang 
    completion = client.chat.completions.create(
    model="ep-20240803173432-g426f",
    messages = [
        {"role": "user", "content": question_str},
    ],
    )
    #counter = Counters.query.filter(Counters.id == 1).first()
    resp1=completion.choices[0].message.content
    return make_succ_response(0) if resp1 is None else make_succ_response(resp1)
