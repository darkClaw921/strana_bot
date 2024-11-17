#https://subzeroid.github.io/aiograpi/usage-guide/direct.html
#https://github.com/subzeroid/aiograpi
from aiograpi import Client
from pprint import pprint
from dotenv import load_dotenv
import asyncio
import os
load_dotenv()
INSTA_USER=os.getenv('INSTA_USER')
INSTA_PASSWORD=os.getenv('INSTA_PASSWORD')
CODE=os.getenv('CODE')
import time



def get_last_not_read_messages(messages)->list[str]:
    lst=[]
    for message in messages:
        if not message.is_sent_by_viewer:
            lst.append(message.text)
        else:
            break
        
    lst.reverse()
    return lst
    # return None
#TODO
#запросить код подтверждения через телеграм бота и вставить его в переменную CODE
async def main(CODE_VER:str):
    cl = Client()
    try:
        await cl.login(username=INSTA_USER, password=INSTA_PASSWORD, verification_code=CODE_VER)
        #отправка сообщения в телеграм что подключились
    except Exception as e:
        #отправка сообщения в телеграм что не подключились
        print(e)
        return
    
    # user_id = await cl.user_id_from_username(INSTA_USER)
    # pprint(user_id)
    # medias = await cl.user_medias(user_id,
#  20)
    # pprint(medias)
    
    while True:
        threads = await cl.direct_threads(20,selected_filter='unread')
        print(f'{"threads":=^50}')        
        print(f'Новых сообщений: {len(threads)}')


        for thread in threads:
            print(f'{"thread":=^50}')
            pprint(thread)

            # textMessge=thread.messages[0].text
            messages=get_last_not_read_messages(thread.messages)
            for textMessge in messages:
                print(f"{'textMessge':=^50}")
                print(textMessge)
                pprint(thread.messages[0].__dict__)
                try:
                    await cl.direct_answer(thread.id,f'Ваше сообщение получено: {textMessge}')
                    # await cl.direct_send_file('voice/voice.mp3',thread.id)
                except TypeError:
                    print("Все ок unsupported operand type(s) for /: 'str' and 'int'")
                
        time.sleep(60)


def main1(CODE_VER):
    asyncio.run(main(CODE_VER))

