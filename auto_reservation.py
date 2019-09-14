from korail2 import *
import threading
import logging
import time
import sys

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

membership_number = ''  # 1466577396
password = ''
dep = '대전'
arr = '서울'
date = '20190915'

korail = Korail(membership_number, password, auto_login=True)

passengers = [AdultPassenger()]

# auto_login is True, so if login succeed then korail.logined should be True.
assert korail.logined is True


def search_train_task():
    logging.info('start search_train_task ...')

    try:
        trains = korail.search_train_allday(dep=dep, arr=arr, date=date,
                                            time=100000,
                                            train_type=TrainType.KTX,
                                            include_no_seats=True)

        # based on 10:00 am means length of trains should be greater than 0.
        assert len(trains) != 0

        print(trains)

        for train in trains:
            if train.reserve_possible is not 'N':
                logging.info('start reservation ...')
                seat = korail.reserve(train=train, passengers=passengers)
                logging.info(seat)

                # Reservation succeed => exit.
                sys.exit()

        threading.Timer(5, search_train_task).start()

    except Exception as e:
        logging.error(e)
        time.sleep(2)


if __name__ == '__main__':
    try:
        search_train_task()
    except Exception as e:
        logging.error(e)
        logging.info('search_train_task() restart...')

        time.sleep(2)
        search_train_task()
