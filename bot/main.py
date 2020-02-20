# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import praw
import os
import sys
from argparse import ArgumentParser

# reddit scraper
import reddit_scraper

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('SADT02d0iaUexaWwgg4XPZD/BvHLpAE9A0jfzqgcmCQQNsLAH9EwoDhQo8IgOQAhqGtk+44QYYvzUET4X7kEwjGxgKiJ1NStjDrH6tkuFJTOTp0N9LGaBcFDxIq3KG/IGw5qY6pSXecn9V5C7caugQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('965755332759aab0bdb7591d49546997')

# # get channel_secret and channel_access_token from your environment variable
# channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
# channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
# if channel_secret is None:
#     print('Specify LINE_CHANNEL_SECRET as environment variable.')
#     sys.exit(1)
# if channel_access_token is None:
#     print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
#     sys.exit(1)
#
# line_bot_api = LineBotApi(channel_access_token)
# handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):

    if "r/" in event.message.text:

        if "/r/" in event.message.text:
            tail = event.message.text[3:]
        else:
            tail = event.message.text[2:]

        tail_list = tail.split()

        if len(tail_list) > 1: # check if specified more than 1 parameter
            sub_name = tail_list[0]
            n = int(tail_list[1])
            top_n = reddit_scraper.get_top_n(sub_name, n)

        else: # defaults to top 5
            sub_name = tail
            n = 5
            top_n = reddit_scraper.get_top_n(sub_name, 5)

        sticky_counter = 0
        for submission in top_n:
            # print('hello')
            if not submission.stickied:
                push_message(event, submission)
            else:
                sticky_counter += 1

        top_n_plus = reddit_scraper.get_top_n(sub_name, n + sticky_counter)
        top_up = []
        for submission in top_n_plus:
            top_up.append(submission)
        for submission in top_up[(-sticky_counter):]:
            if not submission.stickied:
                push_message(event, submission)

    else:
        # print("hello")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

def push_message(event, submission):

    if ('.jpg' or '.JPG' or '.jpeg' or '.JPEG') in submission.url:

        line_bot_api.push_message(
            event.source.user_id,
            TextSendMessage(text=submission.title)
        )

        line_bot_api.push_message(
            event.source.user_id,
            ImageSendMessage(original_content_url=submission.url, preview_image_url=submission.url)
        )

    elif ('.png' or '.PNG') in submission.url:

        line_bot_api.push_message(
            event.source.user_id,
            TextSendMessage(text=submission.title)
        )

        line_bot_api.push_message(
            event.source.user_id,
            ImageSendMessage(original_content_url=submission.url, preview_image_url=submission.url)
        )

    else:
        selftext = submission.selftext

        str_list = []

        if (len(selftext)==0):
            str_list.append(submission.title)
            str_list.append('\n')
            str_list.append(submission.url)
            msg = ''.join(str_list)
            line_bot_api.push_message(
                event.source.user_id,
                TextSendMessage(text=msg)
            )

        else:
            section_length = 1800 - len(submission.title) - len(submission.url)

            while (len(submission.title) + len(selftext) + len(submission.url)) >= 1800:

                # isolate a chunk of the text
                section = selftext[:section_length]

                # self text now has the remaining text
                selftext = selftext[section_length:]

                # reset string to be built
                str_list = []

                str_list.append(submission.title)
                str_list.append('\n~~~~~~~~~~~~~~~~~~~~~~\n')
                str_list.append(section)
                msg = ''.join(str_list)

                # print(msg)
                # print("Length of title: " + str(len(submission.title)))
                # print("Length of section: " + str(len(section)))
                # print("Length of msg: " + str(len(msg)))
                line_bot_api.push_message(
                    event.source.user_id,
                    TextSendMessage(text=msg)
                )
            str_list = []
            str_list.append(submission.title)
            str_list.append('\n~~~~~~~~~~~~~~~~~~~~~~\n')
            str_list.append(selftext)
            str_list.append('\n~~~~~~~~~~~~~~~~~~~~~~\n')
            str_list.append(submission.permalink)
            msg = ''.join(str_list)
            line_bot_api.push_message(
                event.source.user_id,
                TextSendMessage(text=msg)
            )


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
