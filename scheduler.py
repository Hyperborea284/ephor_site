import schedule
from multiprocessing import Process

from fire import *


def scheduled_01():
    f1 = Firefox() 
    fwd1 = f1.driver_web(f1)
    f1.twitter(fwd1)

#schedule.every().sunday.at("22:28").do(scheduled_01())


def scheduled_02():
    f2 = Firefox() 
    fwd2 = f2.driver_web(f2)
    f2.tweetdeck(fwd2)

#schedule.every().wednesday.at("23:36").do(scheduled_02())


def scheduled_03():
    f3 = Firefox() 
    fcr3 = f3.driver_crude(f3)
    f3.acesso_change(fcr3)

#schedule.every().wednesday.at("23:37").do(scheduled_03())


def scheduled_04():
    f4 = Firefox() 
    fsa4 = f4.driver_safe(f4)
    f4.reddit(fsa4)

#schedule.every().thursday.at("00:14").do(scheduled_04())


def scheduled_05():
    f5 = Firefox() 
    fcl5 = f5.driver_class(f5)
    f5.news_google(fcl5)

#schedule.every().wednesday.at("23:45").do(scheduled_05())


def scheduled_06():
    f6 = Firefox() 
    fcr6 = f6.driver_crude(f6)
    f6.acesso_change(fcr6)

#schedule.every().thursday.at("00:02").do(scheduled_06())


#p1 = Process(target=server_start())
#p2 = Process(target=timel())

#if __name__ == '__main__':
    #p1.start()
    #p2.start()

    #p1.join()
    #p2.join()