main1(CODE)
# ======================thread======================
# DirectThread(pk='18319131736198750',
#  
# id='340282366841710301244259594451709868447',
#  
# messages=[DirectMessage(id='31760672622625563799973806070562816',
# 
#  
# user_id='67959321317', 
# thread_id=340282366841710301244259594451709868447, 
# timestamp=datetime.datetime(2024, 7, 23, 18, 45, 12, 852576), 
# item_type='text', 
# is_sent_by_viewer=True, 
# is_shh_mode=False, 
# reactions=None,
#  text='Hello!',
#  reply=None,
#  link=None,
#  animated_media=None,
#  media=None,
#  visual_media=None,
#  media_share=None,
#  reel_share=None,
#  story_share=None,
#  felix_share=None,
#  xma_share=None,
#  clip=None,
#  placeholder=None),
#  DirectMessage(id='31760668604689693026534404418174976',
#  user_id='67959321317',
#  thread_id=340282366841710301244259594451709868447,
#  timestamp=datetime.datetime(2024,
#  7,
#  23,
#  18,
#  41,
#  35,
#  39836),
#  item_type='text',
#  is_sent_by_viewer=True,
#  is_shh_mode=False,
#  reactions=None,
#  text='hi',
#  reply=None,
#  link=None,
#  animated_media=None,
#  media=None,
#  visual_media=None,
#  media_share=None,
#  reel_share=None,
#  story_share=None,
#  felix_share=None,
#  xma_share=None,
#  clip=None,
#  placeholder=None)],
#  users=[UserShort(pk='3241043704',
#  username='strana_com',
#  full_name='Страна Девелопмент',
#  profile_pic_url=Url('https://scontent.cdninstagram.com/v/t51.2885-19/442992728_424183060551672_2234877428992019276_n.jpg?stp=dst-jpg_s200x200&_nc_cat=101&ccb=1-7&_nc_sid=3fd06f&_nc_ohc=dO7_wcSkYGsQ7kNvgEQq9DW&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.cdninstagram.com&oh=00_AYCs9LZVCzRAG6jOiqsxE3sxHenEPiscnj68_J_Uv0jATg&oe=66A5ACCF'),
#  profile_pic_url_hd=None,
#  is_private=False,
#  is_verified=False)],
#  inviter=UserShort(pk='67959321317',
#  username='jordanlauraa365',
#  full_name='Lauraa Jordan',
#  profile_pic_url=Url('https://scontent-fra5-2.cdninstagram.com/v/t51.2885-19/449849893_859258149361614_2761523655607362440_n.jpg?stp=dst-jpg_e0_s150x150&_nc_ht=scontent-fra5-2.cdninstagram.com&_nc_cat=106&_nc_ohc=OGEd769JxJ8Q7kNvgEVhCe3&edm=AI8ESKwBAAAA&ccb=7-5&oh=00_AYD-uUlS5qQJRbERnY0uaooc-u6fuG2XlUHyGdg_taWt6g&oe=66A58E0D&_nc_sid=b1bb43'),
#  profile_pic_url_hd=None,
#  is_private=False,
#  is_verified=False),
#  left_users=[],
#  admin_user_ids=[],
#  last_activity_at=datetime.datetime(2024,
#  7,
#  23,
#  18,
#  45,
#  12,
#  852000),
#  muted=False,
#  is_pin=None,
#  named=False,
#  canonical=True,
#  pending=False,
#  archived=False,
#  thread_type='private',
#  thread_title='Страна Девелопмент',
#  folder=0,
#  vc_muted=False,
#  is_group=False,
#  mentions_muted=False,
#  approval_required_for_new_members=False,
#  input_mode=0,
#  business_thread_folder=0,
#  read_state=0,
#  is_close_friend_thread=False,
#  assigned_admin_id=0,
#  shh_mode_enabled=False,
#  last_seen_at={'67959321317': {'timestamp': '1721749512852576',
#  'item_id': '31760672622625563799973806070562816',
#  'shh_seen_state': {},
#  'created_at': '1721749512852576'}})
# ====================textMessge====================
# Hello!
# {'animated_media': None,
#  'clip': None,
#  'felix_share': None,
#  'id': '31760672622625563799973806070562816',
#  'is_sent_by_viewer': True,
#  'is_shh_mode': False,
#  'item_type': 'text',
#  'link': None,
#  'media': None,
#  'media_share': None,
#  'placeholder': None,
#  'reactions': None,
#  'reel_share': None,
#  'reply': None,
#  'story_share': None,
#  'text': 'Hello!',
#  'thread_id': 340282366841710301244259594451709868447,
#  'timestamp': datetime.datetime(2024, 7, 23, 18, 45, 12, 852576),
#  'user_id': '67959321317',
#  'visual_media': None,
#  'xma_share': None}
# Traceback (most recent call last):
#   File "/root/test-insta/test_insta/test4.py", line 37, in <module>
#     main1()
#   File "/root/test-insta/test_insta/test4.py", line 35, in main1
#     asyncio.run(main())
#   File "/usr/lib/python3.12/asyncio/runners.py", line 194, in run
#     return runner.run(main)
#            ^^^^^^^^^^^^^^^^
#   File "/usr/lib/python3.12/asyncio/runners.py", line 118, in run
#     return self._loop.run_until_complete(task)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/usr/lib/python3.12/asyncio/base_events.py", line 685, in run_until_complete
#     return future.result()
#            ^^^^^^^^^^^^^^^
#   File "/root/test-insta/test_insta/test4.py", line 32, in main
#     await cl.direct_answer(thread.id, 'Hello!2')
#   File "/root/.cache/pypoetry/virtualenvs/test-insta--u2VaHal-py3.12/lib/python3.12/site-packages/aiograpi/mixins/direct.py", line 226, in direct_answer
#     return await self.direct_send(text, [], [int(thread_id)])
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/root/.cache/pypoetry/virtualenvs/test-insta--u2VaHal-py3.12/lib/python3.12/site-packages/aiograpi/mixins/direct.py", line 281, in direct_send
#     return extract_direct_message(result["payload"])
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/root/.cache/pypoetry/virtualenvs/test-insta--u2VaHal-py3.12/lib/python3.12/site-packages/aiograpi/extractors.py", line 409, in extract_direct_message
#     data["timestamp"] = datetime.datetime.fromtimestamp(data["timestamp"] / 1_000_000)
#                                                         ~~~~~~~~~~~~~~~~~~^~~~~~~~~~~
# TypeError: unsupported operand type(s) for /: 'str' and 'int'

