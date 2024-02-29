import logging, time
from app.vcsp import bp
from flask import render_template, jsonify, request
from app.models.vcsp import Event
from app.extensions import db
from app.vcsp.schedule_reindexing import init_reindex
import json
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import distinct
from app.helpers import get_conn_vars
import boto3


@bp.route('/')
def index():
    return render_template('vcsp/index.html')


@bp.route('/events')
def events():
    return render_template('vcsp/events.html')


@bp.route('/getevents')
def getevents():
    events = Event.query.all()
    event_lists = []
    for event in events:
        event_list = [event.eventTime,
                      event.userid,
                      event.eventName,
                      event.bucket,
                      event.object,
                      event.status
                      ]
        event_lists.append(event_list)
    return json.dumps(event_lists)


@bp.route('/s3reindex', methods=['POST'])
def s3reindex():
    # Check if request method is POST
    if request.method != "POST":
        return jsonify({'error': 'Only POST method is allowed'}), 405
    # Try to get the JSON body
    try:
        data = request.get_json()
    except:
        return jsonify({'error': 'Invalid JSON format'}), 400
    # Check if data is valid JSON
    if data is None:
        return jsonify({'error': 'No JSON data found in request body'}), 400

    # Create a thread pool executor with 1 thread
    executor = ThreadPoolExecutor(max_workers=1)
    # Submit the task asynchronously and return immediately
    future = executor.submit(init_reindex, data)

    # Return a success message (optional)
    return jsonify({'message': 'JSON data received and processed successfully'}), 200


@bp.route('/libcontents')
def libcontents():
    # get unique bucket
    buckets_query = db.session.query(distinct(Event.bucket)).all()
    buckets = [bucket[0] for bucket in buckets_query]
    conn_var = get_conn_vars()
    s3_client = boto3.client('s3', region_name=conn_var['region_name'], verify=False,
                             endpoint_url=conn_var['endpoint_url'],
                             aws_access_key_id=conn_var['aws_access_key_id'],
                             aws_secret_access_key=conn_var['aws_secret_access_key'])
    libcontents_list = []
    for bucket in buckets:
        s3_obj = s3_client.get_object(Bucket=bucket, Key='items.json')
        items_data = json.loads(s3_obj['Body'].read().decode('utf-8'))
        items = items_data.get("items")
        for item in items:
            libcontent = [bucket,
                          item.get("type"),
                          item.get("name"),
                          item.get("id"),
                          item.get("created")
                          ]
            libcontents_list.append(libcontent)
    # logging.info(f'{libcontents_list}')
    return render_template('vcsp/libcontents.html', contents=libcontents_list)

    # events = Event.query.all()
    # event_lists = []
    # for event in events:
    #     event_list = [event.eventTime,
    #                   event.userid,
    #                   event.eventName,
    #                   event.bucket,
    #                   event.object,
    #                   event.status
    #                   ]
    #     event_lists.append(event_list)
    return "Library contents."