# DirectThread(pk='18447341848021166',
#  id='340282366841710301244276021307465352294',
#  messages=[DirectMessage(id='31763501522118311317503137902755840',
#  user_id='66422689906',
#  thread_id=340282366841710301244276021307465352294,
#  timestamp=datetime.datetime(2024,
#  7,
#  25,
#  13,
#  21,
#  7,
#  801365),
#  item_type='text',
#  is_sent_by_viewer=False,
#  is_shh_mode=False,
#  reactions=None,
#  text='рудд',
#  reply=None,
#  link=None,
#  animated_media=None,
#  media=None,
#  visual_media=None,
#  media_share=None,
#  reel_share=None,
#  story_share=None,
#  felix_share=None,
#  xma_share=None,
#  clip=None,
#  placeholder=None),
#  DirectMessage(id='31763492620147844062200621552369664',
#  user_id='66422689906',
#  thread_id=340282366841710301244276021307465352294,
#  timestamp=datetime.datetime(2024,
#  7,
#  25,
#  13,
#  13,
#  5,
#  224579),
#  item_type='text',
#  is_sent_by_viewer=False,
#  is_shh_mode=False,
#  reactions=None,
#  text='test',
#  reply=None,
#  link=None,
#  animated_media=None,
#  media=None,
#  visual_media=None,
#  media_share=None,
#  reel_share=None,
#  story_share=None,
#  felix_share=None,
#  xma_share=None,
#  clip=None,
#  placeholder=None)],
#  users=[UserShort(pk='66422689906',
#  username='evashilovva01',
#  full_name='',
#  profile_pic_url=Url('https://scontent.xx.fbcdn.net/v/t1.30497-1/84628273_176159830277856_972693363922829312_n.jpg?stp=c59.0.200.200a_dst-jpg_p200x200&_nc_cat=1&ccb=1-7&_nc_sid=7565cd&_nc_ohc=vuICJkHlwE4Q7kNvgEieb2t&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=00_AYBhLn1umyEN1qtaJ9Fb2O7IwRicApsuK9I6Fh02yUTAvA&oe=66C9A519'),
#  profile_pic_url_hd=None,
#  is_private=False,
#  is_verified=False)],
#  inviter=UserShort(pk='66422689906',
#  username='evashilovva01',
#  full_name='',
#  profile_pic_url=Url('https://scontent-lhr6-1.cdninstagram.com/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=scontent-lhr6-1.cdninstagram.com&_nc_cat=1&_nc_ohc=cXqyMerIMHAQ7kNvgHpCnRH&edm=AEsR1pMBAAAA&ccb=7-5&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-5&oh=00_AYCqv4j9HkfQ9bAVQ5MEavhR1qbbggxgvWqUBO6OoO-fYQ&oe=66A8144F&_nc_sid=e2f88a'),
#  profile_pic_url_hd=None,
#  is_private=False,
#  is_verified=False),
#  left_users=[],
#  admin_user_ids=[],
#  last_activity_at=datetime.datetime(2024,
#  7,
#  25,
#  13,
#  21,
#  7,
#  801000),
#  muted=False,
#  is_pin=None,
#  named=False,
#  canonical=True,
#  pending=False,
#  archived=False,
#  thread_type='private',
#  thread_title='evashilovva01',
#  folder=0,
#  vc_muted=False,
#  is_group=False,
#  mentions_muted=False,
#  approval_required_for_new_members=False,
#  input_mode=0,
#  business_thread_folder=0,
#  read_state=1,
#  is_close_friend_thread=False,
#  assigned_admin_id=0,
#  shh_mode_enabled=False,
#  last_seen_at={'66422689906': {'timestamp': '1721902868034999',
#  'item_id': '31763501515821220080037203105808384',
#  'shh_seen_state': {},
#  'created_at': '1721902867459999'},
#  '67959321317': {'timestamp': '1721902838252999',
#  'item_id': '31763500977047165919202329057296384',
#  'shh_seen_state': {},
#  'created_at': '1721902838252999'}})